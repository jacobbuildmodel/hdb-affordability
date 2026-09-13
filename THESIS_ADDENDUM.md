# Addendum to THESIS.md

`THESIS.md` was sealed on 11 September 2026 and is not edited. Everything after it
goes here, dated, newest section last. Nothing here weakens a pre-registered test.
Where something here changes how a test is interpreted, it says so and says why.

---

## 12 September 2026, entry 1: correction to a date in section 2

Section 2 of the sealed file says the ceiling for the CPF Housing Grant for resale
flats, and for an HDB loan, "went from 14,000 to 16,000 over the same period". That
is loose and a reader checking it will notice, because the 16,000 figure is only
weeks old.

The precise path, which is what the analysis uses:

| In force from | HDB loan and CPF Housing Grant ceiling | EHG ceiling |
|---|---|---|
| before 11 Sep 2019 | 12,000 | no EHG; AHG and SHG instead |
| 11 Sep 2019 | 14,000 | 9,000 |
| 24 Aug 2026 | 16,000 | 9,000 |

So for almost the whole window the purchase and CPF Housing Grant ceiling was
14,000, having risen once from 12,000 in September 2019. The 16,000 took effect on
24 August 2026, after the last complete year in the window. It is a fact about
today, not about the period being measured, and the article must not let it sit in
a sentence about the period.

The seven-year freeze claim is unaffected and is if anything sharpened: the EHG
ceiling has been 9,000 since 11 September 2019, while the ceiling beside it moved
twice. The maximum EHG rose from 80,000 to 120,000 on 20 August 2024.

## 12 September 2026, entry 2: the income basis, checked from primary sources, and it moves T7

This was flagged as an inference rather than a sourced fact. It is now sourced, and
the check found something that changes the expected answer.

**HDB's basis, from HDB's own channel.** ask.gov.sg, "How does HDB determine my
average gross monthly household income?", retrieved 12 September 2026:

> "The income considered refers to the total gross income earned including
> employee's CPF deductions and excluding employer's CPF contributions and
> bonuses."

and

> "The gross monthly household income is averaged over the months worked during a
> 12-month period, which ends 2 months preceding the month of the HFE letter
> application."

**SingStat's basis, from SingStat's own glossary.** Key Household Income Trends
glossary, retrieved 12 September 2026:

> "Monthly household employment income includes one-twelfth of the annual bonus."

MOM's concepts page says the same of its annual series.

**What this settles, and what it breaks.**

Settled: HDB excludes the employer's CPF contribution, so the excluding-employer-CPF
series is the correct one and the sealed file's choice stands. The including-CPF
series remains a sensitivity and nothing more.

Broken: HDB also excludes **bonuses**, and SingStat includes one-twelfth of the
annual bonus. The two bases are therefore not the same construct even after the
employer-CPF question is settled. SingStat's excluding-employer-CPF series sits
**above** HDB-assessed income by roughly the monthly-equivalent bonus.

This is not a small wedge. A one-month annual bonus is about 8 per cent of income,
and at the nominal income growth rates of the last decade 8 per cent is on the
order of two years of drift.

**T7 is therefore restated as a bounded test, not a point estimate.** The test
itself, its threshold and its fail conditions are unchanged. What changes is what
the answer is allowed to be called.

- Computing T7 on the SingStat excluding-employer-CPF series gives the **earliest
  possible crossing year**, because that series is an upper bound on HDB-assessed
  income. If it says the median crossed 9,000 in year Y, the true crossing on HDB's
  basis is year Y **or later**.
- If even that upper-bound series has not crossed, F7a fires cleanly and the
  finding is that the median household still qualifies, with the margin reported.
- A second, lower bound is computed by subtracting a documented bonus share. That
  requires a primary figure for the average bonus as a share of annual wages, now
  requested as item D1. If it cannot be sourced, only the upper bound is published
  and the piece says the true crossing year is that year or later, full stop. No
  divisor is invented.

The 1.17 divisor used in conversation to approximate the employer-CPF wedge does
not appear anywhere in the analysis and must not appear in the article. Employer
CPF rates vary by age and are capped at the CPF wage ceiling, so a single divisor
is not a defensible operation on a percentile of a distribution. The
excluding-employer-CPF series is used directly because it exists.

**The crossing-year calculation, stated so a reader can redo it.** The income
series is annual. Let C be the EHG ceiling in force, and I(y) the median monthly
household income from work excluding employer CPF in year y. Find the adjacent pair
of years y0 and y1 = y0 + 1 with I(y0) <= C < I(y1). Then

    crossing year = y0 + (C - I(y0)) / (I(y1) - I(y0))

