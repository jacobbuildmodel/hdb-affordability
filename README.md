# hdb-affordability

Has HDB resale affordability actually worsened, once income and financing are
accounted for?

Not whether prices rose. They did, everyone knows, and a piece establishing it
would be worthless. Affordability is a ratio, and the three things in it moved
independently.

Companion to the article at jacobbuildmodel.github.io/economics/. Everything in the
prose is reproducible from this directory.

**STATUS, 12 September 2026: complete.** `THESIS.md` was sealed before any data was
downloaded. The pipeline rebuilds from `raw/` with one command, all 14 generated
files come back byte-identical, and all 59 checksums verify. The article is
`2026-09-12.md`, still `draft: true`.

## Run order

    rm -rf out figs && ./run_all.sh

which is

| Step | Script | Reads | Writes |
|---|---|---|---|
| 0 | `00_validate_schedule.py` | `grant_schedule.csv` | nothing; exits 3 on any violation |
| 1 | `01_clean.py` | `raw/resale_*.csv` | `out/resale_clean.csv`, `out/clean_report.txt` |
| 2 | `02_hedonic.py` | `out/resale_clean.csv` | `out/index_hedonic.csv`, diagnostics |
| 2b | `02_hedonic.py --lease-spline` | same | `out/index_hedonic_spline.csv`, robustness |
| 3 | `03_basket.py` | `out/resale_clean.csv` | `out/index_basket.csv` |
| 4 | `04_grants.py` | `ehg_bands.csv`, `grant_schedule.csv`, income | `out/grants_by_buyer.csv` |
| 5 | `05_affordability.py` | indices, grants, `ltv_schedule.csv`, income | `out/affordability.csv` |
| 6 | `06_tests.py` | all of the above | `RESULTS.md` |
| 7 | `07_figures.py` | `out/*` | `figs/*.svg`, `out/figure_captions.txt` |
| 8 | `08_manifest.py` | everything | `CHECKSUMS.md5`, audits `number_manifest.csv` |

`run_all.sh` sets `-euo pipefail` and ends by running `python3 08_manifest.py
--check`, so a broken step or a changed output fails the build rather than passing
quietly. `CHECKSUMS.md5` is in two labelled sections, INPUTS and OUTPUTS, so a
source-data change can be told apart from a pipeline change.

`--check` never writes `CHECKSUMS.md5`. Regenerating it is a manual step, after an
intentional change to code or data: run `python3 08_manifest.py` with no flag,
review the diff, then commit it alongside the change.

**Regenerate it as the last edit before committing, not earlier.** Every file in
the INPUTS section, this README included, is hashed. Regenerating the checksums and
then editing any of those files again leaves the committed hash describing a file
that no longer exists, and `run_all.sh` exits 1 on the next clean run. Prove the
result by running `run_all.sh` from a fresh clone of the pushed branch, not from
the working copy the checksums were generated in: a working copy can pass while the
pushed commit fails.

**Revision note, 17 September 2026.** `run_all.sh` previously ran `08_manifest.py`
with no flag (which rewrites `CHECKSUMS.md5`) immediately before `--check`, so the
check compared the file against itself and could not fail. It now only ever runs
`--check`. Separately, `02_hedonic.py` writes `out/index_hedonic.csv` and
`out/index_hedonic_spline.csv` with `float_format="%.10g"`: the OLS solve agrees
with itself to about 12-13 significant digits across machines, not to the last bit,
so unformatted floats made those two files, and only those two, come back
byte-different on a rebuild on different hardware even though every reported
figure was unchanged. Fixed by rounding to 10 significant digits, well past
anything the pipeline ever displays. `CHECKSUMS.md5` was regenerated once against
the fixed output; a deliberately corrupted output file was confirmed to make
`08_manifest.py --check` exit non-zero before the fix was accepted.

**Revision note, 17 September 2026 (second).** `CHECKSUMS.md5` was regenerated
before the revision note above was written, so the committed hash for this README
described the pre-note file and `run_all.sh` exited 1 with `MISMATCH README.md` on
a clean rebuild. Regenerated in the correct order and verified from a fresh clone.
Separately, `run_all.sh` was committed without its executable bit, so the `./run_all.sh`
invocation documented here failed with "Permission denied" on a fresh clone; the
mode is now `100755`. Neither fault changed a single reported figure.

**Revision note, 21 September 2026.** Charts redrawn for phone screens (smallest
text 11.4px at 390px width, previously 6.0px). Layout only; no figure changed.

`08_manifest.py` also audits the article: every number in the prose must appear in
`number_manifest.csv` against the script that produced it. It currently reports
"every prose figure is in the manifest".

Python 3.11.15. Dependencies pinned in `requirements.txt`: pandas, numpy,
statsmodels. Nothing else is imported.

## The question, in one paragraph

Three things moved over the window and a fourth did not. Prices, household incomes
and grants all changed. The cost of borrowing did not: the HDB concessionary loan
rate is pegged 0.1 percentage points above the CPF Ordinary Account rate, the OA
rate has been 2.5 per cent since 1999, so the concessionary rate has been 2.6 per
cent throughout. That is what makes Singapore different. Elsewhere, falling
mortgage rates have repeatedly rescued affordability measures while prices climbed.
Here that rescue was never available, so whatever happened is price, income and
grants and nothing else.

## Measures

Lead measure is the mortgage servicing ratio for a standardised first-timer buyer
of a constant-quality four-room resale flat, on the price net of grants:

    loan          = min( LTV(t) x P*(t),  P*(t) - G(t, p) )
    repayment     = amortise(loan, HDB concessionary rate, 300 months)
    MSR(t, p)     = repayment / monthly household income at percentile p

