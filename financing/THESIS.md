# THESIS: was the HDB concessionary loan actually the cheaper option? (DRAFT)

**DRAFT, NOT SEALED. 17 September 2026.** Revised 17 September 2026 against the
checker's MSG 005. Written while data is still pending, per Jacob's standing rule:
do not touch any data until this file is sealed with numbered survive-if and
fail-if conditions. Everything below is provisional and open to a checker ruling
or a decision from Jacob.

One marker is used. `PENDING` marks an open item that needs sourcing work rather
than a decision. The `(F3?)` marker used in earlier drafts is gone: F3 has been
read and the question it hung on is closed (section 2). `PENDING-JACOB` is also
gone: the switching-cost grid was confirmed by Jacob on 17 September 2026.

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

**F3 has been read, and it confirms the paragraph above rather than overturning
it.** MAS Monthly Statistical Bulletin, Table III.3, "Interest Rates of Banks and
Finance Companies", monthly, is in `raw/f3_mas_msb_iii3_monthly.csv`. Its columns
are, in full:

> End of Period | Prime Lending Rate | Banks Fixed Deposits 3 Months | Banks Fixed
> Deposits 6 Months | Banks Fixed Deposits 12 Months | Banks Savings Deposits |
> Finance Companies Loans - Hire Purchase of New Vehicles For 3 Years | Finance
> Companies Housing Loans For 15 Years | Finance Companies Fixed Deposits 3 Months
> | Finance Companies Fixed Deposits 6 Months | Finance Companies Fixed Deposits
> 12 Months | Finance Companies Savings Deposits

There is **no banks' housing loan rate**. The one housing loan rate published
anywhere in this table belongs to *finance companies*, not banks, and it is used
in this piece only as a labelled side comparison (section 6, S1), never as a proxy
for what a bank charged. The break-even design therefore stands as written, and
this file is sealed on that basis rather than replaced.

F4 (MAS "Data on Housing and Bridging Loans") is **no longer needed**: it was
wanted only as a second chance at the same question F3 has now closed.

**The HDB side is NOT settled without new data. F2 is required for this piece.**
The concessionary rate is 2.6 per cent, pegged 0.1 points above the CPF Ordinary
Account rate, sourced from `raw/hdb_interest_rate_page.pdf` (peg formula) plus
`raw/cpf2.pdf` (Q1 2016) and `raw/cpf3_q3_2026.pdf` (Q3 2026). Those two CPF Board
notices are ten years apart, Q1 2016 to Q3 2026, and both show the OA rate held at
its 2.5 per cent legislated floor.

Two anchor points bracketing a window were an adequate bar for T2 in the published
piece, where the constancy of the rate was a supporting observation and the
headline rested on price and income (MSG 003, G ACCEPTED, `06_tests.py`, 17
September 2026). That bar is **not** adequate here. In this piece the flat 2.6 per
cent is the comparator itself: every break-even spread, every crossover year and
every number in section 6 is computed against it. Two dated anchors show the rate
was 2.6 per cent at two instants; they do not exclude movement between them, and
the cohorts most exposed to such movement are exactly the 2010-2015 starts that
carry the headline. Adopting the weaker bar here because it was accepted there
would be borrowing an evidentiary standard across a change in what the evidence
has to hold up.

So:

- **F2 (CPF interest rate history, 1955 to 2024) is ESSENTIAL, not optional.** It
  is the continuous primary series for the OA rate and therefore, through the peg,
  for the HDB rate across the whole window.
- **F8 (one CPF quarterly announcement from late 2024 or any quarter of 2025) is
  ESSENTIAL for the same reason**, to close the gap between the end of F2 and the
  Q3 2026 announcement already in `raw/`.
- If F2 shows the OA rate moved at any point in 2010-2025, the HDB leg becomes a
  series rather than a constant and sections 3 and 6 are recomputed against that
  series. This is a survivable outcome, not a design failure, but it must be found
  before sealing rather than after publishing.

