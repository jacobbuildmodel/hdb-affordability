#!/usr/bin/env python3
"""
01_geocode.py -- geocode every HDB block-and-street pair with OneMap Search.

Reads cargradient/out/addresses.csv (block, street_name; no price field) and
writes cargradient/out/blocks_geocoded.csv. Run from the repository root:

    python cargradient/01_geocode.py            # geocode, resumable
    python cargradient/01_geocode.py --write    # rebuild the CSV from the cache

Credentials come from ONEMAP_EMAIL and ONEMAP_PASSWORD. The token lives in
memory only: it is never printed, logged or written to disk.

Rules (Checkpoint 0, round 4):
- At most one call per second, never faster. Back off on 429 and 5xx.
- Resumable: each finished pair is appended to out/geocode_cache.jsonl
  (gitignored), and a rerun skips pairs already there.
- A result is accepted only when its BLK_NO equals the block and its
  ROAD_NAME equals the street once the resale file's abbreviations are
  expanded (EXPAND below). A nearby block is never taken.
- Query 1 is "<block> <street as in the resale file>". If no result on its
  first page matches, query 2 is "<block> <expanded street>", once.
  match_type is exact (query 1 matched), expanded (query 2 matched) or none.

Contains information from OneMap (Singapore Land Authority), under the
Singapore Open Data Licence version 1.0.
"""
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ADDRESSES = "cargradient/out/addresses.csv"
CACHE = "cargradient/out/geocode_cache.jsonl"
OUT = "cargradient/out/blocks_geocoded.csv"
LOG = "cargradient/out/geocode_progress.log"
TOKEN_URL = "https://www.onemap.gov.sg/api/auth/post/getToken"
SEARCH_URL = "https://www.onemap.gov.sg/api/common/elastic/search"
MIN_INTERVAL = 1.0  # seconds between call starts: one call per second at most

# Resale-file abbreviations, token by token, as they appear in the 597 street
# names of addresses.csv. "ST." (with a full stop) is SAINT, as in
# "ST. GEORGE'S RD"; "ST" alone is STREET.
EXPAND = {
    "AVE": "AVENUE", "BT": "BUKIT", "C'WEALTH": "COMMONWEALTH", "CL": "CLOSE",
    "CRES": "CRESCENT", "CTR": "CENTRE", "CTRL": "CENTRAL", "DR": "DRIVE",
    "GDNS": "GARDENS", "HTS": "HEIGHTS", "JLN": "JALAN", "KG": "KAMPONG",
    "LOR": "LORONG", "MKT": "MARKET", "NTH": "NORTH", "PK": "PARK",
    "PL": "PLACE", "RD": "ROAD", "ST": "STREET", "ST.": "SAINT",
    "STH": "SOUTH", "TER": "TERRACE", "TG": "TANJONG", "UPP": "UPPER",
}


def expand(street):
    return " ".join(EXPAND.get(t, t) for t in street.upper().split())


def norm(s):
    """Compare road names without punctuation or spacing differences."""
    s = s.upper().replace("'", "").replace(".", " ")
    return " ".join(s.split())


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg):
    line = f"{now_utc()} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


