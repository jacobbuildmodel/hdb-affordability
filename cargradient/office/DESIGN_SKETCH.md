# DESIGN_SKETCH -- three tests, before the paper is read

A conceptual replication: their result was on URA REALIS private homes; these
tests use public HDB resale data, and every write-up says so. No confidences
(Jacob sets them alone). Items marked [PAPER] are copied from the paper once
PAPER_NOTES.md is filled; until then this sketch cannot be sealed.

**Common set-up.** One row per HDB resale. Outcome: log resale price per
square metre (values unopened). Distance: straight-line km from each block to
the paper's CBD point [PAPER]. COE: the paper's category and averaging
[PAPER], from SingStat M651121. Block fixed effects absorb each block's
fixed distance; month fixed effects absorb the COE level and the whole
market. Controls: flat type, floor area, storey range, flat age at sale
(month minus lease_commence_date), flat model. The test number is the
coefficient on distance x COE: "the paper's sign" means a higher COE goes
with a steeper fall in price with distance (central flats dearer relative to
outer ones). 95 per cent intervals, clustered by block [or as the PAPER
clusters].

**T1. Reproduce their sign on HDB data, their years (2002 to 2015).**
- Survive if: the distance x COE coefficient has the paper's sign and its 95
  per cent interval excludes zero.
- Fail if: the interval includes zero, or the sign is the opposite.
- Series: resale d_43f493c6c50d54243cc1eab0df142d6a (2002-01 to 2012-02,
  approval date), d_2d5ff9ea31397b66239f245f57751537 (2012-03 to 2014-12),
  d_ea9ed51da2787afaf8e51f827c304208 (2015); COE SingStat M651121
  (2002 Feb onward); block coordinates (geocoder to be agreed); CBD point
  [PAPER].
- Sealed in advance: the March 2012 basis change is handled by month fixed
  effects plus a re-run on 2002-01 to 2012-02 alone; the result is reported
  for both, and the pooled run is the scored one.

**T2. The same test, 2016 to 2026.**
- Survive if: as T1, over 2016-01 to the last complete month at the seal.
- Fail if: as T1.
- Series: resale d_ea9ed51da2787afaf8e51f827c304208 (2016),
  d_8b84c4ee58e3cfc0ece0d773c8ca6abc (2017 onward); COE M651121 (or
  data.gov.sg d_69b3380ad7e51aff3a7dcc84eba52b8a, same source, checked to
  agree); block coordinates; CBD point [PAPER].
- Months with no bidding (April to June 2020) are dropped, not filled.

**T3. Did the link change after vehicle growth was cut to 0 per cent
(February 2018)?**
- Prediction to be stated by Jacob at Checkpoint 0: the link got stronger
  after the cut, or weaker. Written here as "stronger".
- Survive if: the distance x COE coefficient for 2018-02 onward minus the
  same coefficient for 2016-01 to 2017-12 has the predicted sign, 95 per
  cent interval excluding zero.
- Fail if: the difference's interval includes zero or has the other sign.
- Series: as T2; plus the LTA primary source for the date and rate (www.lta.gov.sg
  is refused from this session) and its announcement date, which sets
  whether the months between announcement and start are dropped.

**Known threats, each to be answered in THESIS.md before the seal.**
- MRT lines that opened inside the windows move a block's access without
  moving its distance to the CBD; the MRT exit layer has no opening dates.
- Remaining lease shortens as flats age, and outer towns are younger.
- COE moves with incomes and the economy, which also move all flat prices;
  month fixed effects take the level, not a distance-specific income effect.
- HDB buyers face income ceilings and grants that private buyers do not.
