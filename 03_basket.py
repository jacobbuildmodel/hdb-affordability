"""
03_basket.py

Composition correction, method B: a fixed-basket Laspeyres index.

Method A regresses the composition out. This one holds it still instead, and makes
no functional-form assumption at all. If the two agree, the correction is sound.
If they disagree past the threshold in THESIS.md test T6, no single
constant-quality number gets published and a range is published instead.

The construction:

  Cells are town x floor-area band x remaining-lease band, within four-room flats.
  The median price is taken within each cell in each year. Cells are then
  aggregated using each cell's share of BASE YEAR transactions, held fixed. So the
  basket never changes; only the prices inside it do.

  Cells that are empty in any year of the window are dropped, and the weights are
  renormalised over the survivors. That is a real cost and it is reported: a cell
  that stops trading is a cell whose price path cannot be followed. The share of
  base-year transactions that survive the filter is printed, and if it is low the
  index is describing a shrinking part of the market.

Lease bands are included in the cell definition because the stock is ageing and a
Laspeyres index that ignores lease would drift for exactly the reason the index
exists to prevent.

Reads:  out/resale_clean.csv
Writes: out/index_basket.csv
        out/basket_diagnostics.txt

Usage:  python 03_basket.py
        python 03_basket.py --base 2017
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

FLAT_TYPE = "4 ROOM"
FIRST_YEAR, LAST_YEAR = 2013, 2025

AREA_EDGES = [0, 85, 95, 105, 1000]
AREA_LABELS = ["under85", "85to94", "95to104", "105plus"]
LEASE_EDGES = [0, 60, 75, 90, 200]
LEASE_LABELS = ["under60", "60to74", "75to89", "90plus"]


def fail(msg):
    raise AssertionError("BASKET STOPPED: %s" % msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=int, default=FIRST_YEAR)
    ap.add_argument("--min-cell", type=int, default=5,
                    help="minimum transactions for a cell-year to count")
    args = ap.parse_args()

    src = os.path.join(OUT, "resale_clean.csv")
    if not os.path.exists(src):
        fail("out/resale_clean.csv not found. Run 01_clean.py first.")

    df = pd.read_csv(src, low_memory=False)
    df = df[df["flat_type"].str.upper().str.strip() == FLAT_TYPE]
    df = df[(df["year"] >= FIRST_YEAR) & (df["year"] <= LAST_YEAR)].copy()
    if df.empty:
        fail("no %s rows in the window" % FLAT_TYPE)

    df["town"] = df["town"].astype(str).str.upper().str.strip()
    df["area_band"] = pd.cut(df["floor_area_sqm"], AREA_EDGES, labels=AREA_LABELS,
                             right=False)
    df["lease_band"] = pd.cut(df["lease_years"], LEASE_EDGES, labels=LEASE_LABELS,
                              right=False)
    df = df[df["area_band"].notna() & df["lease_band"].notna()]
    df["cell"] = (df["town"].astype(str) + " | " + df["area_band"].astype(str)
                  + " | " + df["lease_band"].astype(str))

    years = list(range(FIRST_YEAR, LAST_YEAR + 1))

    counts = df.groupby(["cell", "year"]).size().unstack("year").reindex(
        columns=years).fillna(0)
    med = df.groupby(["cell", "year"])["resale_price"].median().unstack(
        "year").reindex(columns=years)

    thick = (counts >= args.min_cell).all(axis=1)
    kept = thick[thick].index.tolist()
    if not kept:
        fail("no cell has at least %d transactions in every year. Widen the bands."
             % args.min_cell)

    base_counts = counts[args.base]
    covered = float(base_counts.loc[kept].sum() / base_counts.sum())

    w = base_counts.loc[kept]
    w = w / w.sum()
    m = med.loc[kept]

    rel = m.div(m[args.base], axis=0)          # each cell's price relative to base
    index = 100.0 * (rel.mul(w, axis=0)).sum(axis=0)

    raw = df.groupby("year")["resale_price"].median()
    raw_index = 100.0 * raw / raw[args.base]

    out = pd.DataFrame({
        "year": years,
        "index": index.reindex(years).values,
        "raw_index": raw_index.reindex(years).values,
        "n_cells": len(kept),
        "base_year": args.base,
    })
    out.to_csv(os.path.join(OUT, "index_basket.csv"), index=False,
               lineterminator="\n")

    lines = []
    lines.append("Fixed-basket Laspeyres index, %s flats, %d to %d"
                 % (FLAT_TYPE, FIRST_YEAR, LAST_YEAR))
    lines.append("base year %d = 100, weights are %d transaction shares held fixed"
                 % (args.base, args.base))
    lines.append("")
    lines.append("cells defined            town x floor-area band x lease band")
    lines.append("cells in total           %d" % len(counts))
    lines.append("cells present in every year with at least %d sales  %d"
                 % (args.min_cell, len(kept)))
    lines.append("share of %d transactions covered by those cells     %.1f%%"
                 % (args.base, 100 * covered))
    if covered < 0.5:
        lines.append("WARNING: the surviving cells are less than half the base-year "
                     "market. This index describes a shrinking segment and should "
                     "not be treated as the market.")
    lines.append("")
    lines.append("%-6s %10s %10s" % ("year", "index", "raw_index"))
    for _, r in out.iterrows():
        lines.append("%-6d %10.2f %10.2f" % (r["year"], r["index"], r["raw_index"]))

    lines.append("")
    lines.append("%d to %d, fixed basket   %+.1f%%"
                 % (FIRST_YEAR, LAST_YEAR,
                    100.0 * (out["index"].iloc[-1] / out["index"].iloc[0] - 1)))

    hed_path = os.path.join(OUT, "index_hedonic.csv")
    if os.path.exists(hed_path):
        hed = pd.read_csv(hed_path)
        a = 100.0 * (hed["index"].iloc[-1] / hed["index"].iloc[0] - 1)
        b = 100.0 * (out["index"].iloc[-1] / out["index"].iloc[0] - 1)
        gap = abs(a - b)
        lines.append("%d to %d, hedonic        %+.1f%%" % (FIRST_YEAR, LAST_YEAR, a))
        lines.append("")
        lines.append("T6, the two methods differ by %.1f percentage points" % gap)
        if gap < 2.0:
            lines.append("T6 PASSES. Under 2 points. The composition correction is "
                         "not contested and a single constant-quality number is "
                         "publishable.")
        elif gap > 5.0:
            lines.append("T6 FAILS, F6 TRIGGERED. Over 5 points. No single "
                         "constant-quality number may be published. Publish the "
                         "range %.1f%% to %.1f%%." % (min(a, b), max(a, b)))
        else:
            lines.append("T6 INCONCLUSIVE, between 2 and 5 points. Both are "
                         "published and the text says the correction is doing "
                         "contested work.")
        merged = pd.DataFrame({"year": out["year"],
                               "hedonic": hed["index"].values,
                               "basket": out["index"].values})
        merged["gap_pts"] = merged["hedonic"] - merged["basket"]
        lines.append("")
        lines.append("year by year:")
        lines.append("%-6s %10s %10s %8s" % ("year", "hedonic", "basket", "gap"))
        for _, r in merged.iterrows():
            lines.append("%-6d %10.2f %10.2f %8.2f"
                         % (r["year"], r["hedonic"], r["basket"], r["gap_pts"]))

    text = "\n".join(lines)
    with open(os.path.join(OUT, "basket_diagnostics.txt"), "w",
              newline="\n") as fh:
        fh.write(text + "\n")
    print(text)
    print("")
    print("out/index_basket.csv written")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
