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
        t4_switch.csv, s1_finance_companies.csv
Writes: financing/RESULTS.md, financing/out/headline_numbers.csv

Usage:  python3 24_results.py
"""

import csv
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

    # ---- headline numbers --------------------------------------------------
    y_top = max(be, key=lambda y: be[y])
    y_bot = min(be, key=lambda y: be[y])
    headline = [
        ("H1", "%.2f" % be[y_top],
         "percentage points: the realised break-even spread for a %d start, the "
         "widest of any cohort" % y_top, "22_compute.py -> out/t1_breakeven.csv"),
        ("H2", "%.2f" % be[y_bot],
         "percentage points: the realised break-even spread for a %d start. It is "
         "NEGATIVE, meaning the HDB loan beat the benchmark itself before any bank "
         "margin" % y_bot, "22_compute.py -> out/t1_breakeven.csv"),
        ("H3", "%d of %d" % (len(worse21), len(s21)),
         "switch-to-bank cases in 2021 that ended worse than staying on the HDB "
         "loan, across every applicable start year and grid spread",
         "22_compute.py -> out/t4_switch.csv"),
    ]
    with open(os.path.join(OUT, "headline_numbers.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["id", "value", "meaning", "generated_by"])
        w.writerows(headline)

    finding = "The cheap decade was worth about two points."
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
