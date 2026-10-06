#!/usr/bin/env python3
"""
05_street_points.py -- one street-level point for each street that holds an
unmatched block-and-street pair (THESIS section 7, sensitivity J).

For each street in out/unmatched.csv: OneMap Search on the expanded street
name; the first result whose ROAD_NAME equals the expanded street (any block
number, or the road itself) gives the point. One call per second, token in
memory only (01_geocode.OneMap). Run from the repository root.

Output: cargradient/out/street_points.csv (street_name, lat, lon,
matched_address, query_used, retrieved_utc); empty lat/lon if no match.

Contains information from OneMap (Singapore Land Authority), under the
Singapore Open Data Licence version 1.0.
"""
import csv
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("geocode", os.path.join(HERE, "01_geocode.py"))
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)


def main():
    streets = sorted({r["street_name"] for r in csv.DictReader(open("cargradient/out/unmatched.csv"))})
    om = G.OneMap()
    rows = []
    for s in streets:
        q = G.expand(s)
        want = G.norm(q)
        hit = next((r for r in om.search(q).get("results", []) if G.norm(r.get("ROAD_NAME", "")) == want), None)
        rows.append([s, hit.get("LATITUDE", "") if hit else "", hit.get("LONGITUDE", "") if hit else "",
                     hit.get("ADDRESS", "") if hit else "", q, G.now_utc()])
    with open("cargradient/out/street_points.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["street_name", "lat", "lon", "matched_address", "query_used", "retrieved_utc"])
        w.writerows(rows)
    print(f"streets {len(rows)}, with a point {sum(1 for r in rows if r[1])}")


if __name__ == "__main__":
    main()