**F2 IS STILL NOT IN `raw/`, AND THIS IS THE ONE THING BLOCKING THE SEAL.** The
17 September upload did not contain it: the two files offered as F2
(`cpff1.pdf`, `cpff2.pdf`) were CPF current-rate pages, not the history. One was
byte-for-byte redundant and was removed; the other is kept as
`raw/cpf_faq_interest_rates_page.pdf` because its second page carries the official
link to "historical CPF interest rates (PDF, 0.17MB)", which is the provenance
trail for the file still wanted. An attempt to fetch F2 directly from
`cpf.gov.sg` was refused by this environment's network policy (403 at CONNECT),
so it must come from Jacob.

What `raw/` now holds for the HDB leg is **four dated anchor points**, not a
series: Q1 2016 (`cpf2.pdf`), Q1 2025 (`f8_cpf_rates_q1_2025.pdf`, which states
the OA at the 2.5 per cent floor and the concessionary rate "unchanged at 2.6%
per annum from 1 January to 31 March 2025"), Q3 2026 (`cpf3_q3_2026.pdf`), and
the peg formula (`hdb_interest_rate_page.pdf`). Four anchors are better than the
two this file previously relied on, and F8 usefully closes the late end. They are
still anchors. The argument in this section -- that anchors do not exclude
movement between them, and that here the constant *is* the comparator -- applies
to four exactly as it applied to two.

## 3. Design: solve for the break-even spread

**The headline output is the REALISED break-even spread**, not an assumed one and
not a full-tenure one: for each loan start year (cohort), the constant margin over
compounded 3-month SORA at which a bank borrower would have ended **the last data
month** exactly level with an HDB borrower on 2.6 per cent, counting only interest
actually incurred between the loan start and that month.

This is the definition, not a fallback. On a 25-year tenure every start year from
2010 to 2025 runs past 2026, so no cohort's full tenure is observable and a
full-tenure headline would put a forward rate-path assumption inside every single
number. The realised figure contains no forward assumption at all.

**The full-tenure break-even spread is computed and published as a labelled
projection**, never as the headline and never merged into the same number as the
realised figure. It carries the forward path it assumes in its label (section 7,
item 7), and the point at which the assumption begins to bite is marked on every
figure that shows it.

Why solving for the spread is the honest design, not a workaround: the undocumented
quantity (the bank's margin) becomes the output, not a hidden input, so there is
nothing to rig. A reader who knows what they actually paid can locate their own
cohort without being told anything about their own situation. The result is a
function of cohort, refinancing rule and tenure, not an opinion, and it survives
the fact that nobody publishes spreads.

Alongside the break-even spread, a grid of fixed spreads (0.25 to 1.50 points in
steps of 0.25) lets a reader find the row nearest what they actually paid. The
grid is a table of past outcomes, never a recommendation.

**The indistinguishable band, defined here and not left open.** For each cohort,
the indistinguishable band is the interval of spreads within which

    |total interest, bank route - total interest, HDB route| / total interest, HDB route <= 3 per cent

It is reported as an interval in percentage points around the break-even spread,
computed on the realised figures. Where the band is wide, the honest statement is
that the two routes cannot be told apart for that cohort at any spread inside it,
and the article says so rather than reporting a point estimate that implies a
precision the data does not carry. The 3 per cent threshold is the same verdict
threshold used in the published piece, applied here to total interest rather than
to a ratio; it is fixed now, before any data is seen, so that it cannot be chosen
later to produce a particular verdict shape.

## 4. Cohorts, terms, and what is held constant

- **Cohorts.** Every loan start year 2010 to 2025. Fixed: F3 has been read and
  carries no bank rate history that could have moved this range.
- **Tenure.** 25 years, base case. 30 years, sensitivity (section 7.3). Matches
  the published piece's choice of a fixed tenure so a change in maximum tenure
  cannot masquerade as a change in the financing answer.
- **Principal. S$400,000, held identical across both routes and across all
  cohorts.** Stated explicitly so that every published figure has a scale attached
  to it. Two things follow and both are stated in the article:
  - The **break-even spread does not depend on the principal.** Both routes
    amortise the same principal, so scaling it scales both sides' interest by the
    same factor and leaves the spread that equalises them unchanged. The headline
    is therefore principal-free, and S$400,000 is a presentational choice for the
    dollar figures, not an assumption the answer rests on.
  - The **switching cost does depend on it.** Switching costs are fixed dollar
    amounts (legal and valuation fees, subsidy clawback), so they are a larger
    share of a smaller loan. Every R3 and T4 result is therefore reported at the
    stated principal, and section 7 item 5 tests the sensitivity.
  This is a comparison of the cost of the financing choice, not of how much each
  route lets you borrow; the published piece already covers the loan-size channel.
  Loan-to-value schedules, the mortgage servicing ratio and total debt servicing
  ratio caps, and stress rates do not enter the headline calculation. They appear
  only in one sensitivity where principal is allowed to vary with the cap in force
  (section 7, item 7).
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

**Switching cost. CONFIRMED by Jacob, 17 September 2026.** The grid is
**S$0 / S$3,000 / S$6,000**, covering legal and valuation fees net of any subsidy,
plus clawback of subsidies inside a lock-in period. S$0 is the frictionless bound
and is not a claim that switching is free; it isolates how much of the R3 result
is the refinancing rule and how much is the cost of acting on it. The three
figures remain labelled as assumptions wherever they appear -- confirmed by Jacob
is not the same as sourced from a schedule of fees -- but they are no longer an
open decision. T3 (section 6) reports the answer at all three points rather than
at one, so the grid is the sensitivity and no separate half-and-double run is
needed. If the three points give the same verdict, that is a stated finding and
the exactness of the figure stops mattering.

**The asymmetry that is the whole of T4.** An HDB borrower may refinance to a
bank loan but cannot switch back to an HDB loan afterwards. Modelled, not just
described: a cohort that switched to a bank loan before the 2022-2023 rate rise
and was then stuck is the sharpest test case. The switcher is modelled under
**R2** (see T4).

## 6. Pre-registered tests

Each test states a **directional prediction**, decided now, before any rate data
is downloaded, and written so the data can prove it wrong. Each also states what
it reports. The two are separate: a prediction being wrong is a finding to
publish, not a reporting mode to fall back to. "Fail" below means the prediction
was wrong.

All four tests run on the realised basis defined in section 3. Where a full-tenure
figure is also produced, it is labelled a projection and is never what a
prediction is scored against.

**The rate history is public knowledge, and the predictions are built around
that.** Anyone can look up that compounded SORA ran far below 2.6 per cent until
2022 and above it afterwards. The *direction* of most of what follows is
therefore already known, and predicting it correctly demonstrates nothing about
this design. These predictions are written to test **magnitudes and mechanics**
-- how large the realised gap was, which cohorts it actually reached, where the
crossovers fell, and whether the T4 asymmetry bit -- and they are scored on
those. Where a prediction is little more than a restatement of the public rate
path, it is labelled below as low information and carries no evidential weight.

**T1. Realised break-even spread by cohort, base case R2.**
Compute the constant margin over compounded 3-month SORA that would have made a
bank borrower's cumulative nominal interest from loan start to the last data month
equal to the HDB borrower's, for every start year 2010-2025. Report the
indistinguishable band (section 3) alongside each cohort's figure.
- **Prediction 1a, ordering. Low information, see the note above.** The realised
  break-even spread is **higher for 2010-2015 starts than for 2020-2023 starts**,
  and the ordering across those two groups is strict: the minimum over 2010-2015
  exceeds the maximum over 2020-2023. Reasoning stated in advance: the early
  cohorts banked roughly a decade of sub-2.6 per cent benchmark before the 2022
  rise, so a bank could have charged a wide margin and still tied; the later
  cohorts met the rise almost immediately. This follows from the public rate
  path and is stated only so it can be contradicted.
- **Prediction 1b, magnitude. THIS IS THE HEADLINE CLAIM.** The realised
  break-even spread **exceeds 1.0 percentage point for every start year from 2010
  to 2015, without exception.** Not on average, not for most: for every one of the
  six. This is the claim the piece stands on, and it is the one that can fail
  while the direction still holds. If the realised figures land below it, the
  honest reading is that the HDB borrower's loss over the cheap decade was
  smaller than the framing implies, and the piece says so.
- **The 1.0 threshold is, as things stand, a judgement threshold, not derived
  from a source.** An earlier draft of this file justified it by saying that 1.0
  point sat inside the range of margins Singapore banks plausibly charged. That
  sentence has been removed. No document in `raw/` supports it, and asserting
  that a threshold is demanding without being able to show it is the same species
  of unsourced claim this repository exists to keep out -- more dangerous here
  than elsewhere, because it would have made the headline claim look tested when
  it was assumed. The threshold is settled before sealing, by this procedure,
  fixed now:
  **This has now been done, and the answer is that no source supports a number.**
  F5 and F6 were both read on 17 September 2026, before sealing, for any statement
  of mortgage margins, spreads over a benchmark, or average housing loan rates:
  - **F6** describes the structure and confirms section 2, but gives no figure. It
     states that a variable rate mortgage's "interest rate comprises two
     components, a reference rate and a spread", with the reference rate pegged
     either to a public indicator or to "an administered rate which is determined
     by each FI" (page 3), and that MAS expects disclosure of "which component(s)
     of the interest rate can be revised, e.g. spread over reference rate" (page
     7). Nowhere does it publish, or cite, a level or a range for that spread.
  - **F5** gives movements, never a level and never a spread. The only mortgage
     rate figures in the document are that "the median mortgage rate for newly
     originated loans has fallen by around 90 bps since Q2 2024" (page 34) and
     that a stress test applies "a 100 bps increase in mortgage rates", an
     increase which "would bring mortgage rates to around the elevated levels seen
     in 2023 and 2024" (page 36). Both are changes measured from an unpublished
     base. Every other use of "spread" in F5 refers to corporate bond and credit
     spreads, not mortgage spreads.
  **Conclusion, final:** no primary source available to this piece publishes a
  bank mortgage spread over a benchmark, which is the same finding as section 2
  arrived at from the other direction. The 1.0 point threshold is therefore kept
  and is labelled, here and in the article, **a judgement threshold, not derived
  from a source**. It is not presented as calibrated, and the article does not
  imply that it was. F1 remains unopened until this file is sealed.
- **Fail 1:** either prediction is contradicted.
  - **Fail 1a:** the ordering does not hold, or reverses. The article reports that
    the cheap-decade advantage did not survive into realised cost, and says which
    cohorts broke the ordering and by how much.
  - **Fail 1b:** one or more 2010-2015 starts come in at or below 1.0 point. The
    article reports the actual figures and states plainly that the headline claim
    failed, naming the cohorts and the shortfall. It does not retreat to the
    surviving ordering claim as though that were the finding, and it does not
    relabel the threshold after seeing the data.
  Both are publishable results, not reporting fallbacks.
- **Unreliable, separately from pass or fail:** a cohort whose solve does not
  converge is reported as "not computable" with the reason. Non-convergence is the
  **only** unreliability condition. There is no plausibility filter on the value:
  see the note below.

**Negative and large break-even spreads are valid results, not errors.** A start
year whose benchmark path ran above 2.6 per cent (2022 and 2023 starts, most
likely) can only be tied by a bank charging a *negative* margin, that is, lending
below the benchmark. That is a real and interpretable statement about that cohort
-- the HDB loan was cheaper than the benchmark itself, before any bank margin --
and it is published as a negative number with that reading attached. Equally, an
early cohort may produce a spread well above any margin a bank ever charged; that
too is a real statement, namely that no plausible bank offer could have lost to
the HDB loan over the realised window. Any real value is accepted and reported.
The previous draft's 0 to 5 point plausibility filter is removed: it would have
discarded precisely the cohorts that carry the finding, and a filter that rejects
results for disagreeing with a prior is not a check.

**T2. The crossover year, per start year and per grid spread, under R2.**
For each start year 2010-2025 and each grid spread 0.25 to 1.50 in steps of 0.25,
compute the first year in which the cumulative position flips sign, that is, the
year the bank borrower stops being ahead on cumulative interest and the HDB
borrower takes the lead. A spread is required to define a crossover at all: the
previous draft asked for a crossover without one, which is not a computable
quantity. Reported as a **side-note table or heatmap (start year x spread), not a
third headline**; section 9's cap of three headline items is unchanged.
- **Predictions 2a and 2b are expected from public rate history; low
  information.** Both follow from the shape of the SORA path rather than from
  anything this design contributes, and they are stated so the table can
  contradict them, not as the piece's evidence. A reader should weigh T1b and T4
  instead.
- **Prediction 2a:** for start years 2010-2015, at every grid spread at or below
  0.75 points, **no crossover occurs before 2022**; every such crossover falls in
  2022 or later.
- **Prediction 2b:** for start years 2020-2023, at every grid spread, **a
  crossover occurs within 3 years of the loan start**, or the bank borrower is
  never ahead at all (in which case the crossover year is recorded as the start
  year itself).
- **Fail 2:** either prediction is contradicted by the table. The article reports
  the actual pattern and states which prediction failed and where. Cells where no
  crossover occurs inside observed data are reported as "no crossover to date",
  never filled from a projection.

**T3. Sensitivity to the refinancing rule, R2 versus R3, across the switching-cost
grid.**
Run R3 at each of S$0 / S$3,000 / S$6,000 (section 5) and compare with R2.
- **Prediction 3:** the R3 minus R2 gap in realised break-even spread is
  **largest for 2010-2015 starts and below 0.2 points for 2022-2025 starts**,
  because the later cohorts have had too few repricing dates for a refinancing
  rule to act on.
- **Fail 3:** the gap does not shrink with cohort recency. Reported as a finding
  about when refinancing mattered, with the offending cohorts named.
- A previous draft also predicted that the gap narrows monotonically as the
  switching cost rises from S$0 to S$6,000. That clause is **removed**: it holds
  by construction of the R3 rule, which only moves when the saving exceeds the
  cost, so raising the cost can only remove moves and never add them. A
  prediction that cannot fail is not a test, and stating it would have padded the
  count of surviving predictions with one that was never at risk. The
  switching-cost grid is still run and still reported; it is a sensitivity, not a
  prediction.
- **Reporting rule, unchanged:** if R2 and R3 agree within 0.1 points for nearly
  all cohorts at every point on the cost grid, R3 moves to a footnote and the
  headline runs on R2 alone. This is a presentation decision and is independent of
  whether prediction 3 held.

**T4. The borrower who switched from HDB to bank and could not switch back.**
Modelled under **R2, not R3**: the switcher moves once, on a pre-specified date,
and thereafter reprices every three years at the same spread with no further
shopping around. R3 is the wrong rule here because the whole point of T4 is the
borrower who acted once and was then stuck; letting the model refinance
opportunistically afterwards would assume away the trap being measured.

Pre-specified switch years, fixed now: **2012, 2015, 2018 and 2021.** A switch
year Y applies to every loan start year from 2010 to Y-1 inclusive, since the loan
must exist before it can be switched:
- switch 2012: start years 2010-2011
- switch 2015: start years 2010-2014
- switch 2018: start years 2010-2017
- switch 2021: start years 2010-2020

Each (start year, switch year) pair is run at each grid spread, and compared with
the counterfactual of staying on the HDB loan throughout.
- **Prediction 4:** switching in **2021 produces a worse realised total cost than
  staying on the HDB loan, for every start year it applies to and at every grid
  spread**; switching in **2012 or 2015 produces a better one** for at least the
  2010-2011 start years at spreads at or below 0.75. The 2018 switch is the one
  predicted to be close to the line, and no direction is claimed for it.
- **Fail 4:** the 2021 switch is not uniformly worse, or the 2012 and 2015
  switches are not better where predicted. The article reports where the
  asymmetry bit and where it did not, and names the exceptions.
- If no combination produces a worse outcome, T4 is reported as a structural risk
  the design exposes rather than a cost shown to have landed on anyone, and the
  article says so plainly.

**S1. Side comparison: the only published housing loan rate. NOT A HEADLINE, NOT A
PROXY FOR BANKS.**
F3 publishes one housing loan rate for Singapore over this window: "Finance
Companies Housing Loans For 15 Years" (MAS Monthly Statistical Bulletin, Table
III.3, column 8). It is set against the HDB 2.6 per cent as a labelled side
comparison. It is **not** a bank rate, it is **not** used as a stand-in for one,
and no break-even spread, crossover or T4 result is computed from it. It exists
because it would be strange to hold the one published housing loan rate in `raw/`
and not show it, and because its level bounds the discussion from one side.

