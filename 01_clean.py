"""
01_clean.py

Harmonises the HDB resale transaction files into one tidy table.

Reads:  raw/resale_mar2012_dec2014.csv
        raw/resale_jan2015_dec2016.csv
        raw/resale_jan2017_onwards.csv      (or the gzipped or four-room-filtered
                                             variant, see raw/RETRIEVED.txt)
Writes: out/resale_clean.csv
        out/clean_report.txt

Every structural assumption is an assertion. If HDB reshapes a file or renames a
column, this stops rather than silently producing a wrong number.

Two corrections are documented here because they are the ones a reviewer will ask
about.

CORRECTION 1: remaining lease.
  The `remaining_lease` column exists only from the January 2017 file onwards, and
  in that file it is a string like "61 years 04 months". For earlier years it is
  reconstructed as 99 minus the flat's age at sale, from `lease_commence_date`.
  The script asserts the reconstruction reproduces the published column on the
  overlapping period to within one year. If it does not, it fails loudly and the
  hedonic must run on flat age instead.

CORRECTION 2: registration date, not transaction date.
  The `month` column is when the resale was registered, not when the price was
  agreed. Registration follows agreement by a variable lag of roughly one to two
  months. Nothing in this pipeline makes a month-level claim. Everything is
  aggregated to calendar years, and the annual figures carry the same lag at both
  ends of the window so the comparison is unaffected. This is recorded in
  out/clean_report.txt so it appears in the audit trail rather than only in a
  comment.

Usage:  python 01_clean.py
        python 01_clean.py --inspect     print each raw file's shape and stop
"""

import argparse
import glob
import gzip
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "out")

# filename stem -> (first month expected, last month expected or None for open)
EXPECTED = {
    "resale_mar2012_dec2014": ("2012-03", "2014-12"),
    "resale_jan2015_dec2016": ("2015-01", "2016-12"),
    "resale_jan2017_onwards": ("2017-01", None),
}

REQUIRED = ["month", "town", "flat_type", "block", "street_name", "storey_range",
            "floor_area_sqm", "flat_model", "lease_commence_date", "resale_price"]

LEASE_YEARS = 99


def fail(msg):
    raise AssertionError(
        "CLEANING STOPPED: %s\n"
        "The raw data does not look the way this script expects. Run with "
        "--inspect, compare against README.md, and fix the script rather than "
        "the data." % msg)


