#!/usr/bin/env python3
"""
11_tests.py -- T1, T2 and T3 as THESIS section 6 fixes them, the two gates,
every sealed sensitivity (section 7), the reported calculation (section 7A)
and the verdict (section 8). Reads ROOT/out/ from 10_load.py.

  python3 cargradient/11_tests.py [--root DIR] [--boot N]

Unit: one row per resale (THESIS section 3). Estimator: two-stage least
squares on data demeaned over the fixed effects by pyfixest's alternating
projections (pyfixest.estimation.demean, tolerance 1e-10), with clustered
standard errors computed here:

  V = c x B (sum over clusters g of s_g s_g') B,  B = (Xhat'Xhat)^-1,
  s_g = sum over rows in g of Xhat_i u_i,  u = y - X beta,
  c = G/(G-1) x (N-1)/(N-K),  K = columns of X (fixed effects not counted).

Two-way clustering: V = V_block + V_quarter - V_block-quarter, each with its
own c. Used for the first-stage F of gate 2 (the instrument varies only by
quarter) and for sensitivity E. The 95 per cent interval is beta +/- 1.959964 se. For T1
and T2 the same estimate is also fitted with pyfixest.feols (one endogenous
regressor) and must agree to 1e-6; T3 has two endogenous regressors, which
pyfixest.feols does not take.

Writes ROOT/out/: tests.csv (key, value), sensitivities.csv, year_slopes.csv,
calc_7a.csv, verdict.txt.
"""
import gzip
import io
import os

import numpy as np
import pandas as pd
import pyfixest as pf
from pyfixest.estimation import demean as pf_demean

import cglib as L

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

FE = ["block_id", "lease_quarter", "flat_type", "storey_range", "flat_model"]
TOL = 1e-10


# ---------------------------------------------------------------- estimation
def codes(df, cols):
    return np.column_stack([pd.factorize(df[c])[0] for c in cols]).astype(np.uint64)


def demeaned(df, cols, fe):
    """Demean each column over the fixed effects. Columns are scaled to unit
    standard deviation first and scaled back after (demeaning is linear), so
    the absolute tolerance means the same for COE x distance (~1e6) as for a
    dummy."""
    X = df[cols].to_numpy(dtype=float)
    if not np.isfinite(X).all():
        raise RuntimeError(f"non-finite values in {cols}")
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    res, ok = pf_demean(X / sd, codes(df, fe), np.ones(len(df)), tol=TOL, maxiter=100000)
    if not ok:
        raise RuntimeError("demeaning did not converge")
    return res * sd


def keep(M, raw, first):
    """Column indices of M to keep: the first `first` columns (outcome,
    regressors, instruments) always; a control only if its demeaned spread is
    at least 1e-8 of its raw spread (else it is absorbed by the fixed effects
    and dropped, as pyfixest does). A regressor or instrument that collapses
    is an error."""
    spread = M.std(axis=0)
    rawsd = raw.std(axis=0)
    rawsd[rawsd == 0] = 1.0
    ok = spread >= 1e-8 * rawsd
    if not ok[:first].all():
        raise RuntimeError("a regressor or instrument is absorbed by the fixed effects")
    return [i for i in range(M.shape[1]) if i < first or ok[i]]


def clustered(Xh, u, B, groups):
    """c x B M B for one clustering (groups: integer codes)."""
    s = Xh * u[:, None]
    order = np.argsort(groups, kind="mergesort")
    g = groups[order]
    cuts = np.flatnonzero(np.diff(g)) + 1
    sums = np.add.reduceat(s[order], np.r_[0, cuts], axis=0)
    G, N, K = len(sums), Xh.shape[0], Xh.shape[1]
    c = G / (G - 1) * (N - 1) / (N - K)
    return c * B @ (sums.T @ sums) @ B


def tsls(y, X, Z, clusters):
    """2SLS (or OLS when Z is X). clusters: list of integer-code arrays; one
    for one-way, [block, quarter, block-quarter] for two-way."""
    Xh = Z @ np.linalg.solve(Z.T @ Z, Z.T @ X)
    B = np.linalg.inv(Xh.T @ Xh)
    beta = B @ (Xh.T @ y)
    u = y - X @ beta
    if len(clusters) == 1:
        V = clustered(Xh, u, B, clusters[0])
    else:
        V = clustered(Xh, u, B, clusters[0]) + clustered(Xh, u, B, clusters[1]) - clustered(Xh, u, B, clusters[2])
    return beta, np.sqrt(np.maximum(np.diag(V), 0.0))


