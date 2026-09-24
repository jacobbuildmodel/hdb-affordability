"""
07_figures.py

Three figures, generated from the analysis output. No hand editing. Rerunning on
the same inputs produces byte-identical files.

  fig1_price_to_income.svg   A shape a table hides. The price of a constant-quality
                             four-room flat in years of median household income,
                             2013 to 2025. It falls for six years and then climbs,
                             and it ends below where it started. One series.

  fig2_ehg_crossing.svg      A comparison the reader would otherwise hold in their
                             head. Median household income against the Enhanced CPF
                             Housing Grant ceiling, which has not moved since 2019.
                             Same units, one axis, and the crossing is the finding.

  fig3_binding_constraint.svg  The mechanism the argument depends on. For the
                             20th-percentile buyer, the loan-to-value cap against
                             the price less grants. Whichever is lower is the loan.
                             They swap over, and that is why a bigger grant stopped
                             reducing anyone's monthly payment.

Rules applied: the title is the finding and lives in the caption, not the image;
one axis, never two scales; no broken axes; colour the subject and grey the
context; direct labels at the line ends plus a legend where there are two series;
solid hairline gridlines; a full aria-label; viewBox with no fixed width; CSS
custom properties with literal fallbacks so the figure follows light and dark mode.

Palette: shared across the three site repos as of Phase 3 (--fig-* custom
properties), not just this one. Renamed from --series-1/--series-2/
--text-primary/--text-secondary/--surface-1/--grid to --fig-subject/
--fig-subject-2/--fig-ink/--fig-ink-2/--fig-surface/--fig-rule -- matching
the --fig-subject/--fig-context naming coe-analysis's 09_figures.py already
used independently, which the website's own economics.css also already
defines (unconsumed by any actual chart until Phase 3). This repo's fig2/
fig3 compare two co-equal series rather than a subject against background
context, so --fig-subject-2 stands in where --fig-context wouldn't fit.

Accent hex values re-picked to actually clear WCAG AA 4.5:1 as text (not
just the 3:1 non-text floor they were previously validated against) -- the
old #2a78d6/#eb6834 measured 4.30:1 and 3.12:1 as text on this surface.
  light  --fig-subject #2873ce, --fig-subject-2 #c44613, on --fig-surface #fcfcfb
         (4.61:1 and 4.83:1 against surface)
  dark   --fig-subject #3987e5, --fig-subject-2 #db602f, on --fig-surface #1a1a19
         (4.79:1 and 4.75:1 against surface)
Colour-blindness: blue/orange simulated under protanopia, deuteranopia and
tritanopia (Brettel/Vienot-style linear-RGB matrices), worst-case CIE76 deltaE
94.8 (dark), 97.1 (light) -- still trivially distinguishable under every
simulated form, as this hue pair already was.

Canvas and type scale (480x340, 14/15px, verified 11.4px at 390px) are
unchanged here -- that work merged separately as PR #10 (mobile-charts).
This pass is the token rename and the contrast fix only.

Reads:  out/affordability.csv, out/grants_by_buyer.csv, out/index_hedonic.csv,
        raw/income_percentiles_excl_cpf.csv
Writes: figs/fig1_price_to_income.svg
        figs/fig2_ehg_crossing.svg
        figs/fig3_binding_constraint.svg
        out/figure_captions.txt

Usage:  python 07_figures.py
"""

import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")
FIGS = os.path.join(HERE, "figs")

W, H = 480, 340
PAD_L, PAD_R, PAD_T, PAD_B = 60, 142, 58, 46
EHG_CEILING = 9000.0

STYLE = """
<style>
  .viz { --fig-surface:#fcfcfb; --fig-ink:#0b0b0b; --fig-ink-2:#52514e;
         --fig-rule:#e4e3df; --fig-subject:#2873ce; --fig-subject-2:#c44613; }
  @media (prefers-color-scheme: dark) {
    .viz { --fig-surface:#1a1a19; --fig-ink:#ffffff; --fig-ink-2:#c3c2b7;
           --fig-rule:#383835; --fig-subject:#3987e5; --fig-subject-2:#db602f; }
  }
  :root[data-theme="dark"] .viz { --fig-surface:#1a1a19; --fig-ink:#ffffff;
           --fig-ink-2:#c3c2b7; --fig-rule:#383835; --fig-subject:#3987e5;
           --fig-subject-2:#db602f; }
  :root[data-theme="light"] .viz { --fig-surface:#fcfcfb; --fig-ink:#0b0b0b;
           --fig-ink-2:#52514e; --fig-rule:#e4e3df; --fig-subject:#2873ce;
           --fig-subject-2:#c44613; }
  .viz text { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI,
              Roboto, Helvetica, Arial, sans-serif; }
  .ax   { font-size: 14px; fill: var(--fig-ink-2, #52514e); }
  .lbl  { font-size: 15px; font-weight: 600; }
  .note { font-size: 14px; fill: var(--fig-ink-2, #52514e); }
</style>
"""


