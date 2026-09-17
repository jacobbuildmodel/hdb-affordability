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

Usage:  python3 23_figures.py
"""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")

W, H = 720, 400
PAD_L, PAD_R, PAD_T, PAD_B = 62, 152, 34, 46
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
  .ax   { font-size: 12px; fill: var(--text-secondary, #52514e); }
  .lbl  { font-size: 13px; font-weight: 600; }
  .note { font-size: 11px; fill: var(--text-secondary, #52514e); }
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


def gridlines(ylo, yhi, ticks, fmt):
    x0, x1, y0, y1 = PAD_L, W - PAD_R, H - PAD_B, PAD_T
    p = []
    for t in ticks:
        y = sc(t, ylo, yhi, y0, y1)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="var(--grid, #e4e3df)" stroke-width="1"/>' % (x0, y, x1, y))
        p.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
                 % (x0 - 8, y + 4, esc(fmt(t))))
    return "\n".join(p)


def xlabels(xs, labels):
    x0, x1 = PAD_L, W - PAD_R
    p = []
    for v, lab in labels:
        x = sc(v, xs[0], xs[-1], x0, x1)
        p.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                 % (x, H - PAD_B + 20, esc(lab)))
    return "\n".join(p)


def polyline(xs, ys, xlo, xhi, ylo, yhi, var, fb, width=2.0, dash=None):
    x0, x1, y0, y1 = PAD_L, W - PAD_R, H - PAD_B, PAD_T
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
              % (pt[0] + 10, pt[1] + 18, esc(sub)))
    return s


def legend(items, y_off=0):
    """items: (var, fallback, label) or (var, fallback, label, opacity)."""
    lx, ly = PAD_L + 8, PAD_T + 12 + y_off
    p = []
    for i, it in enumerate(items):
        var, fb, name = it[0], it[1], it[2]
        op = it[3] if len(it) > 3 else 1.0
        p.append('<rect x="%.1f" y="%.1f" width="10" height="10" rx="2" '
                 'fill="var(%s, %s)" fill-opacity="%.2f"/>'
                 % (lx, ly + i * 18 - 8, var, fb, op))
        p.append('<text class="ax" x="%.1f" y="%.1f">%s</text>'
                 % (lx + 16, ly + i * 18, esc(name)))
    return "\n".join(p)


def chart1():
    rows = list(csv.DictReader(open(os.path.join(OUT, "rates_monthly.csv"))))
    rows = [r for r in rows if r["month"] >= "2010-01"]
    xs = list(range(len(rows)))
    sora = [float(r["sora3m"]) for r in rows]
    ylo, yhi = 0.0, max(max(sora), HDB) * 1.15
    p = [gridlines(ylo, yhi, [0, 1, 2, 3, 4], lambda t: "%.0f%%" % t)]

    labels = []
    for i, r in enumerate(rows):
        y, m = r["month"].split("-")
        if m == "01" and int(y) % 3 == 1:
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
                      "unchanged since 1999"))

    path, last = polyline(xs, sora, 0, len(rows) - 1, ylo, yhi, "--series-1", "#2a78d6")
    p.append(path)
    p.append(endlabel(last, "--series-1", "#2a78d6", "%.2f%%" % sora[-1],
                      "3-month SORA"))
    p.append(legend([("--series-1", "#2a78d6", "Compounded 3-month SORA"),
                     ("--series-2", "#eb6834", "HDB concessionary rate")]))
    p.append('<text class="note" x="%.1f" y="%.1f">Monthly, %s to %s. '
             'Source: MAS via data.gov.sg (F1); CPF Board (F2).</text>'
             % (PAD_L, H - 8, rows[0]["month"], rows[-1]["month"]))

    body = "\n".join(p)
    return svg(body,
               "Compounded 3-month SORA against the flat HDB concessionary rate, "
               "2010 to 2026",
               "HDB 2.6% against 3-month SORA",
               "SORA runs far below 2.6 per cent for a decade, rises above it "
               "through 2022 and 2023, then falls back below it by 2026.")


def chart2():
    t1 = list(csv.DictReader(open(os.path.join(OUT, "t1_breakeven.csv"))))
    t3 = list(csv.DictReader(open(os.path.join(OUT, "t3_r2_r3.csv"))))
    r3_at_zero = {int(r["start_year"]): float(r["breakeven_r3"])
                  for r in t3 if r["switch_cost"] == "0" and r["breakeven_r3"]}

    years = [int(r["start_year"]) for r in t1]
    be = [float(r["realised_breakeven_spread_r2"]) for r in t1]
    hi = [r3_at_zero.get(y) for y in years]
    ylo, yhi = min(min(be), -1.5), max(max(v for v in hi if v is not None), 2.4)
    x0, x1 = PAD_L, W - PAD_R
    p = [gridlines(ylo, yhi, [-1, 0, 1, 2], lambda t: "%+.0f" % t if t else "0")]
    p.append(xlabels(years, [(y, str(y)) for y in years if y % 3 == 1 or y == years[-1]]))

    # R3 band: between R2 and R3 at zero switching cost
    top = [(sc(y, years[0], years[-1], x0, x1), sc(hi[i], ylo, yhi, H - PAD_B, PAD_T))
           for i, y in enumerate(years) if hi[i] is not None]
    bot = [(sc(y, years[0], years[-1], x0, x1), sc(be[i], ylo, yhi, H - PAD_B, PAD_T))
           for i, y in enumerate(years) if hi[i] is not None]
    if top:
        d = ("M " + " L ".join("%.1f %.1f" % q for q in top) + " L "
             + " L ".join("%.1f %.1f" % q for q in reversed(bot)) + " Z")
        p.append('<path d="%s" fill="var(--series-1, #2a78d6)" fill-opacity="0.16" '
                 'stroke="none"/>' % d)

    # zero line, labelled, because negative values are expected
    yz = sc(0.0, ylo, yhi, H - PAD_B, PAD_T)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="var(--text-primary, #0b0b0b)" stroke-width="1.5" '
             'stroke-dasharray="4 3"/>' % (x0, yz, x1, yz))
    p.append('<text class="note" x="%.1f" y="%.1f">0 = the HDB loan matched the '
             'benchmark itself, before any bank margin</text>' % (x0 + 4, yz - 6))

    # pre-2020 starts: benchmark substitution applies
    xsub = sc(2019.5, years[0], years[-1], x0, x1)
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
             'fill="var(--text-secondary, #52514e)" fill-opacity="0.06"/>'
             % (x0, PAD_T, xsub - x0, H - PAD_B - PAD_T))
    p.append('<text class="note" x="%.1f" y="%.1f">2010-2019 starts: priced off '
             'SIBOR, quoted here over SORA</text>' % (x0 + 6, H - PAD_B - 8))

    path, last = polyline(years, be, years[0], years[-1], ylo, yhi,
                          "--series-1", "#2a78d6", 2.4)
    p.append(path)
    p.append(endlabel(last, "--series-1", "#2a78d6", "%+.2f" % be[-1], "2025 start"))
    p.append(legend([("--series-1", "#2a78d6",
                      "Realised break-even spread, R2 (points over SORA)"),
                     ("--series-1", "#2a78d6",
                      "Band: up to R3, refinancing at zero switching cost",
                      0.16)]))
    p.append('<text class="note" x="%.1f" y="%.1f">Realised, loan start to '
             '2026-07. S$400,000 over 25 years. Not a projection.</text>'
             % (PAD_L, H - 8))

    body = "\n".join(p)
    return svg(body,
               "Realised break-even spread by loan start year, 2010 to 2025",
               "Break-even spread by start year",
               "The break-even spread falls from about 2 points for 2010 starts "
               "to below zero for 2023 to 2025 starts.")


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
        "Chart 2. Realised break-even spread by loan start year, R2, with the "
        "shaded band running up to R3 at zero switching cost. Zero is drawn "
        "because the 2023 to 2025 cohorts fall below it. Pre-2020 starts are "
        "shaded: they were priced off SIBOR and are quoted here over SORA, which "
        "overstates their break-even spread.",
    ]
    with open(os.path.join(OUT, "figure_captions.txt"), "w", newline="\n") as fh:
        fh.write("\n\n".join(caps) + "\n")
    print("out/figure_captions.txt written")
    print("\nRender both and look at them at 390px before they go anywhere.")


if __name__ == "__main__":
    main()
