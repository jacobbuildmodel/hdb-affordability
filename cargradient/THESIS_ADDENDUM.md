# THESIS_ADDENDUM -- cargradient

THESIS.md is sealed (commit 7ee9b9169c36399a80400b0e2e9ef9bd6b5000af,
"cargradient: SEAL", 12 October 2026; THESIS.md md5
e0d0e732d33f031eb30b2fc925e89e49) and is never edited. Changes and records
after the seal go here, dated. None changes a test, a window, a gate or the
verdict rule, or the scoring.

## 1. Registration, and a duplicate line in SEAL_MANIFEST.md (12 October 2026)

**Registration.** The open question page went live on 12 October 2026 at
https://jacobbuildmodel.github.io/open/2026-10-12-million-dollar-flats/
(site PR 36). Jacob registered the thesis on OSF the same day:
- registration: https://osf.io/t7dup (Open-Ended Registration), in project
  https://osf.io/na3vg;
- DOI: not recorded here. The registration was still archiving when this
  was written, and osf.io is not reachable from the research session (its
  proxy refuses the host), so the page could not be read. The DOI goes in a
  later item once Jacob or the checker reads it from the page.

**The duplicate line.** SEAL_MANIFEST.md lists raw/RETRIEVED.txt twice
(lines 7 and 8), with the same md5 (c1bec458113e68e36aa189b09c29d446).
- Cause: 14_manifest.py's seal() checked a path against whole
  "md5  path" lines, so a file that is both named first and found again
  by raw_files() was written twice.
- Effect: none on the seal. The manifest has 65 md5 lines for 64 distinct
  files, each with one md5; the checker verified all 65.
- Fix, for future pieces, without re-running --seal: seal_lines() now
  keeps each path once, and seal() refuses to run if SEAL_MANIFEST.md
  exists. Checked by comparing seal_lines() with the sealed file: they
  match line for line once the duplicate is removed, except 14_manifest.py
  itself.
- So 14_manifest.py's md5 now differs from the seal manifest's:
  a9b605d011ddd66f99853d4a0d6048b4 at the seal,
  fbd4636b1ee1573b8e50b8d22bf71006 after this fix. Only seal() changed
  (`git diff 7ee9b91 -- cargradient/14_manifest.py`). The scored path
  (10_load.py, 11_tests.py, 15_reproduce.py, cglib.py) is unchanged since
  the seal.

## 2. Fixture confidences no longer inherit Jacob's (12 October 2026)

Found when the fixture suite was rerun after item 1. tests/make_fixtures.py
copies THESIS.md into each invented-data scenario and set the scenario's
confidences by replacing the "[Jacob, at seal]" placeholder. With Jacob's
numbers now in THESIS.md there was no placeholder, so every scenario
inherited 70/40/15, and scenario A's Brier check failed (0.391 against
0.203).
- Fix: each scenario's confidence lines are rewritten to its own values,
  or back to the placeholder when it sets none. Test code only; nothing
  reads a real price and the scored path is unchanged.
- tests/make_fixtures.py md5: fed23841476be95c770d85e41527eb1d at the seal,
  8ad594bab474468a63632acebffed5fe after this fix
  (`git diff 7ee9b91 -- cargradient/tests/make_fixtures.py`).
- The suite passes again: 73 tests (one skipped, as before).