def money(v):
    return "{:,.0f}".format(v)


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def sc(v, lo, hi, a, b):
    return (a + b) / 2.0 if hi == lo else a + (v - lo) * (b - a) / (hi - lo)


def frame(years, ylo, yhi, ticks, fmt):
    x0, x1, y0, y1 = PAD_L, W - PAD_R, H - PAD_B, PAD_T
    p = []
    for t in ticks:
        y = sc(t, ylo, yhi, y0, y1)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="var(--fig-rule, #e4e3df)" stroke-width="1"/>' % (x0, y, x1, y))
        p.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
                 % (x0 - 8, y + 4, esc(fmt(t))))
    for yr in years:
        if (yr - years[0]) % 4 == 0 or yr == years[-1]:
            x = sc(yr, min(years), max(years), x0, x1)
            p.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="middle">%d'
                     '</text>' % (x, H - PAD_B + 20, yr))
    return "\n".join(p)


def line(years, vals, ylo, yhi, var, fb, width=2.0):
    x0, x1, y0, y1 = PAD_L, W - PAD_R, H - PAD_B, PAD_T
    pts = [(sc(y, min(years), max(years), x0, x1), sc(v, ylo, yhi, y0, y1))
           for y, v in zip(years, vals) if v == v]
    if not pts:
        return "", None
    d = "M " + " L ".join("%.1f %.1f" % q for q in pts)
    return ('<path d="%s" fill="none" stroke="var(%s, %s)" stroke-width="%.1f" '
            'stroke-linejoin="round" stroke-linecap="round"/>' % (d, var, fb, width),
            pts[-1])


def endlabel(pt, var, fb, name, sub=None, dy=0.0):
    if not pt:
        return ""
    pt = (pt[0], pt[1] + dy)
    s = ('<circle cx="%.1f" cy="%.1f" r="4" fill="var(%s, %s)" '
         'stroke="var(--fig-surface, #fcfcfb)" stroke-width="2"/>'
         '<text class="lbl" x="%.1f" y="%.1f" fill="var(%s, %s)">%s</text>'
         % (pt[0], pt[1], var, fb, pt[0] + 10, pt[1] + 4, var, fb, esc(name)))
    if sub:
        s += ('<text class="note" x="%.1f" y="%.1f">%s</text>'
              % (pt[0] + 10, pt[1] + 20, esc(sub)))
    return s


def legend(items):
    lx, ly = 8, 18
    p = []
    for i, (var, fb, name) in enumerate(items):
        p.append('<rect x="%.1f" y="%.1f" width="10" height="10" rx="2" '
                 'fill="var(%s, %s)"/>' % (lx, ly + i * 20 - 10, var, fb))
        p.append('<text class="ax" x="%.1f" y="%.1f">%s</text>'
                 % (lx + 16, ly + i * 20, esc(name)))
    return "\n".join(p)


def svg(body, aria, title, desc):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="100%%" role="img" aria-label="%s" class="viz" '
            'preserveAspectRatio="xMidYMid meet">\n<title>%s</title>\n'
            '<desc>%s</desc>\n%s\n<rect x="0" y="0" width="%d" height="%d" '
            'fill="var(--fig-surface, #fcfcfb)"/>\n%s\n</svg>\n'
            % (W, H, esc(aria), esc(title), esc(desc), STYLE, W, H, body))


