# THESIS: was the HDB concessionary loan actually the cheaper option? (DRAFT)

**DRAFT, NOT SEALED. 17 September 2026.** Written while data is still pending, per
Jacob's standing rule: do not touch any data until this file is sealed with
numbered survive-if and fail-if conditions. Everything below is provisional and
open to a checker ruling or a decision from Jacob. Every place whose content
depends on F3 (the MAS Table III.3 column headings, still unread) is marked with
a question mark, `?`. Other open parameters that are not F3-dependent are marked
`PENDING` and named separately, so the two kinds of unknown are not confused with
each other.

Author: hdb (Claude Code session), for the hdb-financing piece. Repository:
hdb-affordability, subdirectory `financing/`.

---

## 1. The question

Was the HDB concessionary loan actually the cheaper option?

It has been fixed at 2.6 per cent since 1999, pegged 0.1 points above the CPF
Ordinary Account rate. Singapore bank mortgage rates ran well below 2.6 per cent
for roughly a decade before rising sharply from 2022. A buyer who chose the HDB
loan in, say, 2015 paid above market for years; whether they came out ahead over
the full loan depends on how long the cheap period lasted, how far rates rose
afterwards, and whether they could have refinanced.

This is a cash-flow comparison over the life of the loan, not a ratio. It is not a
repeat of the published affordability piece, which measured price over income and
found the loan-to-value cap binding by 2025. This measures the cost of the
financing choice itself, which that piece does not touch.

**What this must not become.** No recommendation about which loan anyone should
take. The site publishes reasoning, not advice, and Jacob is not licensed by MAS.
Findings are past tense and cohort-level. See section 8.

## 2. What is already known, before any data is touched

**No public series of the rate Singapore borrowers actually paid on housing loans
exists for 2010 to 2025, fixed or floating, from any official source.** What is
public, primary and continuous is a benchmark: compounded 3-month SORA, from about
2009. The bank rate is that benchmark plus a commercial margin, and no Singapore
authority publishes the margin. MAS's own Information Paper on Residential
Mortgage Pricing and Disclosure Practices (November 2021, `raw/` pending as F6)
states plainly that mortgage pricing reflects each bank's own cost of funds and
competitive position, and that MAS does not intervene in it.

Two things are still unresolved and could change this design:

- **F3 (?).** MAS Monthly Statistical Bulletin, Table III.3, "Interest Rates of
  Banks and Finance Companies," monthly historical CSV, is unread (403 to the
  sandbox that first looked). If it contains a banks' housing loan rate for
  2010-2025, the comparison in section 1 becomes a direct one and this design is
  replaced, not patched. Every downstream section that assumes F3 does not
  contain a housing loan rate is marked `(F3?)`.
- **F4 (?).** MAS "Data on Housing and Bridging Loans" is unread for the same
  reason. Probably volumes rather than rates; one look settles it, marked `(F3?)`
  alongside F3 since both close the same question.

**The HDB side is settled without new data.** The concessionary rate is 2.6 per
cent, pegged 0.1 points above the CPF Ordinary Account rate, sourced from
`raw/hdb_interest_rate_page.pdf` (peg formula) plus `raw/cpf2.pdf` (Q1 2016) and
`raw/cpf3_q3_2026.pdf` (Q3 2026). Those two CPF Board notices are a decade and a
half apart and both show the OA rate held at its 2.5 per cent legislated floor,
which is the same evidentiary bar the checker accepted for T2 in the published
piece's own pipeline (MSG 003, G ACCEPTED, 06_tests.py, 17 September 2026): two
dated primary anchor points bracketing the window, not a downloaded monthly
series. This design adopts that same bar rather than inventing a stricter one
just for this piece.

## 3. Design: solve for the break-even spread

**The headline output is the break-even spread**, not an assumed one: for each
loan start year (cohort), the constant margin over compounded 3-month SORA at
which a bank borrower would have ended the full tenure exactly level with an HDB
borrower on 2.6 per cent.

