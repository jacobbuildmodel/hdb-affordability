"""
22b_reset_sensitivity.py

Sensitivity companion to 22_compute.py, same numbering convention as the root
piece's 02b_hedonic --lease-spline: a lettered suffix for a robustness check
run alongside the base case, not a replacement for it.

THESIS.md section 5 fixes R2's contractual reset at 36 months and treats it as
"the closest thing to a neutral assumption", not as a sourced fact about any
actual mortgage package. This script re-runs T1 (realised break-even, R2),
T2b (2020-2023 crossover), T3 (R3 minus R2 gap) and T4a (2021 switch) at
36, 24, 12 and 3-month reset intervals, so AMENDMENT 3 (THESIS.md) and
RESULTS.md can state how much of each result the 36-month choice drives,
rather than asserting it without a number.

This is the only script in financing/ that overrides RESET_MONTHS; every
other script leaves it at the module default (36).

Reads:  financing/out/rates_monthly.csv
Writes: financing/out/t1_reset_sensitivity.csv
        financing/out/t2_reset_sensitivity.csv
        financing/out/t3_reset_sensitivity.csv
        financing/out/t4_reset_sensitivity.csv
        financing/out/reset_sensitivity_report.txt

Usage:  python3 22b_reset_sensitivity.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_model = __import__("21_model")

PRINCIPAL = _model.PRINCIPAL
TENURE = _model.TENURE_MONTHS
GRID = _model.SPREAD_GRID
COSTS = _model.SWITCH_COSTS
HDB = 2.6
RESETS = [36, 24, 12, 3]

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
START_YEARS = list(range(2010, 2026))
SWITCH_YEARS = [2012, 2015, 2018, 2021]


def load_rates():
    path = os.path.join(OUT, "rates_monthly.csv")
    months, sora = [], []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        months.append(r["month"])
        sora.append(float(r["sora3m"]))
    return months, sora


def main():
    months, sora = load_rates()
    idx = {m: i for i, m in enumerate(months)}
    os.makedirs(OUT, exist_ok=True)
    rep = []

    def say(s=""):
        print(s)
        rep.append(s)

    say("22b_reset_sensitivity.py")
    say("reset intervals tested: %s months (base case is 36, section 5)"
        % ", ".join(str(r) for r in RESETS))
    say()

    starts = [(y, idx["%04d-01" % y]) for y in START_YEARS if "%04d-01" % y in idx]

    # ---- T1: realised break-even, R2, at each reset interval --------------
    t1 = []
    for y, s in starts:
        horizon = len(months) - s
        row = {"start_year": y}
        for rm in RESETS:
            row[rm] = _model.breakeven_spread(PRINCIPAL, sora, s, TENURE,
                                              horizon, HDB, reset_months=rm)
        t1.append(row)
    with open(os.path.join(OUT, "t1_reset_sensitivity.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["start_year"] + ["breakeven_reset_%d" % rm for rm in RESETS])
        for row in t1:
            w.writerow([row["start_year"]] +
                       ["" if row[rm] is None else "%.4f" % row[rm] for rm in RESETS])
    say("T1 reset sensitivity: %d cohorts x %d reset intervals" % (len(t1), len(RESETS)))

    # ---- T1b scored at each reset interval ---------------------------------
    say()
    for rm in RESETS:
        vals = [row[rm] for row in t1 if 2010 <= row["start_year"] <= 2015 and row[rm] is not None]
        holds = bool(vals) and min(vals) > 1.0
        say("T1b at %2d-month reset: 2010-2015 range %.3f to %.3f, %s"
            % (rm, min(vals), max(vals), "HOLDS" if holds else "FAILS"))

    # ---- T2b: 2020-2023 crossover within 3 years, at each reset interval --
    say()
    t2 = []
    for rm in RESETS:
        cells = []
        for y, s in starts:
            if not (2020 <= y <= 2023):
                continue
            horizon = len(months) - s
            for sp in GRID:
                k = _model.crossover_month(PRINCIPAL, sp, sora, s, TENURE,
                                           horizon, HDB, reset_months=rm)
                fails = (k is None) or (k // 12 > 3)
                cells.append(fails)
        fails_n = sum(cells)
        t2.append((rm, fails_n, len(cells)))
        say("T2b at %2d-month reset: %d of %d cells fail" % (rm, fails_n, len(cells)))
    with open(os.path.join(OUT, "t2_reset_sensitivity.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["reset_months", "cells_failing", "cells_total"])
        w.writerows(t2)

    # ---- T3: R3 minus R2 gap, largest 2010-2015 vs largest 2022-2025 ------
    say()
    t3 = []
    for rm in RESETS:
        gap_early, gap_late = [], []
        for y, s in starts:
            horizon = len(months) - s
            be2 = _model.breakeven_spread(PRINCIPAL, sora, s, TENURE, horizon,
                                          HDB, reset_months=rm)
            for c in COSTS:
                be3 = _model.breakeven_spread(PRINCIPAL, sora, s, TENURE, horizon,
                                              HDB, switch_cost=c, reset_months=rm)
                if be2 is None or be3 is None:
                    continue
                g = be3 - be2
                if 2010 <= y <= 2015:
                    gap_early.append(g)
                elif 2022 <= y <= 2025:
                    gap_late.append(g)
        me, ml = max(gap_early), max(gap_late)
        t3.append((rm, me, ml))
        say("T3 at %2d-month reset: largest gap 2010-2015 %.3f, largest 2022-2025 %.3f"
            % (rm, me, ml))
    with open(os.path.join(OUT, "t3_reset_sensitivity.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["reset_months", "max_gap_2010_2015", "max_gap_2022_2025"])
        for rm, me, ml in t3:
            w.writerow([rm, "%.4f" % me, "%.4f" % ml])

    # ---- T4a: 2021 switch worse than staying, at each reset interval ------
    say()
    t4 = []
    for rm in RESETS:
        worse, total = 0, 0
        sy = 2021
        key = "%04d-01" % sy
        if key not in idx:
            continue
        sw = idx[key]
        for y, s in starts:
            if y >= sy:
                continue
            horizon = len(months) - s
            k = sw - s
            hdb_all = _model.run_fixed(PRINCIPAL, HDB, TENURE, horizon)
            if k >= len(hdb_all):
                continue
            r = HDB / 100.0
            pay = _model.amortise(PRINCIPAL, r, TENURE)
            bal = PRINCIPAL
            for _ in range(k):
                bal = max(0.0, bal + bal * r / 12.0 - pay)
            pre = hdb_all[k - 1] if k > 0 else 0.0
            for sp in GRID:
                post, _n = _model.run_floating(bal, sp, sora, sw, TENURE - k,
                                               horizon - k, reset_months=rm)
                if not post:
                    continue
                cost_switch = pre + post[-1]
                cost_stay = hdb_all[-1]
                total += 1
                if cost_switch > cost_stay:
                    worse += 1
        t4.append((rm, worse, total))
        say("T4a at %2d-month reset: %d of %d cases worse than staying"
            % (rm, worse, total))
    with open(os.path.join(OUT, "t4_reset_sensitivity.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["reset_months", "cases_worse", "cases_total"])
        w.writerows(t4)

    with open(os.path.join(OUT, "reset_sensitivity_report.txt"), "w", newline="\n") as fh:
        fh.write("\n".join(rep) + "\n")
    print("\nout/reset_sensitivity_report.txt written")


if __name__ == "__main__":
    main()
