#!/usr/bin/env python3
"""
02_distance.py -- great-circle km from each geocoded block to Raffles Place
MRT and City Hall MRT. Run from the repository root after 01_geocode.py.

Station points, from the LTA MRT station exit layer on data.gov.sg
(d_b39d3a0871985372d7e1637193335da5, saved as
cargradient/raw/lta_mrt_station_exit.geojson; coordinates are lon, lat):
  (i)  "mean":    the mean of the station's exit points;
  (ii) "nearest": the exit nearest to (i), the station's centre.
Which one the scored tests use is sealed later; both are written.

Outputs:
  cargradient/out/station_points.csv  the two points per station, the gap
                                      between them in metres, the exit count
  cargradient/out/block_distance.csv  per block-and-street pair, km to each
                                      point; empty where the block is unmatched
"""
import csv
import json
import math

EXITS = "cargradient/raw/lta_mrt_station_exit.geojson"
BLOCKS = "cargradient/out/blocks_geocoded.csv"
STATIONS = {"raffles": "RAFFLES PLACE MRT STATION", "cityhall": "CITY HALL MRT STATION"}
R_KM = 6371.0088  # mean Earth radius (IUGG)


def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_KM * math.asin(math.sqrt(a))


def station_points():
    feats = json.load(open(EXITS))["features"]
    out = {}
    for key, name in STATIONS.items():
        pts = [(f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0],
                f["properties"]["EXIT_CODE"])
               for f in feats if f["properties"]["STATION_NA"] == name]
        assert pts, name
        mlat = sum(p[0] for p in pts) / len(pts)
        mlon = sum(p[1] for p in pts) / len(pts)
        near = min(pts, key=lambda p: km(mlat, mlon, p[0], p[1]))
        out[key] = {"name": name, "exits": len(pts),
                    "mean": (mlat, mlon), "nearest": (near[0], near[1]),
                    "nearest_exit": near[2],
                    "gap_m": 1000 * km(mlat, mlon, near[0], near[1])}
    return out


def main():
    st = station_points()
    with open("cargradient/out/station_points.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["station", "exits", "mean_lat", "mean_lon", "nearest_exit",
                    "nearest_lat", "nearest_lon", "gap_m"])
        for k, s in st.items():
            w.writerow([s["name"], s["exits"], f"{s['mean'][0]:.7f}", f"{s['mean'][1]:.7f}",
                        s["nearest_exit"], f"{s['nearest'][0]:.7f}", f"{s['nearest'][1]:.7f}",
                        f"{s['gap_m']:.1f}"])
            print(f"{s['name']}: {s['exits']} exits; mean vs nearest exit "
                  f"({s['nearest_exit']}) {s['gap_m']:.1f} m")
    cols = ["block", "street_name", "match_type",
            "km_raffles_mean", "km_raffles_nearest", "km_cityhall_mean", "km_cityhall_nearest"]
    n = m = 0
    with open(BLOCKS) as fin, open("cargradient/out/block_distance.csv", "w", newline="") as fout:
        w = csv.writer(fout)
        w.writerow(cols)
        for r in csv.DictReader(fin):
            n += 1
            row = [r["block"], r["street_name"], r["match_type"]]
            if r["match_type"] in ("exact", "expanded"):
                m += 1
                lat, lon = float(r["lat"]), float(r["lon"])
                for k in ("raffles", "cityhall"):
                    for p in ("mean", "nearest"):
                        row.append(f"{km(lat, lon, *st[k][p]):.4f}")
            else:
                row += [""] * 4
            w.writerow(row)
    print(f"pairs {n}, with distances {m}")


if __name__ == "__main__":
    main()
