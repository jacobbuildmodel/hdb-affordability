# THESIS -- cargradient piece

**UNSEALED DRAFT, 5 October 2026; reframed 6 October 2026** (title chosen
by a real reader; Rule 0 item 5; a reported calculation; the verdict in
plain words). Nothing here is fixed until the commit
"cargradient: SEAL". Until then this file changes by ordinary edits on
cargradient-wip, recorded in the commit history. After the seal it is never
edited; changes go in THESIS_ADDENDUM.md, dated, and are reported, not
applied to the scoring.

Written before any HDB resale price was opened. The resale files were read
for labels, coverage and addresses only (office/FEASIBILITY.md). COE values
were read; they are not the outcome, and the checker allowed it (round 3,
item 4).
- The hook's sources (Parliament records, 6 October 2026) carry HDB
  price-level information: counts of million-dollar flats, and the
  Minister's examples of 4-room prices in named towns.
- None of it bears on the COE x distance link (DESIGN_SKETCH item 9).

Author: research session. Repository: hdb-affordability, subdirectory
`cargradient/`, branch `cargradient-wip`. The title and the opening are not
part of this file. The title, chosen by a real reader on 5 October 2026, is
"Million-dollar flats came with $100,000 COEs. Coincidence?" (office/TITLES.md).
The verdict rule (section 8) answers it in plain words.

**Confidences are Jacob's**, set at the seal. None appears in this draft.
Each test carries "Confidence at seal: [Jacob, at seal]". T3's direction and
Jacob's Why are his (round 3), verbatim.

**A conceptual replication.** Huang, Li and Ross (2018) estimated this on
private non-landed homes (URA REALIS, paid), 2002Q2 to 2015Q4. These tests
use public HDB resale data, which they left out on purpose (their p. 9).
Every public line says so. Paper references are to the working-paper
version (office/PAPER_NOTES.md).

## 1. The question

**What people argue about** (office/RULE0.md). Million-dollar HDB flats and
$100,000 COEs are both constant headlines, argued about separately.
- Flats sold for $1 million or more rose "from 46 flats in 2017 to 259 flats
  in 2021" (MND, 4 Jul 2022). In 2025, "about 6% of resale flats transacted
  above $1 million" (MND, 7 Apr 2026).
- Category B COEs were first at or above $100,000 in June 2022, and
  Category A in April 2023 (SingStat M651121).

**The belief on trial.** Car prices and flat prices are separate stories. A
COE is a car-owner's problem.

