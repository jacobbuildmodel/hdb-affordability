#!/usr/bin/env python3
"""
06_coverage_check.py -- pre-seal placebo check of the scored intervals
(THESIS section 6). Run from the repository root:

  PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py \
      [--sims N] [--sims-t3 N] [--stress-sims N] [--batch N]
  PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py --guard [--guard-sims N]
      (the drift-guard comparison; see "guard mode" below; writes
      out/coverage_guard.csv and coverage_guard.txt)
  PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py --guard2 --test T1   (and T2, T3)
  PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py --guard2-merge
      (round 2, "guard2 mode" below; writes out/coverage_guard2.csv and .txt)

Uses the REAL design and INVENTED outcomes:
- real: which block traded in which quarter, with its flat type, storey
  range, flat model, floor area and lease (read from raw/resale/ with the
  price column excluded, so it is never parsed); real block distances to
  Raffles Place; the real quarterly A/B COE premium and quota. None of these
  is the outcome.
- invented: prices with a true COE x distance slope of ZERO,
    price = block effect + common quarterly shock (+ stress term) + noise.

For T1, T2 and the T3 difference it fits exactly the scored model (section
3, using 11_tests.py's own design code) and records how often the 95 per
cent interval excludes zero, with two-way clustering (scored) and block-only
clustering (sensitivity E).

X, Z and the controls are demeaned once by the scored code. Each invented
outcome is then projected on the fixed effects exactly (Projector, the same
projection the scored code reaches by alternating projections), so a
simulation takes well under a second. The largest gap between the two, for
one invented outcome per test, is reported.

PASS: the two-way rate lies between 2% and 9% for each test, in the main
specification (the one above). Two stress variants add a quarterly shock to
the distance slope itself, independent across quarters or persistent (AR(1),
0.8); they are reported, not part of the pass line.

The first-stage F depends only on the real design, not on the invented
prices, so it is the same in every simulation. It is computed once and is
the value gate 2 will see at the seal.

Output: cargradient/out/coverage_check.csv and coverage_check.txt.
"""
import importlib.util
import os
import sys
import time

import numpy as np
import pandas as pd
import scipy.sparse as sp

import cglib as L

HERE = os.path.dirname(os.path.abspath(__file__))


