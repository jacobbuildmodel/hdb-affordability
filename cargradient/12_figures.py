#!/usr/bin/env python3
"""
12_figures.py -- the cargradient charts, from ROOT/out/ only.

Same rules as sgd/12_figures.py: shared --fig-* tokens with literal
fallbacks, a prefers-color-scheme block plus :root[data-theme="dark"], a
480-wide canvas, no text below 14px, hairline grids, LF line endings.
Titles state the finding, chosen by fixed rules from the outcomes in
out/tests.csv and out/calc_7a.csv (TITLE1, TITLE2 below, written before the
seal). Each caption says how to read the chart. A test that is not scored is
drawn muted, and the caption says why.

  figs/cargradient_chart1_tests.svg  T1, T2, and T3 before and after: the
      change in the gap between a flat 5 km and one 20 km from Raffles Place,
      in dollars per square metre, for each $10,000 on the COE, with 95 per
      cent intervals
  figs/cargradient_chart2_years.svg  that gap year by year, 2016 to 2026,
      against 2020 (section 7A), with the COE premium below it

Presentation only: nothing here computes or changes a tested number.
"""
import html
import os
import textwrap

import cglib as L

INK = "var(--fig-ink,#0b0b0b)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
SURF = "var(--fig-surface,#fcfcfa)"
SUBJ = "var(--fig-subject,#2873ce)"
CTX = "var(--fig-context,#707379)"
MUTED = 0.35
STYLE = ("<style>"
         ":root{--fig-ink:#0b0b0b;--fig-ink-3:#717171;--fig-rule:#e2e1dd;--fig-surface:#fcfcfa;"
         "--fig-subject:#2873ce;--fig-context:#707379;}"
         "@media (prefers-color-scheme: dark){:root{--fig-ink:#ffffff;--fig-ink-3:#9a9a9a;"
         "--fig-rule:#38393a;--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;}}"
         ":root[data-theme=\"dark\"]{--fig-ink:#ffffff;--fig-ink-3:#9a9a9a;--fig-rule:#38393a;"
         "--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;}"
         "text{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;}"
         "</style>")
W = 480
LINE = 19

TITLE1 = {"SURVIVE": "When COEs rose, HDB flats near town gained on flats far out",
          "FAIL_NO_LINK": "No sign that COEs tilted HDB prices toward town since 2016",
          "FAIL_OPPOSITE": "When COEs rose, flats far out gained on flats near town",
          "NOT_SCORED": "The record cannot say whether COEs tilted HDB prices"}


def title2(calc):
    if calc["share_readable"] == "True":
        return f"The COE rise lines up with about {L.printed('share', calc['share'])} of the gap's change, 2020 to 2023"
    return "The gap between near and far did not clearly change from 2020 to 2023"


def text(s, x, y, size=14, fill=INK3, anchor="start", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{html.escape(s)}</text>'


def block(lines_, x, y, size, fill, weight=None, width=46):
    out = []
    for ln in lines_:
        for part in textwrap.wrap(ln, width):
            out.append(text(part, x, y, size, fill, weight=weight))
            y += LINE if size <= 14 else LINE + 4
    return out, y


def svg(height, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:.0f}" width="{W}" '
            f'height="{height:.0f}" role="img" aria-label="{html.escape(label)}">{STYLE}'
            f'<rect width="{W}" height="{height:.0f}" fill="{SURF}"/>' + "".join(body) + "</svg>\n")


