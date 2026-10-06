"""
make_fixtures.py -- invented data in the exact shape of cargradient/raw and
the pre-seal inputs in cargradient/out, so steps 10-15 run end to end without
touching a real price. Every number here is made up.

make(root, **scenario) writes ROOT/raw/..., ROOT/out/{blocks_geocoded,
block_distance, station_points, street_points}.csv and ROOT/THESIS.md.

The scenario sets the true COE x distance slope (beta, in dollars per square
metre per km per dollar of premium) in each period, whether the quota moves
the premium (first-stage strength) in each period, and how many sales sit on
blocks OneMap could not place. Prices follow THESIS section 3's model:

  price_psm = block effect + quarter effect + lease effect
              + beta(period) x COE premium x km to Raffles Place + noise
"""
import csv
import json
import math
import os
import random

MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
RAFFLES = (1.2840, 103.8514)
CITYHALL = (1.2932, 103.8524)
HEADER_OLD = ["month", "town", "flat_type", "block", "street_name", "storey_range", "floor_area_sqm",
              "flat_model", "lease_commence_date", "resale_price"]
HEADER_NEW = HEADER_OLD[:-1] + ["remaining_lease", "resale_price"]
FILES = [("d_ebc5ab87086db484f88045b47411ebc5", "1990-01", "1999-12", HEADER_OLD),
         ("d_43f493c6c50d54243cc1eab0df142d6a", "2000-01", "2012-02", HEADER_OLD),
         ("d_2d5ff9ea31397b66239f245f57751537", "2012-03", "2014-12", HEADER_OLD),
         ("d_ea9ed51da2787afaf8e51f827c304208", "2015-01", "2016-12", HEADER_NEW),
         ("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", "2017-01", "2026-10", HEADER_NEW)]
SERIES = {20: "Cars Up To 1600cc And 97kW, Quota, 1st Bidding",
          21: "Cars Up To 1600cc And 97kW, Successful Bids, 1st Bidding",
          23: "Cars Up To 1600cc And 97kW, Quota Premium, 1st Bidding",
          24: "Cars Up To 1600cc And 97kW, Quota, 2nd Bidding",
          25: "Cars Up To 1600cc And 97kW, Successful Bids, 2nd Bidding",
          27: "Cars Up To 1600cc And 97kW, Quota Premium, 2nd Bidding",
          30: "Cars Above 1600cc Or 97kW, Quota, 1st Bidding",
          31: "Cars Above 1600cc Or 97kW, Successful Bids, 1st Bidding",
          33: "Cars Above 1600cc Or 97kW, Quota Premium, 1st Bidding",
          34: "Cars Above 1600cc Or 97kW, Quota, 2nd Bidding",
          35: "Cars Above 1600cc Or 97kW, Successful Bids, 2nd Bidding",
          37: "Cars Above 1600cc Or 97kW, Quota Premium, 2nd Bidding"}

# beta by period; "pre" is 2002Q2-2012Q1, "before" 2012Q2-2017Q4, "after" 2018Q1 on.
BASE = dict(beta_pre=-0.004, beta_before=-0.004, beta_after=-0.0015, strong_pre=True,
            strong_before=True, strong_after=True, unmatched_t2_share=0.0, blocks=240,
            sales_per_block_quarter=1, noise=60.0, seed=7, actual_gap_shift=None)


def period(y, m):
    if (y, m) < (2012, 3):
        return "pre"
    if (y, m) < (2018, 1):
        return "before"
    return "after"


def months(first, last):
    y, m = int(first[:4]), int(first[5:])
    while (y, m) <= (int(last[:4]), int(last[5:])):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def offset(lat, lon, km, bearing):
    dlat = km / 111.32 * math.cos(bearing)
    dlon = km / (111.32 * math.cos(math.radians(lat))) * math.sin(bearing)
    return lat + dlat, lon + dlon


