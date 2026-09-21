"""
23_figures.py

Chart 1 and Chart 2, the two charts THESIS.md section 10 requires before any
prose is written.

Reads:  financing/out/rates_monthly.csv, financing/out/t1_breakeven.csv,
        financing/out/t3_r2_r3.csv
Writes: financing/figs/chart1_hdb_vs_sora.svg
        financing/figs/chart2_breakeven_by_start_year.svg
        financing/out/figure_captions.txt

Palette and SVG helpers are the published piece's, copied from 07_figures.py
rather than imported, per THESIS.md section 11 (no cross-directory source
dependency). Both charts carry a prefers-color-scheme dark block and are sized
to stay readable at 390px.

Canvas, padding and type sizes follow the phone-screen redraw applied to the
published piece's 07_figures.py on the mobile-charts branch (commit 709f846):
480x340 canvas, 14-15px text, fewer year labels, more right margin. Smallest
rendered text at 390px goes from 6.0px to 11.4px or larger; check.sh fails
anything under 11px.

Usage:  python3 23_figures.py
"""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")

W, H = 480, 340
PAD_L, PAD_R, PAD_T, PAD_B = 60, 150, 58, 70
HDB = 2.6

STYLE = """
<style>
  .viz { --surface-1:#fcfcfb; --text-primary:#0b0b0b; --text-secondary:#52514e;
         --grid:#e4e3df; --series-1:#2a78d6; --series-2:#eb6834; }
  @media (prefers-color-scheme: dark) {
    .viz { --surface-1:#1a1a19; --text-primary:#ffffff; --text-secondary:#c3c2b7;
           --grid:#383835; --series-1:#3987e5; --series-2:#d95926; }
  }
  :root[data-theme="dark"] .viz { --surface-1:#1a1a19; --text-primary:#ffffff;
           --text-secondary:#c3c2b7; --grid:#383835; --series-1:#3987e5;
           --series-2:#d95926; }
  :root[data-theme="light"] .viz { --surface-1:#fcfcfb; --text-primary:#0b0b0b;
           --text-secondary:#52514e; --grid:#e4e3df; --series-1:#2a78d6;
           --series-2:#eb6834; }
  .viz text { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI,
              Roboto, Helvetica, Arial, sans-serif; }
  .ax   { font-size: 14px; fill: var(--text-secondary, #52514e); }
  .lbl  { font-size: 15px; font-weight: 600; }
  .note { font-size: 14px; fill: var(--text-secondary, #52514e); }
</style>
"""


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def sc(v, lo, hi, a, b):
    return (a + b) / 2.0 if hi == lo else a + (v - lo) * (b - a) / (hi - lo)


def svg(body, aria, title, desc):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="100%%" role="img" aria-label="%s" class="viz" '
            'preserveAspectRatio="xMidYMid meet">\n<title>%s</title>\n'
            '<desc>%s</desc>\n%s\n<rect x="0" y="0" width="%d" height="%d" '
            'fill="var(--surface-1, #fcfcfb)"/>\n%s\n</svg>\n'
            % (W, H, esc(aria), esc(title), esc(desc), STYLE, W, H, body))


def gridlines(ylo, yhi, ticks, fmt, pad_r=None, pad_t=None):
    x0 = PAD_L
    x1 = W - (PAD_R if pad_r is None else pad_r)
    y0 = H - PAD_B
    y1 = PAD_T if pad_t is None else pad_t
    p = []
    for t in ticks:
        y = sc(t, ylo, yhi, y0, y1)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="var(--grid, #e4e3df)" stroke-width="1"/>' % (x0, y, x1, y))
        p.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
                 % (x0 - 8, y + 4, esc(fmt(t))))
    return "\n".join(p)


def xlabels(xs, labels, pad_r=None):
    x0, x1 = PAD_L, W - (PAD_R if pad_r is None else pad_r)
    p = []
    for v, lab in labels:
        x = sc(v, xs[0], xs[-1], x0, x1)
        p.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                 % (x, H - PAD_B + 20, esc(lab)))
    return "\n".join(p)


def polyline(xs, ys, xlo, xhi, ylo, yhi, var, fb, width=2.0, dash=None,
             pad_r=None, pad_t=None):
    x0 = PAD_L
    x1 = W - (PAD_R if pad_r is None else pad_r)
    y0 = H - PAD_B
    y1 = PAD_T if pad_t is None else pad_t
    pts = [(sc(x, xlo, xhi, x0, x1), sc(y, ylo, yhi, y0, y1))
           for x, y in zip(xs, ys) if y is not None]
    if not pts:
        return "", None
    d = "M " + " L ".join("%.1f %.1f" % q for q in pts)
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="%s" fill="none" stroke="var(%s, %s)" stroke-width="%.1f"%s '
            'stroke-linejoin="round" stroke-linecap="round"/>' % (d, var, fb, width, ds),
            pts[-1])