class OneMap:
    def __init__(self):
        for v in ("ONEMAP_EMAIL", "ONEMAP_PASSWORD"):
            if not os.environ.get(v):
                sys.exit(f"{v} is not set; stopping.")
        self._token = None
        self._expiry = 0
        self._last = 0.0

    def _get_token(self):
        body = json.dumps({"email": os.environ["ONEMAP_EMAIL"],
                           "password": os.environ["ONEMAP_PASSWORD"]}).encode()
        req = urllib.request.Request(TOKEN_URL, data=body, method="POST",
                                     headers={"Content-Type": "application/json"})
        self._pace()
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        self._token = d["access_token"]
        self._expiry = int(d.get("expiry_timestamp", 0))
        log("token obtained (value not shown)")

    def _pace(self):
        wait = self._last + MIN_INTERVAL - time.time()
        if wait > 0:
            time.sleep(wait)
        self._last = time.time()

    def search(self, text):
        if self._token is None or time.time() > self._expiry - 600:
            self._get_token()
        url = SEARCH_URL + "?" + urllib.parse.urlencode(
            {"searchVal": text, "returnGeom": "Y", "getAddrDetails": "Y", "pageNum": 1})
        backoff = 5
        for attempt in range(10):
            self._pace()
            req = urllib.request.Request(url, headers={"Authorization": self._token})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    d = json.load(r)
            except urllib.error.HTTPError as e:
                if e.code == 401 or (e.code in (400, 403) and b"oken" in e.read()[:300]):
                    log(f"HTTP {e.code}: token refused, requesting a new one")
                    self._get_token()
                    continue
                if e.code == 429 or e.code >= 500:
                    log(f"HTTP {e.code}: backing off {backoff}s")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 600)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                log(f"network error {type(e).__name__}: backing off {backoff}s")
                time.sleep(backoff)
                backoff = min(backoff * 2, 600)
                continue
            err = str(d.get("error", ""))
            if "xpired" in err or "nvalid token" in err or "missing" in err.lower():
                log("token rejected in body, requesting a new one")
                self._get_token()
                continue
            return d
        raise RuntimeError(f"gave up after 10 attempts: {text!r}")


def pick(results, block, street):
    want = norm(expand(street))
    for r in results:
        if r.get("BLK_NO", "").upper() == block.upper() and norm(r.get("ROAD_NAME", "")) == want:
            return r
    return None


def load_cache():
    done = {}
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            for line in f:
                rec = json.loads(line)
                done[(rec["block"], rec["street_name"])] = rec
    return done


def write_csv(done, pairs):
    cols = ["block", "street_name", "postal", "lat", "lon", "matched_address",
            "match_type", "query_used", "retrieved_utc"]
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for key in pairs:
            rec = done.get(key)
            if rec is None:
                continue
            w.writerow([rec[c] for c in cols])


def main():
    with open(ADDRESSES) as f:
        pairs = [(r["block"], r["street_name"]) for r in csv.DictReader(f)]
    done = load_cache()
    if "--write" in sys.argv:
        write_csv(done, pairs)
        return
    todo = [p for p in pairs if p not in done]
    log(f"pairs {len(pairs)}, cached {len(done)}, to do {len(todo)}")
    om = OneMap()
    counts = {"exact": 0, "expanded": 0, "none": 0}
    with open(CACHE, "a") as cache:
        for i, (block, street) in enumerate(todo, 1):
            q1 = f"{block} {street}"
            hit = pick(om.search(q1).get("results", []), block, street)
            match_type, query = ("exact", q1) if hit else (None, None)
            if hit is None:
                q2 = f"{block} {expand(street)}"
                if q2 != q1:
                    hit = pick(om.search(q2).get("results", []), block, street)
                match_type, query = ("expanded", q2) if hit else ("none", q2)
            rec = {"block": block, "street_name": street,
                   "postal": hit.get("POSTAL", "") if hit else "",
                   "lat": hit.get("LATITUDE", "") if hit else "",
                   "lon": hit.get("LONGITUDE", "") if hit else "",
                   "matched_address": hit.get("ADDRESS", "") if hit else "",
                   "match_type": match_type, "query_used": query,
                   "retrieved_utc": now_utc()}
            cache.write(json.dumps(rec) + "\n")
            cache.flush()
            done[(block, street)] = rec
            counts[match_type] += 1
            if i % 100 == 0 or i == len(todo):
                log(f"done {i}/{len(todo)} this run; exact {counts['exact']}, "
                    f"expanded {counts['expanded']}, none {counts['none']}")
    write_csv(done, pairs)
    log(f"wrote {OUT}")


if __name__ == "__main__":
    main()