*Why finance companies are not banks, in one sentence.* Finance companies are
smaller deposit-taking institutions licensed under the Finance Companies Act,
funded largely by fixed deposits rather than by cheap current and savings
balances, and restricted in business lines banks are free to enter, so they fund
themselves at a higher cost and lend to borrowers banks have often declined --
which makes their housing loan rate an **upper bound** on what a bank charged the
same year, not an estimate of it.

*Coverage, established from the file by dates only, before any value was read:*
- The column is populated monthly from **1983-01 to 2022-06**, with **no internal
  gaps**.
- Within the 2010-2025 study window it covers **150 of 192 months**, 2010-01 to
  2022-06.
- The file itself runs to 2023-04, but the last **10 months (2022-07 to 2023-04)
  are empty**: the series stops rather than the file ending.
- **The series therefore ends at the start of the rate rise.** It says nothing
  about 2022-2023, which is the period the whole piece turns on. This is the
  single most important limitation of S1 and is stated wherever S1 appears.

- **Prediction S1:** the finance-company 15-year housing loan rate **exceeded 2.6
  per cent in every month it is published between 2010-01 and 2022-06** -- all 150
  months, without exception.
- **Fail S1:** one or more months come in at or below 2.6 per cent. Reported with
  the months named. A failure here would be genuinely informative: it would mean
  that even a high-cost lender undercut the HDB rate during the cheap decade,
  which would make the bank case stronger than the break-even design assumes it
  needs to be.