def endlabel(pt, var, fb, name, sub=None):
    if not pt:
        return ""
    s = ('<circle cx="%.1f" cy="%.1f" r="4" fill="var(%s, %s)" '
         'stroke="var(--surface-1, #fcfcfb)" stroke-width="2"/>'
         '<text class="lbl" x="%.1f" y="%.1f" fill="var(%s, %s)">%s</text>'
         % (pt[0], pt[1], var, fb, pt[0] + 10, pt[1] + 4, var, fb, esc(name)))
    if sub:
        s += ('<text class="note" x="%.1f" y="%.1f">%s</text>'
              % (pt[0] + 10, pt[1] + 20, esc(sub)))
    return s


def legend(items, x=None, y=None, step=20):
    """items: (var, fallback, label) or (var, fallback, label, opacity).

    Defaults place the legend in the top-left margin, clear of the plot
    area; pass x/y (e.g. into the right padding) to keep it clear of a
    band that covers the left side of the chart.
    """
    lx = 8 if x is None else x
    ly = 18 if y is None else y
    p = []
    for i, it in enumerate(items):
        var, fb, name = it[0], it[1], it[2]
        op = it[3] if len(it) > 3 else 1.0
        p.append('<rect x="%.1f" y="%.1f" width="10" height="10" rx="2" '
                 'fill="var(%s, %s)" fill-opacity="%.2f"/>'
                 % (lx, ly + i * step - 8, var, fb, op))
        p.append('<text class="ax" x="%.1f" y="%.1f">%s</text>'
                 % (lx + 16, ly + i * step, esc(name)))
    return "\n".join(p)


def chart1():
    rows = list(csv.DictReader(open(os.path.join(OUT, "rates_monthly.csv"))))
    rows = [r for r in rows if r["month"] >= "2010-01"]
    xs = list(range(len(rows)))
    sora = [float(r["sora3m"]) for r in rows]
    ylo, yhi = 0.0, max(max(sora), HDB) * 1.15
    p = [gridlines(ylo, yhi, [0, 1, 2, 3, 4], lambda t: "%.0f%%" % t)]

    first_year = int(rows[0]["month"][:4])
    labels = []
    for i, r in enumerate(rows):
        y, m = r["month"].split("-")
        if m == "01" and (int(y) - first_year) % 4 == 0:
            labels.append((i, y))
    last_year = rows[-1]["month"][:4]
    if not any(lab == last_year for _, lab in labels):
        labels.append((len(rows) - 1, last_year))
    p.append(xlabels(xs, labels))

    # HDB constant
    yh = sc(HDB, ylo, yhi, H - PAD_B, PAD_T)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="var(--series-2, #eb6834)" stroke-width="2"/>'
             % (PAD_L, yh, W - PAD_R, yh))
    p.append(endlabel((W - PAD_R, yh), "--series-2", "#eb6834", "HDB 2.6%",
                      "flat since 1999"))

    path, last = polyline(xs, sora, 0, len(rows) - 1, ylo, yhi, "--series-1", "#2a78d6")
    p.append(path)
    p.append(endlabel(last, "--series-1", "#2a78d6", "%.2f%%" % sora[-1],
                      "3-month SORA"))
    p.append(legend([("--series-1", "#2a78d6", "Compounded 3-month SORA"),
                     ("--series-2", "#eb6834", "HDB concessionary rate")]))
    p.append('<text class="note" x="%.1f" y="%.1f">Monthly, %s to %s.</text>'
             % (PAD_L, H - 24, rows[0]["month"], rows[-1]["month"]))
    p.append('<text class="note" x="%.1f" y="%.1f">Source: MAS via '
             'data.gov.sg (F1); CPF Board (F2).</text>' % (PAD_L, H - 8))

    body = "\n".join(p)
    return svg(body,
               "Compounded 3-month SORA against the flat HDB concessionary rate, "
               "2010 to 2026",
               "HDB 2.6% against 3-month SORA",
               "SORA runs far below 2.6 per cent for a decade, rises above it "
               "through 2022 and 2023, then falls back below it by 2026.")


