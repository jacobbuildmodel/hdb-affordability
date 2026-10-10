#!/usr/bin/env python3
"""
15_reproduce.py -- a second, independent route to every scored number and
outcome (T1, T2, T3, both gates). Fails (exit 1) on any difference from
ROOT/out/tests.csv.

  python3 cargradient/15_reproduce.py [--root DIR]

Different from 10 and 11 on purpose:
- raw files are read with the csv and json modules, not pandas;
- the COE premium and quota, the windows, the lease bands and the geocode
  shares are rebuilt here from raw/ and the pre-seal inputs;
- fixed effects are swept out by a hand-written alternating-projections loop
  in numpy (np.bincount group means), not pyfixest;
- 2SLS, the two-way clustered variance (block and quarter, as scored) and
  the first-stage F are written out again.

Tolerance: estimates and standard errors agree to 1e-6 relative (absolute
1e-12 near zero); outcomes, gate flags and sample sizes agree exactly.
Refuses the real cargradient/raw/ before the seal (cglib.guard).
"""
import csv
import json
import math
import os
import sys

import numpy as np

import cglib as L

MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def qlabel(month):
    return "%sQ%d" % (month[:4], (int(month[5:7]) + 2) // 3)


def coe(raw):
    def series(n):
        d = json.load(open(os.path.join(raw, "singstat_M651121", "s%d.json" % n)))
        out = {}
        for c in d["Data"]["row"][0]["columns"]:
            try:
                y, m = c["key"].split()
                out["%s-%02d" % (y, MON[m])] = float(c["value"])
            except (ValueError, KeyError):
                continue
        return out
    acc = {}
    for b in (1, 2):
        pa, sa, qa = (series(n) for n in L.COE_SERIES[("A", b)])
        pb, sb, qb = (series(n) for n in L.COE_SERIES[("B", b)])
        for m in pa:
            if m in sa and m in pb and m in sb and m in qa and m in qb and sa[m] + sb[m] > 0:
                acc.setdefault(qlabel(m), []).append(
                    ((pa[m] * sa[m] + pb[m] * sb[m]) / (sa[m] + sb[m]), qa[m] + qb[m]))
    return {q: (sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v)) for q, v in acc.items()}


