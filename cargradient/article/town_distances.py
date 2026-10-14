#!/usr/bin/env python3
"""
article/town_distances.py -- each HDB town's median block distance from
Raffles Place, for naming towns in the article (not part of the sealed
pipeline, and not scored).

  python3 cargradient/article/town_distances.py

Reads cargradient/out/block_distance.csv (km_raffles_mean: great-circle km
from each geocoded block to the mean of Raffles Place MRT's exits, the
distance the tests use) and the town label of each block from the resale
files in cargradient/raw/resale/ (block, street_name and town only; no price
is read). A block takes the town it is most often listed under.

Writes cargradient/article/town_distances.csv: town, blocks, median_km (one
decimal, as the article prints it).
Standard library only.
"""
import csv
import glob
import os
import statistics
from collections import Counter, defaultdict

CG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    towns = defaultdict(Counter)
    for path in sorted(glob.glob(os.path.join(CG, "raw", "resale", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                towns[(r["block"].strip().upper(), r["street_name"].strip().upper())][r["town"].strip().upper()] += 1
    km = defaultdict(list)
    with open(os.path.join(CG, "out", "block_distance.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r["block"].strip().upper(), r["street_name"].strip().upper())
            if r["km_raffles_mean"] and key in towns:
                km[towns[key].most_common(1)[0][0]].append(float(r["km_raffles_mean"]))
    rows = sorted(((t, len(v), statistics.median(v)) for t, v in km.items()), key=lambda x: x[2])
    out = os.path.join(CG, "article", "town_distances.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["town", "blocks", "median_km"])
        for t, n, m in rows:
            w.writerow([t, n, "%.1f" % m])
    print("wrote %s: %d towns, %d blocks" % (out, len(rows), sum(n for _, n, _ in rows)))


if __name__ == "__main__":
    main()
