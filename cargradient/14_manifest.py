#!/usr/bin/env python3
"""
14_manifest.py -- the cargradient piece's checksums and number manifest.

  python3 cargradient/14_manifest.py [--root DIR]          write ROOT/number_manifest.csv and
                                                           ROOT/CHECKSUMS.md5. Manual step, run LAST.
  python3 cargradient/14_manifest.py [--root DIR] --check  verify, never write: every md5 matches;
                                                           the manifest rebuilt from out/ equals the
                                                           file; every manifest value appears in
                                                           RESULTS.md as printed.
  python3 cargradient/14_manifest.py --seal                write cargradient/SEAL_MANIFEST.md: the md5
                                                           of THESIS.md, RETRIEVED.txt, every raw file,
                                                           every pre-seal input in out/, every script,
                                                           requirements.txt, run_all.sh and tests/.

CHECKSUMS.md5 lists paths relative to ROOT in two sections. INPUTS: the
scripts, THESIS.md, the raw files and the pre-seal inputs. OUTPUTS: what
10-15 write (out/ results, figs/, RESULTS.md, number_manifest.csv).
"""
import glob
import hashlib
import os
import sys

import cglib as L

SCRIPTS = ["cglib.py", "00_coverage.py", "01_geocode.py", "02_distance.py", "03_unmatched.py",
           "04_coe_crossings.py", "05_street_points.py", "06_coverage_check.py", "10_load.py", "11_tests.py", "12_figures.py",
           "13_results.py", "14_manifest.py", "15_reproduce.py", "run_all.sh", "requirements.txt",
           "tests/make_fixtures.py", "tests/test_pipeline.py"]
PRESEAL_OUT = ["out/addresses.csv", "out/address_rowcounts.csv", "out/blocks_geocoded.csv",
               "out/block_distance.csv", "out/station_points.csv", "out/street_points.csv",
               "out/unmatched.csv", "out/coe_ranges.txt", "out/coe_crossings.txt", "out/coverage.txt",
               "out/coverage_check.csv", "out/coverage_check.txt"]
OUTPUTS = ["out/coe_quarterly.csv", "out/geocode_coverage.csv", "out/panel.csv.gz", "out/tests.csv",
           "out/sensitivities.csv", "out/year_slopes.csv", "out/calc_7a.csv", "out/verdict.txt",
           "out/reproduce.txt", "figs/cargradient_chart1_tests.svg", "figs/cargradient_chart2_years.svg",
           "RESULTS.md", "number_manifest.csv"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def raw_files(root):
    out = []
    for p in sorted(glob.glob(os.path.join(root, "raw", "**", "*"), recursive=True)):
        if os.path.isfile(p) and not p.endswith(".pdf"):
            out.append(os.path.relpath(p, root))
    return out


def manifest_rows(root):
    rows = []
    for fn in ("tests.csv", "calc_7a.csv"):
        for r in L.read_csv(os.path.join(root, "out", fn)):
            pr = L.printed(r["key"], r["value"])
            if pr is not None:
                rows.append((fn, r["key"], r["value"], pr))
    return rows


def write_manifest(root):
    L.write_csv(os.path.join(root, "number_manifest.csv"), ["file", "key", "value", "printed"], manifest_rows(root))


def checksum_lines(root):
    inputs = [s for s in SCRIPTS if os.path.exists(os.path.join(L.CG, s))]
    lines = ["# INPUTS"]
    for rel in ["THESIS.md"] + raw_files(root) + [p for p in PRESEAL_OUT if os.path.exists(os.path.join(root, p))]:
        lines.append(f"{md5(os.path.join(root, rel))}  {rel}")
    for rel in inputs:
        lines.append(f"{md5(os.path.join(L.CG, rel))}  {rel}")
    lines.append("# OUTPUTS")
    for rel in OUTPUTS:
        p = os.path.join(root, rel)
        if os.path.exists(p):
            lines.append(f"{md5(p)}  {rel}")
    return lines


def check(root):
    bad = []
    path = os.path.join(root, "CHECKSUMS.md5")
    if not os.path.exists(path):
        bad.append("CHECKSUMS.md5 missing")
    else:
        for line in open(path):
            if line.startswith("#") or not line.strip():
                continue
            h, rel = line.rstrip("\n").split("  ", 1)
            base = L.CG if rel in SCRIPTS else root
            p = os.path.join(base, rel)
            if not os.path.exists(p) or md5(p) != h:
                bad.append(f"md5 mismatch: {rel}")
    want = manifest_rows(root)
    have = [tuple(r[c] for c in ("file", "key", "value", "printed"))
            for r in L.read_csv(os.path.join(root, "number_manifest.csv"))]
    if [(r[0], r[1], L.fmt(r[2]), L.fmt(r[3])) for r in want] != \
       [(r[0], r[1], L.fmt(r[2]), L.fmt(r[3])) for r in have]:
        bad.append("number_manifest.csv differs from out/")
    results = open(os.path.join(root, "RESULTS.md"), encoding="utf-8").read()
    for fn, key, value, pr in want:
        if pr not in results:
            bad.append(f"{key} printed as {pr} not found in RESULTS.md")
    return bad


def seal():
    lines = ["# SEAL_MANIFEST -- cargradient", "",
             "md5 of every file fixed at the seal. Written by 14_manifest.py --seal in the seal commit.", "",
             "```"]
    for rel in ["THESIS.md", "raw/RETRIEVED.txt"] + raw_files(L.CG) + PRESEAL_OUT + SCRIPTS:
        p = os.path.join(L.CG, rel)
        if os.path.exists(p) and rel not in lines:
            lines.append(f"{md5(p)}  {rel}")
    lines += ["```", ""]
    L.write_text(os.path.join(L.CG, "SEAL_MANIFEST.md"), "\n".join(lines))
    print("wrote SEAL_MANIFEST.md")


def main():
    a = L.args("cargradient checksums, number manifest and seal manifest.",
               lambda p: (p.add_argument("--check", action="store_true"),
                          p.add_argument("--seal", action="store_true")))
    if a.seal:
        seal()
        return
    if a.check:
        bad = check(a.root)
        print("\n".join(bad) if bad else "all checksums and numbers verified")
        sys.exit(1 if bad else 0)
    write_manifest(a.root)
    L.write_text(os.path.join(a.root, "CHECKSUMS.md5"), "\n".join(checksum_lines(a.root)) + "\n")
    print("wrote number_manifest.csv and CHECKSUMS.md5")


if __name__ == "__main__":
    main()
