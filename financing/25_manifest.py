"""
25_manifest.py

The financing piece's checksum file and number manifest, and the guard that
stops a wrong number reaching a checkpoint.

  python3 25_manifest.py           regenerate financing/CHECKSUMS.md5 and
                                   financing/number_manifest.csv. Manual step,
                                   run LAST, after every other edit.
  python3 25_manifest.py --check   verify the checksums, verify the manifest,
                                   and audit every number printed in the
                                   article. Never writes.

Two jobs.

1. CHECKSUMS.md5, in two labelled sections. INPUTS are the financing scripts,
   the article and the raw files this piece reads; OUTPUTS are everything under
   financing/out and financing/figs. A changed OUTPUT with unchanged INPUTS
   means the pipeline is not deterministic.

2. number_manifest.csv, one row per number the article prints, each derived
   here from the out/ CSV that produced it rather than typed in. --check then
   reads the article, pulls out every numeric token, and fails on any token
   that is neither in the manifest at its printed rounding nor on the short
   allowlist of design constants below. Checkpoint 2 found a wrong rate-history
   claim and a cohort conflation that the old manifest could not have caught,
   because it only covered the headline numbers; this is the fix for that.
"""

import argparse
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SCRIPTS = ["20_rates.py", "21_model.py", "22_compute.py",
           "22b_reset_sensitivity.py", "23_figures.py",
           "24_results.py", "25_manifest.py"]
ARTICLE = "2026-10-03.md"
DOCS = ["THESIS.md", "RESULTS.md", ARTICLE]
RAW_USED = ["f1_sora_sgs_monthly.csv", "f2_cpf_interest_rate_history.pdf",
            "f3_mas_msb_iii3_monthly.csv", "f5_mas_fsr_2025.pdf",
            "f6_mas_mortgage_pricing_2021.pdf", "f8_cpf_rates_q1_2025.pdf"]

HDB_RATE = 2.6
RESETS = [36, 24, 12, 3]

# Design constants and structural numbers. Everything else the article prints
# must come from the manifest. Kept deliberately short: each entry is a number
# fixed by the sealed thesis or by the shape of the document, not a result.
ALLOW = {
    2.6,        # the HDB concessionary rate
    2.5,        # the CPF Ordinary Account floor
    0.1,        # the peg between them
    400000,     # principal
    25,         # tenure in years
    3, 12, 24, 36,          # reset intervals in months
    0.25, 0.5, 0.75, 1.0, 1.25, 1.5,   # the spread grid
    0.2,        # the sealed T3 threshold
    2020,       # SORA adoption year, also a year
}
ALLOW_INT_MAX = 13          # section numbers, test numbers, T1a/T2b and the like
YEAR_LO, YEAR_HI = 1955, 2030


def md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def collect(section):
    out = []
    if section == "INPUTS":
        for n in RAW_USED:
            p = os.path.join(ROOT, "raw", n)
            if os.path.exists(p):
                out.append(("raw/" + n, md5(p)))
        for n in SCRIPTS + DOCS:
            p = os.path.join(HERE, n)
            if os.path.exists(p):
                out.append(("financing/" + n, md5(p)))
    else:
        for d in ("out", "figs"):
            full = os.path.join(HERE, d)
            if not os.path.isdir(full):
                continue
            for n in sorted(os.listdir(full)):
                p = os.path.join(full, n)
                if os.path.isfile(p) and not n.startswith("."):
                    out.append(("financing/%s/%s" % (d, n), md5(p)))
    return out