- Reported as a side-note chart or table only (section 9), with its end date
  marked on the axis so no reader carries the line past June 2022.

## 7. Sensitivities, all published

1. Refinancing rule: R2 against R3 (R1 dropped, section 5).
2. Start year: every cohort 2010-2025, so the answer is a curve, not an anecdote.
3. Tenure: 25 years base, 30 years alternative.
4. Nominal against present value, discounted at the CPF Ordinary Account rate of
   2.5 per cent.
5. Switching cost in R3: the S$0 / S$3,000 / S$6,000 grid (section 5, confirmed
   by Jacob), reported at all three points as part of T3.
6. Benchmark: SORA throughout, against SIBOR before 2020 if an official history
   can be sourced (F7, PENDING; if not sourced, the pre-2020 numbers carry a
   stated health warning that they are quoted over the wrong benchmark, in a
   known direction, per PRE_THESIS_BRIEFING.md section 4.3).
7. Rate path for the projection only. The realised headline (section 3) contains
   no forward path. The full-tenure projection is published under three: the
   forward path implied by the SGS curve (base), the last observed rate held flat,
   and the long-run average. All three published, with the point where the
   assumption starts to bite marked on the figure. This item depends on F1 (SORA
   and SGS yields), which is in `raw/` but unopened until this file is sealed.

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

