# COE prices and the HDB distance premium, 2002 to 2026

*Title proposal; Jacob decides. Research note, 22 October 2026. This study
applies the method of Huang, Li and Ross (2018), "HLR" below, to HDB resale
flats.*

## The finding

Read the one held test with care. In placebo runs with invented prices and a
slow drift in the distance premium, the scored test found a link 51.6%,
56.0% and 50.0% of the time (T1, T2, T3) when none existed. A held
prediction here is weak evidence; a failed one is not.

HLR found that in private homes, 2002 to 2015, higher COE premiums went with
prices falling faster with distance from the city centre. In HDB resale flats
that tilt appeared in 2002 to 2011, ran the other way in 2012 to 2015, and
showed no clear sign in 2016 to 2026.

Estimates are in dollars per square metre, per km from Raffles Place MRT, per
dollar of COE premium, with 95 per cent intervals; a negative value is HLR's
sign ("e-04" moves the decimal point four places left).

| Years | Sales | Estimate (interval) | First-stage F | Reading |
|---|---|---|---|---|
| 2002 to 2011 (check) | 281,559 | -1.199e-03 (-1.619e-03 to -7.801e-04) | 76.3 | HLR's sign |
| 2012 to 2015 (check) | 67,563 | 1.456e-03 (8.165e-04 to 2.095e-03) | 35.5 | the other way |
| 2002 to 2015 (scored, T1) | 349,122 | -9.663e-04 (-1.370e-03 to -5.624e-04) | 86.7 | HLR's sign |
| 2016 to 2026 (scored, T2) | 257,854 | 7.626e-05 (-1.519e-04 to 3.044e-04) | 74.8 | no clear sign |

The split at 2012 follows HDB's switch from approval to registration dates;
it is a reported check, not a scored test.

## The bets, as sealed

Sealed 12 October 2026, before any resale price was read:

- **T1** (2002 to 2015): "When COEs cost more, HDB flats near Raffles Place
  gained relative to flats further out." Confidence at seal: 70%. Outcome:
  SURVIVE.
- **T2** (2016 to 2026): the same. Confidence at seal: 40%. Outcome:
  FAIL_NO_LINK.
- **T3**: "After growth in the car quota was cut to zero in February 2018, a
  rise in the COE tilted HDB prices toward the centre less than during the
  step-by-step cuts before it." Confidence at seal: 15%. Outcome: could not
  be scored. The sealed rule needed a tilt toward the centre in 2012 to 2017
  to test whether it weakened, and there was none: the 2012 to 2017 estimate
  ran the other way, 1.181e-03 (9.486e-04 to 1.414e-03).

Scored 2, held 1. Brier score 0.125 over the two scored tests; expected
held 1.1 for those two (1.25 for all three, as sealed).

## Limits

- **Drift.** See the opening paragraph: under a persistent drift in the
  distance premium the test finds a link about half the time when none
  exists, so a SURVIVE is weak evidence.
- **Sign flips in the checks.** In log prices, 2002 to 2015 showed no clear
  link (-2.939e-09, interval -9.776e-08 to 9.188e-08) and 2016 to 2026 ran
  the other way (1.685e-07, 1.333e-07 to 2.036e-07). For 2016 to 2026,
  leaving out 2020 to 2022 gave HLR's sign (-2.324e-04, -4.397e-04 to
  -2.507e-05), while ending in early 2023 gave the opposite (2.858e-04,
  9.465e-05 to 4.770e-04). None of these is scored.
- **Imprecision since 2016.** The COE rise from 2020 to 2023 ($36,753 to
  $106,219 on average) implied a change of -79 dollars per square metre in
  the gap between a flat 5 km and one 20 km from Raffles Place, interval
  -317 to 158: too wide to rule out a modest link either way.

## Method

One row per resale. Price per square metre is regressed on the COE premium
times block distance, with block, flat type, storey, flat model and
lease-band by quarter fixed effects and floor area. As in HLR, the car quota
times distance instruments it (two-stage least squares): the estimate is the
COE's effect only if the quota did not move with near-town demand, which the
design cannot check. Intervals are clustered by block and by quarter. The
pipeline has a synthetic suite that forces every outcome branch; pyfixest
refits T1 and T2 to 1e-6; an independent numpy script, 15_reproduce.py,
recomputed 48 numbers and outcomes, every scored one among them, with no
difference; and the checker recomputed the scored numbers with its own code.
Changes after the seal are in THESIS_ADDENDUM.md; none changed a test or a
score.

## For anyone citing HLR on public housing

What this record adds to count:

- The sign depends on the years and the unit: HLR's in 2002 to 2011,
  reversed in 2012 to 2015, unclear since 2016, and absent in percentage
  terms even for 2002 to 2015.
- The untested quota assumption (Method), and the 30,813 COEs LTA
  redistributed and injected from May 2023 (MOT, 4 November 2025).
- HDB buyers face eligibility rules that private buyers do not, and distance
  here is to Raffles Place only.

## Data and code

- Code, outputs and RESULTS.md:
  https://github.com/jacobbuildmodel/hdb-affordability/tree/cargradient-wip/cargradient
- Sealed thesis (commit 7ee9b91):
  https://github.com/jacobbuildmodel/hdb-affordability/blob/7ee9b9169c36399a80400b0e2e9ef9bd6b5000af/cargradient/THESIS.md
- Registration: https://osf.io/rntsk, DOI 10.17605/OSF.IO/RNTSK.
- HDB resale prices: data.gov.sg collection 189
  (https://data.gov.sg/collections/189/view). COE premium and quota:
  SingStat M651121, data source LTA. MRT exits: data.gov.sg, LTA. All under
  the Singapore Open Data Licence version 1.0. Contains information from
  OneMap (Singapore Land Authority), accessed 5 and 6 October 2026.
- Huang, Li and Ross, "The impact of the cost of car ownership on the house
  price gradient in Singapore", Regional Science and Urban Economics 68
  (2018), 160-171.

*AI label: drafted by an AI research assistant from the pipeline's outputs,
for Jacob's review; the confidences are Jacob's. Not advice.*