def fig1(aff):
    d = aff[aff.buyer == "p50"].sort_values("year")
    years = d["year"].astype(int).tolist()
    vals = d["price_to_income_years"].astype(float).tolist()
    ylo, yhi, ticks = 0, 6, [0, 1, 2, 3, 4, 5, 6]
    p = [frame(years, ylo, yhi, ticks, lambda t: "%d" % t)]

    lo_i = vals.index(min(vals))
    for i, lab in ((0, "2013"), (lo_i, "2019 low"), (len(years) - 1, None)):
        if lab:
            x = sc(years[i], min(years), max(years), PAD_L, W - PAD_R)
            y = sc(vals[i], ylo, yhi, H - PAD_B, PAD_T)
            p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                     'stroke="var(--fig-ink-2, #52514e)" stroke-width="1" '
                     'opacity="0.3"/>' % (x, y, x, H - PAD_B))
            anchor = "start" if i == 0 else "middle"
            p.append('<text class="note" x="%.1f" y="%.1f" text-anchor="%s">'
                     '%s %.2f</text>' % (x, y - 10, anchor, esc(lab), vals[i]))

    path, last = line(years, vals, ylo, yhi, "--fig-subject", "#2873ce")
    p.append(path)
    p.append(endlabel(last, "--fig-subject", "#2873ce", "%.2f years" % vals[-1],
                      "of median income"))

    aria = ("Line chart. The price of a constant-quality four-room HDB resale flat "
            "expressed in years of median annual household income, %d to %d, on an "
            "axis running from 0 to 6 years. It starts at %.2f years in %d, falls "
            "to a low of %.2f in %d, then climbs to %.2f in %d, ending below where "
            "it began."
            % (years[0], years[-1], vals[0], years[0], min(vals), years[lo_i],
               vals[-1], years[-1]))
    return svg("\n".join(p), aria, "Years of income to buy a four-room flat",
               "The series falls for six years and then climbs, and ends below its "
               "2013 level."), vals


