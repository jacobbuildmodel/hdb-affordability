#!/usr/bin/env python3
# Pull block, street_name and month only (no price field) from each HDB
# resale dataset on data.gov.sg, page by page, and write the unique pairs.
import json, time, urllib.request, csv, sys
IDS = ["d_ebc5ab87086db484f88045b47411ebc5", "d_43f493c6c50d54243cc1eab0df142d6a",
       "d_2d5ff9ea31397b66239f245f57751537", "d_ea9ed51da2787afaf8e51f827c304208",
       "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"]
LIMIT = 10000
rows = {}
T0 = time.time()
for rid in IDS:
    off, total, n = 0, None, 0
    while total is None or off < total:
        url = (f"https://data.gov.sg/api/action/datastore_search?resource_id={rid}"
               f"&fields=block,street_name,month&limit={LIMIT}&offset={off}")
        for attempt in range(8):
            try:
                d = json.load(urllib.request.urlopen(url, timeout=120))
                if "result" in d:
                    break
            except Exception as e:
                d = {"err": str(e)}
            time.sleep(10 * (attempt + 1))
        else:
            sys.exit(f"failed {rid} offset {off}: {d}")
        r = d["result"]
        total = r["total"]
        for rec in r["records"]:
            assert set(rec) <= {"block", "street_name", "month", "_id"}, rec.keys()
            key = (rec["block"].strip().upper(), rec["street_name"].strip().upper())
            m = rec["month"]
            lo, hi = rows.get(key, (m, m))
            rows[key] = (min(lo, m), max(hi, m))
            n += 1
        off += LIMIT
        print(rid[:10], off, total, len(rows), round(time.time()-T0), flush=True)
        time.sleep(2)
    print(rid, "rows read", n, "of", total, flush=True)
with open("cargradient/out/addresses.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["block", "street_name", "first_month", "last_month"])
    for (b, s), (lo, hi) in sorted(rows.items(), key=lambda x: (x[0][1], x[0][0])):
        w.writerow([b, s, lo, hi])
print("unique pairs", len(rows))