def gcode(df, col):
    return pd.factorize(df[col])[0]


def cluster_codes(df, twoway):
    b = gcode(df, "block_id")
    if not twoway:
        return [b]
    q = gcode(df, "quarter")
    bq = pd.factorize(df["block_id"] + "#" + df["quarter"])[0]
    return [b, q, bq]


# ---------------------------------------------------------------- the panel
def load(out):
    with gzip.open(os.path.join(out, "panel.csv.gz"), "rt", encoding="utf-8") as f:
        df = pd.read_csv(f, dtype={"quarter": str, "block_id": str, "town": str, "flat_type": str,
                                   "storey_range": str, "flat_model": str, "basis": str})
    df["lease_quarter"] = df["lease_band"].astype(int).astype(str) + "|" + df["quarter"]
    return df


def prepare(df, quarters, dd="dd", y="price_psm", street=False, mrt_far=False, log=False):
    d = df[df["quarter"].isin(quarters)].copy()
    if street:
        d["dd_use"] = d[dd].where(d[dd].notna(), d["dd_street"])
    else:
        d["dd_use"] = d[dd]
    d = d[d["dd_use"].notna() & d["coep"].notna() & d["price_psm"].notna()]
    if mrt_far:
        d = d[d["mrt_km"] > L.MRT_FAR_KM]
    d["yv"] = np.log(d[y]) if log else d[y]
    d["cd"] = d["coep"] * d["dd_use"]
    d["qd"] = d["coeq"] * d["dd_use"]
    d["post12dd"] = (d["quarter"] >= L.POST12_FIRST).astype(float) * d["dd_use"]
    return d.reset_index(drop=True)


def town_trends(d):
    towns = sorted(d["town"].unique())[1:]
    cols = []
    for t in towns:
        c = "tt_" + t.replace(" ", "_").replace("/", "_")
        d[c] = (d["town"] == t).astype(float) * (d["year"] - 2000)
        cols.append(c)
    return cols


def fit_single(d, exog, iv=True, twoway=False):
    """One endogenous regressor cd (instrument qd) or OLS on cd."""
    cols = ["yv", "cd", "qd"] + exog
    M = demeaned(d, cols, FE)
    M = M[:, keep(M, d[cols].to_numpy(dtype=float), 3)]
    y, cd, qd = M[:, 0], M[:, 1], M[:, 2]
    W = M[:, 3:]
    X = np.column_stack([cd, W])
    Z = np.column_stack([qd, W]) if iv else X
    beta, se = tsls(y, X, Z, cluster_codes(d, twoway))
    # first stage: cd on qd and the exogenous controls. The instrument varies
    # only by quarter, so its F is clustered two ways (block and quarter);
    # clustered by block alone it overstates strength (DESIGN_SKETCH, round 5).
    fb, fse = tsls(cd, np.column_stack([qd, W]), np.column_stack([qd, W]), cluster_codes(d, True))
    return {"est": beta[0], "se": se[0], "lo": beta[0] - L.Z95 * se[0], "hi": beta[0] + L.Z95 * se[0],
            "F": (fb[0] / fse[0]) ** 2, "n": len(d), "blocks": d["block_id"].nunique(),
            "quarters": d["quarter"].nunique()}


def crosscheck_pyfixest(d, exog, res):
    rhs = " + ".join(exog) if exog else "1"
    fe = " + ".join(FE)
    f = pf.feols(f"yv ~ {rhs} | {fe} | cd ~ qd", d, vcov={"CRV1": "block_id"},
                 ssc=pf.ssc(k_adj=True, k_fixef="none", G_adj=True), fixef_tol=TOL)
    b = float(f.coef()["cd"])
    if abs(b - res["est"]) > 1e-6 * max(1.0, abs(b)):
        raise SystemExit(f"pyfixest cross-check failed: {b} vs {res['est']}")
    return b