def chart1(T):
    rows = [("T1, 2002 to 2015", "T1_est", "T1_lo", "T1_hi", T["T1_outcome"]),
            ("T2, 2016 to 2026", "T2_est", "T2_lo", "T2_hi", T["T2_outcome"]),
            ("T3 before, 2012 to 2017", "T3_before_est", "T3_before_lo", "T3_before_hi", T["T3_outcome"]),
            ("T3 after, 2018 to 2026", "T3_after_est", None, None, T["T3_outcome"])]
    title = TITLE1[T["T2_outcome"]]
    body, y = block([title], 16, 30, 18, INK, "600", 40)
    sub, y = block(["Change in the price gap between a flat 5 km and one 20 km from Raffles Place, "
                    "dollars per square metre, for each $10,000 on the COE"], 16, y + 2, 14, INK3)
    body += sub
    vals = []
    for _, k, lo, hi, _ in rows:
        vals += [L.per10k(float(T[k]))]
        if lo:
            vals += [L.per10k(float(T[lo])), L.per10k(float(T[hi]))]
    vmin, vmax = min(vals + [0.0]), max(vals + [0.0])
    pad = (vmax - vmin) * 0.1 or 1.0
    vmin, vmax = vmin - pad, vmax + pad
    x0, x1 = 200, W - 24
    sx = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    top = y + 10
    body.append(f'<line x1="{sx(0):.1f}" y1="{top - 6:.1f}" x2="{sx(0):.1f}" y2="{top + 4 * 34:.1f}" '
                f'stroke="{RULE}" stroke-width="1"/>')
    for i, (lab, k, lo, hi, oc) in enumerate(rows):
        yy = top + 16 + i * 34
        op = MUTED if oc.startswith("NOT_SCORED") else 1.0
        body.append(f'<g opacity="{op}">')
        body.append(text(lab, 16, yy + 5, 14, INK3))
        v = L.per10k(float(T[k]))
        if lo:
            a, b = sorted((L.per10k(float(T[lo])), L.per10k(float(T[hi]))))
            body.append(f'<line x1="{sx(a):.1f}" y1="{yy:.1f}" x2="{sx(b):.1f}" y2="{yy:.1f}" '
                        f'stroke="{SUBJ}" stroke-width="2"/>')
        body.append(f'<circle cx="{sx(v):.1f}" cy="{yy:.1f}" r="5" fill="{SUBJ}"/>')
        body.append("</g>")
    y = top + 4 * 34 + 14
    body.append(text("0", sx(0), y, 14, INK3, "middle"))
    caption = ["How to read: a dot right of zero means flats near town gained on flats far out when "
               "COEs rose; the line is the 95 per cent interval. A line that crosses zero is no clear "
               "link. T3 after is T3 before plus the difference T3 tests."]
    if any(r[4].startswith("NOT_SCORED") for r in rows):
        caption.append("Muted rows are not scored: a sealed gate failed (geocoding, first-stage "
                       "strength, or no tilt before 2018).")
    cap, y = block(caption, 16, y + 22, 14, INK3)
    body += cap
    return svg(y + 8, body, title), title


def chart2(years, coe, calc):
    title = title2(calc)
    body, y = block([title], 16, 30, 18, INK, "600", 40)
    sub, y = block(["Gap between a flat 5 km and one 20 km from Raffles Place, dollars per square "
                    "metre, change since 2020 (top); COE premium, categories A and B (bottom)"], 16, y + 2, 14, INK3)
    body += sub
    ys = [int(r["year"]) for r in years]
    gap = [float(r["gap_5_20"]) for r in years]
    x0, x1 = 48, W - 24
    sx = lambda yr: x0 + (yr - ys[0]) / max(1, ys[-1] - ys[0]) * (x1 - x0)
    top, h = y + 12, 120
    g0, g1 = min(gap + [0.0]), max(gap + [0.0])
    g0, g1 = (g0 - 1, g1 + 1) if g0 == g1 else (g0, g1)
    sy = lambda v: top + h - (v - g0) / (g1 - g0) * h
    body.append(f'<line x1="{x0}" y1="{sy(0):.1f}" x2="{x1}" y2="{sy(0):.1f}" stroke="{RULE}" stroke-width="1"/>')
    pts = " ".join(f"{sx(a):.1f},{sy(b):.1f}" for a, b in zip(ys, gap))
    body.append(f'<polyline points="{pts}" fill="none" stroke="{SUBJ}" stroke-width="2"/>')
    cq = {}
    for r in coe:
        cq.setdefault(int(r["quarter"][:4]), []).append(float(r["coep"]))
    cy = [(yr, sum(cq[yr]) / len(cq[yr])) for yr in ys if yr in cq]
    top2 = top + h + 24
    c0, c1 = 0.0, max(v for _, v in cy) if cy else 1.0
    sy2 = lambda v: top2 + 80 - (v - c0) / (c1 - c0 or 1) * 80
    pts2 = " ".join(f"{sx(a):.1f},{sy2(b):.1f}" for a, b in cy)
    body.append(f'<polyline points="{pts2}" fill="none" stroke="{CTX}" stroke-width="2"/>')
    y = top2 + 80 + 18
    body.append(text(str(ys[0]), sx(ys[0]), y, 14, INK3, "start"))
    body.append(text(str(ys[-1]), sx(ys[-1]), y, 14, INK3, "end"))
    cap, y = block(["How to read: when the top line rises, the price gap between near and far grew "
                    "against 2020. The bottom line is the COE. A description, not a test: section 7A "
                    "of THESIS.md gives the calculation and its interval."], 16, y + 22, 14, INK3)
    body += cap
    return svg(y + 8, body, title), title


def main():
    a = L.args("cargradient charts.")
    P = L.paths(a.root)
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(P["out"], "tests.csv"))}
    calc = {r["key"]: r["value"] for r in L.read_csv(os.path.join(P["out"], "calc_7a.csv"))}
    years = L.read_csv(os.path.join(P["out"], "year_slopes.csv"))
    coe = L.read_csv(os.path.join(P["out"], "coe_quarterly.csv"))
    s1, t1 = chart1(T)
    s2, t2 = chart2(years, coe, calc)
    L.write_text(os.path.join(P["figs"], "cargradient_chart1_tests.svg"), s1)
    L.write_text(os.path.join(P["figs"], "cargradient_chart2_years.svg"), s2)
    print("chart 1:", t1)
    print("chart 2:", t2)


if __name__ == "__main__":
    main()
