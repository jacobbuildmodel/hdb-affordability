"""
08_manifest.py

Two jobs, both mechanical.

  1. Checks that every number appearing in the prose of the article is listed in
     number_manifest.csv with the script that produced it. Numbers in the article
     that the manifest does not know about are reported, and so are manifest rows
     pointing at outputs that do not exist.

  2. Writes CHECKSUMS.md5 in two labelled sections, INPUTS and OUTPUTS, so a
     reader can tell a source-data change apart from a pipeline change.

Reads:  number_manifest.csv, 2026-09-12.md, raw/*, out/*, figs/*, and the scripts
Writes: CHECKSUMS.md5, but only when run without --check

Usage:  python 08_manifest.py             regenerate CHECKSUMS.md5 (manual step,
                                           after an intentional change; see README)
        python 08_manifest.py --check     verify against the committed CHECKSUMS.md5
                                           and never write it. This is what
                                           run_all.sh calls.

Revision note, 17 September 2026: run_all.sh used to call this script once with no
flags (which rewrites CHECKSUMS.md5) and then again with --check, so the check was
always against a file this same run had just produced, and could not fail. --check
now never writes and is checked against whatever CHECKSUMS.md5 was already on disk.
"""

import argparse
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTICLE = "2026-09-12.md"
SCRIPTS = ["00_validate_schedule.py", "01_clean.py", "02_hedonic.py", "03_basket.py",
           "04_grants.py", "05_affordability.py", "06_tests.py", "07_figures.py",
           "08_manifest.py"]
TABLES = ["grant_schedule.csv", "ehg_bands.csv", "ltv_schedule.csv",
          "number_manifest.csv"]
DOCS = ["THESIS.md", "THESIS_ADDENDUM.md", "README.md", "SOURCES.md", "HANDOVER.md",
        "RESULTS.md", "DATA_REQUEST.md", "requirements.txt", "run_all.sh",
        ".gitattributes", "LICENSE", ARTICLE]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def collect(section):
    out = []
    if section == "INPUTS":
        for name in sorted(os.listdir(os.path.join(HERE, "raw"))):
            p = os.path.join(HERE, "raw", name)
            if os.path.isfile(p):
                out.append(("raw/" + name, md5(p)))
        for name in SCRIPTS + TABLES + DOCS:
            p = os.path.join(HERE, name)
            if os.path.exists(p):
                out.append((name, md5(p)))
    else:
        for d in ("out", "figs"):
            full = os.path.join(HERE, d)
            if not os.path.isdir(full):
                continue
            for name in sorted(os.listdir(full)):
                p = os.path.join(full, name)
                if os.path.isfile(p) and not name.startswith("."):
                    out.append(("%s/%s" % (d, name), md5(p)))
    return out


def audit_numbers():
    """Every number in the prose should be traceable via number_manifest.csv."""
    path = os.path.join(HERE, "number_manifest.csv")
    if not os.path.exists(path):
        return ["number_manifest.csv is missing"]
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    problems = []
    for r in rows:
        out = (r.get("output_file") or "").strip()
        if out and out.lower() not in ("none", "n/a") and \
                not os.path.exists(os.path.join(HERE, out)):
            problems.append("manifest row %s points at missing %s"
                            % (r.get("number_id", "?"), out))

    art = os.path.join(HERE, ARTICLE)
    if os.path.exists(art):
        text = open(art, encoding="utf-8").read().split("---", 2)[2]
        text = text.split("## Sources")[0]
        text = re.sub(r"\{\{<\s*aside.*?\{\{<\s*/aside\s*>\}\}", "", text, flags=re.S)
        found = set()
        # a trailing dot is sentence punctuation, not a decimal point
        for m in re.findall(r"\d[\d,]*(?:\.\d+)?", text):
            v = m.replace(",", "").rstrip(".")
            if len(v.replace(".", "")) >= 2:
                found.add(v)
        known = set()
        for r in rows:
            v = (r.get("value") or "").replace(",", "").strip()
            if v:
                known.add(v)
        unknown = sorted(found - known, key=lambda s: -len(s))
        if unknown:
            problems.append("numbers in the prose not in the manifest: %s"
                            % ", ".join(unknown[:25]))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify against the committed CHECKSUMS.md5; never writes it")
    args = ap.parse_args()

    dest = os.path.join(HERE, "CHECKSUMS.md5")
    sections = [("INPUTS", collect("INPUTS")), ("OUTPUTS", collect("OUTPUTS"))]

    problems = audit_numbers()
    if problems:
        print("NUMBER AUDIT, %d item(s) to look at:" % len(problems))
        for p in problems:
            print("  " + p)
    else:
        print("number audit: every prose figure is in the manifest")

    if args.check:
        if not os.path.exists(dest):
            print("CHECKSUMS.md5 not found", file=sys.stderr)
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
        if bad or problems:
            sys.exit(1)
        print("all %d checksums match" % len(want))
        return

    with open(dest, "w", newline="\n") as fh:
        fh.write("# MD5 checksums. Regenerate with: python 08_manifest.py\n")
        fh.write("# This file is never written by run_all.sh (it only runs --check).\n")
        fh.write("# Regenerating it is a manual step after an intentional change to\n")
        fh.write("# code or data; see README.md.\n")
        fh.write("# Two sections. A changed INPUT means the source data or a script\n")
        fh.write("# moved. A changed OUTPUT with unchanged INPUTS means the pipeline\n")
        fh.write("# is not deterministic and something is wrong.\n")
        for label, entries in sections:
            fh.write("\n# ---- %s ----\n" % label)
            for name, digest in entries:
                fh.write("%s  %s\n" % (digest, name))

    n = sum(len(e) for _, e in sections)
    print("CHECKSUMS.md5 written, %d files (%d inputs, %d outputs)"
          % (n, len(sections[0][1]), len(sections[1][1])))


if __name__ == "__main__":
    main()
