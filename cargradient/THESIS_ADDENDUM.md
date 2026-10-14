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

## 3. The seal guard test after the data key; first-run checksums (12 October 2026)

Found on the first run of run_all.sh after the data key (commit 800ac1f).
The fixture suite failed on one test,
Guard.test_refuses_real_raw_before_seal. That test asserts that
cargradient/SEALED is absent and that 10_load.py and 15_reproduce.py
refuse cargradient/raw/. It was written for the state before the key and
fails by design once the key exists. No real-data step ran.
- Ruling (Jacob): skip that one test when cargradient/SEALED exists, with
  the skip message "verified before the seal (pre-seal runs and the checker
  saw 10_load.py refuse); not applicable once the data key exists". Test
  code only. The test body is unchanged; the scored path (10_load.py,
  11_tests.py, 15_reproduce.py, cglib.py) is untouched.
- tests/test_pipeline.py md5: 78f4067d46f42a7a889d61a0a5078884 at the
  seal, 22b4f50b7e4bc5046c1dbe55ca12944f after this change
  (`git diff 7ee9b91 -- cargradient/tests/test_pipeline.py`).
- First-run checksums. run_all.sh ends with `14_manifest.py --check`, and
  CHECKSUMS.md5 and number_manifest.csv are written only by hand
  (run_all.sh's header). So on the first real run that last check fails
  because both files are missing, after every real step has already run.
  The accepted handling: run `python3 cargradient/14_manifest.py` to write
  them, then `python3 cargradient/14_manifest.py --check`. No script
  changes.

## 4. More iterations for the pyfixest cross-check (13 October 2026)

Found on the first real run after item 3, and again on a rerun with
nothing changed (12 October 12:59 UTC and 13 October 11:30 UTC; the same
failure both times). Step 11 stopped in crosscheck_pyfixest (section 3's
cross-check for T1 and T2). The scored fit for the test in hand had
finished. pyfixest.feols, refitting the same model to compare, raised
"Demeaning failed after 10000 iterations" (its default iteration limit).
Nothing was written to out/tests.csv and no test number was seen.
- Ruling (Jacob): in crosscheck_pyfixest only, add fixef_maxiter=100000 to
  the feols call. The tolerance (1e-10) and the 1e-6 match rule are
  unchanged. The scored fit (fit_single, tsls), the gates, the outcomes and
  the verdict are untouched, and no scored number changes: the cross-check
  only compares.
- 11_tests.py md5: 4123b37ff7c555bd025df3f2ee96f84b at the seal,
  acdf9862695e6722052930568717fc40 after this change
  (`git diff 7ee9b91 -- cargradient/11_tests.py`).
- If the cross-check still fails with this change, the run stops and is
  reported. No other fix is tried without a ruling.

## 5. The pyfixest cross-check on scaled columns (13 October 2026)

Item 4's change did not cure the cross-check's failure to converge.
- Cause: crosscheck_pyfixest passed unscaled columns (COE x distance,
  about 1e6) to pyfixest.feols with fixef_tol=1e-10, an absolute tolerance
  below float64 precision at that scale. demeaned() already scales every
  column to unit standard deviation for exactly this reason (section 3);
  the cross-check did not.
- Ruling (b) (Jacob): in crosscheck_pyfixest only, fit the same feols call
  on a copy of the data in which yv, cd, qd and every exogenous column are
  divided by that column's standard deviation, computed as demeaned() does
  (numpy std, ddof=0; an sd of 0 becomes 1). fixef_tol (1e-10) and
  fixef_maxiter (100000) are unchanged. The compared coefficient is
  coef['cd'] x sd(yv) / sd(cd).
- Unchanged: the 1e-6 match rule, the tolerance, the scored fit (fit_single,
  tsls), the gates, the outcomes and the verdict. No scored number changes:
  the cross-check only compares.
- 11_tests.py md5: acdf9862695e6722052930568717fc40 before this change
  (after item 4), 5a23d12908ef778e053bab59ecd187ad after it
  (`git diff 9d94ef3 -- cargradient/11_tests.py`).
- The fixture suite passes with the change (73 tests run, 2 skipped).

## 6. The OSF registration of record, and when the data were first run (14 October 2026)

Times are from records the research session can see: git commit
timestamps, the session's file timestamps and run log, the site repo's
history, and the OSF API (api.osf.io, read 14 October 2026 00:57 UTC).
SGT is UTC+8. Where no record gives a time, it says "not confirmed".

- **The first attempt.** OSF registration osf.io/t7dup (item 1),
  submitted 12 October 2026, failed to archive (OSF: errors copying files
  from linked third-party services). The OSF API now answers for t7dup:
  "The requested registration is no longer available." (HTTP 410). Its
  submission time is not confirmed.
- **The registration of record.** It was re-registered as
  https://osf.io/rntsk ("million-dollar flats and COEs", Open-Ended
  Registration) and accepted by OSF Registries: date_registered
  2026-10-12T12:41:27 UTC, that is 12 October 2026, 8:41:27 PM SGT. DOI:
  10.17605/OSF.IO/RNTSK. The API shows it public, not withdrawn and not
  archiving.
- **The seal and the open page came first.** The seal, commit 7ee9b91, is
  timestamped 12 October 2026 11:42:09 UTC (7:42:09 PM SGT). The open
  question page's PR (site PR 36) was merged at 11:51:47 UTC (7:51:47 PM
  SGT, site commit b32f4e6); item 1 records the page live on 12 October.
  The exact time it went live is not confirmed.
- **The data key.** Commit 800ac1f is timestamped 12 October 2026
  12:20:40 UTC (8:20:40 PM SGT), 20 min 47 s before the registration. Its
  push time is not confirmed: GitHub's records were not reachable from
  this session. A commit timestamp is the committer's clock, not GitHub's.
- **Earlier real-data runs exist.** Item 4 records two runs that read the
  resale prices and stopped in step 11's cross-check after a scored fit
  had finished, at "12 October 12:59 UTC and 13 October 11:30 UTC". The
  first is about 18 minutes after the registration (item 4 gives the
  minute only). Item 4 does not say whether
  12:59 UTC is when that run started or when it stopped, so whether the
  first real-data run began after the registration is not confirmed. The
  run before it (item 3) stopped in the fixture suite, and no real-data
  step ran. Item 3's fix, commit a881cc1, is timestamped 12:49:51 UTC.
  No record shows whether the 12:59 UTC run began after that commit.
- **The Checkpoint 1 run** (results in commit 86aeea8). run_all.sh was
  launched at 13 October 2026 14:20:37 UTC (10:20:37 PM SGT), the creation
  time of its log, and ran the fixture suite first. Its first real-data
  step, 10_load.py, wrote its first output (out/coe_quarterly.csv) at
  14:24:59 UTC (10:24:59 PM SGT). So that step began between those two
  times; its exact start was not logged.
- The seal (commit 7ee9b91) and the public open question page are the
  primary record that the predictions preceded the data. The OSF
  registration is a second, independent timestamp.