Reported alongside: price to annual household income on the headline price, and
years of income to accumulate the down payment. Three buyers, at the 20th, 50th and
80th percentile. Full specification, and the pre-registered tests, in `THESIS.md`.

## Window

Complete calendar years **2013 to 2025**. Transactions are on a consistent
registration-date basis from March 2012, so 2013 is the first clean complete year,
and the window then spans a peak, a trough and a peak.

A 2017 start was considered and rejected: resale prices fell from 2013 to 2019 and
rose sharply from 2020, so a 2017 base sits near a cyclical low and flatters any
"affordability worsened" finding before a number is computed. The 2017 to 2025
comparison is still published alongside, labelled as the near-trough base, and if
the two windows disagree that gap is itself reported.

## Composition, the largest threat

The mix of flats sold changes over time, so a rising median price partly measures a
changing basket. Handled two independent ways and both published:

- **`02_hedonic.py`**, log price on year dummies with town, floor area, storey
  midpoint, flat model and remaining lease. The year dummy series is the
  constant-quality path.
- **`03_basket.py`**, median price within town by floor-area cells, aggregated on
  each cell's fixed 2013 transaction share. A Laspeyres index, no functional form.

The raw median four-room price is shown beside both, so a reader sees exactly how
much the correction moved the answer. Test T6 fails the piece to a published range
rather than a point if the two methods diverge by more than 5 percentage points.

## Two corrections documented in `01_clean.py`

**Remaining lease.** The column exists only from the January 2017 file. Earlier
years are reconstructed as 99 minus flat age from `lease_commence_date`, and the
script asserts the reconstruction reproduces the published column on the overlap to
within one year on at least 99 per cent of rows. If it does not, it stops.

**Registration date, not transaction date.** The `month` column is when the resale
was registered, which follows the agreed price by a variable one-to-two-month lag.
No claim here is made at month level. Everything is annual, and the lag applies at
both ends of the window.

## The income basis, which is load-bearing

HDB assesses "total gross income earned including employee's CPF deductions and
excluding employer's CPF contributions and bonuses", averaged over the months
worked in a 12-month period ending two months before the application
(ask.gov.sg, HDB's own channel).

SingStat's household employment income "includes one-twelfth of the annual bonus"
(SingStat's Key Household Income Trends glossary).

So the excluding-employer-CPF series is the right one on the CPF question and still
sits **above** HDB's basis by roughly one month's bonus. Every income-threshold
result is therefore reported as a bound rather than a point. See
`THESIS_ADDENDUM.md` entry 2.

## Files

| File | What it is |
|---|---|
| `THESIS.md` | Pre-registered. Sealed 11 September 2026 before any download. Not edited. |
| `THESIS_ADDENDUM.md` | Everything added after sealing, dated. |
| `DATA_REQUEST.md` | What has to be fetched by hand and from where. |
| `grant_schedule.csv` | The grant and ceiling schedule, with a `status` column per row. |
| `SOURCES.md` | Every source, marked primary or secondary, with retrieval dates. |
| `number_manifest.csv` | Every figure in the prose, its source and its script. |
| `RESULTS.md` | The pre-registered tests and how each came out. Written by `06_tests.py`. |
| `2026-09-12.md` | The article. `draft: true`. |
| `ehg_bands.csv` | The 32 Enhanced CPF Housing Grant band rows, two regimes. |
| `ltv_schedule.csv` | Loan-to-value, stress rate and concessionary rate, with quotes. |
| `TODO_JACOB.md`, `TODO_JACOB_2.md` | What had to be fetched by hand, and the outcome. |
| `CHECKSUMS.md5` | Inputs and outputs, in labelled sections. |

## grant_schedule.csv, its status column, and the check that guards it

Every row carries a `status` and, where it claims primary verification, the quoted
sentence from the source in `source_quote`.

| Status | Means |
|---|---|
| `VERIFIED-PRIMARY` | level and dates evidenced by a quoted primary document |
| `LEVEL-VERIFIED-PRIMARY` | the level is quoted from a primary document, the in-force dates are not |
| `NEEDS-PRIMARY` | from a secondary source, or a government page whose table would not render |
| `NOT-OBTAINED` | nothing yet; not modelled anywhere |

`00_validate_schedule.py` runs first and enforces four invariants, all fatal: a row
claiming primary verification must carry its quote (V1); a CPF_HOUSING_GRANT row's
`income_band_high` must equal the purchase ceiling in force on its start date,
because the grant ceiling is not a separate parameter (V2); date spans within a
grant and scope must not overlap or gap (V3); dated rows need a parseable date and
a numeric amount (V4).

    python 00_validate_schedule.py --selftest

reintroduces a known past error into a temporary copy and fails unless V2 rejects
it. A check nobody has seen fail is not a check. `run_all.sh` runs the selftest
before the validation.

This exists because of a real error, recorded in `THESIS_ADDENDUM.md` entry 4: two
rows about February 2023 carried a ceiling that only took effect in August 2026,
which would have credited an 80,000 grant to households earning 14,001 to 16,000
and understated the headline comparison.

No gap is filled with a plausible number. "Not obtained" is a valid output and
appears in the article where it applies.

## Data provenance

`raw/RETRIEVED.txt` records title, publisher, dataset ID, URL, retrieval date, byte
count and MD5 for every raw file. data.gov.sg republishes the resale file monthly
and SingStat revises household income when the labour force survey is reweighted,
so a reader downloading fresh will get different checksums. That is drift in the
source, not a broken pipeline; compare against the "Data Last Updated" date on the
dataset page.

Do not open the raw files in Excel and re-save them. That rewrites the bytes and
every published checksum stops matching. `.gitattributes` contains exactly
`* -text` so Git does not rewrite line endings on a Windows checkout.
