"""
05_affordability.py

The three measures from THESIS.md section 3, for the three pre-registered buyers.

    price P(t)    constant-quality four-room resale price, from the hedonic index
                  anchored on the base-year raw median
    grants G      from 04_grants.py, zero before 2019
    loan   L      = min( LTV(t) x P,  P - G ),  the buyer borrows what is allowed
                  or what is still owed, whichever is smaller
    repayment     amortised at the HDB concessionary rate over 300 months
    own outlay    = max(P - L - G, 0), the cash and CPF the buyer must find

  Measure 1, the lead: mortgage servicing ratio = repayment / monthly income
  Measure 2: price to annual income, in years, on the headline price before grants
  Measure 3: own outlay in years of annual income

Financing parameters come from `ltv_schedule.csv`, which carries the quoted
primary sentence behind each one. The concessionary rate has been 2.6 per cent
throughout, evidenced by CPF announcements ten years apart.

The 3 per cent stress rate HDB introduced on 30 September 2022 is NOT used here.
It governs how much a buyer is allowed to borrow, not what they pay, and the lead
measure is what they pay. It is recorded in `ltv_schedule.csv` and named in the
article as a separate tightening.

Reads:  out/index_hedonic.csv
        out/grants_by_buyer.csv
        ltv_schedule.csv
        raw/income_percentiles_excl_cpf.csv
Writes: out/affordability.csv

Usage:  python 05_affordability.py
"""

import csv
import os
import sys
from datetime import date

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")

FIRST, LAST = 2013, 2025
TENURE_MONTHS = 300
PERCENTILES = {"p20": "20th", "p50": "50th (Median)", "p80": "80th"}


def fail(msg):
    raise AssertionError("AFFORDABILITY STOPPED: %s" % msg)


def load_param(parameter, when):
    with open(os.path.join(HERE, "ltv_schedule.csv"), newline="",
              encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["parameter"] != parameter:
                continue
            f = date(*[int(x) for x in r["in_force_from"].split("-")])
            t = (date(*[int(x) for x in r["in_force_to"].split("-")])
                 if r["in_force_to"].strip() else date(9999, 12, 31))
            if f <= when <= t:
                return float(r["value"])
    fail("no %s row covers %s in ltv_schedule.csv" % (parameter, when))


def amortise(principal, annual_rate, months):
    if principal <= 0:
        return 0.0
    r = annual_rate / 12.0
    if r == 0:
        return principal / months
    return principal * r / (1.0 - (1.0 + r) ** (-months))


def main():
    hed = pd.read_csv(os.path.join(OUT, "index_hedonic.csv")).set_index("year")
    grants = pd.read_csv(os.path.join(OUT, "grants_by_buyer.csv"))

    incdf = pd.read_csv(os.path.join(RAW, "income_percentiles_excl_cpf.csv"))
    inc = {}
    for key, label in PERCENTILES.items():
        r = incdf[incdf["Dollar"].str.strip() == label].iloc[0]
        inc[key] = {int(c): float(r[c]) for c in incdf.columns if c != "Dollar"}

    anchor = float(hed.loc[FIRST, "raw_median"])
    rows = []
    for year in range(FIRST, LAST + 1):
        mid = date(year, 7, 1)
        P = anchor * float(hed.loc[year, "index"]) / 100.0
        ltv = load_param("LTV_HDB_LOAN", mid)
        rate = load_param("HDB_CONCESSIONARY_RATE", mid)

        for key in ("p20", "p50", "p80"):
            y = inc[key][year]
            g = grants[(grants["year"] == year) & (grants["buyer"] == key)]
            if g.empty:
                fail("no grant row for %d %s" % (year, key))
            g = g.iloc[0]
            G = float(g["total_grant"])
            valid = bool(g["grant_series_valid"])

            loan = min(ltv * P, max(P - G, 0.0))
            pay = amortise(loan, rate, TENURE_MONTHS)
            outlay = max(P - loan - G, 0.0)

            rows.append({
                "year": year, "buyer": key,
                "price": round(P, 0),
                "monthly_income": y,
                "ltv": ltv, "rate": rate,
                "grant": G,
                "loan": round(loan, 0),
                "monthly_repayment": round(pay, 2),
                "msr_pct": round(100.0 * pay / y, 2),
                "price_to_income_years": round(P / (y * 12.0), 3),
                "outlay_years": round(outlay / (y * 12.0), 3),
                "grant_series_valid": valid,
            })

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "affordability.csv"), index=False,
              lineterminator="\n")
    print("out/affordability.csv written")
    print("")
    print("Mortgage servicing ratio, per cent of monthly household income.")
    print("Grants are modelled from 2019 only; earlier years are the no-grant case.")
    print("")
    piv = df.pivot(index="year", columns="buyer", values="msr_pct")
    pti = df.pivot(index="year", columns="buyer", values="price_to_income_years")
    out = df.pivot(index="year", columns="buyer", values="outlay_years")
    print("%-6s %26s %26s %20s" % ("", "MSR %", "price / income, yrs", "outlay, yrs"))
    print("%-6s %8s %8s %8s %8s %8s %8s %6s %6s"
          % ("year", "p20", "p50", "p80", "p20", "p50", "p80", "p20", "p50"))
    for y in piv.index:
        flag = "" if df[(df.year == y)]["grant_series_valid"].iloc[0] else "  (no grants)"
        print("%-6d %8.1f %8.1f %8.1f %8.2f %8.2f %8.2f %6.2f %6.2f%s"
              % (y, piv.loc[y, "p20"], piv.loc[y, "p50"], piv.loc[y, "p80"],
                 pti.loc[y, "p20"], pti.loc[y, "p50"], pti.loc[y, "p80"],
                 out.loc[y, "p20"], out.loc[y, "p50"], flag))

    print("")
    v = df[df["grant_series_valid"]]
    a, b = v["year"].min(), v["year"].max()
    print("Change in MSR over the grant-valid window, %d to %d:" % (a, b))
    for key in ("p20", "p50", "p80"):
        s = v[v["buyer"] == key].set_index("year")["msr_pct"]
        print("  %-4s %6.1f -> %6.1f   %+.1f percentage points"
              % (key, s[a], s[b], s[b] - s[a]))
    d20 = (v[v.buyer == "p20"].set_index("year")["msr_pct"][b]
           - v[v.buyer == "p20"].set_index("year")["msr_pct"][a])
    d80 = (v[v.buyer == "p80"].set_index("year")["msr_pct"][b]
           - v[v.buyer == "p80"].set_index("year")["msr_pct"][a])
    print("")
    print("T4a: p20 change is %.1f points %s than p80's, threshold 5.0 points"
          % (abs(d20 - d80), "smaller" if d20 < d80 else "larger"))
    print("T4b: p20 MSR in %d is %s than in %d, so offset is %s"
          % (b, "no higher" if d20 <= 0 else "higher", a,
             "full" if d20 <= 0 else "partial"))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
