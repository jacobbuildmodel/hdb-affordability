"""
cglib.py -- what every cargradient analysis step (10-15) shares: paths, the
seal guard, the windows and thresholds THESIS.md fixes, and output helpers.
No tested number is computed here, so 15_reproduce.py stays a separate path.

Every step takes --root DIR (default: cargradient/). It reads DIR/raw and the
pre-seal inputs in DIR/out (block_distance.csv, blocks_geocoded.csv,
street_points.csv), and writes DIR/out, DIR/figs and DIR/RESULTS.md. The
synthetic fixtures (tests/) run the same way, with --root pointing at a
temporary copy.

The guard: nothing reads resale prices from the real cargradient/raw/ unless
cargradient/SEALED exists. 10_load.py and 15_reproduce.py call guard() before
opening any resale file.
"""
import argparse
import csv
import io
import os
import re
import sys

CG = os.path.dirname(os.path.abspath(__file__))
REAL_RAW = os.path.realpath(os.path.join(CG, "raw"))
SEALED = os.path.join(CG, "SEALED")
FLOAT = "%.8g"

# Raw files (raw/RETRIEVED.txt). Resale files oldest first; the first two are
# on the approval-date basis, the rest on the registration-date basis.
RESALE = ("d_ebc5ab87086db484f88045b47411ebc5", "d_43f493c6c50d54243cc1eab0df142d6a",
          "d_2d5ff9ea31397b66239f245f57751537", "d_ea9ed51da2787afaf8e51f827c304208",
          "d_8b84c4ee58e3cfc0ece0d773c8ca6abc")
# SingStat M651121 series: (premium, successful bids, quota) per bidding.
COE_SERIES = {("A", 1): (23, 21, 20), ("A", 2): (27, 25, 24),
              ("B", 1): (33, 31, 30), ("B", 2): (37, 35, 34)}
EXITS = "lta_mrt_station_exit.geojson"

# THESIS section 5: windows, as year-quarter labels "YYYYQn".
T1_FIRST, T1_LAST, T1_DROP = "2002Q2", "2015Q4", ("2012Q1",)
POST12_FIRST = "2012Q2"            # after the March 2012 switch (option (a))
T2_FIRST, T2_LAST, T2_DROP = "2016Q1", "2026Q3", ("2020Q2",)
T3_BEFORE = ("2012Q2", "2017Q3")
T3_BEFORE_SENS = ("2016Q1", "2017Q3")   # sensitivity G
T3_AFTER = ("2018Q2", "2026Q3")
T3_DROP = ("2020Q2",)
WFH = ("2020Q1", "2022Q4")              # sensitivity F
SPLIT_A = ("2002Q2", "2011Q4")          # sensitivity A, approval basis
SPLIT_B = ("2012Q2", "2015Q4")          # sensitivity A, registration basis
CALC_YEARS = (2020, 2023)               # section 7A
CALC_NEAR_KM, CALC_FAR_KM = 5.0, 20.0

# THESIS section 6: thresholds.
GEO_MIN = 0.95          # gate 1: share of the window's sales geocoded
F_MIN = 10.0            # gate 2: first-stage F
Z95 = 1.959963984540054
LEASE_YEARS, LEASE_BAND = 99, 5
MRT_FAR_KM = 1.0        # sensitivity I
BOOT_N, BOOT_SEED = 999, 20261006
SCORED = ("T1", "T2", "T3")


def args(description, extra=None):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--root", default=CG, help="directory holding raw/ and out/ (default: cargradient/)")
    if extra:
        extra(p)
    a = p.parse_args()
    a.root = os.path.abspath(a.root)
    return a


def paths(root):
    root = os.path.abspath(root)
    thesis = os.path.join(root, "THESIS.md")
    return {"root": root, "raw": os.path.join(root, "raw"), "out": os.path.join(root, "out"),
            "figs": os.path.join(root, "figs"), "results": os.path.join(root, "RESULTS.md"),
            "thesis": thesis if os.path.exists(thesis) else os.path.join(CG, "THESIS.md")}


def guard(raw_dir):
    """Refuse to read resale prices from the real cargradient/raw/ before the
    seal. Returns the path."""
    if os.path.realpath(raw_dir) == REAL_RAW and not os.path.exists(SEALED):
        sys.stderr.write("REFUSED: cargradient/raw/ holds the real resale prices and "
                         "cargradient/SEALED does not exist. The thesis is not sealed; run on "
                         "the synthetic fixtures with --root, or seal first.\n")
        raise SystemExit(3)
    return raw_dir