def chart2():
    t1 = list(csv.DictReader(open(os.path.join(OUT, "t1_breakeven.csv"))))
    rs = list(csv.DictReader(open(os.path.join(OUT, "t1_reset_sensitivity.csv"))))
    RESETS = [36, 24, 12, 3]
    reset_lo, reset_hi = {}, {}
    for r in rs:
        y = int(r["start_year"])
        vals = [float(r["breakeven_reset_%d" % rm]) for rm in RESETS
                if r["breakeven_reset_%d" % rm]]
        if vals:
            reset_lo[y], reset_hi[y] = min(vals), max(vals)

    years = [int(r["start_year"]) for r in t1]
    be = [float(r["realised_breakeven_spread_r2"]) for r in t1]
    rlo = [reset_lo.get(y) for y in years]
    rhi = [reset_hi.get(y) for y in years]
    ylo = min([v for v in be + rlo if v is not None] + [-1.5])
    yhi = max([v for v in be + rhi if v is not None] + [2.4])

    # Full-width plot: the legend moved to a single line above the plot, so
    # the right margin only needs to clear the last point and its threshold
    # label, not a legend column.
    PAD_R2, PAD_T2 = 20, 48
    x0, x1 = PAD_L, W - PAD_R2
    y0, y1 = H - PAD_B, PAD_T2

    def X(year):
        return sc(year, years[0], years[-1], x0, x1)

    def Y(v):
        return sc(v, ylo, yhi, y0, y1)

    p = [gridlines(ylo, yhi, [-1, 0, 2], lambda t: "%+.0f" % t if t else "0",
                   pad_r=PAD_R2, pad_t=PAD_T2)]
    first_year = years[0]
    p.append(xlabels(years, [(y, str(y)) for y in years
                             if (y - first_year) % 4 == 0 or y == years[-1]],
                     pad_r=PAD_R2))

    def band(lo_by_i, hi_by_i, var, fb, op, dash=None):
        idx = [i for i in range(len(years))
               if lo_by_i[i] is not None and hi_by_i[i] is not None]
        if not idx:
            return ""
        top = [(X(years[i]), Y(hi_by_i[i])) for i in idx]
        bot = [(X(years[i]), Y(lo_by_i[i])) for i in idx]
        d = ("M " + " L ".join("%.1f %.1f" % q for q in top) + " L "
             + " L ".join("%.1f %.1f" % q for q in reversed(bot)) + " Z")
        edge = (' stroke="var(%s, %s)" stroke-width="1" stroke-dasharray="%s"'
                % (var, fb, dash)) if dash else ' stroke="none"'
        return ('<path d="%s" fill="var(%s, %s)" fill-opacity="%.2f"%s/>'
                 % (d, var, fb, op, edge))

    # Reset-interval band (AMENDMENT 3, written after results): the only
    # band on this chart. The sealed R3 band lives in RESULTS.md and the
    # side-note table instead, per Task 3b item 1.
    p.append(band(rlo, rhi, "--series-2", "#eb6834", 0.14, dash="3 3"))

    # pre-2020 starts: benchmark substitution applies. Drawn early, under
    # the data, so its label at the plot floor overlaps nothing.
    xsub = X(2019.5)
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
             'fill="var(--text-secondary, #52514e)" fill-opacity="0.06"/>'
             % (x0, y1, xsub - x0, y0 - y1))
    p.append('<text class="note" x="%.1f" y="%.1f">2010-2019: priced off '
             'SIBOR, quoted here over SORA</text>' % (x0 + 6, y0 - 8))

    # T1b threshold: every 2010-2015 start clears +1.0 at every reset
    # interval. A labelled dashed line plus an open bracket over the
    # 2010-2015 span make the claim visible without reading the notes.
    y_thr = Y(1.0)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="var(--text-primary, #0b0b0b)" stroke-width="1.2" '
             'stroke-dasharray="2 2" stroke-opacity="0.55"/>' % (x0, y_thr, x1, y_thr))
    x_2015 = X(2015)
    p.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f" '
             'fill="none" stroke="var(--text-secondary, #52514e)" '
             'stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>'
             % (x0, y_thr, x0, y1, x_2015, y1, x_2015, y_thr))
    p.append('<text class="note" x="%.1f" y="%.1f">2010-2015</text>'
             % (x0 + 4, y_thr - 8))

    # zero line: label sits above the plot, clear of every series.
    yz = Y(0.0)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="var(--text-primary, #0b0b0b)" stroke-width="1.5" '
             'stroke-dasharray="4 3"/>' % (x0, yz, x1, yz))
    p.append('<text class="note" x="%.1f" y="%.1f" text-anchor="end">'
             '0 = HDB matched</text>' % (x1, 34))

    path, last = polyline(years, be, years[0], years[-1], ylo, yhi,
                          "--series-1", "#2a78d6", 2.4,
                          pad_r=PAD_R2, pad_t=PAD_T2)
    p.append(path)

    # Point markers, dimmed for start years with under 36 months realised
    # (2024, 2025: the last data month is 2026-07).
    for i, y in enumerate(years):
        op = 0.40 if y >= 2024 else 1.0
        p.append('<circle cx="%.1f" cy="%.1f" r="3" fill="var(--series-1, #2a78d6)" '
                 'fill-opacity="%.2f"/>' % (X(y), Y(be[i]), op))

    # Only two points labelled: 2010, the widest, and 2023, the first start
    # negative at every reset interval.
    i2010, i2023 = years.index(2010), years.index(2023)
    p.append('<text class="lbl" x="%.1f" y="%.1f" '
             'fill="var(--series-1, #2a78d6)">%s</text>'
             % (X(2010) + 10, Y(be[i2010]) - 22, esc("%+.2f" % be[i2010])))
    p.append('<text class="note" x="%.1f" y="%.1f">widest</text>'
             % (X(2010) + 10, Y(be[i2010]) - 6))
    p.append('<text class="lbl" x="%.1f" y="%.1f" text-anchor="end" '
             'fill="var(--series-1, #2a78d6)">%s</text>'
             % (X(2023) - 8, Y(be[i2023]) + 28, esc("%+.2f" % be[i2023])))
    p.append('<text class="note" x="%.1f" y="%.1f" text-anchor="end">'
             'first below zero, every reset</text>'
             % (X(2023) - 8, Y(be[i2023]) + 44))

    # Legend: a single line above the plot, so the plot keeps the full
    # canvas width. Zero-line note shares the row, at the far right.
    ly = 16
    p.append('<rect x="%.1f" y="%.1f" width="10" height="10" rx="2" '
             'fill="var(--series-1, #2a78d6)"/>'
             '<text class="ax" x="%.1f" y="%.1f">R2 realised</text>'
             % (x0, ly - 8, x0 + 16, ly))
    lx2 = x0 + 112
    p.append('<rect x="%.1f" y="%.1f" width="10" height="10" rx="2" '
             'fill="var(--series-2, #eb6834)" fill-opacity="0.14" '
             'stroke="var(--series-2, #eb6834)" stroke-width="1" '
             'stroke-dasharray="2 2"/>'
             '<text class="ax" x="%.1f" y="%.1f">Reset range</text>'
             % (lx2, ly - 8, lx2 + 16, ly))
    lx3 = lx2 + 112
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="var(--text-primary, #0b0b0b)" stroke-width="1.2" '
             'stroke-dasharray="2 2" stroke-opacity="0.55"/>'
             '<text class="ax" x="%.1f" y="%.1f">threshold 1.0</text>'
             % (lx3, ly - 3, lx3 + 12, ly - 3, lx3 + 18, ly))

    p.append('<text class="note" x="%.1f" y="%.1f">Realised to 2026-07. '
             'S$400,000 over 25 years.</text>' % (PAD_L, H - 24))
    p.append('<text class="note" x="%.1f" y="%.1f">2024 and 2025 dimmed: '
             'under 36 months realised.</text>' % (PAD_L, H - 8))

    body = "\n".join(p)
    return svg(body,
               "Realised break-even spread by loan start year, 2010 to 2025",
               "Break-even spread by start year",
               "Every 2010-2015 start clears the 1.0 threshold at every "
               "reset interval; the spread falls below zero from 2023.")