def load_module(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


T = load_module("t11", "11_tests.py")
LD = load_module("l10", "10_load.py")
COLS = ["month", "town", "flat_type", "block", "street_name", "storey_range", "floor_area_sqm",
        "flat_model", "lease_commence_date"]          # resale_price is not among them


def design_frame(root):
    raw = os.path.join(root, "raw")
    frames = []
    for fid in L.RESALE:
        frames.append(pd.read_csv(os.path.join(raw, "resale", fid + ".csv"), usecols=COLS, dtype=str))
    df = pd.concat(frames, ignore_index=True)
    for c in ("town", "flat_type", "block", "street_name", "storey_range", "flat_model"):
        df[c] = df[c].str.strip().str.upper()
    df["flat_type"] = df["flat_type"].str.replace("MULTI GENERATION", "MULTI-GENERATION", regex=False)
    df["quarter"] = df["month"].map(L.quarter)
    df["year"] = df["month"].str[:4].astype(int)
    df = df[(df["quarter"] >= L.T1_FIRST) & (df["quarter"] <= L.T2_LAST)].copy()
    dist = pd.read_csv(os.path.join(root, "out", "block_distance.csv"), dtype=str)
    dist = dist[dist["match_type"].isin(["exact", "expanded"])]
    df = df.merge(dist[["block", "street_name", "km_raffles_mean"]], on=["block", "street_name"], how="left")
    coe = LD.coe_quarterly(raw)
    df = df.merge(coe, on="quarter", how="left")
    rem = L.LEASE_YEARS - (df["year"] - df["lease_commence_date"].astype(int))
    out = pd.DataFrame({
        "quarter": df["quarter"], "year": df["year"], "block_id": df["block"] + "|" + df["street_name"],
        "town": df["town"], "flat_type": df["flat_type"], "storey_range": df["storey_range"],
        "flat_model": df["flat_model"], "floor_area": df["floor_area_sqm"].astype(float),
        "lease_band": (rem // L.LEASE_BAND) * L.LEASE_BAND,
        "price_psm": 1.0,                                  # placeholder; replaced by invented prices
        "dd": pd.to_numeric(df["km_raffles_mean"], errors="coerce"), "dd_street": np.nan,
        "coep": df["coep"], "coeq": df["coeq"]})
    out["lease_quarter"] = out["lease_band"].astype(int).astype(str) + "|" + out["quarter"]
    return out.reset_index(drop=True)


class Projector:
    """The fixed-effects projection M_D, exact, for many outcome columns at
    once. D = [block dummies, the other fixed effects C]. With M_B the
    within-block demeaning, M_D y = M_B y - M_B C S+ C' M_B y, where
    S = C' M_B C is small (a few hundred to a few thousand columns) and is
    inverted once (pseudo-inverse: each fixed effect in C repeats the
    constant). Mathematically the same projection the scored code reaches by
    alternating projections (MAP); validate() reports the difference."""

    def __init__(self, d, fe):
        n = len(d)
        self.b = pd.factorize(d[fe[0]])[0]
        self.nb = np.bincount(self.b).astype(float)
        cols, off = [], 0
        for c in fe[1:]:
            k = pd.factorize(d[c])[0]
            cols.append(k + off)
            off += k.max() + 1
        rows = np.repeat(np.arange(n), len(cols))
        self.C = sp.csr_matrix((np.ones(n * len(cols)), (rows, np.column_stack(cols).ravel())), shape=(n, off))
        Bm = sp.csr_matrix((np.ones(n), (np.arange(n), self.b)), shape=(n, len(self.nb)))
        CtB = (self.C.T @ Bm).tocsr()
        S = (self.C.T @ self.C).toarray() - (CtB @ sp.diags(1.0 / self.nb) @ CtB.T).toarray()
        lam, V = np.linalg.eigh(S)
        ok = lam > 1e-9 * lam.max()
        self.Sp = (V[:, ok] / lam[ok]) @ V[:, ok].T
        self.rank_drop = int((~ok).sum())

    def within_block(self, Y):
        means = np.column_stack([np.bincount(self.b, weights=Y[:, j]) for j in range(Y.shape[1])]) / self.nb[:, None]
        return Y - means[self.b]

    def apply(self, Y):
        Yb = self.within_block(Y)
        g = self.Sp @ (self.C.T @ Yb)
        return Yb - self.within_block(self.C @ g)


class Fixed:
    """The scored design for one test, demeaned once by the scored code
    (11_tests.demeaned): X, Z, Xhat, B and the clusters. Only y changes
    between simulations; it is projected by Projector."""

    def __init__(self, d, fe, xcols, zcols, wcols, coef):
        raw = d[xcols + zcols + wcols].to_numpy(dtype=float)
        M = T.demeaned(d, xcols + zcols + wcols, fe)
        kx, kz = len(xcols), len(zcols)
        keepi = T.keep(M, raw, kx + kz)
        M = M[:, keepi]
        X = np.column_stack([M[:, :kx], M[:, kx + kz:]])
        Z = np.column_stack([M[:, kx:kx + kz], M[:, kx + kz:]])
        self.X, self.Xh = X, Z @ np.linalg.solve(Z.T @ Z, Z.T @ X)
        self.B = np.linalg.inv(self.Xh.T @ self.Xh)
        self.d, self.fe, self.coef = d, fe, coef
        self.P = Projector(d, fe)
        self.groups = {"two": [self.sorter(g) for g in T.cluster_codes(d, True)],
                       "block": [self.sorter(g) for g in T.cluster_codes(d, False)]}
        self.n = len(d)

    @staticmethod
    def sorter(groups):
        order = np.argsort(groups, kind="mergesort")
        cuts = np.r_[0, np.flatnonzero(np.diff(groups[order])) + 1]
        return order, cuts

    def V(self, u, srt):
        """Same formula as 11_tests.clustered, with the sort done once."""
        order, cuts = srt
        sums = np.add.reduceat((self.Xh * u[:, None])[order], cuts, axis=0)
        G, N, K = len(sums), self.Xh.shape[0], self.Xh.shape[1]
        return G / (G - 1) * (N - 1) / (N - K) * self.B @ (sums.T @ sums) @ self.B

    def validate(self, y_raw):
        """Largest gap between the exact projection and the scored code's
        MAP demeaning of one invented outcome, relative to its spread."""
        a = self.P.apply(y_raw[:, None])[:, 0]
        m = T.demeaned(pd.DataFrame({"y": y_raw, **{c: self.d[c].values for c in self.fe}}), ["y"], self.fe)[:, 0]
        return float(np.abs(a - m).max() / m.std())

    def reject(self, Y_raw):
        """Y_raw: n x s invented outcomes. Returns two boolean arrays (two-way,
        block-only): the 95% interval of coefficient `coef` excludes zero."""
        Y = self.P.apply(Y_raw)
        b = self.B @ (self.Xh.T @ Y)
        k = self.coef
        r2, r1 = [], []
        for j in range(Y.shape[1]):
            u = Y[:, j] - self.X @ b[:, j]
            two = self.groups["two"]
            V2 = self.V(u, two[0]) + self.V(u, two[1]) - self.V(u, two[2])
            V1 = self.V(u, self.groups["block"][0])
            r2.append(abs(b[k, j]) > L.Z95 * np.sqrt(max(V2[k, k], 0.0)))
            r1.append(abs(b[k, j]) > L.Z95 * np.sqrt(V1[k, k]))
        return np.array(r2), np.array(r1)


def first_stage_F(d, fe, exog):
    raw = d[["cd", "qd"] + exog].to_numpy(dtype=float)
    M = T.demeaned(d, ["cd", "qd"] + exog, fe)
    M = M[:, T.keep(M, raw, 2)]
    fb, fse = T.tsls(M[:, 0], M[:, 1:], M[:, 1:], T.cluster_codes(d, True))
    return (fb[0] / fse[0]) ** 2


def build(df):
    tests = {}
    for t, w, exog in (("T1", "T1", ["floor_area", "post12dd"]), ("T2", "T2", ["floor_area"])):
        d = T.prepare(df, L.window(w))
        tests[t] = (Fixed(d, T.FE, ["cd"], ["qd"], exog, 0), {"F": first_stage_F(d, T.FE, exog)})
    d = T.prepare(df, L.window("T3_before") + L.window("T3_after"))
    d["after"] = (d["quarter"] >= L.T3_AFTER[0]).astype(int)
    for c in ("block_id", "flat_type", "storey_range", "flat_model"):
        d[c + "_a"] = d[c] + "#" + d["after"].astype(str)
    d["cd_a"], d["qd_a"], d["fa_a"] = d["cd"] * d["after"], d["qd"] * d["after"], d["floor_area"] * d["after"]
    fe3 = ["block_id_a", "lease_quarter", "flat_type_a", "storey_range_a", "flat_model_a"]
    F = {}
    for w in ("T3_before", "T3_after"):
        dw = T.prepare(df, L.window(w))
        F["F_" + w.split("_")[1]] = first_stage_F(dw, T.FE, ["floor_area"])
    tests["T3"] = (Fixed(d, fe3, ["cd", "cd_a"], ["qd", "qd_a"], ["floor_area", "fa_a"], 1), F)
    return tests


def simulate(fx, rng, spec, s):
    """s invented outcome columns: block effect + common quarterly shock +
    noise, true COE x distance slope zero; the stress specs add a quarterly
    shock to the distance slope."""
    d = fx.d
    _, bi = np.unique(d["block_id"].values, return_inverse=True)
    _, qi = np.unique(d["quarter"].values, return_inverse=True)
    nb, nq = bi.max() + 1, qi.max() + 1
    Y = rng.normal(0, 400, (nb, s))[bi] + rng.normal(0, 300, (nq, s))[qi] + rng.normal(0, 800, (fx.n, s))
    if spec != "main":
        g = rng.normal(0, 15, (nq, s))
        if spec == "stress_ar1":
            for i in range(1, nq):
                g[i] = 0.8 * g[i - 1] + np.sqrt(1 - 0.64) * g[i]
        Y = Y + g[qi] * d["dd_use"].values[:, None]
    return Y


# ------------------------------------------------------------ guard mode
# --guard compares candidate designs against a drift in the distance slope
# (THESIS section 6, stress cases). The fixed effects are the same in every
# design, so each invented outcome is projected once and reused; the designs
# differ only in their controls and their variance estimator:
#   S0  the scored model, two-way clustered (block, quarter)
#   G1  S0 + DD x linear quarter trend (T3: one trend per window)
#   G2  S0's model, Driscoll-Kraay standard errors, lags 3 and 8
#   G3  G1 with Driscoll-Kraay, lag 3
#   G4  S0 + town x year linear trends (sensitivity H; T3: per window)
# Driscoll-Kraay: quarter sums of the scores, Bartlett weights 1 - l/(L+1) on
# calendar-quarter lags (an excluded quarter is a zero), the same
# small-sample factor as clustering with quarters as the groups.
# Power: y = invented + beta * regressor. 2SLS on a design that contains the
# regressor returns exactly b0 + beta with unchanged residuals, so power at
# beta is read off the null draws (checked on the first batch by refitting).

VARIANCES = {"S0": ("base", "two"), "G1": ("trend", "two"), "G2_L3": ("base", "dk3"),
             "G2_L8": ("base", "dk8"), "G3": ("trend", "dk3"), "G4": ("town", "two")}


def qindex(quarters):
    return np.array([int(q[:4]) * 4 + int(q[5]) - 1 for q in quarters])


def add_controls(d, kind, t3):
    """Extra control columns for a design ('base', 'trend', 'town')."""
    if kind == "base":
        return []
    if kind == "trend":
        t = qindex(d["quarter"].values)
        d["ddt"] = d["dd_use"].values * (t - t.min()) / 4.0
        cols = ["ddt"]
    else:
        cols = T.town_trends(d)
    if t3:
        for c in list(cols):
            d[c + "_a"] = d[c] * d["after"]
            cols.append(c + "_a")
    return cols


class Variance:
    """Sorted groups for two-way clustering and calendar positions for
    Driscoll-Kraay, built once per frame."""

    def __init__(self, d):
        self.two = [Fixed.sorter(g) for g in T.cluster_codes(d, True)]
        qi = qindex(d["quarter"].values)
        self.qsort = Fixed.sorter(qi)
        uq = np.unique(qi)
        self.qpos = uq - uq.min()
        self.span = uq.max() - uq.min() + 1

    @staticmethod
    def crv(S, srt, B, N, K):
        order, cuts = srt
        sums = np.add.reduceat(S[order], cuts, axis=0)
        G = len(sums)
        return G / (G - 1) * (N - 1) / (N - K) * B @ (sums.T @ sums) @ B

    def V(self, Xh, u, B, kind):
        S = Xh * u[:, None]
        N, K = Xh.shape
        if kind == "two":
            return (self.crv(S, self.two[0], B, N, K) + self.crv(S, self.two[1], B, N, K)
                    - self.crv(S, self.two[2], B, N, K))
        lag = int(kind[2:])
        order, cuts = self.qsort
        h = np.zeros((self.span, K))
        h[self.qpos] = np.add.reduceat(S[order], cuts, axis=0)
        M = h.T @ h
        for l in range(1, lag + 1):
            G = h[l:].T @ h[:-l]
            M += (1 - l / (lag + 1)) * (G + G.T)
        Tn = len(self.qpos)
        return Tn / (Tn - 1) * (N - 1) / (N - K) * B @ M @ B


class GuardDesign:
    """One test's design under one set of controls: Xhat, B, and the
    first-stage pieces, all on the exactly projected columns."""

    def __init__(self, d, P, var, xcols, zcols, wcols, coef):
        cols = xcols + zcols + wcols
        raw = d[cols].to_numpy(dtype=float)
        M = P.apply(raw)
        kx, kz = len(xcols), len(zcols)
        M = M[:, T.keep(M, raw, kx + kz)]
        W = M[:, kx + kz:]
        self.X = np.column_stack([M[:, :kx], W])
        Z = np.column_stack([M[:, kx:kx + kz], W])
        self.Xh = Z @ np.linalg.solve(Z.T @ Z, Z.T @ self.X)
        self.B = np.linalg.inv(self.Xh.T @ self.Xh)
        self.coef, self.var = coef, var
        self.reg = M[:, coef]                         # the projected regressor of interest
        self.Z = Z

    def fit(self, Y, kinds):
        b = self.B @ (self.Xh.T @ Y)
        k = self.coef
        se = {v: np.empty(Y.shape[1]) for v in kinds}
        for j in range(Y.shape[1]):
            u = Y[:, j] - self.X @ b[:, j]
            for v in kinds:
                se[v][j] = np.sqrt(max(self.var.V(self.Xh, u, self.B, v)[k, k], 0.0))
        return b[k], se

    def first_stage_F(self, kind):
        """cd on the instrument(s) and controls (single-endogenous designs)."""
        X = self.Z
        B = np.linalg.inv(X.T @ X)
        pi = B @ (X.T @ self.X[:, 0])
        u = self.X[:, 0] - X @ pi
        V = self.var.V(X, u, B, kind)
        return pi[0] ** 2 / V[0, 0]


def guard_build(df):
    """Per test: frame, projector, variance helper, designs by control kind,
    and the first-stage F per design (T3: in each window separately)."""
    out = {}
    for t, w, exog in (("T1", "T1", ["floor_area", "post12dd"]), ("T2", "T2", ["floor_area"])):
        d = T.prepare(df, L.window(w))
        P, var = Projector(d, T.FE), Variance(d)
        des = {k: GuardDesign(d, P, var, ["cd"], ["qd"], exog + add_controls(d, k, False), 0)
               for k in ("base", "trend", "town")}
        F = {name: {"window": des[ck].first_stage_F(vk)} for name, (ck, vk) in VARIANCES.items()}
        out[t] = dict(d=d, P=P, des=des, F=F)
    d = T.prepare(df, L.window("T3_before") + L.window("T3_after"))
    d["after"] = (d["quarter"] >= L.T3_AFTER[0]).astype(int)
    for c in ("block_id", "flat_type", "storey_range", "flat_model"):
        d[c + "_a"] = d[c] + "#" + d["after"].astype(str)
    d["cd_a"], d["qd_a"], d["fa_a"] = d["cd"] * d["after"], d["qd"] * d["after"], d["floor_area"] * d["after"]
    fe3 = ["block_id_a", "lease_quarter", "flat_type_a", "storey_range_a", "flat_model_a"]
    P, var = Projector(d, fe3), Variance(d)
    des = {k: GuardDesign(d, P, var, ["cd", "cd_a"], ["qd", "qd_a"],
                          ["floor_area", "fa_a"] + add_controls(d, k, True), 1)
           for k in ("base", "trend", "town")}
    F = {name: {} for name in VARIANCES}
    for wname in ("before", "after"):
        dw = T.prepare(df, L.window("T3_" + wname))
        Pw, vw = Projector(dw, T.FE), Variance(dw)
        for ck in ("base", "trend", "town"):
            g = GuardDesign(dw, Pw, vw, ["cd"], ["qd"], ["floor_area"] + add_controls(dw, ck, False), 0)
            for name, (c2, vk) in VARIANCES.items():
                if c2 == ck:
                    F[name][wname] = g.first_stage_F(vk)
    out["T3"] = dict(d=d, P=P, des=des, F=F)
    return out


def guard_run(a, t0):
    tests = guard_build(design_frame(a.root))
    print(f"guard designs built ({time.time() - t0:.0f} s)", flush=True)
    rng = np.random.default_rng(L.BOOT_SEED)
    rows, draws = [], {}
    kinds = {}
    for name, (ck, vk) in VARIANCES.items():
        kinds.setdefault(ck, []).append(vk)
    for spec in ("main", "stress_iid", "stress_ar1"):
        for t, g in tests.items():
            fxlike = type("F", (), {"d": g["d"], "n": len(g["d"])})
            b = {ck: [] for ck in kinds}
            se = {name: [] for name in VARIANCES}
            for start in range(0, a.guard_sims, a.batch):
                s = min(a.batch, a.guard_sims - start)
                Yraw = simulate(fxlike, rng, spec, s)
                Y = g["P"].apply(Yraw)
                for ck, vks in kinds.items():
                    bk, sek = g["des"][ck].fit(Y, vks)
                    b[ck].append(bk)
                    for name, (c2, vk) in VARIANCES.items():
                        if c2 == ck:
                            se[name].append(sek[vk])
                if spec == "main" and start == 0:          # the power identity, checked by refitting
                    beta = 1e-3
                    reg = g["d"]["cd_a" if t == "T3" else "cd"].values
                    Y2 = g["P"].apply(Yraw[:, :2] + beta * reg[:, None])
                    for ck in kinds:
                        bb, _ = g["des"][ck].fit(Y2, [])
                        b0, _ = g["des"][ck].fit(Y[:, :2], [])
                        assert np.allclose(bb - b0, beta, rtol=1e-6, atol=1e-9), (t, ck, bb - b0)
                print(f"  {spec} {t}: {start + s}/{a.guard_sims} ({time.time() - t0:.0f} s)", flush=True)
            b = {ck: np.concatenate(v) for ck, v in b.items()}
            se = {name: np.concatenate(v) for name, v in se.items()}
            draws[(spec, t)] = (b, se)
            for name, (ck, vk) in VARIANCES.items():
                rows.append([spec, t, name, a.guard_sims, float(np.mean(np.abs(b[ck]) > L.Z95 * se[name]))])
            print(f"{spec} {t}: " + ", ".join(f"{r[2]} {r[4]:.3f}" for r in rows[-len(VARIANCES):])
                  + f" ({time.time() - t0:.0f} s)", flush=True)
    # power: the slope (paper's sign, negative) at which S0 rejects in 80% of null-design runs
    power = {}
    for t in tests:
        b, se = draws[("main", t)]
        rate = lambda beta, ck, name: float(np.mean(np.abs(b[ck] + beta) > L.Z95 * se[name]))
        lo, hi = 0.0, 10 * float(np.median(se["S0"]))
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if rate(-mid, "base", "S0") >= 0.80 else (mid, hi)
        beta = -hi
        power[t] = beta
        for name, (ck, vk) in VARIANCES.items():
            rows.append(["power", t, name, a.guard_sims, rate(beta, ck, name)])
    est = {}
    for t, g in tests.items():
        for name in VARIANCES:
            F = g["F"][name]
            est[(t, name)] = all(v >= L.F_MIN for v in F.values())
    L.write_csv(os.path.join(a.root, "out", "coverage_guard.csv"),
                ["scenario", "test", "design", "sims", "reject"], rows)
    R = {(r[0], r[1], r[2]): r[4] for r in rows}
    lines = ["Guard comparison: share of runs whose 95% interval excludes zero (" + f"{a.guard_sims:,} runs per cell).",
             "null = no slope shock; iid = independent quarterly slope shock, sd 15 per km; "
             "ar1 = persistent slope drift, AR(1) 0.8, sd 15 per km; power = at the slope where S0 rejects 80% "
             "of null-design runs.",
             "Power slopes (per km per S$ of premium): " + "; ".join(f"{t} {v:.3e}" for t, v in power.items())]
    for t in tests:
        lines.append(f"{t}:")
        for name in VARIANCES:
            F = tests[t]["F"][name]
            Fs = ", ".join(f"{k} {v:.1f}" for k, v in F.items())
            lines.append(f"  {name:<6} null {100 * R[('main', t, name)]:5.1f}%  iid {100 * R[('stress_iid', t, name)]:5.1f}%"
                         f"  ar1 {100 * R[('stress_ar1', t, name)]:5.1f}%  power {100 * R[('power', t, name)]:5.1f}%"
                         f"  first-stage F {Fs}  F gate passes: {'yes' if est[(t, name)] else 'no'}")
    lines.append("T3 estimable (cd x AFTER identified, F >= 10 in both windows): "
                 + "; ".join(f"{n} {'yes' if est[('T3', n)] else 'no'}" for n in VARIANCES))
    L.write_text(os.path.join(a.root, "out", "coverage_guard.txt"), "\n".join(lines) + "\n")
    print("\n".join(lines))


# ----------------------------------------------------------- guard2 mode
# --guard2 (round 2, 11 October 2026): against a persistent drift in the
# distance slope, compare
#   S0     the scored model, two-way clustered (block, quarter), normal cv
#   A      S0's model, two-way clustered by block AND 8-quarter time block
#          (blocks counted from each window's first quarter), cv from
#          t(G-1), G = number of time blocks. If the two-way variance is
#          not positive, the larger one-way variance is used.
#   B_lev  two-step: (1) the distance gradient g_q of every quarter, from
#          the scored fixed effects and controls with DD x quarter dummies
#          (one base quarter per window, g = 0 there); (2) g_q on the COE
#          premium instrumented by the quota, quarter level, with a
#          constant (T1: + POST12; T3: + AFTER and premium x AFTER,
#          instrumented by quota x AFTER), Newey-West Bartlett lag 4,
#          fixed-b critical value (Kiefer-Vogelsang polynomial, b = 5/T;
#          checked against a simulation of the fixed-b limit)
#   B_fd   the same in first differences of consecutive quarters within a
#          window (a constant is kept: a linear drift in levels)
# Scenarios: null; iid slope shock sd 15 per km; AR(0.8) drift, innovation
# sd 9 (stationary sd 15, round 1); and the dose-response, AR(0.8) with
# innovation sd 5, 10, 15. Power is read at the slope where S0 rejects 80%
# of null-design runs (the identity used in --guard holds for every design:
# the regressor's coefficient shifts by exactly the slope; checked by refit).
# Each test runs in its own process (--test), seed [20261006, test number];
# --guard2-merge writes out/coverage_guard2.csv and .txt.

from scipy import stats as _st

G2_SPECS = [("null", None), ("iid15", None), ("ar1_i9", 9.0), ("ar1_i5", 5.0), ("ar1_i10", 10.0), ("ar1_i15", 15.0)]
G2_DESIGNS = ["S0", "A", "B_lev", "B_fd"]
NW_LAG = 4


def fixed_b_cv(T, lag=NW_LAG):
    b = (lag + 1) / T
    return L.Z95 + 2.9694 * b + 0.4160 * b ** 2 - 0.5324 * b ** 3


def simulate2(d, rng, spec, s):
    _, bi = np.unique(d["block_id"].values, return_inverse=True)
    _, qi = np.unique(d["quarter"].values, return_inverse=True)
    nb, nq = bi.max() + 1, qi.max() + 1
    Y = rng.normal(0, 400, (nb, s))[bi] + rng.normal(0, 300, (nq, s))[qi] + rng.normal(0, 800, (len(d), s))
    if spec == "null":
        return Y
    if spec == "iid15":
        g = rng.normal(0, 15, (nq, s))
    else:
        inn = dict(G2_SPECS)[spec]
        e = rng.normal(0, inn, (nq, s))
        g = np.empty((nq, s))
        g[0] = e[0] / np.sqrt(1 - 0.64)
        for i in range(1, nq):
            g[i] = 0.8 * g[i - 1] + e[i]
    return Y + g[qi] * d["dd_use"].values[:, None]


def time_blocks(d, windows):
    """8-quarter blocks counted from each window's first quarter."""
    qi = qindex(d["quarter"].values)
    tb = np.full(len(d), -1)
    for w, qs in enumerate(windows):
        q0 = qindex([qs[0]])[0]
        inw = np.isin(d["quarter"].values, qs)
        tb[inw] = w * 1000 + (qi[inw] - q0) // 8
    assert (tb >= 0).all()
    return tb


class Variance2(Variance):
    def __init__(self, d, tb):
        super().__init__(d)
        b = T.gcode(d, "block_id")
        bt = pd.factorize(pd.Series(b).astype(str) + "#" + pd.Series(tb).astype(str))[0]
        self.tbs = [Fixed.sorter(b), Fixed.sorter(pd.factorize(tb)[0]), Fixed.sorter(bt)]
        self.G_tb = len(np.unique(tb))

    def V(self, Xh, u, B, kind):
        if kind != "tb":
            return super().V(Xh, u, B, kind)
        S = Xh * u[:, None]
        N, K = Xh.shape
        Vb, Vt, Vbt = (self.crv(S, s, B, N, K) for s in self.tbs)
        V = Vb + Vt - Vbt
        bad = np.diag(V) <= 0
        if bad.any():
            alt = np.maximum(np.diag(Vb), np.diag(Vt))
            V = V.copy()
            V[np.diag_indices_from(V)] = np.where(bad, alt, np.diag(V))
        return V


def nw(Xh, u, B, lag=NW_LAG):
    s = Xh * u[:, None]
    M = s.T @ s
    for l in range(1, lag + 1):
        G = s[l:].T @ s[:-l]
        M += (1 - l / (lag + 1)) * (G + G.T)
    return B @ M @ B


class TwoStep:
    """Step 1 is linear in y: g = A y, A computed once. Step 2 is a
    quarter-level 2SLS whose design does not depend on y."""

    def __init__(self, d, P, windows, t3):
        q = d["quarter"].values
        allq = [qq for w in windows for qq in w if qq in set(q)]
        base = [next(qq for qq in w if qq in set(q)) for w in windows]
        free = [qq for qq in allq if qq not in base]
        dd = d["dd_use"].values
        cols = [dd * (q == qq) for qq in free]
        W = ["floor_area"] + (["fa_a"] if t3 else [])
        raw = np.column_stack(cols + [d[c].values.astype(float) for c in W])
        M = P.apply(raw)
        self.A = np.linalg.solve(M.T @ M, M.T)[:len(free)]
        self.allq, self.free = allq, free
        qt = d.groupby("quarter")[["coep", "coeq"]].first().loc[allq]
        self.coep, self.coeq = qt["coep"].values, qt["coeq"].values
        self.win = np.concatenate([[w] * sum(1 for qq in ws if qq in set(q)) for w, ws in enumerate(windows)])
        self.post12 = (np.array(allq) >= L.POST12_FIRST).astype(float)
        self.t3 = t3
        self.post = (not t3) and self.post12.min() == 0 and self.post12.max() == 1
        self.lev = self.design(False)
        self.fd = self.design(True)

    def frame(self, fd):
        """(rows to keep, X, Z, coefficient index) for step 2."""
        c, z, aft = self.coep, self.coeq, (self.win == 1).astype(float)
        one = np.ones(len(c))
        if self.t3:
            X = np.column_stack([one, aft, c, c * aft])
            Z = np.column_stack([one, aft, z, z * aft])
            k = 3
        else:
            X = np.column_stack([one, c] + ([self.post12] if self.post else []))
            Z = np.column_stack([one, z] + ([self.post12] if self.post else []))
            k = 1
        if not fd:
            return None, X, Z, k
        same = self.win[1:] == self.win[:-1]
        D = lambda A: (A[1:] - A[:-1])[same]
        Xd, Zd = D(X), D(Z)
        Xd[:, 0] = 1.0
        Zd[:, 0] = 1.0
        if self.t3:
            Xd[:, 1] = Zd[:, 1] = aft[1:][same]
        return same, Xd, Zd, k

    def design(self, fd):
        same, X, Z, k = self.frame(fd)
        Xh = Z @ np.linalg.solve(Z.T @ Z, Z.T @ X)
        B = np.linalg.inv(Xh.T @ Xh)
        return dict(same=same, X=X, Z=Z, Xh=Xh, B=B, k=k, cv=fixed_b_cv(len(X)))

    def gradients(self, Y):
        G = np.zeros((len(self.allq), Y.shape[1]))
        idx = [self.allq.index(qq) for qq in self.free]
        G[idx] = self.A @ Y
        return G

    def fit(self, Y, fd):
        g = self.gradients(Y)
        D = self.fd if fd else self.lev
        if fd:
            g = (g[1:] - g[:-1])[D["same"]]
        b = D["B"] @ (D["Xh"].T @ g)
        se = np.empty(g.shape[1])
        for j in range(g.shape[1]):
            u = g[:, j] - D["X"] @ b[:, j]
            se[j] = np.sqrt(max(nw(D["Xh"], u, D["B"])[D["k"], D["k"]], 0.0))
        return b[D["k"]], se, D["cv"]

    def first_stage_F(self, fd):
        """Premium (or its change) on quota (or its change), each window
        separately, NW lag 4: list of F."""
        out = []
        for w in np.unique(self.win):
            m = self.win == w
            c, z = self.coep[m], self.coeq[m]
            if fd:
                c, z = np.diff(c), np.diff(z)
            X = np.column_stack([np.ones(len(c)), z])
            if self.post and not fd:
                X = np.column_stack([X, self.post12[m]])
            if self.post and fd:
                X = np.column_stack([X, np.diff(self.post12[m])])
            B = np.linalg.inv(X.T @ X)
            pi = B @ (X.T @ c)
            V = nw(X, c - X @ pi, B)
            out.append(pi[1] ** 2 / V[1, 1])
        return out


def guard2_build(df, t):
    if t in ("T1", "T2"):
        d = T.prepare(df, L.window(t))
        exog = ["floor_area"] + (["post12dd"] if t == "T1" else [])
        windows = [L.window(t)]
        P = Projector(d, T.FE)
        var = Variance2(d, time_blocks(d, windows))
        s0 = GuardDesign(d, P, var, ["cd"], ["qd"], exog, 0)
        two = TwoStep(d, P, windows, False)
        F = {"S0": [s0.first_stage_F("two")], "A": [s0.first_stage_F("tb")],
             "B_lev": two.first_stage_F(False), "B_fd": two.first_stage_F(True)}
        G = {"A": [var.G_tb]}
        return dict(d=d, P=P, s0=s0, two=two, F=F, G=G, reg="cd")
    windows = [L.window("T3_before"), L.window("T3_after")]
    d = T.prepare(df, windows[0] + windows[1])
    d["after"] = (d["quarter"] >= L.T3_AFTER[0]).astype(int)
    for c in ("block_id", "flat_type", "storey_range", "flat_model"):
        d[c + "_a"] = d[c] + "#" + d["after"].astype(str)
    d["cd_a"], d["qd_a"], d["fa_a"] = d["cd"] * d["after"], d["qd"] * d["after"], d["floor_area"] * d["after"]
    fe3 = ["block_id_a", "lease_quarter", "flat_type_a", "storey_range_a", "flat_model_a"]
    P = Projector(d, fe3)
    var = Variance2(d, time_blocks(d, windows))
    s0 = GuardDesign(d, P, var, ["cd", "cd_a"], ["qd", "qd_a"], ["floor_area", "fa_a"], 1)
    two = TwoStep(d, P, windows, True)
    F = {"S0": [], "A": []}
    G = {"A": []}
    for w in windows:
        dw = T.prepare(df, w)
        vw = Variance2(dw, time_blocks(dw, [w]))
        g = GuardDesign(dw, Projector(dw, T.FE), vw, ["cd"], ["qd"], ["floor_area"], 0)
        F["S0"].append(g.first_stage_F("two"))
        F["A"].append(g.first_stage_F("tb"))
        G["A"].append(vw.G_tb)
    F["B_lev"], F["B_fd"] = two.first_stage_F(False), two.first_stage_F(True)
    G["A_pooled"] = [var.G_tb]
    return dict(d=d, P=P, s0=s0, two=two, F=F, G=G, reg="cd_a")


def guard2_run(a, t0):
    t = a.test
    g = guard2_build(design_frame(a.root), t)
    d, s0, two = g["d"], g["s0"], g["two"]
    cvA = float(_st.t.ppf(0.975, (g["G"]["A_pooled"][0] if t == "T3" else g["G"]["A"][0]) - 1))
    print(f"{t}: built ({time.time() - t0:.0f} s); A: G {g['G']}, cv {cvA:.3f}; "
          f"B cv levels {two.lev['cv']:.3f}, fd {two.fd['cv']:.3f}", flush=True)
    rng = np.random.default_rng([L.BOOT_SEED, ["T1", "T2", "T3"].index(t)])
    res = {}
    for spec, _ in G2_SPECS:
        acc = {k: [] for k in ("b0", "se_two", "se_tb", "bl", "sel", "bf", "sef")}
        for start in range(0, a.guard_sims, a.batch):
            s = min(a.batch, a.guard_sims - start)
            Yraw = simulate2(d, rng, spec, s)
            Y = g["P"].apply(Yraw)
            b, se = s0.fit(Y, ["two", "tb"])
            bl, sel, _ = two.fit(Y, False)
            bf, sef, _ = two.fit(Y, True)
            for k, v in (("b0", b), ("se_two", se["two"]), ("se_tb", se["tb"]), ("bl", bl), ("sel", sel),
                         ("bf", bf), ("sef", sef)):
                acc[k].append(v)
            if spec == "null" and start == 0:
                beta = 1e-3
                Y2 = g["P"].apply(Yraw[:, :2] + beta * d[g["reg"]].values[:, None])
                for f in (lambda Z: s0.fit(Z, [])[0], lambda Z: two.fit(Z, False)[0], lambda Z: two.fit(Z, True)[0]):
                    assert np.allclose(f(Y2) - f(Y[:, :2]), beta, rtol=1e-6, atol=1e-9), t
            print(f"  {spec} {t}: {start + s}/{a.guard_sims} ({time.time() - t0:.0f} s)", flush=True)
        acc = {k: np.concatenate(v) for k, v in acc.items()}
        res[spec] = {"S0": (acc["b0"], acc["se_two"], L.Z95), "A": (acc["b0"], acc["se_tb"], cvA),
                     "B_lev": (acc["bl"], acc["sel"], two.lev["cv"]), "B_fd": (acc["bf"], acc["sef"], two.fd["cv"])}
        print(f"{spec} {t}: " + ", ".join(f"{k} {np.mean(np.abs(b) > c * se):.3f}" for k, (b, se, c) in res[spec].items())
              + f" ({time.time() - t0:.0f} s)", flush=True)
    rate = lambda beta, k: float(np.mean(np.abs(res["null"][k][0] + beta) > res["null"][k][2] * res["null"][k][1]))
    lo, hi = 0.0, 10 * float(np.median(res["null"]["S0"][1]))
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if rate(-mid, "S0") >= 0.80 else (mid, hi)
    beta = -hi
    qt = d.groupby("quarter")["coep"].first()
    rows = []
    for k in G2_DESIGNS:
        for spec, _ in G2_SPECS:
            b, se, c = res[spec][k]
            rows.append([t, k, spec, a.guard_sims, float(np.mean(np.abs(b) > c * se))])
        rows.append([t, k, "power", a.guard_sims, rate(beta, k)])
        rows.append([t, k, "F_min", "", min(g["F"][k])])
        for i, f in enumerate(g["F"][k]):
            rows.append([t, k, f"F_{i}", "", f])
    rows.append([t, "all", "power_slope", "", beta])
    rows.append([t, "all", "coep_sd", "", float(qt.std())])
    for k, v in g["G"].items():
        for i, x in enumerate(v):
            rows.append([t, k, f"G_{i}", "", x])
    L.write_csv(os.path.join(a.root, "out", f"coverage_guard2_{t}.part.csv"),
                ["test", "design", "item", "sims", "value"], rows)
    print(f"{t} done ({time.time() - t0:.0f} s)", flush=True)


def guard2_merge(a):
    rows = []
    for t in ("T1", "T2", "T3"):
        rows += L.read_csv(os.path.join(a.root, "out", f"coverage_guard2_{t}.part.csv"))
    L.write_csv(os.path.join(a.root, "out", "coverage_guard2.csv"), ["test", "design", "item", "sims", "value"],
                [[r["test"], r["design"], r["item"], r["sims"], r["value"]] for r in rows])
    V = {(r["test"], r["design"], r["item"]): float(r["value"]) for r in rows}
    sims = next(r["sims"] for r in rows if r["sims"])
    lines = [f"Guard round 2: share of runs whose 95% interval excludes zero ({int(sims):,} runs per cell).",
             "iid15 = independent quarterly slope shock, sd 15 per km; ar1_iN = AR(0.8) drift in the distance "
             "slope with innovation sd N per km (ar1_i9 is round 1's case, stationary sd 15).",
             "F: first-stage F under the design's own variance (S0, A: each window; B: quarter level, each window; "
             "B_fd: on the quota's change). Gate: F >= 10 in every window."]
    for t in ("T1", "T2", "T3"):
        beta, sd = V[(t, "all", "power_slope")], V[(t, "all", "coep_sd")]
        lines.append(f"{t}: power slope {beta:.3e} per km per S$ of premium; times the premium's quarterly sd "
                     f"(S${sd:,.0f}) = {abs(beta) * sd:.2f} S$ per sqm per km")
        for k in G2_DESIGNS:
            Fs = [V[x] for x in sorted(V) if x[0] == t and x[1] == k and x[2].startswith("F_") and x[2] != "F_min"]
            Gs = [int(V[x]) for x in sorted(V) if x[0] == t and x[1].startswith(k) and x[2].startswith("G_")]
            gate = all(f >= L.F_MIN for f in Fs)
            lines.append(f"  {k:<5} null {100 * V[(t, k, 'null')]:5.1f}%  iid {100 * V[(t, k, 'iid15')]:5.1f}%  "
                         f"ar1 i9 {100 * V[(t, k, 'ar1_i9')]:5.1f}%  [i5 {100 * V[(t, k, 'ar1_i5')]:4.1f} "
                         f"i10 {100 * V[(t, k, 'ar1_i10')]:4.1f} i15 {100 * V[(t, k, 'ar1_i15')]:4.1f}]  "
                         f"power {100 * V[(t, k, 'power')]:5.1f}%  F {'/'.join(f'{f:.1f}' for f in Fs)} "
                         f"gate {'passes' if gate else 'FIRES'}" + (f"  G {Gs}" if Gs else ""))
    L.write_text(os.path.join(a.root, "out", "coverage_guard2.txt"), "\n".join(lines) + "\n")
    for t in ("T1", "T2", "T3"):
        os.remove(os.path.join(a.root, "out", f"coverage_guard2_{t}.part.csv"))
    print("\n".join(lines))


def main():
    a = L.args("cargradient pre-seal placebo coverage check.",
               lambda p: (p.add_argument("--sims", type=int, default=200),
                          p.add_argument("--sims-t3", type=int, default=100),
                          p.add_argument("--stress-sims", type=int, default=100),
                          p.add_argument("--batch", type=int, default=25),
                          p.add_argument("--guard", action="store_true"),
                          p.add_argument("--guard-sims", type=int, default=1000),
                          p.add_argument("--guard2", action="store_true"),
                          p.add_argument("--guard2-merge", action="store_true"),
                          p.add_argument("--test", choices=["T1", "T2", "T3"])))
    t0 = time.time()
    if a.guard:
        guard_run(a, t0)
        return
    if a.guard2:
        guard2_run(a, t0)
        return
    if a.guard2_merge:
        guard2_merge(a)
        return
    df = design_frame(a.root)
    tests = build(df)
    print(f"design built in {time.time() - t0:.0f} s", flush=True)
    rows, lines = [], []
    rng = np.random.default_rng(L.BOOT_SEED)
    check = {}
    for t, (fx, F) in tests.items():
        check[t] = fx.validate(simulate(fx, rng, "main", 1)[:, 0])
        print(f"{t}: exact projection vs MAP, max gap {check[t]:.1e} of the outcome's spread; "
              f"{fx.P.rank_drop} redundant fixed-effect directions ({time.time() - t0:.0f} s)", flush=True)
    for spec in ("main", "stress_iid", "stress_ar1"):
        for t, (fx, F) in tests.items():
            n = (a.sims_t3 if t == "T3" else a.sims) if spec == "main" else a.stress_sims
            rej2 = rej1 = 0
            for start in range(0, n, a.batch):
                s = min(a.batch, n - start)
                r2, r1 = fx.reject(simulate(fx, rng, spec, s))
                rej2 += int(r2.sum())
                rej1 += int(r1.sum())
                print(f"  {spec} {t}: {start + s}/{n} ({time.time() - t0:.0f} s)", flush=True)
            rows.append((spec, t, n, rej2 / n, rej1 / n, fx.n))
            print(f"{spec} {t}: sims {n}, rejected two-way {rej2 / n:.3f}, block-only {rej1 / n:.3f} "
                  f"({time.time() - t0:.0f} s)", flush=True)
    main_rows = [r for r in rows if r[0] == "main"]
    ok = all(0.02 <= r[3] <= 0.09 for r in main_rows)
    Fs = {f"{t}_{k}": v for t, (_, F) in tests.items() for k, v in F.items()}
    L.write_csv(os.path.join(a.root, "out", "coverage_check.csv"),
                ["spec", "test", "sims", "reject_twoway", "reject_block_only", "sales"], rows)
    lines.append(f"PASS line: two-way rejection between 2% and 9% for each test (main spec): {'PASS' if ok else 'FAIL'}")
    for r in rows:
        lines.append(f"{r[0]:<11} {r[1]}: {r[2]} simulations, sales {r[5]}; 95% interval excluded zero in "
                     f"{100 * r[3]:.1f}% two-way, {100 * r[4]:.1f}% block-only")
    lines.append("Exact fixed-effects projection of the invented prices vs the scored code's MAP demeaning, "
                 "largest gap relative to the outcome's spread: " + "; ".join(f"{t} {v:.1e}" for t, v in check.items()))
    lines.append("First-stage F (two-way), the same in every simulation (it does not depend on prices): "
                 + "; ".join(f"{k} {v:.1f}" for k, v in Fs.items()))
    lines.append("F gate fires (F < 10): " + "; ".join(f"{k} {'yes' if v < L.F_MIN else 'no'}" for k, v in Fs.items()))
    L.write_text(os.path.join(a.root, "out", "coverage_check.txt"), "\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