def fig2(med, years):
    vals = [med[y] for y in years]
    yhi = 12000
    ticks = list(range(0, yhi + 1, 3000))
    p = [frame(years, 0, yhi, ticks, lambda t: "%d,000" % (t // 1000) if t else "0")]

    yc = sc(EHG_CEILING, 0, yhi, H - PAD_B, PAD_T)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="var(--fig-subject-2, #c44613)" stroke-width="2"/>'
             % (PAD_L, yc, W - PAD_R, yc))
    p.append(endlabel((W - PAD_R, yc), "--fig-subject-2", "#c44613", "9,000 ceiling",
                      "frozen since 2019"))

    path, last = line(years, vals, 0, yhi, "--fig-subject", "#2873ce")
    p.append(path)
    p.append(endlabel(last, "--fig-subject", "#2873ce", money(vals[-1]),
                      "median income"))

    # the crossing
    cx = None
    for i in range(len(years) - 1):
        if vals[i] <= EHG_CEILING < vals[i + 1]:
            f = (EHG_CEILING - vals[i]) / (vals[i + 1] - vals[i])
            cx = sc(years[i] + f, min(years), max(years), PAD_L, W - PAD_R)
            cyear = years[i] + f
    if cx:
        p.append('<circle cx="%.1f" cy="%.1f" r="5" fill="none" '
                 'stroke="var(--fig-ink, #0b0b0b)" stroke-width="2"/>'
                 % (cx, yc))
        p.append('<text class="note" x="%.1f" y="%.1f" text-anchor="middle">'
                 'crosses %.1f</text>' % (cx, yc - 14, cyear))

    p.append(legend([("--fig-subject", "#2873ce", "Median household income"),
                     ("--fig-subject-2", "#c44613",
                      "Enhanced CPF Housing Grant ceiling")]))

    aria = ("Line chart in Singapore dollars a month, %d to %d, on one axis. A "
            "rising line is median monthly household income from work excluding "
            "employer CPF contributions. A flat horizontal line at 9,000 dollars is "
            "the Enhanced CPF Housing Grant income ceiling, unchanged since 2019. "
            "The income line crosses the ceiling in %s and is %.0f dollars by %d."
            % (years[0], years[-1], ("%.1f" % cyear) if cx else "no year",
               vals[-1], years[-1]))
    return svg("\n".join(p), aria,
               "Median income against the frozen grant ceiling",
               "The ceiling has not moved since 2019. Incomes have.")


def fig3(aff, grants):
    a = aff[aff.buyer == "p20"].set_index("year")
    g = grants[grants.buyer == "p20"].set_index("year")
    years = [y for y in a.index if bool(a.loc[y, "grant_series_valid"])]
    cap = [float(a.loc[y, "ltv"]) * float(a.loc[y, "price"]) for y in years]
    net = [float(a.loc[y, "price"]) - float(g.loc[y, "total_grant"]) for y in years]

    hi = max(max(cap), max(net))
    yhi = int((hi // 100000 + 1) * 100000)
    ticks = list(range(0, yhi + 1, 100000))
    p = [frame(years, 0, yhi, ticks,
               lambda t: "%dk" % (t // 1000) if t else "0")]

    p1, l1 = line(years, cap, 0, yhi, "--fig-subject-2", "#c44613")
    p2, l2 = line(years, net, 0, yhi, "--fig-subject", "#2873ce")
    p += [p1, p2]
    push = 0.0
    if l1 and l2 and abs(l1[1] - l2[1]) < 38:
        push = (38 - abs(l1[1] - l2[1])) / 2.0
        if l1[1] < l2[1]:
            d1, d2 = -push, push
        else:
            d1, d2 = push, -push
    else:
        d1 = d2 = 0.0
    p.append(endlabel(l1, "--fig-subject-2", "#c44613", "LTV cap",
                      money(cap[-1]), dy=d1))
    p.append(endlabel(l2, "--fig-subject", "#2873ce", "price - grants",
                      money(net[-1]), dy=d2))
    p.append(legend([("--fig-subject", "#2873ce", "Price less grants"),
                     ("--fig-subject-2", "#c44613", "Loan-to-value cap")]))

    aria = ("Line chart in Singapore dollars, %d to %d, on one axis, for a buyer at "
            "the 20th percentile of household income. One line is the loan-to-value "
            "cap on the loan. The other is the purchase price less grants. The loan "
            "is whichever is lower. In %d the price less grants is lower, so grants "
            "set the loan. By %d the cap is lower, so the cap sets the loan and an "
            "extra dollar of grant no longer reduces it."
            % (years[0], years[-1], years[0], years[-1]))
    return svg("\n".join(p), aria, "Which constraint sets the loan",
               "The loan is the lower of the two lines. They swap over inside the "
               "window.")


def main():
    os.makedirs(FIGS, exist_ok=True)
    aff = pd.read_csv(os.path.join(OUT, "affordability.csv"))
    grants = pd.read_csv(os.path.join(OUT, "grants_by_buyer.csv"))
    incdf = pd.read_csv(os.path.join(RAW, "income_percentiles_excl_cpf.csv"))
    r = incdf[incdf["Dollar"].str.strip() == "50th (Median)"].iloc[0]
    med = {int(c): float(r[c]) for c in incdf.columns if c != "Dollar"}
    years = sorted(aff["year"].unique().tolist())

    caps = []
    s1, vals = fig1(aff)
    open(os.path.join(FIGS, "fig1_price_to_income.svg"), "w", newline="\n").write(s1)
    caps.append("Figure 1. A four-room flat cost %.2f years of median household "
                "income in %d, %.2f in %d, and %.2f in %d. Constant-quality price "
                "from the hedonic index in 02_hedonic.py, divided by annual median "
                "monthly household income from work excluding employer CPF "
                "contributions. Sources: HDB resale transactions and SingStat, both "
                "via data.gov.sg."
                % (vals[0], years[0], min(vals), years[vals.index(min(vals))],
                   vals[-1], years[-1]))

    open(os.path.join(FIGS, "fig2_ehg_crossing.svg"), "w", newline="\n").write(
        fig2(med, years))
    caps.append("Figure 2. Median household income passed the Enhanced CPF Housing "
                "Grant ceiling in 2022. The ceiling has been 9,000 dollars a month "
                "since the grant was introduced in September 2019. Income is an "
                "upper bound on HDB's assessed basis, which excludes bonuses, so "
                "the crossing is 2022 or later.")

    open(os.path.join(FIGS, "fig3_binding_constraint.svg"), "w", newline="\n").write(
        fig3(aff, grants))
    caps.append("Figure 3. Grants set the loan in 2019. The loan-to-value cap sets "
                "it by 2025. For a buyer at the 20th percentile the loan is the "
                "lower of the two lines, and they swap over, which is why a larger "
                "grant stopped reducing the monthly repayment.")

    with open(os.path.join(OUT, "figure_captions.txt"), "w", newline="\n") as fh:
        fh.write("\n\n".join(caps) + "\n")

    for f in ("fig1_price_to_income.svg", "fig2_ehg_crossing.svg",
              "fig3_binding_constraint.svg"):
        print("figs/%s written" % f)
    print("out/figure_captions.txt written")
    print("")
    print("Now render all three and look at them. The palette validator checks "
          "colour, not layout.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FIGURES FAILED: %s" % exc, file=sys.stderr)
        sys.exit(2)
