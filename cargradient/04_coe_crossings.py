#!/usr/bin/env python3
"""
04_coe_crossings.py -- when the COE premium for categories A and B was at or
above $100,000, bidding by bidding, from SingStat M651121 (data source LTA).
COE is not this piece's outcome. Run from the repository root.
Output: cargradient/out/coe_crossings.txt
"""
import json

MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
SERIES = {"A (Cars Up To 1600cc And 97kW)": (23, 27), "B (Cars Above 1600cc Or 97kW)": (33, 37)}


def load(s):
    cols = json.load(open(f"cargradient/raw/singstat_M651121/s{s}.json"))["Data"]["row"][0]["columns"]
    out = {}
    for c in cols:
        try:
            y, m = c["key"].split()
            out[(int(y), MON[m])] = float(c["value"])
        except ValueError:
            pass
    return out


def label(t):
    (y, m), b = t
    return f"{y}-{m:02d} bidding {b}"


lines = []
for cat, (first, second) in SERIES.items():
    prem = {}
    for s, b in ((first, 1), (second, 2)):
        for ym, v in load(s).items():
            prem[(ym, b)] = v
    runs, above, prev = [], False, None
    for t in sorted(prem):
        a = prem[t] >= 100000
        if a and not above:
            runs.append([t, None])
        if not a and above:
            runs[-1][1] = prev
        above, prev = a, t
    lines.append(f"Category {cat}: first at or above $100,000 in {label(runs[0][0])}")
    for start, end in runs:
        lines.append(f"  run: {label(start)} to {label(end) if end else 'latest (' + label(prev) + ')'}")
open("cargradient/out/coe_crossings.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
