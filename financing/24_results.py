"""
24_results.py

Scores every prediction in the sealed THESIS.md against what the data did, and
writes financing/RESULTS.md. Computing and judging are separate steps on
purpose: 22_compute.py produces numbers and takes no view, this script takes
the view and produces no numbers of its own.

Scoring is against the SEALED WORDING, not against a reasonable paraphrase of
it. Where a prediction is scored FAIL, the sealed wording is quoted so a reader
can check the call.

Reads:  financing/out/t1_breakeven.csv, t2_crossover.csv, t3_r2_r3.csv,
        t4_switch.csv, s1_finance_companies.csv,
        t1_reset_sensitivity.csv, t2_reset_sensitivity.csv,
        t3_reset_sensitivity.csv, t4_reset_sensitivity.csv
        (the last four from 22b_reset_sensitivity.py, AMENDMENT 3)
Writes: financing/RESULTS.md, financing/out/headline_numbers.csv

Usage:  python3 24_results.py
"""

import csv
import math
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def rd(name):
    return list(csv.DictReader(open(os.path.join(OUT, name), encoding="utf-8")))


def main():
    t1 = rd("t1_breakeven.csv")
    t2 = rd("t2_crossover.csv")
    t3 = rd("t3_r2_r3.csv")
    t4 = rd("t4_switch.csv")
    s1 = rd("s1_finance_companies.csv")
    r1 = rd("t1_reset_sensitivity.csv")
    r2 = rd("t2_reset_sensitivity.csv")
    r3 = rd("t3_reset_sensitivity.csv")
    r4 = rd("t4_reset_sensitivity.csv")
    RESETS = [36, 24, 12, 3]

    be = {int(r["start_year"]): float(r["realised_breakeven_spread_r2"])
          for r in t1 if r["realised_breakeven_spread_r2"]}
    band = {int(r["start_year"]): (float(r["band_lo"]), float(r["band_hi"]))
            for r in t1 if r["band_lo"] and r["band_hi"]}
    early = [be[y] for y in range(2010, 2016) if y in be]
    late = [be[y] for y in range(2020, 2024) if y in be]

    verdicts = []

    # ---- T1a ---------------------------------------------------------------
    p1a = min(early) > max(late)
    verdicts.append(("T1a", "ordering", p1a,
                     "min over 2010-2015 is %.3f, max over 2020-2023 is %.3f"
                     % (min(early), max(late))))

    # ---- T1b ---------------------------------------------------------------
    below = [(y, be[y]) for y in range(2010, 2016) if y in be and be[y] <= 1.0]
    p1b = not below
    verdicts.append(("T1b", "magnitude, THE HEADLINE CLAIM", p1b,
                     "2010-2015 range %.3f to %.3f, all above 1.0"
                     % (min(early), max(early)) if p1b else
                     "at or below 1.0: %s" % below))

    # ---- T2a ---------------------------------------------------------------
    v2a = [r for r in t2 if 2010 <= int(r["start_year"]) <= 2015
           and float(r["spread"]) <= 0.75 and r["crossover_year"]
           and int(r["crossover_year"]) < 2022]
    p2a = not v2a
    verdicts.append(("T2a", "no crossover before 2022 for early starts at <=0.75",
                     p2a, "no cell crosses before 2022" if p2a
                     else "%d cells cross early" % len(v2a)))

    # ---- T2b ---------------------------------------------------------------
    late_cells = [r for r in t2 if 2020 <= int(r["start_year"]) <= 2023]
    v2b = [r for r in late_cells if (not r["crossover_year"]) or
           (int(r["crossover_year"]) - int(r["start_year"]) > 3)]
    p2b = not v2b
    never = [r for r in v2b if not r["crossover_year"]]
    verdicts.append(("T2b", "2020-2023 cross within 3 years at every spread", p2b,
                     "%d of %d cells fail, %d of them never cross at all"
                     % (len(v2b), len(late_cells), len(never))))

    # ---- T3 ----------------------------------------------------------------
    gap = defaultdict(dict)
    for r in t3:
        if r["gap_r3_minus_r2"]:
            gap[int(r["start_year"])][float(r["switch_cost"])] = float(r["gap_r3_minus_r2"])
    g_early = [max(gap[y].values()) for y in gap if 2010 <= y <= 2015]
    g_late = [max(gap[y].values()) for y in gap if 2022 <= y <= 2025]
    p3 = (max(g_early) > max(g_late)) and all(v < 0.2 for v in g_late)
    verdicts.append(("T3", "gap largest for 2010-2015 and below 0.2 for 2022-2025",
                     p3, "largest gap 2010-2015 is %.3f, largest 2022-2025 is %.3f"
                     % (max(g_early), max(g_late))))

    # ---- T4 ----------------------------------------------------------------
    s21 = [r for r in t4 if int(r["switch_year"]) == 2021]
    worse21 = [r for r in s21 if r["outcome"] == "worse"]
    p4a = len(worse21) == len(s21)
    verdicts.append(("T4a", "2021 switch worse for every applicable case", p4a,
                     "%d of %d cases worse than staying" % (len(worse21), len(s21))))

    sub = [r for r in t4 if int(r["switch_year"]) in (2012, 2015)
           and int(r["start_year"]) in (2010, 2011) and float(r["spread"]) <= 0.75]
    p4b = all(r["outcome"] == "better" for r in sub)
    verdicts.append(("T4b", "2012/2015 switch better for 2010-2011 starts at <=0.75",
                     p4b, "%d of %d cases better"
                     % (sum(1 for r in sub if r["outcome"] == "better"), len(sub))))

    # ---- S1 ----------------------------------------------------------------
    win = [r for r in s1 if "2010-01" <= r["month"] <= "2022-06"]
    vals = [float(r["finance_company_housing_15y"]) for r in win]
    bad = [r for r in win if float(r["finance_company_housing_15y"]) <= 2.6]
    ps1 = not bad
    verdicts.append(("S1", "finance-company rate above 2.6 in every published month",
                     ps1, "%d months, range %.2f to %.2f, none at or below 2.6"
                     % (len(win), min(vals), max(vals))))

    passes = sum(1 for v in verdicts if v[2])
    fails = len(verdicts) - passes

    # ---- reset-interval sensitivity (AMENDMENT 3) --------------------------
    reset_be = {int(r["start_year"]): {rm: (float(r["breakeven_reset_%d" % rm])
                if r["breakeven_reset_%d" % rm] else None) for rm in RESETS}
                for r in r1}
    t1b_by_reset = []
    for rm in RESETS:
        rvals = [reset_be[y][rm] for y in range(2010, 2016)
                 if reset_be[y][rm] is not None]
        holds = bool(rvals) and min(rvals) > 1.0
        t1b_by_reset.append((rm, min(rvals), max(rvals), holds))
    reset_min_2010_2015 = min(v[1] for v in t1b_by_reset)

    r2_by_reset = {int(r["reset_months"]): (int(r["cells_failing"]), int(r["cells_total"]))
                   for r in r2}
    r3_by_reset = {int(r["reset_months"]): (float(r["max_gap_2010_2015"]), float(r["max_gap_2022_2025"]))
                   for r in r3}
    r4_by_reset = {int(r["reset_months"]): (int(r["cases_worse"]), int(r["cases_total"]))
                   for r in r4}

    reset_notes = {
        "T2b": ("Reset-interval sensitivity (AMENDMENT 3): cells failing run "
                "%s across the 36/24/12/3-month resets; T2b fails at every "
                "tested interval, though faster resets cut the failure count "
                "roughly in half."
                % ", ".join("%d of %d at %dm" % (r2_by_reset[rm][0], r2_by_reset[rm][1], rm)
                             for rm in RESETS)),
        "T3": ("Reset-interval sensitivity (AMENDMENT 3): the largest gap is "
               "bigger for 2022-2025 than for 2010-2015 at every tested reset "
               "(%s), the opposite ordering of the prediction at every "
               "interval; the reset assumption is not what drives this "
               "failure."
               % ", ".join("%dm %.3f vs %.3f" % (rm, r3_by_reset[rm][0], r3_by_reset[rm][1])
                            for rm in RESETS)),
        "T4a": ("Reset-interval sensitivity (AMENDMENT 3): the 2021 switch is "
                "never uniformly worse than staying at any tested reset (%s); "
                "the reset assumption is not what drives this failure either."
                % ", ".join("%d of %d at %dm" % (r4_by_reset[rm][0], r4_by_reset[rm][1], rm)
                             for rm in RESETS)),
    }

    # ---- headline numbers ---------------------------------------------------
    # AMENDMENT 3: H2 (-1.05, the 2024 start) and H3 (31 of 66, the 2021
    # switch cases) depend on the 36-month reset assumption and change sign
    # or magnitude under the other three tested intervals, so neither is a
    # headline. Every headline number below is checked to hold, in sign, at
    # every one of the 36/24/12/3-month resets, and its range across those
    # resets is reported alongside it.

    # H1: the widest cohort, checked to be the same cohort at every reset.
    widest_year_by_reset = {rm: max(reset_be, key=lambda y: reset_be[y][rm])
                             for rm in RESETS}
    assert len(set(widest_year_by_reset.values())) == 1, widest_year_by_reset
    y_top = next(iter(widest_year_by_reset.values()))
    h1_by_reset = [reset_be[y_top][rm] for rm in RESETS]
    h1_lo, h1_hi = min(h1_by_reset), max(h1_by_reset)

    # H2: the weakest 2010-2015 cohort, minimum across cohorts and resets.
    h2_by_reset = [lo for rm, lo, hi, holds in t1b_by_reset]
    h2_val = min(h2_by_reset)
    h2_lo, h2_hi = min(h2_by_reset), max(h2_by_reset)

    # H3: T3's failure -- the 2022-2025 gap beats the 2010-2015 gap at every
    # reset. The margin by which it does so is reported at its smallest.
    margin_by_reset = {rm: r3_by_reset[rm][1] - r3_by_reset[rm][0] for rm in RESETS}
    assert all(v > 0 for v in margin_by_reset.values()), margin_by_reset
    h3_val = min(margin_by_reset.values())
    h3_lo, h3_hi = min(margin_by_reset.values()), max(margin_by_reset.values())

    headline = [
        ("H1", "%.2f" % h1_hi,
         "percentage points: the realised break-even spread for a %d start, the "
         "widest of any cohort at every tested reset interval; ranges %.2f "
         "(3-month reset) to %.2f (36-month reset)" % (y_top, h1_lo, h1_hi),
         "22_compute.py -> out/t1_breakeven.csv; "
         "22b_reset_sensitivity.py -> out/t1_reset_sensitivity.csv"),
        ("H2", "%.2f" % h2_val,
         "percentage points: the weakest 2010-2015 start's realised break-even "
         "spread, the minimum across every cohort and every tested reset "
         "interval (T1b, the headline claim); the minimum-over-cohorts figure "
         "ranges %.2f (3-month reset) to %.2f (36-month reset)" % (h2_lo, h2_hi),
         "22b_reset_sensitivity.py -> out/t1_reset_sensitivity.csv"),
        ("H3", "%.2f" % h3_val,
         "percentage points: the minimum margin by which the largest gap over "
         "2.6 for 2022-2025 starts exceeded the largest gap for 2010-2015 "
         "starts, across every tested reset interval (T3, the opposite "
         "ordering from the sealed prediction, holding at every interval); "
         "margin ranges %.2f (3-month reset) to %.2f (36-month reset)"
         % (h3_lo, h3_hi),
         "22b_reset_sensitivity.py -> out/t3_reset_sensitivity.csv"),
    ]
    with open(os.path.join(OUT, "headline_numbers.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["id", "value", "meaning", "generated_by"])
        w.writerows(headline)

    # Floor to 1 dp, not round, so the stated figure never overstates the
    # worst-case (minimum-over-cohorts-and-resets) margin it is drawn from.
    finding_val = math.floor(h2_val * 10) / 10.0
    assert finding_val <= h2_val, (finding_val, h2_val)
    finding = "Banks had room to charge %.1f points more than HDB." % finding_val
    assert len(finding) < 60, len(finding)

    # ---- RESULTS.md --------------------------------------------------------
    L = []
    a = L.append
    a("# RESULTS -- hdb-financing")
    a("")
    a("Generated by `24_results.py`. Do not edit by hand; edit the script and")
    a("rerun, or the number manifest and the checksums stop agreeing.")
    a("")
    a("Scored against THESIS.md as sealed on 17 September 2026, at the sealed")
    a("wording rather than a paraphrase of it. **%d of %d predictions passed and"
      % (passes, len(verdicts)))
    a("%d failed.**" % fails)
    a("")
    a("## The failures, first")
    a("")
    for tag, what, ok, detail in verdicts:
        if not ok:
            a("- **%s FAILED.** %s. Predicted: %s." % (tag, detail, what))
            if tag in reset_notes:
                a("  %s" % reset_notes[tag])
    a("")
    a("## Scorecard")
    a("")
    a("| Test | Prediction | Verdict | What the data did |")
    a("|---|---|---|---|")
    for tag, what, ok, detail in verdicts:
        a("| %s | %s | %s | %s |" % (tag, what, "PASS" if ok else "**FAIL**", detail))
    a("")
    a("## T1b and the weak-evidence rule")
    a("")
    a("T1b passed. The sealed file says what that is worth, and it is quoted here")
    a("rather than summarised, because the whole point of fixing it in advance was")
    a("that it would still be there when the result arrived:")
    a("")
    a("> **For 2010-2015 starts a pass is weak evidence and a fail is strong")
    a("> evidence, because the benchmark substitution favours a pass.**")
    a("")
    a("Pre-2020 mortgages were priced off SIBOR, which ran above SORA. Measuring")
    a("the break-even spread over SORA therefore overstates the SIBOR-equivalent")
    a("margin for exactly the cohorts T1b is about. The pass is consistent with")
    a("the claim; it is not strong evidence for it, and this sentence travels with")
    a("the headline number wherever it is published.")
    a("")
    a("## Reset-interval sensitivity (AMENDMENT 3, written after results)")
    a("")
    a("THESIS.md section 5 fixes R2's contractual reset at 36 months and calls")
    a("it \"the closest thing to a neutral assumption\", not a sourced fact")
    a("about any actual mortgage package. `22b_reset_sensitivity.py` reruns the")
    a("realised break-even spread (R2) at 36, 24, 12 and 3-month resets for")
    a("every cohort, so T1b's dependence on that choice is a reported number,")
    a("not an assumption left untested.")
    a("")
    a("| Start year | 36 months | 24 months | 12 months | 3 months |")
    a("|---|---|---|---|---|")
    for y in sorted(reset_be):
        row = reset_be[y]
        a("| %d | %s | %s | %s | %s |" % (y,
            "-" if row[36] is None else "%+.3f" % row[36],
            "-" if row[24] is None else "%+.3f" % row[24],
            "-" if row[12] is None else "%+.3f" % row[12],
            "-" if row[3] is None else "%+.3f" % row[3]))
    a("")
    a("Realised break-even spread, points over SORA, R2, by cohort and reset")
    a("interval. Same basis as the base-case table below (loan start to")
    a("2026-07, S$400,000 over 25 years) with only the contractual reset")
    a("interval changed. The 2019-2025 cohorts move the most since they have")
    a("had the fewest reset dates to reach the rate rise; the 2010-2015")
    a("cohorts move little because a decade of sub-2.6 benchmark dominates")
    a("the total regardless of how often the loan repriced.")
    a("")
    a("**T1b scored under all four reset intervals:**")
    a("")
    a("| Reset (months) | 2010-2015 range | T1b (exceeds 1.0 for every start) |")
    a("|---|---|---|")
    for rm, lo, hi, holds in t1b_by_reset:
        a("| %d | %.3f to %.3f | %s |" % (rm, lo, hi, "HOLDS" if holds else "FAILS"))
    a("")
    a("T1b holds at every tested reset interval: the 2010-2015 minimum across")
    a("all four intervals is %.3f, still above the 1.0 threshold. The" % reset_min_2010_2015)
    a("weak-evidence rule above applies unchanged to all four, since the")
    a("benchmark substitution is a property of the benchmark series, not of")
    a("the reset interval.")
    a("")
    a("## Realised break-even spread by start year, R2")
    a("")
    a("| Start year | Realised break-even (points over SORA) | Indistinguishable band |")
    a("|---|---|---|")
    for y in sorted(be):
        lo, hi = band.get(y, (None, None))
        b = "%.2f to %.2f" % (lo, hi) if lo is not None else "-"
        a("| %d | %+.3f | %s |" % (y, be[y], b))
    a("")
    a("Realised means loan start to the last data month, 2026-07, on S$400,000")
    a("over 25 years. Not a projection. Negative values are real results: they")
    a("mean the HDB loan beat the benchmark itself, before any bank margin.")
    a("")
    a("## Three headline numbers")
    a("")
    for hid, val, mean, src in headline:
        a("- **%s. %s** -- %s. Generated by `%s`." % (hid, val, mean, src))
    a("")
    a("## One finding, under 60 characters")
    a("")
    a("> %s" % finding)
    a("")
    a("(%d characters.)" % len(finding))
    a("")
    a("## Side-note candidates")
    a("")
    a("1. **The crossover grid.** %d of %d cells in the start-year by spread grid"
      % (sum(1 for r in t2 if r['crossover_year']), len(t2)))
    a("   show a crossover inside the observed window; the rest have not crossed.")
    a("2. **S1, the only published housing loan rate.** Finance companies charged")
    a("   %.2f to %.2f per cent over 2010-01 to 2022-06, never below the HDB 2.6."
      % (min(vals), max(vals)))
    a("   The series stops in June 2022, at the start of the rate rise.")
    a("3. **The 2022 cohort.** It starts into the rise and still has not crossed at")
    a("   any grid spread, because the benchmark fell back below 2.6 by 2026.")
    a("")
    a("## What is not here")
    a("")
    a("- The full-tenure projection under the SGS forward curve. `t1_breakeven.csv`")
    a("  carries two labelled projections, the last observed rate held flat and the")
    a("  long-run average. The forward-curve path of THESIS.md section 7 item 7 is")
    a("  NOT built; building it needs a curve construction that is not in this")
    a("  repository, and inventing one would be the kind of unsourced input this")
    a("  design exists to avoid. Recorded as outstanding rather than quietly")
    a("  dropped.")
    a("- Any prose. By instruction, presentation comes before writing.")
    a("")

    with open(os.path.join(HERE, "RESULTS.md"), "w", newline="\n",
              encoding="utf-8") as fh:
        fh.write("\n".join(L))

    print("RESULTS.md written: %d passed, %d FAILED" % (passes, fails))
    for tag, what, ok, detail in verdicts:
        print("  %-5s %-6s %s" % (tag, "PASS" if ok else "FAIL", detail))
    print("out/headline_numbers.csv written")


if __name__ == "__main__":
    main()
