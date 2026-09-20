"""
25_manifest.py

The financing piece's own checksum file and number manifest, following the same
rules as the root 08_manifest.py: two labelled sections, and --check never
writes.

  python3 25_manifest.py           regenerate financing/CHECKSUMS.md5 and
                                   financing/number_manifest.csv. Manual step,
                                   run LAST, after every other edit.
  python3 25_manifest.py --check   verify against the committed files and never
                                   write. This is what run_all.sh calls.

INPUTS are the financing scripts plus the raw files this piece actually reads.
OUTPUTS are everything under financing/out and financing/figs. A changed OUTPUT
with unchanged INPUTS means the pipeline is not deterministic.

The number manifest ties every headline figure to the script that produced it,
so no number reaches prose without a traceable origin.
"""

import argparse
import csv
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SCRIPTS = ["20_rates.py", "21_model.py", "22_compute.py",
           "22b_reset_sensitivity.py", "23_figures.py",
           "24_results.py", "25_manifest.py"]
DOCS = ["THESIS.md", "RESULTS.md"]
RAW_USED = ["f1_sora_sgs_monthly.csv", "f2_cpf_interest_rate_history.pdf",
            "f3_mas_msb_iii3_monthly.csv", "f5_mas_fsr_2025.pdf",
            "f6_mas_mortgage_pricing_2021.pdf", "f8_cpf_rates_q1_2025.pdf"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def collect(section):
    out = []
    if section == "INPUTS":
        for n in RAW_USED:
            p = os.path.join(ROOT, "raw", n)
            if os.path.exists(p):
                out.append(("raw/" + n, md5(p)))
        for n in SCRIPTS + DOCS:
            p = os.path.join(HERE, n)
            if os.path.exists(p):
                out.append(("financing/" + n, md5(p)))
    else:
        for d in ("out", "figs"):
            full = os.path.join(HERE, d)
            if not os.path.isdir(full):
                continue
            for n in sorted(os.listdir(full)):
                p = os.path.join(full, n)
                if os.path.isfile(p) and not n.startswith("."):
                    out.append(("financing/%s/%s" % (d, n), md5(p)))
    return out


def build_manifest():
    """Every headline number, against the script and output that produced it."""
    rows = []
    hp = os.path.join(HERE, "out", "headline_numbers.csv")
    if os.path.exists(hp):
        for r in csv.DictReader(open(hp, encoding="utf-8")):
            rows.append([r["id"], r["value"], r["meaning"][:90],
                         "22_compute.py", "financing/out/t1_breakeven.csv"])
    t1 = os.path.join(HERE, "out", "t1_breakeven.csv")
    if os.path.exists(t1):
        for r in csv.DictReader(open(t1, encoding="utf-8")):
            if r["realised_breakeven_spread_r2"]:
                rows.append(["be_%s" % r["start_year"],
                             r["realised_breakeven_spread_r2"],
                             "realised break-even spread, %s start, R2" % r["start_year"],
                             "22_compute.py", "financing/out/t1_breakeven.csv"])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify against the committed files; never writes")
    args = ap.parse_args()

    dest = os.path.join(HERE, "CHECKSUMS.md5")
    man = os.path.join(HERE, "number_manifest.csv")
    sections = [("INPUTS", collect("INPUTS")), ("OUTPUTS", collect("OUTPUTS"))]
    rows = build_manifest()

    if args.check:
        problems = []
        if not os.path.exists(dest):
            print("financing/CHECKSUMS.md5 not found", file=sys.stderr)
            sys.exit(1)
        want = {}
        for line in open(dest, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            digest, name = line.split("  ", 1)
            want[name] = digest
        have = dict(sections[0][1] + sections[1][1])
        bad = [n for n in want if have.get(n) != want[n]]
        for n in bad:
            print("MISMATCH  %s" % n, file=sys.stderr)
            problems.append(n)
        missing = [n for n in have if n not in want]
        for n in missing:
            print("UNRECORDED  %s" % n, file=sys.stderr)
            problems.append(n)
        if os.path.exists(man):
            existing = open(man, encoding="utf-8").read()
            fresh = to_csv(rows)
            if existing != fresh:
                print("MISMATCH  financing/number_manifest.csv", file=sys.stderr)
                problems.append("number_manifest.csv")
        if problems:
            sys.exit(1)
        print("financing: all %d checksums match, number manifest agrees" % len(want))
        return

    with open(dest, "w", newline="\n", encoding="utf-8") as fh:
        fh.write("# MD5 checksums, financing piece. Regenerate with:\n"
                 "#   python3 financing/25_manifest.py\n"
                 "# Never written by run_all.sh, which only runs --check.\n"
                 "# Regenerate LAST, after every other edit; see README.md.\n")
        for label, entries in sections:
            fh.write("\n# ---- %s ----\n" % label)
            for name, digest in entries:
                fh.write("%s  %s\n" % (digest, name))

    with open(man, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(to_csv(rows))

    n = sum(len(e) for _, e in sections)
    print("financing/CHECKSUMS.md5 written, %d files (%d inputs, %d outputs)"
          % (n, len(sections[0][1]), len(sections[1][1])))
    print("financing/number_manifest.csv written, %d numbers" % len(rows))


def to_csv(rows):
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["number_id", "value", "meaning", "script", "output_file"])
    w.writerows(rows)
    return buf.getvalue()


if __name__ == "__main__":
    main()
