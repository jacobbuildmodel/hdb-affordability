"""
22_compute.py

Runs T1, T2, T3, T4 and S1 exactly as THESIS.md (sealed 17 September 2026)
specifies them, and writes one CSV per test. It scores nothing: scoring is
24_results.py, so that computing a number and judging it are separate steps.

Reads:  financing/out/rates_monthly.csv   (from 20_rates.py)
        raw/f3_mas_msb_iii3_monthly.csv   (S1 only)
Writes: financing/out/t1_breakeven.csv
        financing/out/t2_crossover.csv
        financing/out/t3_r2_r3.csv
        financing/out/t4_switch.csv
        financing/out/s1_finance_companies.csv
        financing/out/compute_report.txt

Usage:  python3 22_compute.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")

START_YEARS = list(range(2010, 2026))
SWITCH_YEARS = [2012, 2015, 2018, 2021]
BAND = 0.03          # indistinguishable band, section 3
S1_COL = 8           # Finance Companies Housing Loans For 15 Years
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_rates():
    path = os.path.join(OUT, "rates_monthly.csv")
    months, sora = [], []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        months.append(r["month"])
        sora.append(float(r["sora3m"]))
    return months, sora


def band_edges(rates, start, horizon):
    """
    The indistinguishable band: the spread interval inside which
    |bank - HDB| / HDB total interest <= 3 per cent (THESIS.md section 3).
    Returns (lo, hi) in percentage points, or (None, None).
    """
    hdb = _model.run_fixed(PRINCIPAL, HDB, TENURE, horizon)
    if not hdb:
        return None, None
    out = []
    for mult in (1.0 - BAND, 1.0 + BAND):
        target = hdb[-1] * mult
        lo, hi = -10.0, 20.0
        def excess(s):
            p, _ = _model.run_floating(PRINCIPAL, s, rates, start, TENURE, horizon)
            return p[-1] - target if p else None
        a, b = excess(lo), excess(hi)
        if a is None or b is None or a > 0 or b < 0:
            out.append(None)
            continue
        for _ in range(200):
            mid = (lo + hi) / 2.0
            e = excess(mid)
            if abs(e) < 1e-7:
                break
            if e < 0:
                lo = mid
            else:
                hi = mid
        out.append((lo + hi) / 2.0)
    return out[0], out[1]


def main():
    months, sora = load_rates()
    idx = {m: i for i, m in enumerate(months)}
    last_month = months[-1]
    os.makedirs(OUT, exist_ok=True)
    rep = []

    def say(s=""):
        print(s)
        rep.append(s)

    say("22_compute.py")
    say("benchmark: compounded 3-month SORA, %s to %s, %d months"
        % (months[0], last_month, len(months)))
    say("principal S$%s, tenure %d months, HDB leg %.2f per cent constant"
        % ("{:,.0f}".format(PRINCIPAL), TENURE, HDB))
    say("realised basis: loan start to %s inclusive" % last_month)
    say()

    starts = [(y, idx["%04d-01" % y]) for y in START_YEARS if "%04d-01" % y in idx]

    # ---- T1 ---------------------------------------------------------------
    t1 = []
    for y, s in starts:
        horizon = len(months) - s
        be = _model.breakeven_spread(PRINCIPAL, sora, s, TENURE, horizon, HDB)
        blo, bhi = band_edges(sora, s, horizon)
        # full-tenure projections, labelled, never the headline (section 3)
        flat = sora[:s + horizon] + [sora[-1]] * TENURE
        avg = sum(sora) / len(sora)
        mean = sora[:s + horizon] + [avg] * TENURE
        be_flat = _model.breakeven_spread(PRINCIPAL, flat, s, TENURE, TENURE, HDB)
        be_mean = _model.breakeven_spread(PRINCIPAL, mean, s, TENURE, TENURE, HDB)
        t1.append(dict(start_year=y, months_realised=horizon,
                       breakeven_r2=be, band_lo=blo, band_hi=bhi,
                       proj_last_flat=be_flat, proj_long_run_avg=be_mean))
    with open(os.path.join(OUT, "t1_breakeven.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["start_year", "months_realised", "realised_breakeven_spread_r2",
                    "band_lo", "band_hi",
                    "PROJECTION_full_tenure_last_rate_flat",
                    "PROJECTION_full_tenure_long_run_average"])
        for r in t1:
            w.writerow([r["start_year"], r["months_realised"],
                        "" if r["breakeven_r2"] is None else "%.4f" % r["breakeven_r2"],
                        "" if r["band_lo"] is None else "%.4f" % r["band_lo"],
                        "" if r["band_hi"] is None else "%.4f" % r["band_hi"],
                        "" if r["proj_last_flat"] is None else "%.4f" % r["proj_last_flat"],
                        "" if r["proj_long_run_avg"] is None else "%.4f" % r["proj_long_run_avg"]])
    say("T1: %d cohorts, %d solved, %d non-converging"
        % (len(t1), sum(1 for r in t1 if r["breakeven_r2"] is not None),
           sum(1 for r in t1 if r["breakeven_r2"] is None)))

    # ---- T2 ---------------------------------------------------------------
    t2 = []
    for y, s in starts:
        horizon = len(months) - s
        for sp in GRID:
            k = _model.crossover_month(PRINCIPAL, sp, sora, s, TENURE, horizon, HDB)
            if k is None:
                cy, note = "", "no crossover to date"
            else:
                cy, note = y + k // 12, ""
            t2.append((y, sp, cy, note))
    with open(os.path.join(OUT, "t2_crossover.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["start_year", "spread", "crossover_year", "note"])
        w.writerows(t2)
    say("T2: %d cells, %d with a crossover, %d without"
        % (len(t2), sum(1 for r in t2 if r[2] != ""),
           sum(1 for r in t2 if r[2] == "")))

    # ---- T3 ---------------------------------------------------------------
    t3 = []
    for y, s in starts:
        horizon = len(months) - s
        be2 = _model.breakeven_spread(PRINCIPAL, sora, s, TENURE, horizon, HDB)
        for c in COSTS:
            be3 = _model.breakeven_spread(PRINCIPAL, sora, s, TENURE, horizon, HDB,
                                          switch_cost=c)
            gap = None if (be2 is None or be3 is None) else be3 - be2
            t3.append((y, c, be2, be3, gap))
    with open(os.path.join(OUT, "t3_r2_r3.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["start_year", "switch_cost", "breakeven_r2", "breakeven_r3",
                    "gap_r3_minus_r2"])
        for y, c, a, b, g in t3:
            w.writerow([y, "%.0f" % c,
                        "" if a is None else "%.4f" % a,
                        "" if b is None else "%.4f" % b,
                        "" if g is None else "%.4f" % g])
    say("T3: %d rows across %d cohorts and %d switching costs"
        % (len(t3), len(starts), len(COSTS)))

    # ---- T4 ---------------------------------------------------------------
    # The switcher starts on the HDB loan, moves once in the switch year, and
    # thereafter reprices every 36 months at the same spread (R2, not R3).
    t4 = []
    for sy in SWITCH_YEARS:
        for y, s in starts:
            if y >= sy:
                continue                      # loan must exist before it switches
            key = "%04d-01" % sy
            if key not in idx:
                continue
            sw = idx[key]
            horizon = len(months) - s
            k = sw - s                        # months on the HDB loan before moving
            hdb_all = _model.run_fixed(PRINCIPAL, HDB, TENURE, horizon)
            if k >= len(hdb_all):
                continue
            # balance and interest at the switch
            r = HDB / 100.0
            pay = _model.amortise(PRINCIPAL, r, TENURE)
            bal = PRINCIPAL
            for _ in range(k):
                bal = max(0.0, bal + bal * r / 12.0 - pay)
            pre = hdb_all[k - 1] if k > 0 else 0.0
            for sp in GRID:
                post, _n = _model.run_floating(bal, sp, sora, sw, TENURE - k,
                                               horizon - k)
                if not post:
                    continue
                cost_switch = pre + post[-1]
                cost_stay = hdb_all[-1]
                t4.append((y, sy, sp, cost_switch, cost_stay,
                           "worse" if cost_switch > cost_stay else "better"))
    with open(os.path.join(OUT, "t4_switch.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["start_year", "switch_year", "spread", "cost_switched",
                    "cost_stayed_on_hdb", "outcome"])
        for r in t4:
            w.writerow([r[0], r[1], "%.2f" % r[2], "%.2f" % r[3], "%.2f" % r[4], r[5]])
    say("T4: %d (start, switch, spread) cases, %d worse than staying"
        % (len(t4), sum(1 for r in t4 if r[5] == "worse")))

    # ---- S1 ---------------------------------------------------------------
    path = os.path.join(ROOT, "raw", "f3_mas_msb_iii3_monthly.csv")
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    year, s1 = None, []
    for r in rows[5:]:
        if not r or len(r) <= S1_COL:
            continue
        if r[0].strip().isdigit():
            year = int(r[0].strip())
        m = r[1].strip() if len(r) > 1 else ""
        if year is None or m not in MONTHS:
            continue
        v = r[S1_COL].strip()
        if v:
            s1.append(("%04d-%02d" % (year, MONTHS.index(m) + 1), float(v)))
    with open(os.path.join(OUT, "s1_finance_companies.csv"), "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["month", "finance_company_housing_15y", "hdb"])
        for m, v in s1:
            w.writerow([m, "%.4f" % v, "%.4f" % HDB])
    win = [(m, v) for m, v in s1 if "2010-01" <= m <= "2025-12"]
    say("S1: %d published months, %s to %s; %d inside the study window"
        % (len(s1), s1[0][0], s1[-1][0], len(win)))

    with open(os.path.join(OUT, "compute_report.txt"), "w", newline="\n") as fh:
        fh.write("\n".join(rep) + "\n")
    print("\nout/compute_report.txt written")


if __name__ == "__main__":
    main()