def fit_t3(df, before, after, dd="dd", twoway=False, wfh=False):
    after_q = [q for q in after if not (wfh and L.WFH[0] <= q <= L.WFH[1])]
    d = prepare(df, list(before) + after_q, dd=dd)
    d["after"] = (d["quarter"] >= L.T3_AFTER[0]).astype(int)
    for c in ("block_id", "flat_type", "storey_range", "flat_model"):
        d[c + "_a"] = d[c] + "#" + d["after"].astype(str)
    d["cd_a"] = d["cd"] * d["after"]
    d["qd_a"] = d["qd"] * d["after"]
    d["fa_a"] = d["floor_area"] * d["after"]
    fe = ["block_id_a", "lease_quarter", "flat_type_a", "storey_range_a", "flat_model_a"]
    cols = ["yv", "cd", "cd_a", "qd", "qd_a", "floor_area", "fa_a"]
    M = demeaned(d, cols, fe)
    M = M[:, keep(M, d[cols].to_numpy(dtype=float), 5)]
    y = M[:, 0]
    W = M[:, 5:]
    X = np.column_stack([M[:, 1], M[:, 2], W])
    Z = np.column_stack([M[:, 3], M[:, 4], W])
    beta, se = tsls(y, X, Z, cluster_codes(d, twoway))
    out = {"before_est": beta[0], "before_se": se[0], "before_lo": beta[0] - L.Z95 * se[0],
           "before_hi": beta[0] + L.Z95 * se[0], "diff_est": beta[1], "diff_se": se[1],
           "diff_lo": beta[1] - L.Z95 * se[1], "diff_hi": beta[1] + L.Z95 * se[1],
           "after_est": beta[0] + beta[1], "n": len(d), "blocks": d["block_id"].nunique()}
    # first-stage F in each window separately (THESIS: below 10 in either)
    for w, qs in (("before", before), ("after", after_q)):
        dw = prepare(df, list(qs), dd=dd)
        cw = ["cd", "qd", "floor_area"]
        Mw = demeaned(dw, cw, FE)
        Mw = Mw[:, keep(Mw, dw[cw].to_numpy(dtype=float), 2)]
        fb, fse = tsls(Mw[:, 0], Mw[:, 1:], Mw[:, 1:], cluster_codes(dw, True))
        out[f"F_{w}"] = (fb[0] / fse[0]) ** 2
    return out


# ---------------------------------------------------------------- 7A
def year_slopes(d, years):
    cols = []
    for y in years:
        if y == L.CALC_YEARS[0]:
            continue
        c = f"ddy_{y}"
        d[c] = (d["year"] == y).astype(float) * d["dd_use"]
        cols.append(c)
    allc = ["yv"] + cols + ["floor_area"]
    M = demeaned(d, allc, FE)
    M = M[:, keep(M, d[allc].to_numpy(dtype=float), 1 + len(cols))]
    X = M[:, 1:]
    beta, se = tsls(M[:, 0], X, X, cluster_codes(d, False))
    return {y: (0.0, 0.0) if y == L.CALC_YEARS[0] else (beta[cols.index(f"ddy_{y}")], se[cols.index(f"ddy_{y}")])
            for y in years}


def coe_change(out):
    coe = pd.read_csv(os.path.join(out, "coe_quarterly.csv"), dtype={"quarter": str})
    m = {y: coe[coe["quarter"].str.startswith(str(y))]["coep"].mean() for y in L.CALC_YEARS}
    return m[L.CALC_YEARS[1]] - m[L.CALC_YEARS[0]], m


def boot_share(d, years, dcoe, n, seed):
    rng = np.random.default_rng(seed)
    idx = d.groupby("block_id").indices
    keys = list(idx)
    shares = []
    for _ in range(n):
        pick = rng.integers(0, len(keys), len(keys))
        rows = np.concatenate([idx[keys[k]] for k in pick])
        newid = np.concatenate([np.full(len(idx[keys[k]]), j) for j, k in enumerate(pick)])
        b = d.iloc[rows].copy()
        b["block_id"] = newid.astype(str)
        beta = fit_single(b, ["floor_area"])["est"]
        th = year_slopes(b, years)[L.CALC_YEARS[1]][0]
        imp, act = -15 * beta * dcoe, -15 * th
        shares.append(imp / act if act != 0 else np.nan)
    s = np.array(shares)
    s = s[np.isfinite(s)]
    return (np.percentile(s, 2.5), np.percentile(s, 97.5)) if len(s) else (np.nan, np.nan)