1. Realised break-even spread by start year, under R2, with the indistinguishable
   band shown.
2. R3 reported as a band around the R2 line, not a second headline series.
3. T4, the switch-and-cannot-switch-back borrower, as a worked example.

Two things sit in the side-note tier, and neither is a headline: the T2 crossover
table or heatmap (start year x spread), and the S1 finance-company comparison with
its June 2022 end date marked. The full-tenure projection is repository and
RESULTS.md material, never a headline number.

## 10. Chart plan, as the production spec (point F)

Presentation comes before prose. Before any article text is drafted, the pipeline
must deliver, in this order:

1. **Chart 1.** HDB rate against compounded 3-month SORA, 2010-2026, one panel.
2. **Chart 2.** Realised break-even spread by start year under R2 (line or
   points), R3 as a shaded range around it, the indistinguishable band shown, and
   years before 2020 marked distinctly where the benchmark substitution
   (section 7, item 6) applies. Zero is drawn as a labelled reference line, since
   negative values are expected for the 2022-2023 cohorts and must not read as a
   plotting error.
3. **Three headline numbers**, each with the script that generated it named
   alongside it.
4. **One finding**, under 60 characters.
5. **The two side-note items** (section 9): the T2 crossover heatmap (start year
   x spread), and the S1 finance-company housing loan rate against the HDB 2.6 per
   cent, drawn only to June 2022 with the series end marked on the axis and a
   caption saying in as many words that it is a finance-company rate and not a
   bank one.

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
- The full-tenure outcome for every cohort. No 2010-2025 start year completes a
  25-year tenure inside the data, so the full-tenure figure is a projection under
  a labelled rate path and is never reported as an observed result (sections 3
  and 7 item 7).