Why this is the honest design, not a workaround: the undocumented quantity (the
bank's margin) becomes the output, not a hidden input, so there is nothing to
rig. A reader who knows what they actually paid can locate their own cohort
without being told anything about their own situation. The result is a function
of cohort, refinancing rule and tenure, not an opinion, and it survives the fact
that nobody publishes spreads.

Alongside the break-even spread, a grid of fixed spreads (0.25 to 1.50 points in
steps of 0.25) lets a reader find the row nearest what they actually paid. The
grid is a table of past outcomes, never a recommendation.

## 4. Cohorts, terms, and what is held constant

- **Cohorts.** Every loan start year 2010 to 2025. `(F3?)` if F3 turns up a bank
  rate history with a different usable start date, the cohort range is revisited.
- **Tenure.** 25 years, base case. 30 years, sensitivity (section 7.3). Matches
  the published piece's choice of a fixed tenure so a change in maximum tenure
  cannot masquerade as a change in the financing answer.
- **Principal.** Held identical across both routes. This is a comparison of the
  cost of the financing choice, not of how much each route lets you borrow; the
  published piece already covers the loan-size channel. Loan-to-value schedules,
  the mortgage servicing ratio and total debt servicing ratio caps, and stress
  rates do not enter the headline calculation. They appear only in one sensitivity
  where principal is allowed to vary with the cap in force (section 7, item 7).
- **Currency and basis.** Nominal Singapore dollars unless labelled present
  value. No inflation adjustment; stated once and not repeated as a caveat per
  number.

## 5. What happens when a fixed or teaser period ends

Two rules, both published side by side. A third rule, R1 ("never act, roll onto
the floating rate forever"), was considered and dropped: board rates that a
never-acting borrower would roll onto are not published anywhere, so R1 could
only be modelled with an assumed spread step-up, which is exactly the thing this
design exists to avoid inventing. Recorded as a checker ruling, DECISIONS.md,
17 September 2026.

- **R2, reprice on schedule. Base case.** Every three years the loan reprices to
  the then-prevailing benchmark plus the same spread, with no shopping around and
  no change of bank. The closest thing to a neutral assumption.
- **R3, refinance whenever it pays. Upper bound, not a real person.** Move every
  time the saving over the remaining tenure exceeds the switching cost. Reported
  explicitly as an upper bound on what the bank route could have delivered, never
  as a description of a typical borrower.

**Switching cost, R3. PENDING, not F3-dependent.** A single dollar figure for
legal and valuation fees net of any subsidy, plus clawback of subsidies inside a
lock-in period, is needed before R3 can run. Not set yet. Once set, T3 (section
6) tests whether the answer is sensitive to it; if it is not, the figure's
exactness matters less and that becomes a stated finding rather than a loose end.

**The asymmetry that is the whole of T4.** An HDB borrower may refinance to a
bank loan but cannot switch back to an HDB loan afterwards. Modelled, not just
described: a cohort that switched to a bank loan before the 2022-2023 rate rise
and was then stuck on the bank's floating rate is the sharpest test case.

## 6. Pre-registered tests

Each test states its own survive-if and fail-if condition, decided now, before
any rate data is downloaded. "Survive" means the design produces a number worth
publishing as stated; "fail" means the article says explicitly why it does not
and what it reports instead.

**T1. Break-even spread by cohort, base case R2.**
Compute the constant margin over compounded 3-month SORA that would have made a
bank borrower's total nominal interest over the full tenure equal to the HDB
borrower's, for every start year 2010-2025.
- Survive-if 1: the break-even spread is computable and lies in a plausible
  range, 0 to 5 percentage points, for at least three-quarters of cohorts.
- Fail-if 1a: a cohort's computed spread falls outside 0 to 5 points. That
  cohort's number is reported as unreliable (most likely a rate-path or
  tenure-completion artifact, section 7 item 7) rather than published as a
  headline figure.
- Fail-if 1b: cohorts whose 25-year tenure does not complete inside the data
  (roughly start years after 2001, so every cohort in this window) report a
  **realised break-even spread to the last data month** as the headline, and a
  **full-tenure spread under a labelled rate-path assumption** separately, never
  merged into one number. This is the realised-versus-projection split, point A
  below.

**T2. The crossover year, if any, where cumulative position flips, per cohort,
under R2.**
- Survive-if 2: at least one cohort shows an observed (not projected) crossover
  inside 2010 to the present. That gives T4 a concrete year to describe rather
  than a hypothetical.
- Fail-if 2: no cohort crosses inside observed data. Reported as "no observed
  crossover to date" for every cohort, not inferred from a projection.

**T3. Sensitivity to the refinancing rule, R2 versus R3.**
- Survive-if 3: the R3 break-even spread differs from the R2 spread by more than
  0.2 percentage points for at least half of cohorts, meaning the refinancing
  assumption changes the answer enough to justify reporting R3 as a headline
  range rather than a footnote.
- Fail-if 3: R2 and R3 agree within 0.1 points for nearly all cohorts. R3 moves
  to a footnote and the headline runs on R2 alone.
- This test also carries the switching-cost sensitivity (section 5, PENDING):
  once a switching-cost figure is set, T3 is rerun at half and double that figure
  and the result is reported as part of the same test, not a separate one.

**T4. The borrower who switched from HDB to bank and could not switch back.**
- Survive-if 4: at least one cohort and switch-timing combination (switching
  before the 2022-2023 rate rise) produces a worse total-cost outcome under R3
  than staying on the HDB loan throughout. This demonstrates the asymmetry with a
  number rather than an adjective.
- Fail-if 4: no such combination produces a worse outcome in the observed data.
  T4 is then reported as a structural risk the design exposes rather than a cost
  that is shown to have landed on anyone, and the article says so plainly.

## 7. Sensitivities, all published

1. Refinancing rule: R2 against R3 (R1 dropped, section 5).
2. Start year: every cohort 2010-2025, so the answer is a curve, not an anecdote.
3. Tenure: 25 years base, 30 years alternative.
4. Nominal against present value, discounted at the CPF Ordinary Account rate of
   2.5 per cent.
5. Switching cost in R3: PENDING figure, tested at half and double (section 5).
6. Benchmark: SORA throughout, against SIBOR before 2020 if an official history
   can be sourced (F7, optional; if not sourced, the pre-2020 numbers carry a
   stated health warning that they are quoted over the wrong benchmark, in a
   known direction, per PRE_THESIS_BRIEFING.md section 4.3).
7. Rate path for years still in the future, needed because most cohorts on a
   25-year tenure run past the last data month. Base case: the forward path
   implied by the SGS curve. Alternatives: the last observed rate held flat, and
   the long-run average. All three published, with the point where the
   assumption starts to bite marked on the figure. `(F3?)` does not affect this
   item; it depends on F1 (SORA and SGS yields), not F3.

## 8. The compliance line

A historical comparison by loan start year and nothing else. It will not contain
"choose," "should," "better option," "recommend," or any second-person
construction aimed at a decision. Findings are past tense and cohort-level. The
article carries an explicit line stating it is not advice and that Jacob is not
licensed under the Financial Advisers Act. The finished text is grepped against a
banned-word list before handover, same as the published piece.

## 9. Presentation, capped (point E)

The headline is capped at exactly these three things; everything else goes into
the repository plus one side-note table, and the seven sensitivities in section 7
go into `financing/RESULTS.md`, not the article body:

1. Break-even spread by start year, under R2.
2. R3 reported as a band around the R2 line, not a second headline series.
3. T4, the switch-and-cannot-switch-back borrower, as a worked example.

## 10. Chart plan, as the production spec (point F)

Presentation comes before prose. Before any article text is drafted, the pipeline
must deliver, in this order:

1. **Chart 1.** HDB rate against compounded 3-month SORA, 2010-2026, one panel.
2. **Chart 2.** Break-even spread by start year under R2 (line or points), R3 as
   a shaded range around it, years before 2020 marked distinctly where the
   benchmark substitution (section 7, item 6) applies.
3. **Three headline numbers**, each with the script that generated it named
   alongside it.
4. **One finding**, under 60 characters.
5. **Up to three side-note candidates**, for the table mentioned in section 9.

Both charts as SVG, readable at 390px, with a `prefers-color-scheme` dark-mode
block, drawn with the same palette and helpers as the published piece's
`07_figures.py` (reused per PRE_THESIS_BRIEFING.md section 6, no source
dependency).

## 11. Repository placement

New scripts inside `financing/`, numbered from 20 so run order across the whole
repository stays unambiguous against the existing `00` to `08`. Own
`CHECKSUMS.md5` covering financing inputs and outputs, following the same
INPUTS/OUTPUTS split and the same "`--check` never writes it" rule fixed in the
main pipeline on 17 September 2026 (see `README.md`). Own `RESULTS.md`. Reused
without modification: `amortise()` lifted from `05_affordability.py` into the
financing module rather than imported across directories, and the SVG helpers
from `07_figures.py`. Not reused: `grant_schedule.csv`, `ehg_bands.csv`, the
resale transaction data, `01_clean.py` -- none of them bear on a constant-principal
financing-cost comparison.

## 12. What this design cannot settle, known in advance

- Fixed-rate packages are approximated as a constant rate equal to benchmark plus
  spread at inception, labelled as an approximation; no primary source gives an
  actual fixed-package history either.
- The "indistinguishable" band width in break-even terms (the equivalent of the
  published piece's 3 per cent verdict threshold, restated per the checker's
  point B) is not yet a number. It will be set once real spreads exist to check
  it against, not chosen in advance to produce a particular verdict shape, and is
  marked PENDING here rather than guessed.
- `(F3?)` If F3 shows a usable banks' housing loan rate series, this entire
  section 3 design is replaced by a direct comparison, and this file is
  re-sealed from a different section 1 onward rather than patched in place.

## 13. Open items, one list

`(F3?)`: sections 2, 4 (cohort range), 12.
PENDING, not F3-dependent: switching cost dollar figure (section 5), the
indistinguishable-band width (section 12), SIBOR sourcing for pre-2020 years
(section 7 item 6).
