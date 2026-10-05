# DESIGN_SKETCH -- three tests, Checkpoint 0 round 3

A conceptual replication. Their result was on URA REALIS private homes; these
tests use public HDB resale data, and every write-up says so. There are no
confidences here; Jacob sets them alone at the seal. Paper references (p.,
Table) are to the working-paper PDF (see PAPER_NOTES.md and raw/RETRIEVED.txt;
the PDF itself is not in the repo). The full draft is cargradient/THESIS.md,
UNSEALED.

## Decided by Jacob (round 3, and 5 October 2026)

1. The paper PDF is out of the repo. It is in no commit on cargradient-wip,
   and cargradient/raw/*.pdf is gitignored. Its URL, date and md5 stay in
   raw/RETRIEVED.txt.
2. T1 and the March 2012 switch: options (a) plus (d). Add an
   after-March-2012 x distance control, and drop 2012Q1. Option (c), the
   split run, is a sealed sensitivity, reported and not scored.
3. T3's direction: WEAKER after 2018.

   Why (Jacob, verbatim): "I'd lean weaker, but not by much. The "stronger"
   story needs a big change, and 2018 was a small one. Moving from 0.25%
   growth to 0% hardly changes how many households can get a car. It's hard
   to see that pushing many more families to stay car-free and pay up for
   flats near town. Most of what changed after 2018 cuts the other way. New
   rail lines and working from home both make living further out cheaper in
   time and effort. Either would make a COE rise matter less for where people
   choose to live. Two catches. A weaker result wouldn't tell you whether rail
   or COVID caused it, so the bet is about direction, not the reason. And my
   honest best guess is close to "no clear change," given how small the 2018
   change was."

   **Jacob's 0.25% figure, checked:**
   - NOT verified from a primary source.
   - What was found: LTA's 13 Aug 2020 release says Category C's rate "was
     maintained at 0.25% per annum" when A, B and D went to 0% in February
     2018 (raw/lta_20200813_vehicle_growth_rate.html). That fits 0.25% for
     all categories before, but does not say it for A and B.
   - News reports give 0.25% from February 2015 to January 2018 (for
     example Fortune, 23 Oct 2017; The Edge Malaysia).
   - LTA's newsroom index on lta.gov.sg starts in 2020, so its 2014 and
     2017 releases are not there.
   - www.mot.gov.sg and www.gov.sg refuse the session (CONNECT 403), so
     the search stopped for those hosts.
   - Status: NEEDS-PRIMARY. The figure is used only in Jacob's Why line,
     which stays verbatim. No test depends on it.

4. T3's before-window and gate (approved by Jacob, 5 October 2026):
   - The before-window is 2012Q2-2017Q3.
   - 2016Q1-2017Q3 stays as a reported sensitivity.
   - T3 is NOT SCORED if the first-stage F for COE premium x distance is
     below 10 in either window.
   - Disclosed: the window was chosen after seeing COE ranges (item 4
     below), not prices. COE is not the outcome.

## Common set-up (following the paper's column 4, Table 3b, p. 30)

- **Unit:** each resale, with block fixed effects and controls for flat
  type, area, storey and model, plus remaining-lease band x year-quarter
  effects. (The paper takes project medians, since its units are
  near-identical within a project, p. 14; HDB blocks mix flat types.)
- **Outcome:** resale price per square metre, in levels (p. 11), with log as
  a sensitivity. It stays unopened until the seal.
- **Distance:** km from the block to Raffles Place MRT (p. 11).
- **COE:** categories A and B. Each bidding is weighted by successful bids,
  then the biddings in a quarter are averaged (p. 14), from SingStat M651121.
- **Estimation:** block and year x quarter fixed effects, and IV, with quota
  and quota x distance as instruments (p. 13).
- **Test number:** the coefficient on COE premium x distance. The paper's
  sign is negative.
- **Main intervals:** 95 per cent, clustered by block.

## Checker considerations: proposals for Jacob to approve

**4. T3's power (the before-window).** COE ranges below are from
01_coe_ranges.py on SingStat M651121, the quarterly A and B premium built as
the paper builds it (out/coe_ranges.txt). COE is not the outcome; the checker
allowed reading it.

| Window | Quarters | Low (quarter) | High (quarter) | High / low | SD |
|---|---|---|---|---|---|
| Before, as drafted: 2016Q1-2017Q3 | 7 | 45,827 (2017Q3) | 53,960 (2016Q3) | 1.18 | 2,609 |
| After: 2018Q2-2026Q3 | 33 | 28,222 (2018Q4) | 129,951 (2026Q3) | 4.60 | 33,538 |
| Before, proposed: 2012Q2-2017Q3 | 22 | 45,827 (2017Q3) | 82,867 (2013Q1) | 1.81 | 11,790 |

- **Proposal (APPROVED by Jacob, 5 October 2026): move the before-window to
  2012Q2-2017Q3**, and keep 2016Q1-2017Q3 as a reported sensitivity.
- Reasons:
  - The drafted window has almost no COE movement: highest over lowest is
    1.18. So the slope before 2018 would be estimated from noise, and any
    "change" would mostly be the before-estimate's error.
  - 2012Q2 is the first quarter after the dropped 2012Q1. The whole
    proposed window is on the registration-date basis, so T3 never crosses
    the March 2012 switch.
  - 22 quarters before against 33 after; the before-window's SD rises from
    2,609 to 11,790.
- **Backstop gate, outcome-blind (APPROVED by Jacob, 5 October 2026):** T3
  is NOT SCORED if the first-stage F
  statistic for COE premium x distance is below 10 in either window.
  - The first stage uses only COE, quota, distance and which blocks traded
    when. It never uses prices, so it can be computed and gated without
    opening the outcome.
  - Ten is the usual weak-instrument line (judgement).
- **Disclosed:** the window was proposed after seeing these COE ranges.
  That is allowed (COE is not the outcome), and it is recorded so a reader
  can see it.

**5. Lease decay (statements in 2017, VERS announced August 2018, older
estates nearer town).**
- **Proposal:** remaining lease at sale, in 5-year bands, x year-quarter
  fixed effects.
  - This lets the price of a given remaining lease change every quarter, for
    every location at once. So a nationwide repricing of short leases around
    2017-2018 is absorbed, and is not read as a change in the COE slope.
  - Distance x COE is then estimated from blocks with similar lease left.
- **What is left over, stated now:**
  - Any repricing of lease that differs by location for the same lease
    left. For example, hopes of redevelopment may be stronger for old blocks
    in central estates.
  - Differences in lease within a 5-year band.
  - If either moved at 2018, it loads onto T3.
- **Sensitivity:** add planning-area x year linear trends (the paper's
  column 5).
- The dates of the 2017 statements and of VERS are to be sourced (hdb.gov.sg
  is now allowed) before the seal.

**6. Working from home (2020-2022).**
- **Proposal: a sealed sensitivity** that drops 2020Q1 to 2022Q4 from T2
  and from T3's after-window. Reported, not scored.
- Reasons:
  - Jacob's bet is about direction, not the reason. So the scored test
    keeps those years, and the sensitivity shows whether any change survives
    without them.
  - The after-window keeps 22 quarters (2018Q2-2019Q4 and 2023Q1-2026Q3),
    with COE high over low still 4.60 (SD 35,792), so it stays readable.
- **Why whole calendar years (judgement):** no single dated end of
  working from home was found to cut at. 2020Q2 has no COE bidding anyway
  (M651121 footnote).

**7. Clustering.** COE varies only by quarter.
- **Sealed sensitivity:** two-way clustering by block and quarter, printed
  beside the block-clustered interval for every test.
- With 22 to 55 quarters per window, the two-way interval rests on few time
  clusters and can be wide. That is stated beside it.
- The scored rule uses the block-clustered interval, as the paper does.

**8. The October 2017 announcement.**
- LTA's newsroom on lta.gov.sg lists releases from 2020 only. The October
  2017 release was not found there.
- www.mot.gov.sg and www.gov.sg: refused (CONNECT 403). Stopped for both
  hosts.
- The 23 October 2017 date rests on news reports only. It sets only the
  window T3 drops (2017Q4 to 2018Q1), and that drop covers any date in
  October to December 2017, so the design does not hinge on the exact day.

**9. Exposure.**
- The paper's COE summaries (Table 1, Figure 3, Table A2) were seen. They
  are COE values, not this piece's outcome; the checker ruled this no
  problem.
- Jacob and the chats saw town-level HDB price findings in the earlier
  affordability piece. That is prior knowledge of price levels, not of the
  COE x distance interaction.

## The tests (detail and verdict rule in THESIS.md)

- **T1. 2002Q2 to 2015Q4.**
  - 2012Q1 dropped; after-March-2012 x distance control.
  - The interaction is negative, 95 per cent interval excluding zero.
- **T2. 2016Q1 to 2026Q3.** The same.
- **T3. WEAKER after 2018.**
  - The after-window interaction (2018Q2 to 2026Q3) minus the before-window
    interaction (proposed 2012Q2 to 2017Q3) is POSITIVE: closer to zero, a
    flatter tilt toward town. 95 per cent interval excluding zero.
  - 2017Q4 to 2018Q1 dropped.
  - First-stage gate as above.
  - Not scored if the before-window interaction is not negative with an
    interval excluding zero: there is then no link to weaken.

## T3: the two cases, kept for the record

- *Stronger.*
  - 0 per cent growth from February 2018 (LTA, 13 Aug 2020).
  - In the paper's model, car-free households pay most to be near the centre
    (pp. 10-11).
- *Weaker (Jacob's pick).*
  - The paper's centre premium rests on trains being densest in the centre
    (p. 10).
  - The Thomson-East Coast Line opened in stages from 31 January 2020 to 23
    June 2024 (raw/lta_tel_project_page.html).
  - Working from home cut commuting.