**The rival explanation** (the paper's). When owning a car costs more, living
near town is worth more. So part of the near-town premium moves with the COE.

**The honest limit, stated up front.** At most, this explains part of the
near-town premium, not million-dollar flats as a whole. Nothing in this file
says where million-dollar flats are.

**Sealed question 1.** "When COE premiums were higher, did HDB resale flats
near Raffles Place gain relative to flats further out, as the paper found for
private homes, over its years (2002 to 2015) and since (2016 to 2026)?"

**Sealed question 2.** "After growth in the car quota was cut to zero in
February 2018, did that tilt get weaker?"

Question 1 tests the belief directly: a tilt means the COE reaches flats.
Question 2 asks whether the tilt changed after the 2018 policy. T1 and T2
answer question 1; T3 answers question 2.

## 2. The two extremes (thought experiments, labelled as such)

- **Cars nearly free.** Every household drives. Distance costs little time,
  so a flat near the end of the line costs little less than one near town.
  A change in the price of cars barely moves the gap.
- **Cars nearly unaffordable.** Almost nobody drives, and every household
  lives by the train timetable. Nearness to the centre is everything. A
  further rise in the price of cars changes little, because few were driving
  anyway.
- **Singapore sits between them.** Some households are on the edge of owning
  a car. A rise in the COE tips some of them into going without, and they
  then pay more to live close in. That edge is where the paper's tilt comes
  from (its pp. 10-11).

These are pictures of the two ends, not claims about the data.

## 3. Why this is answerable, and how far

**The estimating equation** (the paper's equation (1), p. 11, in its
column (4) form, Table 3b, p. 30, adapted to HDB data):

    p_ibq = beta * COEP_q x DD_b + kappa * POST12_q x DD_b
            + gamma_b + delta_q + lambda_{L(i),q} + X_i' theta + u_ibq

- `p_ibq`: resale price per square metre of sale i in block b in quarter q,
  in Singapore dollars (levels, as the paper uses). The paper takes project
  medians because its units are near-identical within a project (p. 14). HDB
  blocks mix flat types, so this uses each sale, with controls.
- `COEP_q`: the quarterly COE premium, categories A and B. Each bidding's A
  and B premiums are weighted by successful bids, then the biddings in the
  quarter are averaged (p. 14). Source: SingStat M651121.
- `DD_b`: great-circle distance in km from block b to Raffles Place MRT
  station. The station point is the mean of its exit points in the LTA exit
  layer.
- `POST12_q x DD_b`: Jacob's option (a) for the March 2012 switch from
  approval date to registration date (T1 only; section 5).
- `gamma_b`: block fixed effects. They take each block's fixed distance and
  amenities, as the paper's project effects do.
- `delta_q`: year x quarter fixed effects. They take the COE level and the
  whole market; `COEP_q` alone is absorbed, as in the paper's column (4).
- `lambda_{L(i),q}`: remaining-lease band (5-year bands) x year-quarter
  fixed effects. The price of a given lease left may change every quarter
  (checker item 5).
- `X_i`: flat type, storey range, floor area and flat model.
- **IV** (p. 13): `COEP_q x DD_b` is instrumented by `COEQ_q x DD_b`, the
  quarterly A plus B quota built the same way.
- **The test number:** `beta`. The paper's sign is negative: when COEs cost
  more, prices fall faster with distance.

**How far.**
- The IV gives a causal reading only if the quota is unrelated to
  distance-specific shifts in demand. That is the paper's assumption (p. 13),
  and it is not tested here.
- A negative `beta` on HDB data says the tilt is there. It does not show the
  paper's mechanism (car-free households) in HDB buyers.
- HDB buyers face eligibility rules, income ceilings and grants that private
  buyers do not (the paper's p. 9). The piece reports, and does not explain
  away, any difference from the paper.

## 4. Data (pointers; detail in office/FEASIBILITY.md)

- **HDB resale** (data.gov.sg collection 189), five datasets, 1990 to 2026.
  This piece uses 2000-Feb 2012 (approval date) and Mar 2012 onward
  (registration date). Fields: month, town, flat_type, block, street_name,
  storey_range, floor_area_sqm, flat_model, lease_commence_date, and
  resale_price (the outcome, unopened).
- **COE:** SingStat M651121 (data source LTA), 2002 Feb to 2026 Sep, saved
  in raw/singstat_M651121/. No bidding was held in April to June 2020.
- **Block coordinates:** OneMap Search, 5 October 2026, 10,016 unique
  block and street pairs.
  - 9,856 were matched on block and street: 9,855 exact, 1 expanded.
  - 160 were not matched.
  - Unmatched sales: 0.83 per cent of T1's window and none of T2's
    (office/GEOCODE_REPORT.md).
  - Fallback (Jacob, 6 October 2026, option C): the 160 unmatched pairs are
    left out of the scored runs. Street-level points are a reported
    sensitivity (section 7, J).
  - The exclusion is not random. 111 of the 160 last sold before 2010
    (likely SERS or demolished), and older estates sit nearer town. At 0.83
    per cent of T1's rows and none of T2's, it is disclosed, not corrected.
- **Raffles Place and City Hall MRT:** data.gov.sg exit layer
  d_b39d3a0871985372d7e1637193335da5 (10 and 4 exits).
- **The vehicle growth rate, step by step** (Parliament, raw/hansard/; LTA,
  raw/):

  | Rate per annum | From | Source |
  |---|---|---|
  | 3% | 1990 | MOT, 5 Feb 2013 |
  | 1.5% | 2009 | MOT, 5 Feb 2013 |
  | 1% | 2012 (the month is not in the saved record) | MOT, 5 Feb 2013 |
  | 0.5% | February 2013 | MOT, 5 Feb 2013 |
  | 0.25% | by 11 March 2015 ("We have lowered ... from 0.5% per annum to 0.25%"), "effective until January 2018" | MOT, 11 Mar 2015; MOT, 9 May 2016 |
  | 0% (A, B and D) | February 2018 ("from the current 0.25% per annum to 0% with effect from February 2018") | MOT, 6 Nov 2017; LTA, 13 Aug 2020 |

  - The October 2017 announcement itself is not found as a primary
    source. Parliament's 6 Nov 2017 answer shows the change was public by
    then. Both dates fall inside T3's dropped quarters.

## 5. Windows, fixed now (quarters)

- **T1: 2002Q2 to 2015Q4**, the paper's own window (p. 4). 2012Q1 is
  dropped: it mixes approval-date and registration-date sales, and a sale
  approved in February and registered in March can sit in both files
  (Jacob's option (d)). `POST12_q x DD_b` is in (option (a)). 54 quarters.
- **T2: 2016Q1 to 2026Q3**, the last full quarter before the seal. It is
  fixed now, and does not move if the seal slips. 2020Q2 has no bidding and
  is dropped. 42 quarters.
- **T3:**
  - Before-window: 2012Q2 to 2017Q3, 22 quarters, registration date
    throughout (approved by Jacob, 5 October 2026).
  - Disclosed: this window was chosen after seeing COE ranges, not prices.
    COE is not the outcome, and the checker allowed reading it.
    2016Q1-2017Q3 (7 quarters) stays as a reported sensitivity (section 7,
    G).
  - After-window: 2018Q2 to 2026Q3, less 2020Q2, 33 quarters.
  - Dropped: 2017Q4 to 2018Q1, between the announcement and the first full
    quarter of 0 per cent growth.
  - **What T3 compares, exactly.** The before-window is not one 0.25%
    period. It spans step-by-step cuts:
    - 1.5% or 1% in 2012 (the month of the 2012 cut is not in the saved
      record);
    - 0.5% from February 2013;
    - 0.25% from early 2015 (in force by 11 March 2015) to January 2018.

    The after-window is 0% throughout. So T3 compares a period of
    step-by-step cuts against 0%, not 0.25% against 0%. The window and the
    bet are Jacob's, approved; this only describes them correctly. Jacob's
    Why line speaks of the last step (0.25% to 0%) and stays verbatim.
- **COE movement in each window** (out/coe_ranges.txt; COE is not the
  outcome):
  - T1: high over low 23.03.
  - T3 before: 1.81.
  - T3 after: 4.60.
  - The before-window as first drafted (2016Q1 to 2017Q3) was 1.18, too
    flat to read. That is why the window moved.

## 5A. What the theory says (context only)

The paper's model (pp. 10-11) has two bid-rent curves, one for households
that drive and one for those that take the train. Prices follow the higher
of the two. A dearer car moves the households between the two crossing
points onto the train, and raises what they pay near the centre. The model
predicts the sign of `beta`, not its size.

## 6. Pre-registered tests

Three tests are scored: T1, T2 and T3. A failed prediction is a finding to
publish, not a reason to change the test. Thresholds marked "judgement" are
the researcher's, with reasons, and Jacob accepts or changes them before the
seal.

**Two gates, outcome-blind, for every test.** Neither uses a price.
- **Geocoding:** the test is NOT SCORED if fewer than 95 per cent of the
  window's sales match a geocoded block (judgement: a larger gap could be
  concentrated in demolished, older, central estates).
- **First stage:** the test is NOT SCORED if the first-stage F statistic
  for `COEP_q x DD_b` is below 10 (judgement: the usual weak-instrument
  line). For T3 this is checked in each window, before and after; a value
  below 10 in either means T3 is not scored (approved by Jacob, 5 October
  2026).

### T1. Their sign, on HDB flats, over their years

- **Estimate.** `beta` on 2002Q2 to 2015Q4, less 2012Q1, with
  `POST12_q x DD_b`.
- **Prediction.** When COEs cost more, HDB flats near Raffles Place gained
  relative to flats further out.
- **Survive if:** `beta` < 0 and its 95 per cent interval (clustered by
  block) excludes zero.
- **Fail if:** the interval includes zero, or `beta` > 0.
- **Weak evidence, stated now.** COE premiums rise in good times. If good
  times also lift central flats more than outer ones, for reasons that have
  nothing to do with cars, `beta` turns negative without the paper's
  mechanism. The year-quarter effects take out the level of the market, not
  a tilt in it. So a SURVIVE is weaker evidence for the car channel than a
  FAIL is against it.
- **Confidence at seal: [Jacob, at seal].**

### T2. The same, 2016 to 2026

- **Estimate.** `beta` on 2016Q1 to 2026Q3, less 2020Q2. No `POST12` term;
  all sales are on the registration-date basis.
- **Survive if / Fail if:** as T1.
- **Weak evidence, stated now.** As T1. Also, this window holds both the
  2018 change and the pandemic years. T2 reads the average tilt over all of
  it; T3 asks whether it changed.
- **Confidence at seal: [Jacob, at seal].**

### T3. Weaker after February 2018 (Jacob's direction)

- **Estimate.** One regression on the before-window and the after-window
  together. Every term in section 3 is allowed to differ after 2018,
  including `beta`. The test number is `beta_after - beta_before`: the
  coefficient on `COEP_q x DD_b x AFTER_q`, instrumented by
  `COEQ_q x DD_b x AFTER_q`.
- **Prediction.** After growth in the car quota was cut to zero in February
  2018, a rise in the COE tilted HDB prices toward the centre less than
  during the step-by-step cuts before it (section 5).
- **Survive if:** `beta_after - beta_before` > 0 (closer to zero, a flatter
  tilt), with its 95 per cent interval excluding zero.
- **Fail if:** the interval includes zero ("no clear change"), or the
  difference is negative (stronger).
- **Not scored if:**
  - `beta_before` is not negative with an interval excluding zero. There is
    then no tilt before 2018 to weaken, and the verdict says so.
  - Either gate fails in either window.
- **Weak evidence, stated now.**
  - A WEAKER result cannot say whether rail, working from home or something
    else caused it. Jacob's bet is about direction, not the reason.
  - The before-window has less COE movement than the after-window (1.81
    against 4.60, high over low). So `beta_before` is the noisier of the
    two, and that leans toward "no clear change", a FAIL.
  - Jacob's own best guess is close to "no clear change" (his Why, below).
- **Why (Jacob, verbatim):** "I'd lean weaker, but not by much. The
  "stronger" story needs a big change, and 2018 was a small one. Moving from
  0.25% growth to 0% hardly changes how many households can get a car. It's
  hard to see that pushing many more families to stay car-free and pay up for
  flats near town. Most of what changed after 2018 cuts the other way. New
  rail lines and working from home both make living further out cheaper in
  time and effort. Either would make a COE rise matter less for where people
  choose to live. Two catches. A weaker result wouldn't tell you whether rail
  or COVID caused it, so the bet is about direction, not the reason. And my
  honest best guess is close to "no clear change," given how small the 2018
  change was."
  - Note: the 0.25% before February 2018 is confirmed (MOT, 6 Nov 2017,
    "from the current 0.25% per annum"). The before-window as a whole
    spans 1.5% or 1%, then 0.5%, then 0.25% (section 5). The Why line
    stays as written.
- **Confidence at seal: [Jacob, at seal].**

### Computation, fixed with the analysis scripts (before the seal)

As for the sgd and pwm pieces:
- scripts 10 onward are written blind, before the seal;
- a synthetic test suite on invented data forces every outcome branch,
  including both gates and T3's not-scored rule;
- a `SEALED` guard file stops the loader reading resale_price before the
  seal;
- every printed number goes through one function;
- an independent reproduction script re-derives every scored number.

Before the seal:
- `00_addresses.py` (addresses only);
- `01_coe_ranges.py` and `04_coe_crossings.py` (COE only);
- `01_geocode.py`, `02_distance.py` and `03_unmatched.py` (addresses, OneMap
  and row counts only).

None of these reads a resale price.

## 7. Sensitivities (sealed, reported, not scored)

- **A. The split run (Jacob's option (c)).** T1 on 2002Q2 to 2011Q4
  (approval date only) and 2012Q2 to 2015Q4 (registration date only),
  separately.
- **B. City Hall** as the centre (the paper's Table 5).
- **C. Log price** per square metre instead of levels.
- **D. OLS** beside every IV estimate (the paper's Table 2).
- **E. Two-way clustering** by block and quarter, beside the block-clustered
  interval, for every test (checker item 7). With 22 to 54 quarters, it
  rests on few time clusters.
- **F. Without 2020 to 2022** (checker item 6). T2 and T3's after-window
  drop 2020Q1 to 2022Q4. The after-window keeps 22 quarters, with COE high
  over low still 4.60.
- **G. T3's first-drafted before-window**, 2016Q1 to 2017Q3 (7 quarters).
- **H. Planning-area x year linear trends** (the paper's column (5)).
- **I. Blocks more than 1 km from the nearest station** (the paper's Table
  4), using today's exit layer. The paper used 2015's existing and proposed
  stations; today's layer includes lines opened since, which is stated
  beside it.
- **J. The 160 unmatched block-and-street pairs, put back** (Jacob's option
  C). Each gets a street-level point from a scripted OneMap Search on its
  street name, labelled match_type "street". T1 is re-run with them. T2 has
  none.

## 7A. Reported calculation: the money answer to "Coincidence?" (sealed, not scored)

Descriptive, with no pass line. The article states its 95 per cent interval.
The numbers are computed only after the seal.

**Inputs.**
- `beta_T2`: T2's IV estimate of `beta` (section 3), in Singapore dollars
  per square metre, per km, per dollar of COE premium, with its 95 per cent
  interval (clustered by block).
- `dCOE = COEbar_2023 - COEbar_2020`.
  - `COEbar_Y` is the mean of `COEP_q` over the quarters of year Y that had
    bidding: all four for 2023; 2020Q1, Q3 and Q4 for 2020 (no bidding in
    2020Q2).
  - `COEP_q` is built as in section 3 (A and B, weighted by successful bids,
    averaged within the quarter).
  - COE is not the outcome, but this difference is computed only with the
    rest, after the seal.
- `theta_Y`: the year-specific distance slope from the T2 sample.
  - Same specification as section 3, but with `COEP_q x DD_b` replaced by
    `DD_b x 1[year = Y]` for each year Y in 2016 to 2026, base year 2020
    (`theta_2020 = 0`).
  - Estimated by OLS: it is a description, not a causal estimate.

**The gap.** Prices are linear in distance in this model, so the gap per
square metre between a flat 5 km and one 20 km from Raffles Place is
`(5 - 20) x slope = -15 x slope`.

**Implied change in the gap, 2020 to 2023, from the COE rise:**

    dGAP_implied = -15 x beta_T2 x dCOE        (dollars per square metre)

Its 95 per cent interval is `-15 x dCOE` times the interval of `beta_T2`
(`dCOE` is treated as known).

**Actual change in the gap, 2020 to 2023:**

    dGAP_actual = -15 x (theta_2023 - theta_2020) = -15 x theta_2023

**Share:**

    SHARE = dGAP_implied / dGAP_actual

- Its 95 per cent interval comes from a block-cluster bootstrap (999 draws)
  of both regressions together.
- **Reported only if** `dGAP_actual`'s interval excludes zero and both
  changes have the same sign.
- Otherwise the article reports `dGAP_implied` alone and says the share is
  not meaningful: the gap did not clearly change, or moved the other way.
- **Not scored, and no pass line.** It answers "how much money", not "is
  there a link"; T2 answers that.

## 8. The verdict rule (fixed at seal)

The verdict answers the title, "Million-dollar flats came with $100,000
COEs. Coincidence?", in plain words. It is one sentence, built from Part A
then Part B. The title is about recent years, so T2 leads and T1 follows.

**Part A, the link (T2, then T1).** For T2 (2016 to 2026), exactly one of:
- **SURVIVE:** "Not only a coincidence: in HDB flats, the gap between near
  and far widened more when COEs rose, since 2016."
- **Interval includes zero (FAIL):** "No sign of a link in HDB flats since
  2016."
- **`beta` > 0, interval excluding zero (FAIL):** "If anything the
  opposite: since 2016, flats further out gained on flats near town when
  COEs rose."
- **A gate fails (not scored):** "The record cannot say whether there is a
  link in HDB flats since 2016."

Then T1 (2002 to 2015, the paper's years), in the same words for its
years:
- "... and the same was true in 2002 to 2015";
- "... and there was no sign of it in 2002 to 2015";
- "... and the opposite in 2002 to 2015";
- "... and the record cannot say for 2002 to 2015".

**Part B, after the 2018 cut (T3).** Exactly one of:
- **SURVIVE:** "The link weakened after growth in the car quota was cut to
  zero in 2018." The weak-evidence sentence is printed beside it: the
  record cannot say whether rail, working from home or something else
  weakened it.
- **Interval includes zero (FAIL):** "No clear change after the 2018 cut."
- **Difference negative, interval excluding zero (FAIL):** "The link got
  stronger after the 2018 cut."
- **No tilt before 2018 (not scored):** "There was no link before 2018 to
  weaken."
- **A gate fails (not scored):** "The record cannot say whether the 2018
  cut changed it."

**Beside the verdict.**
- The reported calculation (section 7A), when it can be read: "Of the
  change in the gap between a flat 5 km and one 20 km from Raffles Place
  from 2020 to 2023, about X per cent (95 per cent interval L to U) lines
  up with the COE rise."
- **The limit, always:** at most part of the near-town premium, not
  million-dollar flats as a whole.

**The scorecard.** Three tests: T1, T2 and T3. A test not scored drops out
of both the count and the Brier score. Each confidence is the chance the
test holds if it is scored. Jacob's expected count is the sum of his three
confidences, set at the seal. Section 7A is not scored.

## 8A. What it changes (planned for both directions)

Every answer article carries this section (QUESTION_RULES, WEBSITE project).
It states what the result changes for each reader in RULE0 item 5. It never
tells anyone what to do.

**If the link holds (T2 SURVIVE):**
- *A buyer comparing a flat near town with one further out:* part of the
  gap between them tracked how scarce cars were. That part could shrink if
  quotas loosen.
- *Vehicle-quota policy:* the quota had a side-effect on households that
  never drive. It reached them through the price of where they live.
- *The pricing of new flats near town (the Prime Location model):* the
  near-town premium it prices includes a part that moves with COEs, which
  it does not count now.

**If there is no sign of a link (T2 FAIL):**
- *A buyer:* no sign that the gap between near and far moved with COEs in
  HDB flats since 2016. The near-town premium is about other things.
- *Vehicle-quota policy:* no evidence here of a side-effect on flat prices
  for households that never drive.
- *The Prime Location model:* no case from this data for counting COEs in
  the near-town premium.

**For T3, either way:** whether the 2018 cut changed the link, and the
limit that the record cannot say why.

## 9. What would prove the framing wrong, and what it leaves out

- **The belief.** If T1 and T2 both find no clear tilt, the belief survives
  on HDB data: the COE did not reach flat prices through location, in these
  years, by this measure. The piece says so plainly.
- **The paper.** A different HDB result is not a finding against the paper,
  whose homes, buyers and rules differ. It is reported as a difference,
  never as an error in the paper.
- **Left out.**
  - Private homes (paid data).
  - What households actually did: who gave up a car, who moved. No survey
    or registration data by household is used.
  - Why the tilt changed, if it did (rail, working from home, other). Jacob's
    bet is on direction only.
  - Rents, and flats sold new by HDB.
  - Million-dollar flats as such. At most, this explains part of the
    near-town premium. Nothing here says where million-dollar flats are.

## 10. Open before the seal

1. **The geocode.** Done, 5 October 2026. Gate 1 passes: 99.17 per cent of
   T1's sales and 100 per cent of T2's are geocoded. Still open:
   - which station point is used (mean of exits, or the nearest exit).
   - The fallback is decided (Jacob, 6 October 2026, option C, section 4).
2. **The before-window for T3 and the first-stage gate.** Approved by
   Jacob, 5 October 2026: 2012Q2 to 2017Q3, and F below 10 in either window
   means not scored.
3. **Primary sources.**
   - The growth-rate steps are now sourced (section 4; raw/hansard/).
   - Still missing:
     - the month of the 2012 cut to 1%;
     - LTA's October 2017 release (inside T3's dropped quarters);
   - the dates of the 2017 lease statements and of VERS (hdb.gov.sg is now
     allowed).
4. **The analysis scripts, the synthetic suite and the SEALED guard.**
5. **Jacob's confidences** for T1, T2 and T3, with his Why lines.
6. **The answer date and the seal date.**
7. **Title and opening:** the title is chosen by a real reader (5 October
   2026). The opening paragraph (office/TITLES.md) goes to the Editor's blind
   review.
