#!/usr/bin/env python3
"""
00_coverage.py -- labels and coverage of the five HDB resale files, by counts
only. Run from the repository root:  python3 cargradient/00_coverage.py

The resale_price column is never parsed, summarised or printed: each row is
split by the csv module and only the columns named in KEEP are looked at.
Output: cargradient/out/coverage.txt (also printed).
"""
import collections
import csv
import os

RAW = "cargradient/raw/resale"
FILES = [  # data.gov.sg collection 189, oldest first
    ("d_ebc5ab87086db484f88045b47411ebc5", "1990-1999, approval date"),
    ("d_43f493c6c50d54243cc1eab0df142d6a", "2000-Feb 2012, approval date"),
    ("d_2d5ff9ea31397b66239f245f57751537", "Mar 2012-Dec 2014, registration date"),
    ("d_ea9ed51da2787afaf8e51f827c304208", "Jan 2015-Dec 2016, registration date"),
    ("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", "Jan 2017 onwards, registration date"),
]
KEEP = ("month", "town", "flat_type", "storey_range", "flat_model", "lease_commence_date",
        "block", "street_name", "floor_area_sqm")
PRICE = "resale_price"


def main():
    lines = []
    total = 0
    for fid, label in FILES:
        path = os.path.join(RAW, fid + ".csv")
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            header = next(r)
            idx = {c: header.index(c) for c in KEEP if c in header}
            n = 0
            months = collections.Counter()
            cats = {c: collections.Counter() for c in ("town", "flat_type", "storey_range", "flat_model")}
            lease = []
            empty_area = 0
            for row in r:
                n += 1
                months[row[idx["month"]]] += 1
                for c in cats:
                    cats[c][row[idx[c]].strip().upper()] += 1
                lease.append(row[idx["lease_commence_date"]])
                if not row[idx["floor_area_sqm"]].strip():
                    empty_area += 1
        total += n
        lines.append(f"{fid}  {label}")
        lines.append(f"  columns: {', '.join(header)}")
        lines.append(f"  price column present: {PRICE in header} (not read)")
        lines.append(f"  rows: {n}; months {min(months)} to {max(months)}; distinct months {len(months)}")
        lines.append(f"  lease_commence_date (a year): {min(lease)} to {max(lease)}")
        lines.append(f"  rows with empty floor_area_sqm: {empty_area}")
        for c, cnt in cats.items():
            lines.append(f"  {c}: {len(cnt)} labels: " + "; ".join(sorted(cnt)))
    lines.append(f"TOTAL rows: {total}")
    text = "\n".join(lines) + "\n"
    os.makedirs("cargradient/out", exist_ok=True)
    open("cargradient/out/coverage.txt", "w", encoding="utf-8").write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
