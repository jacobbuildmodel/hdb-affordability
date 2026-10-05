#!/usr/bin/env python3
# Quarterly COE premium, categories A and B, built as the paper does (p. 14):
# per bidding, A and B premiums weighted by successful bids; then the mean of
# the biddings in the quarter. Source: SingStat M651121.
import json, statistics as st
def load(s):
    r = json.load(open(f"cargradient/raw/singstat_M651121/s{s}.json"))["Data"]["row"][0]["columns"]
    out = {}
    for c in r:
        try: out[c["key"]] = float(c["value"])
        except ValueError: pass
    return out
A1p, A1s, A2p, A2s = load(23), load(21), load(27), load(25)
B1p, B1s, B2p, B2s = load(33), load(31), load(37), load(35)
MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
q = {}
for (pa, sa, pb, sb) in [(A1p, A1s, B1p, B1s), (A2p, A2s, B2p, B2s)]:
    for k in pa:
        if k in sa and k in pb and k in sb and sa[k] + sb[k] > 0:
            y, m = k.split(); qq = f"{y}Q{(MON[m]-1)//3+1}"
            q.setdefault(qq, []).append((pa[k]*sa[k] + pb[k]*sb[k]) / (sa[k] + sb[k]))
Q = {k: st.mean(v) for k, v in q.items()}
N = {k: len(v) for k, v in q.items()}
keys = sorted(Q)
def win(a, b):
    ks = [k for k in keys if a <= k <= b]
    v = [Q[k] for k in ks]
    return ks, v
for name, a, b in [("before 2016Q1-2017Q3", "2016Q1", "2017Q3"),
                   ("after 2018Q2-2026Q3", "2018Q2", "2026Q3"),
                   ("alt before 2013Q1-2017Q3", "2013Q1", "2017Q3"),
                   ("alt before 2010Q1-2017Q3", "2010Q1", "2017Q3"),
                   ("T1 2002Q2-2015Q4", "2002Q2", "2015Q4")]:
    ks, v = win(a, b)
    lo, hi = min(v), max(v)
    print(f"{name}: quarters {len(ks)} | min {lo:,.0f} ({ks[v.index(lo)]}) | max {hi:,.0f} ({ks[v.index(hi)]}) | max/min {hi/lo:.2f} | sd {st.pstdev(v):,.0f} | biddings/qtr {min(N[k] for k in ks)}-{max(N[k] for k in ks)}")
print("2020 quarters:", {k: N[k] for k in keys if k.startswith("2020")})
print("last quarter", keys[-1], N[keys[-1]])
for name, a, b in [("reg-basis before 2012Q2-2017Q3", "2012Q2", "2017Q3"),
                   ("after excl WFH 2018Q2-2019Q4 + 2023Q1-2026Q3", None, None)]:
    if a:
        ks, v = win(a, b)
    else:
        ks = [k for k in keys if ("2018Q2" <= k <= "2019Q4") or ("2023Q1" <= k <= "2026Q3")]
        v = [Q[k] for k in ks]
    lo, hi = min(v), max(v)
    print(f"{name}: quarters {len(ks)} | min {lo:,.0f} ({ks[v.index(lo)]}) | max {hi:,.0f} ({ks[v.index(hi)]}) | max/min {hi/lo:.2f} | sd {st.pstdev(v):,.0f}")
