#!/usr/bin/env python3
"""
article/town_prices.py -- median HDB resale price per square metre by town
and calendar year, for the article's raw Toa Payoh and Woodlands comparison
(not part of the sealed pipeline, and not scored).

  python3 cargradient/article/town_prices.py

Reads every file in cargradient/raw/resale/: month, town, resale_price and
floor_area_sqm. Price per square metre is resale_price / floor_area_sqm, as
in THESIS section 3. The year is the first four characters of month (the
approval month to February 2012, the registration month from March 2012).

Writes cargradient/article/town_prices.csv: town, year, sales,
median_psm (whole dollars). Standard library only.
"""
import csv
import glob
import os
import statistics
from collections import defaultdict

CG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    psm = defaultdict(list)
    for path in sorted(glob.glob(os.path.join(CG, "raw", "resale", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                area = float(r["floor_area_sqm"])
                if area > 0:
                    psm[(r["town"].strip().upper(), r["month"][:4])].append(float(r["resale_price"]) / area)
    out = os.path.join(CG, "article", "town_prices.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["town", "year", "sales", "median_psm"])
        for (town, year), v in sorted(psm.items()):
            w.writerow([town, year, len(v), "%.0f" % statistics.median(v)])
    print("wrote %s: %d town-years" % (out, len(psm)))


if __name__ == "__main__":
    main()
