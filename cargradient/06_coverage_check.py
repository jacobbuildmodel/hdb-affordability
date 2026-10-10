#!/usr/bin/env python3
"""
06_coverage_check.py -- pre-seal placebo check of the scored intervals
(THESIS section 6). Run from the repository root:

  PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py \
      [--sims N] [--sims-t3 N] [--stress-sims N] [--batch N]

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


def main():
    a = L.args("cargradient pre-seal placebo coverage check.",
               lambda p: (p.add_argument("--sims", type=int, default=200),
                          p.add_argument("--sims-t3", type=int, default=100),
                          p.add_argument("--stress-sims", type=int, default=100),
                          p.add_argument("--batch", type=int, default=25)))
    t0 = time.time()
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