def main():
    os.makedirs(FIGS, exist_ok=True)
    for name, fn in (("chart1_hdb_vs_sora.svg", chart1),
                     ("chart2_breakeven_by_start_year.svg", chart2)):
        dest = os.path.join(FIGS, name)
        with open(dest, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(fn())
        print("%s written" % name)

    caps = [
        "Chart 1. The HDB concessionary rate has been 2.6 per cent throughout, "
        "while compounded 3-month SORA ran far below it for a decade, rose above "
        "it through 2022 and 2023, and fell back below it by 2026.",
        "Chart 2. Realised break-even spread by loan start year, R2, with a "
        "band showing the range across 3, 12, 24 and 36-month reset intervals "
        "(AMENDMENT 3). A dashed line marks the 1.0 threshold discussed in T1b: "
        "every 2010-2015 start clears it at every reset interval. Zero is drawn "
        "because the 2023 to 2025 cohorts fall below it. The 2024 and 2025 "
        "markers are dimmed: under 36 months realised. Pre-2020 starts are "
        "shaded: they were priced off SIBOR and are quoted here over SORA, which "
        "overstates their break-even spread.",
    ]
    with open(os.path.join(OUT, "figure_captions.txt"), "w", newline="\n") as fh:
        fh.write("\n\n".join(caps) + "\n")
    print("out/figure_captions.txt written")
    print("\nRender both and look at them at 390px before they go anywhere.")


if __name__ == "__main__":
    main()