def rd(name):
    p = os.path.join(HERE, "out", name)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def build_manifest():
    """
    Every number the article prints, derived from the out/ CSV that produced it.
    Nothing here is typed in by hand; if a figure moves, this moves with it.
    """
    rows = []

    def add(nid, value, meaning, src):
        rows.append([nid, value, meaning[:110], "22_compute.py", src])

    # ---- headline numbers and the per-cohort base case ---------------------
    for r in rd("headline_numbers.csv"):
        add(r["id"], r["value"], r["meaning"], "financing/out/headline_numbers.csv")
    for r in rd("t1_breakeven.csv"):
        if r["realised_breakeven_spread_r2"]:
            add("be_%s" % r["start_year"], r["realised_breakeven_spread_r2"],
                "realised break-even spread, %s start, 36-month reset" % r["start_year"],
                "financing/out/t1_breakeven.csv")

    # ---- reset sensitivity: every cell, plus the endpoints the article quotes
    rs = rd("t1_reset_sensitivity.csv")
    SRC = "financing/out/t1_reset_sensitivity.csv"
    cells = {}
    for r in rs:
        y = int(r["start_year"])
        for k in RESETS:
            v = r.get("breakeven_reset_%d" % k, "")
            if v:
                cells[(y, k)] = float(v)
                add("be_%d_r%d" % (y, k), v,
                    "realised break-even spread, %d start, %d-month reset" % (y, k), SRC)
    if cells:
        early = {yk: v for yk, v in cells.items() if 2010 <= yk[0] <= 2015}
        if early:
            lo = min(early.items(), key=lambda kv: kv[1])
            add("reset_min_2010_2015", "%.4f" % lo[1],
                "lowest break-even anywhere in the 2010-2015 block (%d start, "
                "%d-month reset)" % (lo[0][0], lo[0][1]), SRC)
            e36 = {yk: v for yk, v in early.items() if yk[1] == 36}
            lo36 = min(e36.items(), key=lambda kv: kv[1])
            add("reset_min36_2010_2015", "%.4f" % lo36[1],
                "lowest break-even at the 36-month reset across 2010-2015 "
                "(%d start)" % lo36[0][0], SRC)
        for y in (2010, 2023):
            vs = [v for yk, v in cells.items() if yk[0] == y]
            if vs:
                add("be_%d_lo" % y, "%.4f" % min(vs),
                    "lowest break-even across resets, %d start" % y, SRC)
                add("be_%d_hi" % y, "%.4f" % max(vs),
                    "highest break-even across resets, %d start" % y, SRC)

    # ---- T2b: 2020-2023 crossovers that missed the three-year window -------
    t2 = [r for r in rd("t2_crossover.csv") if 2020 <= int(r["start_year"]) <= 2023]
    if t2:
        missed = [r for r in t2 if (not r["crossover_year"]) or
                  (int(r["crossover_year"]) - int(r["start_year"]) > 3)]
        never = [r for r in missed if not r["crossover_year"]]
        S = "financing/out/t2_crossover.csv"
        add("t2b_cells_total", str(len(t2)), "2020-2023 start-year by spread cells", S)
        add("t2b_cells_missed", str(len(missed)),
            "of those, cells that did not cross within three years", S)
        add("t2b_never_crossed", str(len(never)),
            "of those, cells that never crossed inside the data", S)

    # ---- T3: largest R3 minus R2 gap per cohort block ----------------------
    t3 = rd("t3_r2_r3.csv")
    if t3:
        per = {}
        for r in t3:
            if r["gap_r3_minus_r2"]:
                y = int(r["start_year"])
                per[y] = max(per.get(y, float("-inf")), float(r["gap_r3_minus_r2"]))
        S = "financing/out/t3_r2_r3.csv"
        for lab, lo, hi in (("2010_2015", 2010, 2015), ("2022_2025", 2022, 2025)):
            vs = [v for y, v in per.items() if lo <= y <= hi]
            if vs:
                add("t3_gap_max_%s" % lab, "%.3f" % max(vs),
                    "largest R3 minus R2 gap, %s starts" % lab.replace("_", "-"), S)

    # ---- T4: the 2021 switch, the early switches, and the worked example ---
    t4 = rd("t4_switch.csv")
    if t4:
        S = "financing/out/t4_switch.csv"
        s21 = [r for r in t4 if int(r["switch_year"]) == 2021]
        worse = [r for r in s21 if r["outcome"] == "worse"]
        add("t4a_cases_total", str(len(s21)), "2021-switch start-year by spread cases", S)
        add("t4a_cases_worse", str(len(worse)), "of those, worse than staying on HDB", S)
        add("t4a_cases_better", str(len(s21) - len(worse)), "of those, better than staying", S)
        early = [r for r in t4 if int(r["switch_year"]) in (2012, 2015)
                 and int(r["start_year"]) in (2010, 2011) and float(r["spread"]) <= 0.75]
        add("t4b_cases_better", str(sum(1 for r in early if r["outcome"] == "better")),
            "early-switch cases that came out ahead of staying", S)
        ex = {r["spread"]: r for r in t4
              if r["start_year"] == "2010" and r["switch_year"] == "2021"}
        stay = None
        for sp, nid in (("1.25", "125"), ("0.25", "025")):
            if sp in ex:
                c = float(ex[sp]["cost_switched"]); stay = float(ex[sp]["cost_stayed_on_hdb"])
                add("t4_example_cost_%s" % nid, "%.2f" % c,
                    "2010 start switching in 2021 at %s points, cumulative interest" % sp, S)
                add("t4_example_diff_%s" % nid, "%.2f" % abs(c - stay),
                    "difference against staying on the HDB loan, %s points" % sp, S)
        if stay is not None:
            add("t4_example_stay", "%.2f" % stay,
                "2010 start staying on the HDB loan, cumulative interest", S)

    # ---- S1: the finance-company series inside the window ------------------
    s1 = [r for r in rd("s1_finance_companies.csv")
          if "2010-01" <= r["month"] <= "2025-12"]
    if s1:
        vals = [float(r["finance_company_housing_15y"]) for r in s1]
        S = "financing/out/s1_finance_companies.csv"
        add("s1_months_in_window", str(len(s1)),
            "months the finance-company rate is published inside 2010-2025", S)
        add("s1_min", "%.2f" % min(vals), "lowest finance-company rate in the window", S)
        add("s1_max", "%.2f" % max(vals), "highest finance-company rate in the window", S)

    # ---- the benchmark's own history ---------------------------------------
    rates = rd("rates_monthly.csv")
    if rates:
        above = [r["month"] for r in rates if float(r["sora3m"]) > HDB_RATE]
        run = []
        for m in above:
            if run and _next_month(run[-1][-1]) == m:
                run[-1].append(m)
            else:
                run.append([m])
        longest = max(run, key=len) if run else []
        S = "financing/out/rates_monthly.csv"
        if longest:
            add("sora_months_above_hdb", str(len(longest)),
                "consecutive months compounded 3M SORA was above 2.6, %s to %s"
                % (longest[0], longest[-1]), S)

    # ---- the CPF quarter count, as recorded when F2 was verified -----------
    ret = os.path.join(ROOT, "raw", "RETRIEVED.txt")
    if os.path.exists(ret):
        txt = re.sub(r"\s+", " ", io.open(ret, encoding="utf-8").read())
        # Two different counts are recorded there and they must not be confused:
        # the whole document, and the 2010-2024 study window.
        m = re.search(r"ALL (\d+) quarters it publishes", txt)
        if m:
            add("f2_quarters_published", m.group(1),
                "quarters the CPF history publishes, every one at a 2.50 per cent "
                "Ordinary Account rate", "raw/RETRIEVED.txt")
        m = re.search(r"ALL (\d+) quarters from", txt)
        if m:
            add("f2_quarters_window", m.group(1),
                "quarters of that history inside the 2010 to Sep 2024 window",
                "raw/RETRIEVED.txt")

    # ---- the source table's own shape --------------------------------------
    f3 = os.path.join(ROOT, "raw", "f3_mas_msb_iii3_monthly.csv")
    if os.path.exists(f3):
        hdr = list(csv.reader(open(f3, encoding="utf-8-sig")))[4]
        n = len([x for i, x in enumerate(hdr) if i >= 2 and x.strip()])
        add("f3_series_count", str(n),
            "interest rate series published in MAS Table III.3",
            "raw/f3_mas_msb_iii3_monthly.csv")

    return rows


