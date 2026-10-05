# THESIS -- cargradient piece

**UNSEALED DRAFT, 5 October 2026.** Nothing here is fixed until the commit
"cargradient: SEAL". Until then this file changes by ordinary edits on
cargradient-wip, recorded in the commit history. After the seal it is never
edited; changes go in THESIS_ADDENDUM.md, dated, and are reported, not
applied to the scoring.

Written before any HDB resale price was opened. The resale files were read
for labels, coverage and addresses only (office/FEASIBILITY.md). COE values
were read; they are not the outcome, and the checker allowed it (round 3,
item 4).

Author: research session. Repository: hdb-affordability, subdirectory
`cargradient/`, branch `cargradient-wip`. The title and the opening are not
part of this file: office/TITLES.md proposes them for the Editor and Jacob.

**Confidences are Jacob's**, set at the seal. None appears in this draft.
Each test carries "Confidence at seal: [Jacob, at seal]". T3's direction and
Jacob's Why are his (round 3), verbatim.

**A conceptual replication.** Huang, Li and Ross (2018) estimated this on
private non-landed homes (URA REALIS, paid), 2002Q2 to 2015Q4. These tests
use public HDB resale data, which they left out on purpose (their p. 9).
Every public line says so. Paper references are to the working-paper
version (office/PAPER_NOTES.md).

## 1. The question

**The belief on trial.** A COE is a car-owner's problem. If you never buy a
car, its price is none of your business.

**The rival explanation (the paper's).** When owning a car costs more, more
households go without one, and being near the centre is worth more to them.
So flats near town gain relative to flats further out. Part of the COE lands
on the price of every flat, car or no car.

**Sealed question 1.** "When COE premiums were higher, did HDB resale flats
near Raffles Place gain relative to flats further out, as the paper found for
private homes, over its years (2002 to 2015) and since (2016 to 2026)?"

**Sealed question 2.** "After growth in car numbers was cut to 0 per cent in
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
- **Block coordinates:** OneMap Search, 10,016 unique block and street
  pairs (out/addresses.csv). The full run waits for Jacob's OneMap
  credentials.
- **Raffles Place and City Hall MRT:** data.gov.sg exit layer
  d_b39d3a0871985372d7e1637193335da5 (10 and 4 exits).
- **The 2018 change:** LTA, 13 Aug 2020 (raw/), "0% per annum for Categories
  A, B and D since February 2018". The October 2017 announcement is from
  news reports only (NEEDS-PRIMARY).

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
- **Prediction.** After growth in car numbers was cut to 0 per cent, a rise
  in the COE tilted HDB prices toward the centre less than before.
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
  - Note: the 0.25% before February 2018 is not yet confirmed by a primary
    source (DESIGN_SKETCH item 3). The Why line stays as written.
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
- `01_coe_ranges.py` (COE only);
- the geocoding script, once Jacob's OneMap credentials are in the
  environment.

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

## 8. The verdict rule (fixed at seal)

The verdict has two parts in one sentence.

**Part A, question 1 (T1 and T2).** For each window, exactly one of these:
- **"the record cannot say"**: a gate fails.
- **"HDB flats near town gained relative to flats further out when COEs cost
  more"**: the test survives.
- **"no clear tilt toward town when COEs cost more"**: the interval includes
  zero.
- **"flats further out gained relative to flats near town when COEs cost
  more"**: `beta` > 0 with an interval excluding zero.

**Part B, question 2 (T3).** Exactly one of these:
- **"there was no tilt before 2018 to weaken"**: `beta_before` is not
  negative with an interval excluding zero.
- **"the record cannot say"**: a gate fails.
- **"the tilt got weaker after 2018"**: T3 survives. The weak-evidence
  sentence is printed beside it.
- **"no clear change after 2018"**: the interval includes zero.
- **"the tilt got stronger after 2018"**: the difference is negative, with an
  interval excluding zero.

**The scorecard.** Three tests: T1, T2 and T3. A test not scored drops out
of both the count and the Brier score. Each confidence is the chance the
test holds if it is scored. Jacob's expected count is the sum of his three
confidences, set at the seal.

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

## 10. Open before the seal

1. **OneMap credentials** (Jacob), then the full geocode. Report the match
   rate before the seal (gate 1 is defined on it).
2. **The before-window for T3 and the first-stage gate.** Approved by
   Jacob, 5 October 2026: 2012Q2 to 2017Q3, and F below 10 in either window
   means not scored.
3. **Primary sources still missing:**
   - the 0.25% growth rate before February 2018;
   - LTA's October 2017 release;
   - the dates of the 2017 lease statements and of VERS (hdb.gov.sg is now
     allowed).
4. **The analysis scripts, the synthetic suite and the SEALED guard.**
5. **Jacob's confidences** for T1, T2 and T3, with his Why lines.
6. **The answer date and the seal date.**
7. **Title and opening:** Editor's blind review of office/TITLES.md, then
   readers.
