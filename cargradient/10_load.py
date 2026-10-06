#!/usr/bin/env python3
"""
10_load.py -- build the analysis panel (THESIS sections 3 to 5).

  python3 cargradient/10_load.py [--root DIR]

Refuses the real cargradient/raw/ until cargradient/SEALED exists (guard).

Reads:
  ROOT/raw/resale/<id>.csv               the five HDB resale files
  ROOT/raw/singstat_M651121/s<n>.json    COE premium, successful bids, quota
  ROOT/raw/lta_mrt_station_exit.geojson  MRT exits (sensitivity I)
  ROOT/out/blocks_geocoded.csv           OneMap points (pre-seal)
  ROOT/out/block_distance.csv            km to Raffles Place and City Hall (pre-seal)
  ROOT/out/street_points.csv             street points for unmatched pairs (pre-seal)
Writes:
  ROOT/out/coe_quarterly.csv   quarter, COE premium (A and B, each bidding
                               weighted by successful bids, then the mean of
                               the quarter's biddings), quota (A plus B per
                               bidding, mean of the quarter's biddings)
  ROOT/out/geocode_coverage.csv  per window: sales, sales on a geocoded block
  ROOT/out/panel.csv.gz        one row per sale from 2002Q2 to 2026Q3
"""
import gzip
import io
import json
import math
import os

import numpy as np
import pandas as pd

import cglib as L

MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
R_KM = 6371.0088


def coe_quarterly(raw):
    def series(n):
        cols = json.load(open(os.path.join(raw, "singstat_M651121", f"s{n}.json")))["Data"]["row"][0]["columns"]
        out = {}
        for c in cols:
            try:
                y, m = c["key"].split()
                out[(int(y), MON[m])] = float(c["value"])
            except (ValueError, KeyError):
                pass
        return out
    S = {k: [series(n) for n in v] for k, v in L.COE_SERIES.items()}
    rows = {}
    for b in (1, 2):
        pa, sa, qa = S[("A", b)]
        pb, sb, qb = S[("B", b)]
        for ym in sorted(set(pa) & set(sa) & set(pb) & set(sb) & set(qa) & set(qb)):
            if sa[ym] + sb[ym] <= 0:
                continue
            prem = (pa[ym] * sa[ym] + pb[ym] * sb[ym]) / (sa[ym] + sb[ym])
            quota = qa[ym] + qb[ym]
            q = L.quarter("%04d-%02d" % ym)
            rows.setdefault(q, []).append((prem, quota))
    out = pd.DataFrame([(q, sum(p for p, _ in v) / len(v), sum(x for _, x in v) / len(v), len(v))
                        for q, v in sorted(rows.items())], columns=["quarter", "coep", "coeq", "n_biddings"])
    return out


def km(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R_KM * np.arcsin(np.sqrt(a))


def nearest_exit_km(lat, lon, raw):
    feats = json.load(open(os.path.join(raw, L.EXITS)))["features"]
    ex = np.array([[f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0]] for f in feats])
    out = np.full(len(lat), np.nan)
    for i in range(0, len(lat), 2000):
        a, b = lat[i:i + 2000, None], lon[i:i + 2000, None]
        out[i:i + 2000] = km(a, b, ex[None, :, 0], ex[None, :, 1]).min(axis=1)
    return out


def read_resale(raw):
    frames = []
    for fid in L.RESALE:
        df = pd.read_csv(os.path.join(raw, "resale", fid + ".csv"), dtype=str)
        df["basis"] = "approval" if fid in L.RESALE[:2] else "registration"
        frames.append(df[["month", "town", "flat_type", "block", "street_name", "storey_range",
                          "floor_area_sqm", "flat_model", "lease_commence_date", "resale_price", "basis"]])
    df = pd.concat(frames, ignore_index=True)
    for c in ("town", "flat_type", "block", "street_name", "storey_range", "flat_model"):
        df[c] = df[c].str.strip().str.upper()
    df["flat_type"] = df["flat_type"].str.replace("MULTI GENERATION", "MULTI-GENERATION", regex=False)
    df["quarter"] = df["month"].map(L.quarter)
    df["year"] = df["month"].str[:4].astype(int)
    return df