def _next_month(m):
    y, mm = int(m[:4]), int(m[5:])
    return "%04d-%02d" % (y + 1, 1) if mm == 12 else "%04d-%02d" % (y, mm + 1)


def article_body(path):
    """The article's prose, with front matter, images, links and code removed."""
    t = io.open(path, encoding="utf-8").read()
    if t.startswith("---"):
        t = t.split("---", 2)[2] if t.count("---") >= 2 else t
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)     # images
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)  # links: keep text, drop URL
    t = re.sub(r"`[^`]*`", " ", t)                  # inline code, e.g. dataset ids
    t = re.sub(r"\{\{<[^>]*>\}\}", " ", t)          # shortcode tags, keep the body
    months = ("January|February|March|April|May|June|July|August|September|"
              "October|November|December")
    t = re.sub(r"\b\d{1,2}\s+(?:%s)\s+\d{4}\b" % months, " ", t)  # 17 September 2026
    t = re.sub(r"\b(?:%s)\s+\d{4}\b" % months, " ", t)              # November 2022
    t = re.sub(r"\bQ[1-4]\s+\d{4}\b", " ", t)                       # Q1 2016
    t = re.sub(r"\b\d{4}-\d{2}\b", " ", t)                          # 2005-10
    return t


def audit_article():
    """
    Every numeric token the article prints must be in the manifest at its
    printed rounding, or on the allowlist. Returns a list of problems.
    """
    path = os.path.join(HERE, ARTICLE)
    if not os.path.exists(path):
        return []
    body = article_body(path)
    values = []
    for r in build_manifest():
        try:
            values.append(float(str(r[1]).replace(",", "")))
        except ValueError:
            pass

    bad = []
    for m in re.finditer(r"(?<![\w.])(-?)\$?(\d[\d,]*(?:\.\d+)?)(?![\d.]*[\w])", body):
        raw = (m.group(1) + m.group(2))
        tok = raw.replace(",", "")
        try:
            val = float(tok)
        except ValueError:
            continue
        dp = len(tok.split(".")[1]) if "." in tok else 0
        if val in ALLOW:
            continue
        if dp == 0 and (abs(val) <= ALLOW_INT_MAX or YEAR_LO <= val <= YEAR_HI):
            continue
        if any(round(v, dp) == round(val, dp) for v in values):
            continue
        ctx = re.sub(r"\s+", " ", body[max(0, m.start() - 45):m.end() + 45]).strip()
        bad.append((raw, ctx))
    return bad