def quarter(month):
    """'YYYY-MM' -> 'YYYYQn'."""
    return f"{month[:4]}Q{(int(month[5:7]) - 1) // 3 + 1}"


def qrange(first, last):
    out, y, q = [], int(first[:4]), int(first[5])
    while f"{y}Q{q}" <= last:
        out.append(f"{y}Q{q}")
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


def window(name):
    """Quarters in a scored window, drops removed."""
    if name == "T1":
        return [q for q in qrange(T1_FIRST, T1_LAST) if q not in T1_DROP]
    if name == "T2":
        return [q for q in qrange(T2_FIRST, T2_LAST) if q not in T2_DROP]
    if name == "T3_before":
        return qrange(*T3_BEFORE)
    if name == "T3_after":
        return [q for q in qrange(*T3_AFTER) if q not in T3_DROP]
    raise KeyError(name)


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return str(v)
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f != f:
        return ""
    return FLOAT % f


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in rows:
        w.writerow([fmt(x) for x in r])
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(buf.getvalue())


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def confidences(thesis_path):
    """{test: probability or None} from each test's 'Confidence at seal:'
    line. '[Jacob, at seal]' (not yet set) gives None."""
    text = open(thesis_path, encoding="utf-8").read()
    out = {}
    for t in SCORED:
        sec = re.search(rf"^### {t}\..*?(?=^### |^## |\Z)", text, re.S | re.M)
        m = re.search(r"\*\*Confidence at seal: (\d+(?:\.\d+)?)%", sec.group(0)) if sec else None
        out[t] = float(m.group(1)) / 100 if m else None
    return out


# THESIS section 6: the outcome rules, shared by 11 and 15 so both apply the
# same words to their own numbers.
def outcome_sign_test(est, lo, hi, gates_ok):
    """T1 and T2: SURVIVE if est < 0 and hi < 0; FAIL_NO_LINK if the interval
    includes zero; FAIL_OPPOSITE if lo > 0; NOT_SCORED if a gate fails."""
    if not gates_ok:
        return "NOT_SCORED"
    if hi < 0:
        return "SURVIVE"
    if lo > 0:
        return "FAIL_OPPOSITE"
    return "FAIL_NO_LINK"


def outcome_t3(diff, lo, hi, before_hi, gates_ok):
    """T3: NOT_SCORED_NO_TILT if beta_before's interval does not lie wholly
    below zero; NOT_SCORED if a gate fails; SURVIVE if the difference's
    interval lies wholly above zero (weaker); FAIL_STRONGER if wholly below;
    FAIL_NO_CHANGE otherwise."""
    if not gates_ok:
        return "NOT_SCORED"
    if not before_hi < 0:
        return "NOT_SCORED_NO_TILT"
    if lo > 0:
        return "SURVIVE"
    if hi < 0:
        return "FAIL_STRONGER"
    return "FAIL_NO_CHANGE"


def held(outcome):
    """1 held, 0 failed, None not scored."""
    if outcome.startswith("NOT_SCORED"):
        return None
    return 1 if outcome == "SURVIVE" else 0


# How RESULTS.md prints each number; 14_manifest.py checks the same forms.
def printed(key, value):
    """The printed form of a tests.csv or calc_7a.csv value, or None when the
    key is not a number RESULTS.md prints."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v != v:
        return None
    if re.search(r"(_n|_blocks|_quarters|n_scored|held_count|boot_n)$", key):
        return "{:d}".format(int(v))
    if re.search(r"geo_share", key):
        return "{:.2f}%".format(100 * v)
    if re.search(r"(_F|_F_before|_F_after)$", key):
        return "{:.1f}".format(v)
    if re.search(r"^(brier|expected_held)$", key):
        return "{:.3f}".format(v)
    if re.search(r"^(share|share_lo|share_hi)$", key):
        return "{:.0f}%".format(100 * v)
    if re.search(r"^(dgap_|coebar_|dcoe)", key):
        return "{:,.0f}".format(v)
    if re.search(r"(_est|_se|_lo|_hi)$", key):
        return "{:.3e}".format(v)
    return None


def per10k(beta):
    """A COE x distance slope as dollars per square metre, for a flat 5 km
    against one 20 km from Raffles Place, per $10,000 of COE premium."""
    return (CALC_NEAR_KM - CALC_FAR_KM) * beta * 10000