def main():
    a = L.args("Build the cargradient analysis panel.")
    P = L.paths(a.root)
    raw = L.guard(P["raw"])
    os.makedirs(P["out"], exist_ok=True)

    coe = coe_quarterly(raw)
    L.write_csv(os.path.join(P["out"], "coe_quarterly.csv"), list(coe.columns), coe.itertuples(index=False))

    df = read_resale(raw)
    df = df[(df["quarter"] >= L.T1_FIRST) & (df["quarter"] <= L.T2_LAST)].copy()

    geo = pd.read_csv(os.path.join(P["out"], "blocks_geocoded.csv"), dtype=str)
    dist = pd.read_csv(os.path.join(P["out"], "block_distance.csv"), dtype=str)
    blk = geo.merge(dist[["block", "street_name", "km_raffles_mean", "km_cityhall_mean"]],
                    on=["block", "street_name"], how="left")
    blk["matched"] = blk["match_type"].isin(["exact", "expanded"]).astype(int)
    df = df.merge(blk[["block", "street_name", "matched", "lat", "lon", "km_raffles_mean", "km_cityhall_mean"]],
                  on=["block", "street_name"], how="left")
    df["matched"] = df["matched"].fillna(0).astype(int)

    # Gate 1 inputs: every sale in each window, geocoded or not.
    cov = []
    for w in ("T1", "T2", "T3_before", "T3_after"):
        s = df[df["quarter"].isin(L.window(w))]
        cov.append((w, len(s), int(s["matched"].sum())))
    L.write_csv(os.path.join(P["out"], "geocode_coverage.csv"), ["window", "sales", "sales_geocoded"], cov)

    # Street-level points for unmatched pairs (sensitivity J).
    sp = pd.read_csv(os.path.join(P["out"], "street_points.csv"), dtype=str)
    sp = sp[sp["lat"].notna() & (sp["lat"] != "")]
    st = pd.read_csv(os.path.join(P["out"], "station_points.csv"), dtype=str)
    raff = st[st["station"] == "RAFFLES PLACE MRT STATION"].iloc[0]
    sp["km_street"] = km(sp["lat"].astype(float).values, sp["lon"].astype(float).values,
                         float(raff["mean_lat"]), float(raff["mean_lon"]))
    df = df.merge(sp[["street_name", "km_street"]], on="street_name", how="left")
    df.loc[df["matched"] == 1, "km_street"] = np.nan

    lat = pd.to_numeric(df["lat"], errors="coerce").values
    lon = pd.to_numeric(df["lon"], errors="coerce").values
    ok = ~np.isnan(lat)
    mrt = np.full(len(df), np.nan)
    mrt[ok] = nearest_exit_km(lat[ok], lon[ok], raw)

    df = df.merge(coe, on="quarter", how="left")
    area = df["floor_area_sqm"].astype(float)
    rem = L.LEASE_YEARS - (df["year"] - df["lease_commence_date"].astype(int))
    out = pd.DataFrame({
        "quarter": df["quarter"], "year": df["year"], "basis": df["basis"],
        "block_id": df["block"] + "|" + df["street_name"], "town": df["town"],
        "flat_type": df["flat_type"], "storey_range": df["storey_range"], "flat_model": df["flat_model"],
        "floor_area": area, "rem_lease": rem, "lease_band": (rem // L.LEASE_BAND) * L.LEASE_BAND,
        "price_psm": df["resale_price"].astype(float) / area,
        "matched": df["matched"],
        "dd": pd.to_numeric(df["km_raffles_mean"], errors="coerce"),
        "dd_cityhall": pd.to_numeric(df["km_cityhall_mean"], errors="coerce"),
        "dd_street": df["km_street"], "mrt_km": mrt,
        "coep": df["coep"], "coeq": df["coeq"]})
    out = out.sort_values(["quarter", "block_id", "flat_type", "storey_range", "floor_area", "price_psm"],
                          kind="mergesort").reset_index(drop=True)
    buf = io.StringIO()
    out.to_csv(buf, index=False, float_format="%.10g", lineterminator="\n")
    with open(os.path.join(P["out"], "panel.csv.gz"), "wb") as f:
        with gzip.GzipFile(fileobj=f, mode="wb", mtime=0, filename="") as g:
            g.write(buf.getvalue().encode("utf-8"))
    print(f"panel rows {len(out)}; quarters with COE {coe.shape[0]}; geocode coverage {cov}")


if __name__ == "__main__":
    main()