def open_maybe_gz(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return open(path, "r", encoding="utf-8", newline="")


def find_raw(stem):
    """Accept plain, gzipped, or the four-room-filtered fallback."""
    for pat in ("%s.csv" % stem, "%s.csv.gz" % stem, "%s*.csv" % stem,
                "%s*.csv.gz" % stem):
        hits = sorted(glob.glob(os.path.join(RAW, pat)))
        if hits:
            return hits[0]
    return None


def load(stem, required=True):
    path = find_raw(stem)
    if path is None:
        if required:
            fail("no raw file found for '%s'. See DATA_REQUEST.md." % stem)
        return None, None
    with open_maybe_gz(path) as fh:
        df = pd.read_csv(fh, dtype=str, keep_default_na=False)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        fail("%s is missing columns %s. Found: %s"
             % (os.path.basename(path), missing, list(df.columns)))
    df["source_file"] = os.path.basename(path)
    return df, path


def to_number(val):
    txt = str(val).strip().replace(",", "").replace("$", "")
    if txt in ("", "na", "n.a.", "-", "NA"):
        return float("nan")
    try:
        return float(txt)
    except ValueError:
        return float("nan")


def parse_remaining_lease(val):
    """'61 years 04 months' or '61' or '61.5' -> years as a float."""
    txt = str(val).strip().lower()
    if txt in ("", "na", "-"):
        return float("nan")
    m = re.match(r"^\s*(\d+)\s*years?(?:\s*(\d+)\s*months?)?\s*$", txt)
    if m:
        yrs = int(m.group(1))
        mos = int(m.group(2)) if m.group(2) else 0
        return yrs + mos / 12.0
    try:
        return float(txt)
    except ValueError:
        return float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inspect", action="store_true")
    args = ap.parse_args()

    if args.inspect:
        for p in sorted(glob.glob(os.path.join(RAW, "*.csv*"))):
            with open_maybe_gz(p) as fh:
                df = pd.read_csv(fh, dtype=str, nrows=5, keep_default_na=False)
            print("=" * 70)
            print("%s  (%d bytes on disk)" % (os.path.basename(p), os.path.getsize(p)))
            print("columns: %s" % list(df.columns))
            print(df.head(3).to_string())
        return

    os.makedirs(OUT, exist_ok=True)
    report = []
    frames = []

    for stem, (first, last) in EXPECTED.items():
        required = stem == "resale_jan2017_onwards"
        df, path = load(stem, required=required)
        if df is None:
            report.append("MISSING  %s  window falls back, see README" % stem)
            print("missing (not required): %s" % stem)
            continue

        bad = df[~df["month"].str.fullmatch(r"(19|20)\d{2}-\d{2}")]
        if len(bad):
            fail("%s has %d rows whose month is not YYYY-MM, e.g. %s"
                 % (stem, len(bad), bad["month"].head(3).tolist()))
        lo, hi = df["month"].min(), df["month"].max()
        if lo != first:
            fail("%s starts at %s, expected %s" % (stem, lo, first))
        if last is not None and hi != last:
            fail("%s ends at %s, expected %s" % (stem, hi, last))

        report.append("%-28s %8d rows  %s to %s  from %s"
                      % (stem, len(df), lo, hi, os.path.basename(path)))
        frames.append(df)

    if not frames:
        fail("no resale files loaded at all")

    df = pd.concat(frames, ignore_index=True, sort=False)

    df["resale_price"] = df["resale_price"].map(to_number)
    df["floor_area_sqm"] = df["floor_area_sqm"].map(to_number)
    df["lease_commence_date"] = df["lease_commence_date"].map(to_number)
    df["year"] = df["month"].str.slice(0, 4).astype(int)
    df["flat_type"] = df["flat_type"].str.upper().str.strip()
    df["town"] = df["town"].str.upper().str.strip()

    for col in ("resale_price", "floor_area_sqm", "lease_commence_date"):
        n = int(df[col].isna().sum())
        if n:
            fail("%d rows have an unparseable %s" % (n, col))
    if (df["resale_price"] <= 0).any():
        fail("non-positive resale prices present")

    # storey_range '04 TO 06' -> midpoint, an ordinal the hedonic can use
    def storey_mid(txt):
        nums = re.findall(r"\d+", str(txt))
        if len(nums) >= 2:
            return (int(nums[0]) + int(nums[1])) / 2.0
        return float(nums[0]) if nums else float("nan")

    df["storey_mid"] = df["storey_range"].map(storey_mid)
    if df["storey_mid"].isna().any():
        fail("%d rows have an unparseable storey_range"
             % int(df["storey_mid"].isna().sum()))

    # CORRECTION 1: remaining lease
    df["lease_years_recon"] = LEASE_YEARS - (df["year"] - df["lease_commence_date"])
    if "remaining_lease" in df.columns:
        pub = df["remaining_lease"].map(parse_remaining_lease)
        have = pub.notna()
        if have.sum() == 0:
            report.append("remaining_lease column present but entirely unparseable; "
                          "reconstruction used throughout")
        else:
            diff = (pub[have] - df.loc[have, "lease_years_recon"]).abs()
            worst = float(diff.max())
            share_ok = float((diff <= 1.0).mean())
            report.append("remaining_lease check: %d rows compared, worst gap "
                          "%.2f years, %.4f within 1 year" % (int(have.sum()), worst, share_ok))
            if share_ok < 0.99:
                fail("reconstruction matches the published remaining_lease on only "
                     "%.2f%% of rows within one year. Run the hedonic on flat age "
                     "instead and say so." % (100 * share_ok))
        df["lease_years"] = pub.where(pub.notna(), df["lease_years_recon"])
    else:
        report.append("no remaining_lease column in any file; reconstruction used "
                      "throughout")
        df["lease_years"] = df["lease_years_recon"]

    df["flat_age"] = df["year"] - df["lease_commence_date"]

    dup = int(df.duplicated(subset=["month", "block", "street_name", "storey_range",
                                    "floor_area_sqm", "resale_price"]).sum())
    report.append("exact duplicate transactions on the natural key: %d (kept, "
                  "genuine repeat sales in a month are possible)" % dup)

    keep = ["month", "year", "town", "flat_type", "block", "street_name",
            "storey_range", "storey_mid", "floor_area_sqm", "flat_model",
            "lease_commence_date", "lease_years", "flat_age", "resale_price",
            "source_file"]
    out = df[keep].sort_values(["month", "town", "block"]).reset_index(drop=True)
    out.to_csv(os.path.join(OUT, "resale_clean.csv"), index=False, lineterminator="\n")

    four = out[out["flat_type"] == "4 ROOM"]
    report.append("")
    report.append("TOTAL          %8d rows  %s to %s" % (len(out), out["month"].min(),
                                                          out["month"].max()))
    report.append("4 ROOM         %8d rows  %.1f%% of all transactions"
                  % (len(four), 100.0 * len(four) / len(out)))
    report.append("complete years %8s" % ", ".join(
        str(y) for y in sorted(out.groupby("year")["month"].nunique()
                               .loc[lambda s: s == 12].index)))
    report.append("")
    report.append("REGISTRATION DATE, NOT TRANSACTION DATE. The month column is when "
                  "the resale was registered with HDB, which follows the agreed "
                  "price by a variable lag of roughly one to two months. No claim "
                  "in this analysis is made at month level. All figures are annual, "
                  "and the lag applies equally at both ends of the window.")

    with open(os.path.join(OUT, "clean_report.txt"), "w", newline="\n") as fh:
        fh.write("\n".join(report) + "\n")

    print("\n".join(report))
    print("")
    print("out/resale_clean.csv written")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
