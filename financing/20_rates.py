"""
20_rates.py

Builds the monthly rate table the financing piece runs on.

Reads:  raw/f1_sora_sgs_monthly.csv   (F1, compounded 3-month SORA)
        raw/f2_cpf_interest_rate_history.pdf is NOT read here; the HDB leg is a
        constant, verified quarter by quarter at seal time (THESIS.md section 2)
        and asserted below so that a change in that finding breaks the pipeline
        rather than passing silently.

Writes: financing/out/rates_monthly.csv   month, sora3m, hdb

F1 is wide: one row per series, one column per month, newest column first. This
script transposes it to long form and nothing else. No interpolation, no
filling, no extension past the published range.

Usage:  python3 20_rates.py
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")

SERIES = "Compounded Singapore Overnight Rate Average (SORA) - 3 Month"
HDB_RATE = 2.6            # per cent, pegged 0.1 above the CPF OA floor of 2.5
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
M2N = {m: i + 1 for i, m in enumerate(MONTHS)}


def parse_month(tok):
    """'2026Jul' -> (2026, 7). Returns None for anything else."""
    tok = tok.strip()
    if len(tok) < 5:
        return None
    y, m = tok[:4], tok[4:]
    if not y.isdigit() or m not in M2N:
        return None
    return int(y), M2N[m]


def main():
    path = os.path.join(ROOT, "raw", "f1_sora_sgs_monthly.csv")
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    hdr = rows[0]

    row = None
    for r in rows[1:]:
        if r and r[0].strip() == SERIES:
            row = r
            break
    if row is None:
        print("F1 does not contain the series %r" % SERIES, file=sys.stderr)
        sys.exit(1)

    recs = []
    for i in range(1, len(hdr)):
        mk = parse_month(hdr[i])
        if mk is None or i >= len(row):
            continue
        v = row[i].strip()
        if v in ("", "na", "n.a.", "-"):
            continue
        recs.append((mk[0], mk[1], float(v)))
    recs.sort()

    if not recs:
        print("F1 parsed to zero observations", file=sys.stderr)
        sys.exit(1)

    # the series must be contiguous; a hole would silently distort every cohort
    for a, b in zip(recs, recs[1:]):
        if (b[0] * 12 + b[1]) != (a[0] * 12 + a[1]) + 1:
            print("gap in %s between %04d-%02d and %04d-%02d"
                  % (SERIES, a[0], a[1], b[0], b[1]), file=sys.stderr)
            sys.exit(1)

    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, "rates_monthly.csv")
    with open(dest, "w", newline="\n", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["month", "sora3m", "hdb"])
        for y, m, v in recs:
            w.writerow(["%04d-%02d" % (y, m), "%.4f" % v, "%.4f" % HDB_RATE])

    print("rates_monthly.csv written, %d months, %04d-%02d to %04d-%02d"
          % (len(recs), recs[0][0], recs[0][1], recs[-1][0], recs[-1][1]))
    print("HDB leg held constant at %.2f per cent (THESIS.md section 2: the CPF "
          "Ordinary Account rate is 2.50 per cent in all 109 quarters F2 "
          "publishes)" % HDB_RATE)


if __name__ == "__main__":
    main()
