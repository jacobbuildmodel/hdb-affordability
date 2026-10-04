# DESIGN_SKETCH -- three tests, Checkpoint 0 draft

A conceptual replication. Their result was on URA REALIS private homes; these
tests use public HDB resale data, and every write-up says so. There are no
confidences here; Jacob sets them alone. Paper references (p., Table) are to
the working-paper PDF in cargradient/raw/ (see PAPER_NOTES.md).

**Common set-up, following the paper's column (4) (Table 3b, p. 30).**
- Unit: block x quarter, with resales of all flat types pooled after
  adjustment for flat type, area, storey, age and model. (The paper uses
  project medians with at least three sales a quarter, p. 14; whether HDB
  data keeps per-sale rows instead is a choice to seal.)
- Outcome: resale price per square metre, in levels as the paper uses
  (p. 11), with log as a reported alternative. Values stay unopened until the
  seal.
- Distance: km from the block to Raffles Place MRT station (p. 11). City Hall
  is used as a robustness check (Table 5).
- COE: categories A and B. Each bidding's premium is weighted by successful
  bids, then the biddings are averaged by quarter (p. 14). All of this comes
  from SingStat M651121, which carries premium, quota and successful bids per
  bidding for A and B.
- Fixed effects: block, and year x quarter. Estimated by IV, with COE quota
  and quota x distance as instruments (p. 13). OLS is reported beside it.
- Test number: the coefficient on COE premium x distance. "The paper's sign"
  is negative: when COEs cost more, prices rise more near Raffles Place than
  further out. 95 per cent intervals, clustered by block (the paper clusters
  by project, p. 16).

**T1. Reproduce their sign on HDB data, over their years (2002Q2 to 2015Q4).**
- Survive if: the interaction is negative and its 95 per cent interval
  excludes zero.
- Fail if: the interval includes zero, or the sign is positive.
- Series:
  - resale d_43f493c6c50d54243cc1eab0df142d6a (to 2012-02, approval date);
  - resale d_2d5ff9ea31397b66239f245f57751537 (2012-03 to 2014-12);
  - resale d_ea9ed51da2787afaf8e51f827c304208 (2015);
  - COE: SingStat M651121;
  - block coordinates (OneMap, see FEASIBILITY.md);
  - Raffles Place MRT coordinates.

**Approval date vs registration date (March 2012). Jacob decides; options
with reasons.** Before March 2012 a sale is dated when HDB approved it; from
March 2012, when it was registered. The approval comes first, so the same
sale would carry an earlier month before the switch.
- (a) Basis-break term: add after-March-2012 x distance as a control. The
  year x quarter effects already absorb any level jump, so the only thing the
  switch could distort is the slope, and this term takes it out. Cost: it
  also absorbs any real change in slope at that date, and it is one more
  parameter close to the one being tested.
- (b) Shift the earlier series forward by a fixed lag (approval to
  registration). Reason: it lines each sale up with the COE quarter it was
  actually priced in. Cost: the lag needs an HDB source not yet found.
  Quarterly aggregation makes a lag of a month or two matter little.
- (c) Split: score T1 on 2002Q2 to 2011Q4 (approval basis only, 39
  quarters), and report 2012Q2 to 2015Q4 separately. Reason: no mixing at all.
  Cost: fewer quarters of COE variation in the scored run.
- (d) With any of (a) to (c), drop 2012Q1. It is the quarter that mixes both
  bases, and a sale approved in February and registered in March could sit in
  both files.

**T2. The same test, 2016Q1 to the last complete quarter at the seal.**
- Survive if / Fail if: as T1.
- Series:
  - resale d_ea9ed51da2787afaf8e51f827c304208 (2016);
  - resale d_8b84c4ee58e3cfc0ece0d773c8ca6abc (2017 onward);
  - COE: M651121;
  - coordinates as T1.
- No bidding was held in April, May and June 2020 (M651121 footnote). That
  quarter is dropped, not filled.

**T3. Did the link change after car growth was cut to 0 per cent in
February 2018?**
- Survive if: the interaction for 2018Q2 onward minus the interaction for
  2016Q1 to 2017Q3 has the sign Jacob picks, with a 95 per cent interval
  excluding zero.
- Fail if: the interval includes zero, or the sign is the other one.
- Dropped: 2017Q4 to 2018Q1. The cut was announced in October 2017 and took
  effect in February 2018. The announcement date is from news reports only;
  the LTA release of October 2017 has not been found. The February 2018 start
  is from LTA itself (raw/lta_20200813_vehicle_growth_rate.html).
- Series: as T2, plus that LTA release.

**T3's direction. Jacob picks it when he approves Checkpoint 0. The case for
each:**
- *Stronger after 2018.*
  - From February 2018 the growth rate for categories A and B was 0 per cent
    (LTA, 13 Aug 2020). Quota then came "largely" from deregistrations
    (same release).
  - With no growth, a household that wants a car can only get one by
    outbidding another. More households stay car-free at any given premium.
  - In the paper's model, car-free households are the ones who pay most to
    be near the centre (pp. 10-11). So the same rise in premium should tilt
    prices toward the centre more than before.
- *Weaker after 2018.*
  - The paper's centre premium comes from where trains are: people near the
    CBD, "where the subway system is the most extensive, do not need a car"
    (p. 10).
  - After 2018, rail reached further out. The Thomson-East Coast Line opened
    in stages on 31 January 2020 (Woodlands), 28 August 2021 (Thomson),
    13 November 2022 (direct access to the CBD) and 23 June 2024 (the east)
    (LTA project page, raw/lta_tel_project_page.html).
  - A car-free household far out now gives up less by not driving. Any given
    COE rise should push it toward the centre less.

**Known threats, each answered in THESIS.md before the seal.**
- MRT lines that opened inside the windows. The exit layer has no opening
  dates; the LTA line pages carry stage dates.
- Remaining lease shortens as flats age, and outer towns are younger.
- COE moves with incomes and the economy, which also move flat prices. Time
  effects take out the level, but not a distance-specific income effect.
- HDB buyers face income ceilings and grants that private buyers do not (the
  paper's own reason for leaving HDB out, p. 9).