reported to one decimal place, with I(y0), I(y1) and C printed beside it. Linear
interpolation within a year, which is an assumption and is labelled as one. The
article gives those three numbers in the text, not only in the repository, so a
reader with the published series can reproduce the figure without downloading
anything.

## 12 September 2026, entry 3: what this does to the expected headline

Section 8 of the sealed file names four outcomes and four headlines. The bonus
wedge makes outcome one less likely than it looked and makes the honest version of
it narrower. Both remain publishable and neither is being dropped.

If the upper-bound series crosses and the piece can only say "2023 or later", that
is still the finding, and the headline has to carry the bound rather than a year.
Something shaped like "The grant grew. The middle stopped qualifying." rather than
a headline naming a year the analysis cannot pin down.

If F7a fires, "the median household still qualifies, but only just" is a real
finding and a more surprising one than the consensus, which assumes the middle has
been priced out of everything.

## 12 September 2026, entry 4: an error in a row marked VERIFIED-PRIMARY, and the control added

**The error.** Two rows in `grant_schedule.csv` dated 14 February 2023, for the CPF
Housing Grant, carried `income_band_high = 16000` and were marked VERIFIED-PRIMARY
against MOF Budget 2023 Annex E-1. The annex says:

> "meet the prevailing monthly income ceiling ($14,000 if purchasing with family
> members or other singles, $7,000 if purchasing alone)"

Budget 2023 raised the grant amount from 50,000 to 80,000 for 2- to 4-room resale
flats and did not touch the income ceiling. The 16,000 ceiling took effect on
24 August 2026, after the last complete year in the window. I had written a fact
about today into a row about 2023.

**What it would have done.** Every household earning 14,001 to 16,000 would have
been awarded an 80,000 grant it was not eligible for. That band sits above the EHG
cutoff of 9,000 and below the 80th percentile, so the households wrongly credited
are exactly the upper group in T4. The effect would have been to inflate the
high-income buyer's grants and **understate the T4 divergence**, which is the
headline comparison. A quiet, directional error in the one place it mattered most.

**Why it survived entry.** The file already contained the correct ceiling path in
its `PURCHASE_AND_CPFHG_CEILING` rows. The same fact was held in two places and
only one was right. The contradiction was sitting in plain text and nothing was
reading it.

**Corrections made.** The 2- to 4-room and 5-room rows are now split at
11 September 2019 and 24 August 2026, so each row's `income_band_high` matches the
purchase ceiling actually in force over its span: 12,000 before September 2019,
14,000 from then until 23 August 2026, 16,000 after.

**The control, which is the part that matters.** `00_validate_schedule.py` now runs
before anything reads the schedule, and `run_all.sh` calls it first. Four
invariants, all fatal:

- **V1.** A row claiming primary verification must carry the quoted sentence.
  `source_quote` is a new column and VERIFIED-PRIMARY and LEVEL-VERIFIED-PRIMARY
  both require it to be non-empty. You cannot mark a row as evidenced without
  pasting the evidence. Had that rule existed, writing "16000" next to a quote
  saying "$14,000" would have been visibly absurd at the moment of entry, which is
  where errors are cheapest to catch.
- **V2.** A CPF_HOUSING_GRANT row's `income_band_high` must equal the
  PURCHASE_AND_CPFHG_CEILING in force on that row's start date. The grant ceiling
  is not a separate parameter. It is the purchase ceiling. This is the check that
  catches this specific error mechanically.
- **V3.** Date spans within a grant and scope pair must not overlap or leave gaps.
- **V4.** Dated rows need a parseable start date and a numeric amount.

`python 00_validate_schedule.py --selftest` reintroduces the exact original error
into a temporary copy and fails unless V2 rejects it. A check nobody has seen fail
is not a check. `run_all.sh` runs the selftest before the validation, so a build
that silently loses the invariant fails rather than passing.

**Status vocabulary, now four values and enforced.**

| Status | Means |
|---|---|
| `VERIFIED-PRIMARY` | level and dates evidenced by a quoted primary document |
| `LEVEL-VERIFIED-PRIMARY` | the level is quoted from a primary document, the in-force dates are not |
| `NEEDS-PRIMARY` | from a secondary source, or a government page whose table would not render |
| `NOT-OBTAINED` | nothing yet; not modelled anywhere |

The middle value is new and exists because of this error. Annex E-1 evidences what
the ceiling was in February 2023. It does not evidence when that ceiling started or
stopped. Marking the row fully verified overstated what the document supports, and
the overstatement is what let the wrong number in. Of nineteen rows, two are
VERIFIED-PRIMARY, five LEVEL-VERIFIED-PRIMARY, nine NEEDS-PRIMARY and three
NOT-OBTAINED.