def to_csv(rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["number_id", "value", "meaning", "script", "output_file"])
    w.writerows(rows)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify checksums, manifest and article numbers; never writes")
    args = ap.parse_args()

    dest = os.path.join(HERE, "CHECKSUMS.md5")
    man = os.path.join(HERE, "number_manifest.csv")
    sections = [("INPUTS", collect("INPUTS")), ("OUTPUTS", collect("OUTPUTS"))]
    rows = build_manifest()

    if args.check:
        problems = []
        if not os.path.exists(dest):
            print("financing/CHECKSUMS.md5 not found", file=sys.stderr)
            sys.exit(1)
        want = {}
        for line in open(dest, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            digest, name = line.split("  ", 1)
            want[name] = digest
        have = dict(sections[0][1] + sections[1][1])
        for n in sorted(set(want) | set(have)):
            if n not in have:
                print("MISSING     %s" % n, file=sys.stderr); problems.append(n)
            elif n not in want:
                print("UNRECORDED  %s" % n, file=sys.stderr); problems.append(n)
            elif have[n] != want[n]:
                print("MISMATCH    %s" % n, file=sys.stderr); problems.append(n)
        if os.path.exists(man) and open(man, encoding="utf-8").read() != to_csv(rows):
            print("MISMATCH    financing/number_manifest.csv", file=sys.stderr)
            problems.append("number_manifest.csv")

        bad = audit_article()
        if bad:
            print("NUMBER AUDIT, %d token(s) in %s not traceable:"
                  % (len(bad), ARTICLE), file=sys.stderr)
            for tok, ctx in bad:
                print("  %-12s ...%s..." % (tok, ctx), file=sys.stderr)
            problems.append("article numbers")
        else:
            print("article number audit: every figure in %s is in the manifest "
                  "or on the allowlist" % ARTICLE)

        if problems:
            sys.exit(1)
        print("financing: all %d checksums match, manifest agrees, %d numbers tracked"
              % (len(want), len(rows)))
        return

    with open(dest, "w", newline="\n", encoding="utf-8") as fh:
        fh.write("# MD5 checksums, financing piece. Regenerate with:\n"
                 "#   python3 financing/25_manifest.py\n"
                 "# Never written by run_all.sh, which only runs --check.\n"
                 "# Regenerate LAST, after every other edit; see README.md.\n")
        for label, entries in sections:
            fh.write("\n# ---- %s ----\n" % label)
            for name, digest in entries:
                fh.write("%s  %s\n" % (digest, name))

    with open(man, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(to_csv(rows))

    n = sum(len(e) for _, e in sections)
    print("financing/CHECKSUMS.md5 written, %d files (%d inputs, %d outputs)"
          % (n, len(sections[0][1]), len(sections[1][1])))
    print("financing/number_manifest.csv written, %d numbers" % len(rows))
    bad = audit_article()
    print("article number audit: %s"
          % ("clean" if not bad else "%d token(s) NOT traceable" % len(bad)))
    for tok, ctx in bad:
        print("  %-12s ...%s..." % (tok, ctx))


if __name__ == "__main__":
    main()