def make(root, **kw):
    s = dict(BASE, **kw)
    rnd = random.Random(s["seed"])
    raw = os.path.join(root, "raw")
    out = os.path.join(root, "out")
    for d in (os.path.join(raw, "resale"), os.path.join(raw, "singstat_M651121"), out):
        os.makedirs(d, exist_ok=True)

    # COE biddings, Feb 2002 to Sep 2026; no bidding in Apr-Jun 2020.
    coe = {k: {} for k in SERIES}
    quarter_prem = {}
    for y, m in months("2002-02", "2026-09"):
        if (y, m) in ((2020, 4), (2020, 5), (2020, 6)):
            continue
        per = period(y, m)
        strong = s[{"pre": "strong_pre", "before": "strong_before", "after": "strong_after"}[per]]
        for b in (1, 2):
            qa, qb = rnd.randint(500, 2500), rnd.randint(400, 2200)
            sa, sb = qa - rnd.randint(0, 20), qb - rnd.randint(0, 20)
            base = 120000 - 25 * (qa + qb) if strong else rnd.uniform(15000, 110000)
            pa = max(2000.0, base + rnd.gauss(0, 3000))
            pb = max(2500.0, pa * 1.15 + rnd.gauss(0, 2000))
            key = f"{y} {MON[m - 1]}"
            for n, v in ((20, qa), (21, sa), (23, pa), (24, qa), (25, sa), (27, pa),
                         (30, qb), (31, sb), (33, pb), (34, qb), (35, sb), (37, pb)):
                if (n in (20, 21, 23) and b == 1) or (n in (24, 25, 27) and b == 2) or \
                   (n in (30, 31, 33) and b == 1) or (n in (34, 35, 37) and b == 2):
                    coe[n][key] = v
            q = f"{y}Q{(m - 1) // 3 + 1}"
            quarter_prem.setdefault(q, []).append((pa * sa + pb * sb) / (sa + sb))
    for n, rows in coe.items():
        cols = [{"key": k, "value": "%.2f" % v if n in (23, 27, 33, 37) else "%d" % v} for k, v in rows.items()]
        doc = {"Data": {"row": [{"seriesNo": str(n), "rowText": SERIES[n], "columns": cols}]}}
        json.dump(doc, open(os.path.join(raw, "singstat_M651121", f"s{n}.json"), "w"))
    qprem = {q: sum(v) / len(v) for q, v in quarter_prem.items()}

    # MRT exits: Raffles Place (2 exits), City Hall (2), and a few elsewhere.
    feats = []
    for name, (la, lo) in (("RAFFLES PLACE MRT STATION", RAFFLES), ("CITY HALL MRT STATION", CITYHALL)):
        for i, d in enumerate((-0.0002, 0.0002)):
            feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lo + d, la + d]},
                          "properties": {"STATION_NA": name, "EXIT_CODE": f"Exit {'AB'[i]}"}})
    for i in range(8):
        la, lo = offset(*RAFFLES, 3 + 2 * i, i)
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lo, la]},
                      "properties": {"STATION_NA": f"STATION {i}", "EXIT_CODE": "Exit A"}})
    json.dump({"type": "FeatureCollection", "features": feats},
              open(os.path.join(raw, "lta_mrt_station_exit.geojson"), "w"))
    with open(os.path.join(out, "station_points.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["station", "exits", "mean_lat", "mean_lon", "nearest_exit", "nearest_lat", "nearest_lon", "gap_m"])
        w.writerow(["RAFFLES PLACE MRT STATION", 2, RAFFLES[0], RAFFLES[1], "Exit A", RAFFLES[0], RAFFLES[1], 0])
        w.writerow(["CITY HALL MRT STATION", 2, CITYHALL[0], CITYHALL[1], "Exit A", CITYHALL[0], CITYHALL[1], 0])

    # Blocks.
    towns = ["ANG MO KIO", "BEDOK", "TAMPINES", "WOODLANDS", "QUEENSTOWN", "PUNGGOL"]
    blocks = []
    n_unmatched = int(round(s["blocks"] * s["unmatched_t2_share"]))
    for i in range(s["blocks"]):
        d = rnd.uniform(1.0, 20.0)
        la, lo = offset(*RAFFLES, d, rnd.uniform(0, 2 * math.pi))
        street = f"STREET {i % 40}"
        blocks.append({"block": str(100 + i), "street": street, "d": d, "lat": la, "lon": lo,
                       "town": towns[i % len(towns)], "fe": rnd.gauss(0, 400),
                       "lease": rnd.randint(1970, 2001), "matched": i >= n_unmatched})
    with open(os.path.join(out, "blocks_geocoded.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block", "street_name", "postal", "lat", "lon", "matched_address", "match_type",
                    "query_used", "retrieved_utc"])
        for b in blocks:
            if b["matched"]:
                w.writerow([b["block"], b["street"], "000000", b["lat"], b["lon"], "X", "exact", "q", "t"])
            else:
                w.writerow([b["block"], b["street"], "", "", "", "", "none", "q", "t"])
    with open(os.path.join(out, "block_distance.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block", "street_name", "match_type", "km_raffles_mean", "km_raffles_nearest",
                    "km_cityhall_mean", "km_cityhall_nearest"])
        for b in blocks:
            if b["matched"]:
                w.writerow([b["block"], b["street"], "exact", b["d"], b["d"], b["d"] + 1.0, b["d"] + 1.0])
            else:
                w.writerow([b["block"], b["street"], "none", "", "", "", ""])
    with open(os.path.join(out, "street_points.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["street_name", "lat", "lon", "matched_address", "query_used", "retrieved_utc"])
        for st in sorted({b["street"] for b in blocks if not b["matched"]}):
            la, lo = offset(*RAFFLES, 10.0, 1.0)
            w.writerow([st, la, lo, "X", "q", "t"])

    # Sales.
    qfe = {}
    rows = {f[0]: [] for f in FILES}
    types = [("3 ROOM", 67.0), ("4 ROOM", 92.0), ("5 ROOM", 112.0)]
    for y, m in months("1995-01", "2026-10"):
        q = f"{y}Q{(m - 1) // 3 + 1}"
        if q not in qfe:
            qfe[q] = rnd.gauss(0, 300) + 40 * (y - 2000)
        if m % 3 != 2:          # one month per quarter carries the sales
            continue
        per = period(y, m)
        beta = s[{"pre": "beta_pre", "before": "beta_before", "after": "beta_after"}[per]]
        coep = qprem.get(q)
        for b in blocks:
            unmatched_here = not b["matched"] and y >= 2016
            if not b["matched"] and not unmatched_here:
                continue
            for _ in range(s["sales_per_block_quarter"]):
                ft, area = types[rnd.randrange(3)]
                area = area + rnd.choice((-3.0, 0.0, 2.0, 5.0))
                lease = min(b["lease"], y)
                rem = 99 - (y - lease)
                shift = 0.0
                if s["actual_gap_shift"] is not None and y >= 2021:
                    shift = s["actual_gap_shift"] * b["d"]
                price_psm = (20000 + b["fe"] + qfe[q] + 15 * rem + (beta * coep * b["d"] if coep else 0.0)
                             + 8 * area + shift + rnd.gauss(0, s["noise"]))
                row = [f"{y}-{m:02d}", b["town"], ft, b["block"], b["street"], "04 TO 06", "%.1f" % area,
                       "MODEL A", str(lease), "%.0f" % (price_psm * area)]
                for fid, a, z, hdr in FILES:
                    if a <= f"{y}-{m:02d}" <= z:
                        if hdr is HEADER_NEW:
                            row = row[:-1] + [f"{rem} years", row[-1]]
                        rows[fid].append(row)
    for fid, a, z, hdr in FILES:
        with open(os.path.join(raw, "resale", fid + ".csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(hdr)
            w.writerows(rows[fid])

    thesis = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "THESIS.md")
    text = open(thesis, encoding="utf-8").read()
    conf = s.get("confidences")
    if conf:
        for t, v in conf.items():
            text = _set_conf(text, t, v)
    open(os.path.join(root, "THESIS.md"), "w", encoding="utf-8").write(text)
    return s


def _set_conf(text, test, pct):
    import re
    sec = re.search(rf"^### {test}\..*?(?=^### |^## |\Z)", text, re.S | re.M)
    new = sec.group(0).replace("**Confidence at seal: [Jacob, at seal].**", f"**Confidence at seal: {pct}%**")
    return text.replace(sec.group(0), new)
