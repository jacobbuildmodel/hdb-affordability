#!/usr/bin/env python3
"""
03_unmatched.py -- how many resale rows each block-and-street pair covers,
and which pairs OneMap could not place. Counts rows only; the price field is
never requested (the script asserts it). Run from the repository root.

    python cargradient/03_unmatched.py --counts   # pull counts from data.gov.sg
    python cargradient/03_unmatched.py            # report, after 01_geocode.py

Windows (THESIS.md section 5), by sale month:
  T1: 2002-04 to 2015-12, less 2012-01 to 2012-03 (2012Q1 dropped)
  T2: 2016-01 to 2026-09, less 2020-04 to 2020-06 (no COE bidding)
Outputs:
  cargradient/out/address_rowcounts.csv  rows per pair: all, T1, T2
  cargradient/out/unmatched.csv          unmatched pairs, with first and last
                                         month, row counts, and a flag for
                                         pairs last sold before 2010
"""
import csv
import json
import sys
import time
import urllib.request

IDS = ["d_ebc5ab87086db484f88045b47411ebc5", "d_43f493c6c50d54243cc1eab0df142d6a",
       "d_2d5ff9ea31397b66239f245f57751537", "d_ea9ed51da2787afaf8e51f827c304208",
       "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"]
COUNTS = "cargradient/out/address_rowcounts.csv"


def in_t1(m):
    return "2002-04" <= m <= "2015-12" and not ("2012-01" <= m <= "2012-03")


def in_t2(m):
    return "2016-01" <= m <= "2026-09" and not ("2020-04" <= m <= "2020-06")


def pull_counts():
    c = {}
    for rid in IDS:
        off, total = 0, None
        while total is None or off < total:
            url = (f"https://data.gov.sg/api/action/datastore_search?resource_id={rid}"
                   f"&fields=block,street_name,month&limit=10000&offset={off}")
            for attempt in range(8):
                try:
                    d = json.load(urllib.request.urlopen(url, timeout=120))
                    if "result" in d:
                        break
                except Exception:
                    pass
                time.sleep(10 * (attempt + 1))
            else:
                sys.exit(f"failed {rid} at offset {off}")
            total = d["result"]["total"]
            for rec in d["result"]["records"]:
                assert set(rec) <= {"block", "street_name", "month", "_id"}, rec.keys()
                k = (rec["block"].strip().upper(), rec["street_name"].strip().upper())
                a = c.setdefault(k, [0, 0, 0])
                a[0] += 1
                a[1] += in_t1(rec["month"])
                a[2] += in_t2(rec["month"])
            off += 10000
            time.sleep(2)
        print(rid, "done", flush=True)
    with open(COUNTS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block", "street_name", "rows_all", "rows_t1", "rows_t2"])
        for (b, s), a in sorted(c.items(), key=lambda x: (x[0][1], x[0][0])):
            w.writerow([b, s, *a])


def report():
    cnt = {(r["block"], r["street_name"]): r for r in csv.DictReader(open(COUNTS))}
    addr = {(r["block"], r["street_name"]): r
            for r in csv.DictReader(open("cargradient/out/addresses.csv"))}
    geo = {(r["block"], r["street_name"]): r
           for r in csv.DictReader(open("cargradient/out/blocks_geocoded.csv"))}
    assert set(cnt) == set(addr), "count file and addresses.csv disagree"
    missing = set(addr) - set(geo)
    if missing:
        sys.exit(f"{len(missing)} pairs not geocoded yet; run 01_geocode.py first")
    tot = {"all": 0, "t1": 0, "t2": 0}
    un = {"all": 0, "t1": 0, "t2": 0}
    types = {}
    rows = []
    for k, a in addr.items():
        c = cnt[k]
        mt = geo[k]["match_type"]
        types[mt] = types.get(mt, 0) + 1
        for w, col in (("all", "rows_all"), ("t1", "rows_t1"), ("t2", "rows_t2")):
            tot[w] += int(c[col])
            if mt == "none":
                un[w] += int(c[col])
        if mt == "none":
            rows.append([k[0], k[1], a["first_month"], a["last_month"],
                         c["rows_all"], c["rows_t1"], c["rows_t2"],
                         "yes" if a["last_month"] < "2010-01" else "no"])
    rows.sort(key=lambda r: (r[1], r[0]))
    with open("cargradient/out/unmatched.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block", "street_name", "first_month", "last_month", "rows_all",
                    "rows_t1", "rows_t2", "last_sold_before_2010"])
        w.writerows(rows)
    print("match types:", types)
    for w in ("all", "t1", "t2"):
        print(f"{w}: unmatched rows {un[w]} of {tot[w]} = {100 * un[w] / tot[w]:.2f}%")
    pre = [r for r in rows if r[7] == "yes"]
    print(f"unmatched pairs {len(rows)}, of which last sold before 2010: {len(pre)}")


if __name__ == "__main__":
    pull_counts() if "--counts" in sys.argv else report()
