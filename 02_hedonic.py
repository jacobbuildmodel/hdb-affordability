"""
02_hedonic.py

Composition correction, method A: a hedonic price index for a constant-quality
four-room resale flat.

The problem this solves. The mix of flats sold changes every year. More Sengkang
and Punggol, fewer mature estates; newer leases, then ageing ones. A rising median
price is partly a changing basket rather than a rising price. Restricting to
four-room flats removes the largest single source of drift. What remains is drift
in town, size, height and remaining lease, and that is what this regresses out.

The model, on four-room transactions only, complete calendar years:

    log(resale_price) = year dummies
                      + town fixed effects
                      + flat model fixed effects
                      + floor area, linear and squared
                      + storey midpoint
                      + remaining lease, linear and squared
                      + error

The year dummies are the constant-quality price path. Everything else is held
still by construction.

Two modelling choices a reviewer will ask about, both deliberate:

  Remaining lease enters as a quadratic because lease decay is not linear. A flat
  with 90 years left and one with 80 loses far less value per year than one with
  50 and one with 40. A linear term would force the same slope everywhere and
  would push the difference into the year dummies, which is exactly the thing
  being measured.

  Floor area enters as a quadratic for the same reason within the four-room band,
  where the range is roughly 80 to 110 square metres.

Retransformation. The dependent variable is a log, so exp(beta_t) is a
geometric-mean index rather than an arithmetic-mean one. The usual half-variance
correction, exp(beta + s^2 / 2), cancels in the ratio between two years as long as
the residual variance is common across years, which the homoskedastic assumption
already imposes. The index is therefore reported as 100 x exp(beta_t - beta_base)
and is a constant-quality geometric index. This is stated so nobody has to guess.

Reads:  out/resale_clean.csv
Writes: out/index_hedonic.csv
        out/hedonic_diagnostics.txt

Usage:  python 02_hedonic.py
        python 02_hedonic.py --base 2017     (rerun on the near-trough base)
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

FLAT_TYPE = "4 ROOM"
FIRST_YEAR, LAST_YEAR = 2013, 2025          # complete calendar years, per THESIS.md


def fail(msg):
    raise AssertionError("HEDONIC STOPPED: %s" % msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=int, default=FIRST_YEAR)
    ap.add_argument("--lease-spline", action="store_true",
                    help="piecewise-linear lease with knots at 60, 75, 90")
    args = ap.parse_args()

    src = os.path.join(OUT, "resale_clean.csv")
    if not os.path.exists(src):
        fail("out/resale_clean.csv not found. Run 01_clean.py first.")

    df = pd.read_csv(src, low_memory=False)
    df = df[df["flat_type"].str.upper().str.strip() == FLAT_TYPE]
    df = df[(df["year"] >= FIRST_YEAR) & (df["year"] <= LAST_YEAR)].copy()
    if df.empty:
        fail("no %s rows between %d and %d" % (FLAT_TYPE, FIRST_YEAR, LAST_YEAR))
    if args.base not in set(df["year"]):
        fail("base year %d is not in the sample" % args.base)

    df["flat_model"] = df["flat_model"].astype(str).str.upper().str.strip()
    df["town"] = df["town"].astype(str).str.upper().str.strip()
    df["log_price"] = np.log(df["resale_price"])
    df["year_c"] = pd.Categorical(df["year"],
                                  categories=[args.base] +
                                  [y for y in sorted(df["year"].unique())
                                   if y != args.base])

    # drop flat models with too few observations to identify a fixed effect
    counts = df["flat_model"].value_counts()
    rare = counts[counts < 30].index.tolist()
    n_rare = int(df["flat_model"].isin(rare).sum())
    if rare:
        df = df[~df["flat_model"].isin(rare)]

    # Lease specification. The default quadratic is the pre-registered one. The
    # spline is a robustness check added after the quadratic came back with a
    # POSITIVE second-order term, implying the marginal value of a lease year rises
    # with lease length, which is the opposite curvature to Bala's table. See
    # THESIS_ADDENDUM.md entry 5. Both are run and both are reported.
    if args.lease_spline:
        for k in (60, 75, 90):
            df["lease_k%d" % k] = np.maximum(df["lease_years"] - k, 0.0)
        lease_terms = "+ lease_years + lease_k60 + lease_k75 + lease_k90"
    else:
        lease_terms = "+ lease_years + I(lease_years**2)"

    formula = ("log_price ~ C(year_c) + C(town) + C(flat_model) "
               "+ floor_area_sqm + I(floor_area_sqm**2) "
               "+ storey_mid " + lease_terms)
    model = smf.ols(formula, data=df).fit(cov_type="HC1")

    rows = []
    base_ok = False
    for name, beta in model.params.items():
        if not name.startswith("C(year_c)[T."):
            continue
        yr = int(name.split("T.")[1].rstrip("]"))
        se = float(model.bse[name])
        rows.append({"year": yr, "log_coef": float(beta), "se": se,
                     "index": 100.0 * float(np.exp(beta)),
                     "ci_low": 100.0 * float(np.exp(beta - 1.96 * se)),
                     "ci_high": 100.0 * float(np.exp(beta + 1.96 * se))})
    rows.append({"year": args.base, "log_coef": 0.0, "se": 0.0,
                 "index": 100.0, "ci_low": 100.0, "ci_high": 100.0})
    base_ok = True
    idx = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)

    if len(idx) != (LAST_YEAR - FIRST_YEAR + 1):
        fail("expected %d year coefficients including the base, got %d. Year "
             "dummies are not identified."
             % (LAST_YEAR - FIRST_YEAR + 1, len(idx)))

    # raw median for the same cells, so T5 can compare
    raw = (df.groupby("year")["resale_price"].median()
             .rename("raw_median").reset_index())
    raw["raw_index"] = 100.0 * raw["raw_median"] / float(
        raw.loc[raw["year"] == args.base, "raw_median"].iloc[0])
    idx = idx.merge(raw, on="year")
    idx["n"] = df.groupby("year").size().reindex(idx["year"]).values
    idx["base_year"] = args.base

    # float_format pins output to 10 significant digits so the file is
    # byte-identical across machines. The OLS solve (LAPACK/BLAS) agrees with
    # itself to about 12-13 significant digits across platforms, not to the
    # last bit; unformatted floats therefore differ past that point even on
    # identical inputs and code, which is noise, not a pipeline bug. 10 sig
    # figs is far past the precision anything downstream reports (at most 6).
    stem = "index_hedonic_spline" if args.lease_spline else "index_hedonic"
    idx.to_csv(os.path.join(OUT, stem + ".csv"), index=False,
               lineterminator="\n", float_format="%.10g")

    lines = []
    lines.append("Hedonic constant-quality index, %s flats, %d to %d"
                 % (FLAT_TYPE, FIRST_YEAR, LAST_YEAR))
    lines.append("base year %d = 100" % args.base)
    lines.append("lease specification     %s"
                 % ("piecewise-linear spline, knots 60/75/90"
                    if args.lease_spline else "quadratic (pre-registered)"))
    lines.append("")
    lines.append("observations            %d" % int(model.nobs))
    lines.append("R-squared               %.4f" % model.rsquared)
    lines.append("adjusted R-squared      %.4f" % model.rsquared_adj)
    lines.append("residual sd (log)       %.4f" % float(np.sqrt(model.mse_resid)))
    lines.append("covariance              HC1 heteroskedasticity-robust")
    lines.append("towns                   %d" % df["town"].nunique())
    lines.append("flat models kept        %d" % df["flat_model"].nunique())
    lines.append("flat models dropped     %d models, %d rows, fewer than 30 obs each"
                 % (len(rare), n_rare))
    lines.append("")
    lines.append("non-year coefficients, for inspection:")
    for name in ("floor_area_sqm", "I(floor_area_sqm ** 2)", "storey_mid",
                 "lease_years", "I(lease_years ** 2)",
                 "lease_k60", "lease_k75", "lease_k90"):
        if name in model.params:
            lines.append("  %-24s %12.6f  (se %.6f)"
                         % (name, model.params[name], model.bse[name]))
    lines.append("")
    lines.append("%-6s %10s %10s %10s %10s %10s %8s"
                 % ("year", "index", "ci_low", "ci_high", "raw_index",
                    "raw_median", "n"))
    for _, r in idx.iterrows():
        lines.append("%-6d %10.2f %10.2f %10.2f %10.2f %10.0f %8d"
                     % (r["year"], r["index"], r["ci_low"], r["ci_high"],
                        r["raw_index"], r["raw_median"], r["n"]))

    first = idx.iloc[0]
    last = idx.iloc[-1]
    lines.append("")
    lines.append("%d to %d, constant quality  %+.1f%%"
                 % (first["year"], last["year"],
                    last["index"] - 100.0 if args.base == FIRST_YEAR
                    else 100.0 * (last["index"] / first["index"] - 1)))
    lines.append("%d to %d, raw median        %+.1f%%"
                 % (first["year"], last["year"],
                    100.0 * (last["raw_index"] / first["raw_index"] - 1)))
    lines.append("composition correction is worth %.1f percentage points"
                 % (100.0 * (last["index"] / first["index"] - 1)
                    - 100.0 * (last["raw_index"] / first["raw_index"] - 1)))

    text = "\n".join(lines)
    dstem = "hedonic_diagnostics_spline" if args.lease_spline else "hedonic_diagnostics"
    with open(os.path.join(OUT, dstem + ".txt"), "w",
              newline="\n") as fh:
        fh.write(text + "\n")
    print(text)
    print("")
    print("out/%s.csv written" % stem)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