def rows(root):
    raw = L.guard(os.path.join(root, "raw"))
    prem = coe(raw)
    dist = {}
    with open(os.path.join(root, "out", "block_distance.csv")) as f:
        for r in csv.DictReader(f):
            if r["match_type"] in ("exact", "expanded"):
                dist[(r["block"], r["street_name"])] = float(r["km_raffles_mean"])
    out = []
    for fid in L.RESALE:
        with open(os.path.join(raw, "resale", fid + ".csv"), newline="") as f:
            for r in csv.DictReader(f):
                q = qlabel(r["month"])
                if not (L.T1_FIRST <= q <= L.T2_LAST):
                    continue
                blk = (r["block"].strip().upper(), r["street_name"].strip().upper())
                ft = r["flat_type"].strip().upper().replace("MULTI GENERATION", "MULTI-GENERATION")
                area = float(r["floor_area_sqm"])
                rem = L.LEASE_YEARS - (int(r["month"][:4]) - int(r["lease_commence_date"]))
                out.append({"q": q, "blk": "|".join(blk), "dd": dist.get(blk), "ft": ft,
                            "st": r["storey_range"].strip().upper(), "fm": r["flat_model"].strip().upper(),
                            "area": area, "band": (rem // L.LEASE_BAND) * L.LEASE_BAND,
                            "y": float(r["resale_price"]) / area,
                            "coep": prem.get(q, (None, None))[0], "coeq": prem.get(q, (None, None))[1]})
    return out


def ids(values):
    m = {}
    return np.array([m.setdefault(v, len(m)) for v in values], dtype=np.int64)


def sweep(X, groups, tol=1e-12, maxit=200000):
    """Alternating projections: subtract group means for each factor in turn
    until no column moves by more than tol (columns scaled to unit sd)."""
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    Y = X / sd
    counts = [np.bincount(g).astype(float) for g in groups]
    for _ in range(maxit):
        old = Y.copy()
        for g, c in zip(groups, counts):
            for j in range(Y.shape[1]):
                Y[:, j] -= (np.bincount(g, weights=Y[:, j]) / c)[g]
        if np.max(np.abs(Y - old)) < tol:
            return Y * sd
    raise RuntimeError("sweep did not converge")


def keep(M, raw, first):
    s, r = M.std(axis=0), raw.std(axis=0)
    r[r == 0] = 1.0
    ok = s >= 1e-8 * r
    if not ok[:first].all():
        raise RuntimeError("regressor absorbed")
    return [i for i in range(M.shape[1]) if i < first or ok[i]]


def cov(S, A, cl, N, K):
    order = np.argsort(cl, kind="stable")
    bounds = np.r_[0, np.flatnonzero(np.diff(cl[order])) + 1]
    G = len(bounds)
    meat = np.zeros((S.shape[1], S.shape[1]))
    for i, start in enumerate(bounds):
        stop = bounds[i + 1] if i + 1 < G else len(order)
        v = S[order[start:stop]].sum(axis=0)
        meat += np.outer(v, v)
    return (G / (G - 1)) * ((N - 1) / (N - K)) * A @ meat @ A


def iv(y, X, Z, cl, cl_q=None, cl_bq=None):
    """2SLS with one-way (cl) or, given cl_q and cl_bq, two-way clustering."""
    PZX = Z @ np.linalg.lstsq(Z, X, rcond=None)[0]
    A = np.linalg.inv(PZX.T @ PZX)
    b = A @ PZX.T @ y
    e = y - X @ b
    S = PZX * e[:, None]
    N, K = X.shape
    V = cov(S, A, cl, N, K)
    if cl_q is not None:
        V = V + cov(S, A, cl_q, N, K) - cov(S, A, cl_bq, N, K)
    return b, np.sqrt(np.maximum(np.diag(V), 0.0))


def sample(data, quarters):
    qs = set(quarters)
    return [r for r in data if r["q"] in qs and r["dd"] is not None and r["coep"] is not None]


def design(s, extra_after=False, post12=False):
    after = np.array([1.0 if r["q"] >= L.T3_AFTER[0] else 0.0 for r in s])
    dd = np.array([r["dd"] for r in s])
    cd = np.array([r["coep"] for r in s]) * dd
    qd = np.array([r["coeq"] for r in s]) * dd
    area = np.array([r["area"] for r in s])
    y = np.array([r["y"] for r in s])
    sfx = (lambda r, a: "%s#%d" % (r, a)) if extra_after else (lambda r, a: r)
    groups = [ids([sfx(r["blk"], a) for r, a in zip(s, after)]),
              ids(["%d|%s" % (r["band"], r["q"]) for r in s]),
              ids([sfx(r["ft"], a) for r, a in zip(s, after)]),
              ids([sfx(r["st"], a) for r, a in zip(s, after)]),
              ids([sfx(r["fm"], a) for r, a in zip(s, after)])]
    cl = ids([r["blk"] for r in s])
    cl2 = (ids([r["q"] for r in s]), ids([r["blk"] + "#" + r["q"] for r in s]))
    return y, cd, qd, area, after, dd, groups, (cl, cl2)


def single(data, quarters, post12):
    s = sample(data, quarters)
    y, cd, qd, area, after, dd, groups, (cl, cl2) = design(s)
    cols = [y, cd, qd, area]
    if post12:
        cols.append(np.array([1.0 if r["q"] >= L.POST12_FIRST else 0.0 for r in s]) * dd)
    raw = np.column_stack(cols)
    M = sweep(raw, groups)
    M = M[:, keep(M, raw, 3)]
    W = M[:, 3:]
    b, se = iv(M[:, 0], np.column_stack([M[:, 1], W]), np.column_stack([M[:, 2], W]), cl, *cl2)
    fb, fse = iv(M[:, 1], np.column_stack([M[:, 2], W]), np.column_stack([M[:, 2], W]), cl, *cl2)
    return {"est": b[0], "se": se[0], "lo": b[0] - L.Z95 * se[0], "hi": b[0] + L.Z95 * se[0],
            "F": (fb[0] / fse[0]) ** 2, "n": len(s)}


def first_stage_F(data, quarters):
    s = sample(data, quarters)
    y, cd, qd, area, after, dd, groups, (cl, cl2) = design(s)
    raw = np.column_stack([cd, qd, area])
    M = sweep(raw, groups)
    M = M[:, keep(M, raw, 2)]
    fb, fse = iv(M[:, 0], M[:, 1:], M[:, 1:], cl, *cl2)
    return (fb[0] / fse[0]) ** 2


def t3(data):
    s = sample(data, L.window("T3_before") + L.window("T3_after"))
    y, cd, qd, area, after, dd, groups, (cl, cl2) = design(s, extra_after=True)
    raw = np.column_stack([y, cd, cd * after, qd, qd * after, area, area * after])
    M = sweep(raw, groups)
    M = M[:, keep(M, raw, 5)]
    W = M[:, 5:]
    b, se = iv(M[:, 0], np.column_stack([M[:, 1], M[:, 2], W]), np.column_stack([M[:, 3], M[:, 4], W]), cl, *cl2)
    return {"before_est": b[0], "before_se": se[0], "before_hi": b[0] + L.Z95 * se[0],
            "diff_est": b[1], "diff_se": se[1], "diff_lo": b[1] - L.Z95 * se[1],
            "diff_hi": b[1] + L.Z95 * se[1], "n": len(s),
            "F_before": first_stage_F(data, L.window("T3_before")),
            "F_after": first_stage_F(data, L.window("T3_after"))}


def geo_share(root, data_all):
    raw = os.path.join(root, "raw")
    matched = set()
    with open(os.path.join(root, "out", "blocks_geocoded.csv")) as f:
        for r in csv.DictReader(f):
            if r["match_type"] in ("exact", "expanded"):
                matched.add(r["block"] + "|" + r["street_name"])
    out = {}
    for w in ("T1", "T2", "T3_before", "T3_after"):
        qs = set(L.window(w))
        s = [r for r in data_all if r["q"] in qs]
        out[w] = sum(1 for r in s if r["blk"] in matched) / len(s) if s else 0.0
    return out


def main():
    a = L.args("cargradient independent reproduction of T1-T3.")
    root = a.root
    data = rows(root)
    geo = geo_share(root, data)
    mine = {}
    for t, w, post in (("T1", "T1", True), ("T2", "T2", False)):
        r = single(data, L.window(w), post)
        ok = geo[w] >= L.GEO_MIN and r["F"] >= L.F_MIN
        mine.update({f"{t}_{k}": v for k, v in r.items()})
        mine[f"{t}_geo_share"] = geo[w]
        mine[f"{t}_outcome"] = L.outcome_sign_test(r["est"], r["lo"], r["hi"], ok)
    r = t3(data)
    ok = (geo["T3_before"] >= L.GEO_MIN and geo["T3_after"] >= L.GEO_MIN
          and r["F_before"] >= L.F_MIN and r["F_after"] >= L.F_MIN)
    mine.update({f"T3_{k}": v for k, v in r.items()})
    mine["T3_outcome"] = L.outcome_t3(r["diff_est"], r["diff_lo"], r["diff_hi"], r["before_hi"], ok)

    theirs = {row["key"]: row["value"] for row in L.read_csv(os.path.join(root, "out", "tests.csv"))}
    bad = []
    for k, v in sorted(mine.items()):
        if k not in theirs:
            bad.append(f"{k}: missing from tests.csv")
            continue
        t = theirs[k]
        if isinstance(v, str):
            if v != t:
                bad.append(f"{k}: {v} vs {t}")
        elif k.endswith("_n"):
            if int(v) != int(float(t)):
                bad.append(f"{k}: {v} vs {t}")
        else:
            tv = float(t)
            if abs(v - tv) > max(1e-12, 1e-6 * max(abs(v), abs(tv))):
                bad.append(f"{k}: {v!r} vs {t}")
    lines = [f"compared {len(mine)} numbers and outcomes; differences {len(bad)}"] + bad
    L.write_text(os.path.join(root, "out", "reproduce.txt"), "\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