# ---------------------------------------------------------------- verdict
def verdict(o):
    a2 = {"SURVIVE": "Not only a coincidence: in HDB flats, the gap between near and far widened more "
                     "when COEs rose, since 2016",
          "FAIL_NO_LINK": "No sign of a link in HDB flats since 2016",
          "FAIL_OPPOSITE": "If anything the opposite: since 2016, flats further out gained on flats near "
                           "town when COEs rose",
          "NOT_SCORED": "The record cannot say whether there is a link in HDB flats since 2016"}[o["T2"]]
    a1 = {"SURVIVE": "and the same was true in 2002 to 2015",
          "FAIL_NO_LINK": "and there was no sign of it in 2002 to 2015",
          "FAIL_OPPOSITE": "and the opposite in 2002 to 2015",
          "NOT_SCORED": "and the record cannot say for 2002 to 2015"}[o["T1"]]
    b = {"SURVIVE": "The link weakened after growth in the car quota was cut to zero in 2018 (the record "
                    "cannot say whether rail, working from home or something else weakened it).",
         "FAIL_NO_CHANGE": "No clear change after the 2018 cut.",
         "FAIL_STRONGER": "The link got stronger after the 2018 cut.",
         "NOT_SCORED_NO_TILT": "There was no link before 2018 to weaken.",
         "NOT_SCORED": "The record cannot say whether the 2018 cut changed it."}[o["T3"]]
    return f"{a2}, {a1}. {b}"