**What this does not change.** No pre-registered test is altered. T4's threshold
and its three fail conditions stand as sealed. The correction moves the expected
result in the direction of more divergence, not less, which is worth stating
plainly: the error would have flattered nothing about the thesis, it would have
weakened the headline comparison.

## 12 September 2026, entry 5: the composition correction ran, and two results the sealed file did not anticipate

Scripts `02_hedonic.py` and `03_basket.py` are written and run on the real data.
121,765 four-room transactions, complete years 2013 to 2025.

**Constant-quality four-room resale price, 2013 to 2025**

| Method | Change |
|---|---|
| Hedonic, year dummies, R-squared 0.876 | +40.4% |
| Fixed 2013 basket, Laspeyres | +37.9% |
| Raw median, no correction | +38.2% |

**T5, did composition matter.** The hedonic and the raw median differ by 2.2
percentage points cumulatively, which clears the 3-point threshold only narrowly.
Reported as: composition mattered, but less than expected, because restricting to
four-room flats had already removed most of the drift before any modelling.

**T6, do the two methods agree. INCONCLUSIVE, and reported as such.** They differ
by 2.5 percentage points, which falls between the 2-point pass threshold and the
5-point fail threshold. Per the sealed file, both are published and the text says
the correction is doing contested work. F6 is not triggered, so a single number may
still be quoted, but it must be quoted with the other method beside it.

A limitation of method B that belongs in the piece: requiring a cell to have at
least five sales in every one of the thirteen years leaves 75 cells out of 298,
covering **58.2 per cent** of 2013 transactions. The fixed basket therefore follows
a little over half the base-year market. That is inherent to a Laspeyres index over
a long window and is why it is the check rather than the headline.

**A gap in my own pre-registration, stated plainly.** T1 was written to pass if the
price-to-income ratio ROSE by more than 0.5 years, and F1 to trigger if it moved by
less than 0.25 years either way. The actual result on the 2013 base is a FALL of
0.39 years. That is neither outcome. I wrote a one-sided test for a two-sided
question and the data landed in the gap between my own thresholds.

The result is therefore reported as what it is, a fall of 0.39 years, and this
paragraph records that the threshold structure did not anticipate it. The
thresholds are not being rewritten after the fact. On the 2017 base the ratio rises
by 0.76 years, so T1 as written PASSES on that base and fails to apply on the other.

**The headline consequence, and why the window argument decided the piece.**

Four-room resale price as a multiple of annual median household income, excluding
employer CPF:

| Year | Years of income |
|---|---|
| 2013 | 5.43 |
| 2019 | 4.04 |
| 2025 | 5.04 |

From the 2013 peak, constant-quality prices rose 40.4 per cent and median household
income rose 51.3 per cent, so the ratio fell. From the 2019 trough it rose steeply.
Today's flat costs about a year less of income than the same flat in 2013 and a
year more than in 2019.

Had the window started at 2017, as originally drafted, the piece would have
reported a clean worsening of 0.76 years and would have been true, one-directional
and materially misleading. The base year decides the sign. That is now the spine of
the article rather than a robustness note.

**Still provisional.** None of this includes grants. The lead measure remains
blocked on the EHG band table.

**One diagnostic to resolve before publication.** In the hedonic, remaining lease
enters with a positive quadratic term, so the marginal value of an extra lease year
rises with lease length: about 0.71 per cent a year at 40 years remaining and 0.85
per cent at 90. Bala's table implies the opposite curvature. The magnitude is small
and the index is a ratio of year dummies, so the effect on the headline is likely
second order, but a spline in lease should be run as a robustness check and the
result reported either way.

## Running list of primary sources added since sealing

All retrieved 12 September 2026.

- HDB, ask.gov.sg, "How does HDB determine my average gross monthly household
  income?" https://ask.gov.sg/hdb/questions/clxsp9q6x0029df0en2tm8ch3
- SingStat, Key Household Income Trends glossary.
  https://www.singstat.gov.sg/-/media/files/publications/households/khitglossary.pdf
- MOM, "Gross Monthly Income from Employment: Concepts and Definitions".
  https://stats.mom.gov.sg/SL/Pages/Gross-Monthly-Income-from-Employment-Concepts-and-Definitions.aspx
- MOM, "Average (Mean) Monthly Earnings: Concepts and Definitions".
  https://stats.mom.gov.sg/SL/Pages/Average-Mean-Monthly-Earnings-Concepts-and-Definitions.aspx