- Whether any individual borrower's actual spread was inside or outside the
  indistinguishable band. The band is reported per cohort; the article does not
  and cannot place a reader in it.
- What a bank actually charged. F3 has been read and publishes no banks' housing
  loan rate, so the break-even spread remains an inferred quantity and the S1
  side comparison is a finance-company rate, not a bank one. This design cannot
  close that gap, and no public source closes it either.
- Anything about the 2022-2023 rate rise from S1. The finance-company series ends
  in June 2022 (section 6, S1), so the one published housing loan rate stops
  exactly where the interesting period begins.

## 13. Open items, one list

**Blocking the seal, one item only:**

- **F2, the CPF interest rate history.** Not in `raw/`; not fetchable from this
  environment (403 at CONNECT to `cpf.gov.sg`); must come from Jacob. Until it
  arrives the HDB leg rests on four dated anchors rather than a continuous series
  (section 2).

**Open but not blocking:**

- `PENDING` (sourcing): F7, an official SIBOR history for the pre-2020 cohorts
  (section 7 item 6). If it is never sourced, the pre-2020 numbers carry the
  stated health warning and the piece still runs.
- The start date of compounded 3-month SORA inside F1, and whether the early
  window is official or back-calculated. Deliberately not checked: it needs F1
  values, which stay unopened until this file is sealed. It is the first thing
  examined afterwards, and it is a real risk to the 2010-2019 cohorts.

**Closed since the previous draft:**

- F3 read. No banks' housing loan rate; the design stands; every `(F3?)` marker
  removed (section 2). F4 no longer needed.
- The 1.0 threshold. F5 and F6 read; neither publishes a spread or a rate level;
  1.0 is kept and labelled a judgement threshold, not derived from a source
  (section 6). No longer an open item, though it remains a judgement.
- The switching-cost grid, confirmed by Jacob at S$0 / S$3,000 / S$6,000
  (section 5).
- F8 obtained, closing the late end of the CPF anchor set (section 2).
- The indistinguishable band (section 3) and the principal (section 4), both
  settled in earlier drafts.
