"""
04_grants.py

Works out what a standardised first-timer family buying a four-room resale flat
would have received in grants, in each year, at each of the three pre-registered
income percentiles.

Two grants are modelled:

  Enhanced CPF Housing Grant. Banded by average gross monthly household income,
  tapering to nothing above 9,000 dollars a month. Two regimes, both from HDB's
  own Annex A of 19 August 2024, which prints the old and the new table side by
  side. Bands in `ehg_bands.csv`.

  CPF Housing Grant for resale flats. A flat amount for 2- to 4-room, subject to
  the purchase income ceiling. 50,000 until 13 February 2023 and 80,000 after,
  from MOF Budget 2023 Annex E-1. Schedule in `grant_schedule.csv`.

One grant is deliberately NOT modelled:

  Proximity Housing Grant. It is worth 20,000 or 30,000 dollars and has no income
  test, so it would simply shift every buyer by the same amount and change no
  comparison in this piece. More importantly it is conditional on living with or
  near a parent, which is a household circumstance rather than an income one, and
  modelling it would mean assuming a living arrangement for a hypothetical buyer.
  The article states that it is omitted and what that omission is worth.

The EHG did not exist before 11 September 2019. It replaced the Additional and
Special CPF Housing Grants, whose schedule is not sourced. So the grant-adjusted
series starts in 2019 and the article says why rather than modelling a grant it
cannot document.

Mid-year rule: a scheme in force on 1 July of a calendar year is treated as the
scheme for that year. The February 2023 change therefore counts from 2023 and the
August 2024 change from 2025. Stated here because it is a judgement call and it
moves two years.

Reads:  ehg_bands.csv
        grant_schedule.csv
        raw/income_percentiles_excl_cpf.csv
Writes: out/grants_by_buyer.csv

Usage:  python 04_grants.py
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
EHG_START_YEAR = 2019          # EHG effective 11 September 2019
PERCENTILES = {"p20": "20th", "p50": "50th (Median)", "p80": "80th"}


def fail(msg):
    raise AssertionError("GRANTS STOPPED: %s" % msg)


def load_income():
    df = pd.read_csv(os.path.join(RAW, "income_percentiles_excl_cpf.csv"))
    out = {}
    for key, label in PERCENTILES.items():
        row = df[df["Dollar"].str.strip() == label]
        if row.empty:
            fail("income series '%s' not found" % label)
        r = row.iloc[0]
        out[key] = {int(c): float(r[c]) for c in df.columns if c != "Dollar"}
    return out


def load_bands():
    bands = {}
    with open(os.path.join(HERE, "ehg_bands.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            bands.setdefault(r["regime"], []).append(
                (float(r["income_upper"]), float(r["ehg_amount"])))
    for k in bands:
        bands[k].sort()
    if not bands:
        fail("ehg_bands.csv is empty")
    return bands


def ehg_for(income, bands, regime):
    """Banded, tapering to zero above the top band."""
    for upper, amount in bands[regime]:
        if income <= upper:
            return amount
    return 0.0


def load_family_grant():
    """(from_date, to_date, ceiling, amount) for 2- to 4-room first-timer families."""
    rows = []
    with open(os.path.join(HERE, "grant_schedule.csv"), newline="",
              encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["grant"] != "CPF_HOUSING_GRANT":
                continue
            if "2-4 room" not in r["scope"]:
                continue
            if r["status"] == "NOT-OBTAINED":
                continue
            f = date(*[int(x) for x in r["in_force_from"].split("-")])
            t = (date(*[int(x) for x in r["in_force_to"].split("-")])
                 if r["in_force_to"].strip() else date(9999, 12, 31))
            rows.append((f, t, float(r["income_band_high"]), float(r["amount"])))
    if not rows:
        fail("no CPF_HOUSING_GRANT rows for 2- to 4-room found")
    return sorted(rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = load_income()
    bands = load_bands()
    fam = load_family_grant()

    out = []
    for year in range(FIRST, LAST + 1):
        mid = date(year, 7, 1)
        regime = "post_aug2024" if mid >= date(2024, 8, 20) else "pre_aug2024"

        ceiling = amount = None
        for f, t, c, a in fam:
            if f <= mid <= t:
                ceiling, amount = c, a
        valid = year >= EHG_START_YEAR
        if valid and ceiling is None:
            fail("no CPF Housing Grant row covers %s, and the grant series is "
                 "supposed to be valid from %d" % (mid, EHG_START_YEAR))

        for key in ("p20", "p50", "p80"):
            y = inc[key][year]
            if valid:
                ehg = ehg_for(y, bands, regime)
                ehg_note = "banded, %s regime" % regime
                fg = amount if y <= ceiling else 0.0
            else:
                # Before 11 September 2019 the EHG did not exist; it replaced the
                # Additional and Special CPF Housing Grants, whose schedule is not
                # sourced. Nothing is modelled for these years and the flag says so.
                ehg = 0.0
                fg = 0.0
                ehg_note = ("before the EHG; AHG and SHG not sourced, nothing "
                            "modelled, see README")
                ceiling = ceiling if ceiling is not None else float("nan")
            out.append({
                "year": year,
                "buyer": key,
                "monthly_income": y,
                "ehg": ehg,
                "ehg_note": ehg_note,
                "family_grant": fg,
                "family_grant_ceiling": ceiling,
                "total_grant": ehg + fg,
                "grant_series_valid": valid,
            })

    df = pd.DataFrame(out)
    df.to_csv(os.path.join(OUT, "grants_by_buyer.csv"), index=False,
              lineterminator="\n")

    print("out/grants_by_buyer.csv written")
    print("")
    print("Grants for a first-timer family buying a four-room resale flat.")
    print("PHG omitted by design. Series valid from %d only." % EHG_START_YEAR)
    print("")
    piv = df[df["grant_series_valid"]].pivot(index="year", columns="buyer",
                                             values="total_grant")
    ehgp = df[df["grant_series_valid"]].pivot(index="year", columns="buyer",
                                              values="ehg")
    print("%-6s %28s %28s" % ("", "TOTAL GRANT", "of which EHG"))
    print("%-6s %9s %9s %9s %9s %9s %9s"
          % ("year", "p20", "p50", "p80", "p20", "p50", "p80"))
    for y in piv.index:
        print("%-6d %9.0f %9.0f %9.0f %9.0f %9.0f %9.0f"
              % (y, piv.loc[y, "p20"], piv.loc[y, "p50"], piv.loc[y, "p80"],
                 ehgp.loc[y, "p20"], ehgp.loc[y, "p50"], ehgp.loc[y, "p80"]))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