def main():
    a = L.args("cargradient T1-T3, gates, sensitivities, 7A and verdict.",
               lambda p: p.add_argument("--boot", type=int, default=int(os.environ.get("CG_BOOT_N", L.BOOT_N))))
    P = L.paths(a.root)
    out = P["out"]
    df = load(out)
    cov = {r["window"]: int(r["sales_geocoded"]) / int(r["sales"]) if int(r["sales"]) else 0.0
           for r in L.read_csv(os.path.join(out, "geocode_coverage.csv"))}
    T = {}
    sens = []

    # T1 and T2
    for t, w, exog in (("T1", "T1", ["floor_area", "post12dd"]), ("T2", "T2", ["floor_area"])):
        d = prepare(df, L.window(w))
        r = fit_single(d, exog)
        crosscheck_pyfixest(d, exog, r)
        geo_ok = bool(cov[w] >= L.GEO_MIN)
        f_ok = bool(r["F"] >= L.F_MIN)
        oc = L.outcome_sign_test(r["est"], r["lo"], r["hi"], geo_ok and f_ok)
        T.update({f"{t}_{k}": v for k, v in r.items()})
        T.update({f"{t}_geo_share": cov[w], f"{t}_geo_ok": geo_ok, f"{t}_F_ok": f_ok, f"{t}_outcome": oc})

    # T3
    r3 = fit_t3(df, L.window("T3_before"), L.window("T3_after"))
    geo_ok = bool(cov["T3_before"] >= L.GEO_MIN and cov["T3_after"] >= L.GEO_MIN)
    f_ok = bool(r3["F_before"] >= L.F_MIN and r3["F_after"] >= L.F_MIN)
    oc3 = L.outcome_t3(r3["diff_est"], r3["diff_lo"], r3["diff_hi"], r3["before_hi"], geo_ok and f_ok)
    T.update({f"T3_{k}": v for k, v in r3.items()})
    T.update({"T3_geo_share_before": cov["T3_before"], "T3_geo_share_after": cov["T3_after"],
              "T3_geo_ok": geo_ok, "T3_F_ok": f_ok, "T3_outcome": oc3})

    # Sensitivities (section 7), reported, not scored.
    def add(name, test, r, note=""):
        if "diff_est" in r:
            oc = L.outcome_t3(r["diff_est"], r["diff_lo"], r["diff_hi"], r["before_hi"], True)
            sens.append((name, test, r["diff_est"], r["diff_se"], r["diff_lo"], r["diff_hi"], r["n"], oc, note))
        else:
            oc = L.outcome_sign_test(r["est"], r["lo"], r["hi"], True)
            sens.append((name, test, r["est"], r["se"], r["lo"], r["hi"], r["n"], oc, note))

    add("A_split_approval", "T1", fit_single(prepare(df, L.qrange(*L.SPLIT_A)), ["floor_area"]))
    add("A_split_registration", "T1", fit_single(prepare(df, L.qrange(*L.SPLIT_B)), ["floor_area"]))
    for t, w, exog in (("T1", "T1", ["floor_area", "post12dd"]), ("T2", "T2", ["floor_area"])):
        add("B_cityhall", t, fit_single(prepare(df, L.window(w), dd="dd_cityhall"), exog))
        add("C_log_price", t, fit_single(prepare(df, L.window(w), log=True), exog))
        add("D_ols", t, fit_single(prepare(df, L.window(w)), exog, iv=False))
        add("E_twoway", t, fit_single(prepare(df, L.window(w)), exog, twoway=True))
        d = prepare(df, L.window(w))
        add("H_town_trends", t, fit_single(d, exog + town_trends(d)))
        add("I_far_from_mrt", t, fit_single(prepare(df, L.window(w), mrt_far=True), exog),
            "today's MRT exit layer, not 2015's stations")
    add("J_street_points", "T1", fit_single(prepare(df, L.window("T1"), street=True), ["floor_area", "post12dd"]))
    t2w = [q for q in L.window("T2") if not (L.WFH[0] <= q <= L.WFH[1])]
    add("F_without_2020_2022", "T2", fit_single(prepare(df, t2w), ["floor_area"]))
    add("B_cityhall", "T3", fit_t3(df, L.window("T3_before"), L.window("T3_after"), dd="dd_cityhall"))
    add("E_twoway", "T3", fit_t3(df, L.window("T3_before"), L.window("T3_after"), twoway=True))
    add("F_without_2020_2022", "T3", fit_t3(df, L.window("T3_before"), L.window("T3_after"), wfh=True))
    add("G_before_2016Q1_2017Q3", "T3", fit_t3(df, L.qrange(*L.T3_BEFORE_SENS), L.window("T3_after")))

    # 7A
    d2 = prepare(df, L.window("T2"))
    years = sorted(int(y) for y in d2["year"].unique())
    slopes = year_slopes(d2, years)
    dcoe, coebar = coe_change(out)
    beta2, lo2, hi2 = T["T2_est"], T["T2_lo"], T["T2_hi"]
    imp = -15 * beta2 * dcoe
    imp_lo, imp_hi = sorted((-15 * lo2 * dcoe, -15 * hi2 * dcoe))
    th, ths = slopes[L.CALC_YEARS[1]]
    act = -15 * th
    act_lo, act_hi = sorted((-15 * (th - L.Z95 * ths), -15 * (th + L.Z95 * ths)))
    readable = (act_lo > 0 or act_hi < 0) and np.sign(imp) == np.sign(act) and imp != 0
    share = imp / act if readable else np.nan
    sh_lo, sh_hi = boot_share(d2, years, dcoe, a.boot, L.BOOT_SEED) if readable else (np.nan, np.nan)
    calc = [("coebar_2020", coebar[L.CALC_YEARS[0]]), ("coebar_2023", coebar[L.CALC_YEARS[1]]), ("dcoe", dcoe),
            ("dgap_implied", imp), ("dgap_implied_lo", imp_lo), ("dgap_implied_hi", imp_hi),
            ("dgap_actual", act), ("dgap_actual_lo", act_lo), ("dgap_actual_hi", act_hi),
            ("share_readable", bool(readable)), ("share", share), ("share_lo", sh_lo), ("share_hi", sh_hi),
            ("boot_n", a.boot)]
    L.write_csv(os.path.join(out, "calc_7a.csv"), ["key", "value"], calc)
    L.write_csv(os.path.join(out, "year_slopes.csv"), ["year", "theta", "se", "gap_5_20"],
                [(y, b, s, -15 * b) for y, (b, s) in sorted(slopes.items())])

    o = {t: T[f"{t}_outcome"] for t in L.SCORED}
    v = verdict(o)
    conf = L.confidences(P["thesis"])
    scored = [t for t in L.SCORED if L.held(o[t]) is not None]
    T["n_scored"] = len(scored)
    T["held_count"] = sum(L.held(o[t]) for t in scored)
    if all(conf[t] is not None for t in scored) and scored:
        T["brier"] = sum((conf[t] - L.held(o[t])) ** 2 for t in scored) / len(scored)
        T["expected_held"] = sum(conf[t] for t in scored)
    L.write_csv(os.path.join(out, "tests.csv"), ["key", "value"], sorted(T.items()))
    L.write_csv(os.path.join(out, "sensitivities.csv"),
                ["name", "test", "est", "se", "lo", "hi", "n", "outcome_if_scored", "note"], sens)
    L.write_text(os.path.join(out, "verdict.txt"), v + "\n")
    print("outcomes:", o)
    print("verdict:", v)


if __name__ == "__main__":
    main()
