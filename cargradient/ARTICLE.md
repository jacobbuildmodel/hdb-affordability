---
# DRAFT for Checkpoint 2. The title is a proposal: Jacob decides titles.
# Round 3 proposals (towns from article/town_distances.csv): "$100,000 COEs:
# Toa Payoh did not clearly outpace Woodlands" (58 characters); "Toa Payoh
# did not clearly outpace Woodlands as COEs soared" (58); "COEs nearly
# tripled. Toa Payoh did not outpace Woodlands" (56). The title below is
# the round 1 proposal and holds in dollars only. Jacob decides. The date is a proposal, not agreed:
# 2026-10-31 and 2026-11-14 are taken in content/economics/.
title: "Flats near town gained when COEs rose. Not since 2016."
question: "Million-dollar flats came with $100,000 COEs. Coincidence?"
date: 2026-11-28
draft: true
showToc: true
summary: "Does a dearer COE make a flat near town worth more, even to a family with no car? Three predictions were sealed before the HDB resale prices were opened. From 2002 to 2015 flats near Raffles Place gained on flats further out when COEs rose, in dollars per square metre though not in percentage terms; since 2016 there was no sign of it."
tags: ["economics"]
repo: "https://github.com/jacobbuildmodel/hdb-affordability/tree/main/cargradient"
dataset: "https://data.gov.sg/collections/189/view"
# Method strip -- transcribed from cargradient/THESIS.md's seal line and
# cargradient/RESULTS.md's scorecard. testsOther is 1: T3 was not scored
# (no tilt before 2018 to weaken), which the sealed rule drops from the count.
thesisSealed: "12 October 2026"
testsPassed: 1
testsFailed: 1
testsOther: 1
testsTotal: 3
---

> **Question:** million-dollar flats came with $100,000 COEs. Coincidence?\
> **Verdict:** no sign of a link in HDB flats since 2016. In 2002 to 2015, the paper's years, the gap widened more when COEs rose. There was no link before 2018 to weaken.\
> In percentage terms the 2002 to 2015 tilt did not show (a check, not scored).\
> **Key number:** the COE rise from 2020 to 2023 implied a change of -79 dollars per square metre in the price gap between a flat 5 km and one 20 km from Raffles Place (95 per cent interval -317 to 158), from 257,854 resales since 2016.\
> **My confidence going in:** 70%, 40% and 15% on three predictions, 1.25 expected to hold (1.10 for the two that were scored).\
> **Scored:** 1 of 2 held; the third was not scored.\
> **What would change it:** a near-town tilt since 2016 that holds up with the drift in near-town prices ruled out.

In the first bidding of June 2022, the COE for larger cars (the Certificate of
Entitlement every car in Singapore needs) closed at or above $100,000 for the
first time. The year before, 259 HDB resale flats had sold for
$1 million or more, up from 46 in 2017. Two headlines, argued about
separately. Could they be one story?

Most people would say no. A COE is a car-owner's problem. A family with no car
pays nothing for it. But one study of private condos found that when COEs cost
more, homes near the city centre gained on homes further out. I put the same
question to HDB resale flats and wrote down my bets before I opened the price
data. In dollars per square metre, the tilt was there from 2002 to 2015. Since
2016 there was no sign of it.

## The argument: two separate prices, or one story

**Separate stories.** A COE is the price of the right to own a car. What a flat
costs is about its size, its lease and where it is. A family that will never
drive has no stake in the COE.

**One story.** Huang, Li and Ross (2018) argued the opposite for private homes.
Some households sit on the edge of owning a car. When the COE rises, some of
them go without one, and a household without a car values a short train ride
to work more than one with a car does. So part of what a home near town costs
moves with the COE, whoever buys it. They found that tilt in private condos
from 2002 to 2015.

## Pushed to the extreme: the last bus home

These are thought experiments, not claims about the data.

Picture cars costing almost nothing: every family drives, and the price of
cars barely moves what a flat near town is worth. Now picture cars out of
reach: every family lives by the train timetable, and nearness to town is
everything. Singapore sits between the two, where a COE rise can tip a few
households from one side to the other.

It works like the last bus home. When it stops running, the room nearest the
office is worth more, to everyone who has no other way back. Call it the
last-bus premium: the extra a home near town is worth when getting around
without a car gets harder. The question is whether it moved with the COE in
HDB prices.

## My bets: a tilt in both periods, weaker after 2018

I sealed three predictions on 12 October 2026, before opening the resale
prices, and posted them on an
[open question page](/open/2026-10-12-million-dollar-flats/). This study
applies the method of Huang, Li and Ross (2018) to HDB resale flats.

1. **Their years** (70%). From 2002 to 2015, when COEs cost more, HDB flats
   near Raffles Place gained relative to flats further out. Why: "Same city,
   same years and same COE swings as a paper that found the effect strongly
   in condos, and the central HDB premium widened over most of those years."
2. **Since then** (40%). The same was true from 2016 to 2026. Why: "COEs
   tripled in 2021-23, but outer towns kept pace with central ones, and the
   only clear tilt toward far-out flats came just as COEs started rising."
3. **After the 2018 cut** (15%). After growth in the car quota was cut to zero
   in February 2018, the tilt got weaker. My Why began: "I'd lean weaker, but
   not by much."

Together the percentages put the expected number holding at 1.25 of 3. The
full wording is in the
[sealed thesis](https://github.com/jacobbuildmodel/hdb-affordability/blob/7ee9b9169c36399a80400b0e2e9ef9bd6b5000af/cargradient/THESIS.md).

## What the data said: a tilt to 2015, no sign since

![Change in the price gap between a flat 5 km and one 20 km from Raffles Place for each $10,000 on the COE premium, by period](/figs/cargradient_chart1_tests.svg)

Notes: a dot right of zero means flats near town gained on flats far out when
COEs rose; lines are 95 per cent intervals; a line crossing zero is no clear
link; muted rows were not scored. Values are per $10,000 of COE premium.

Sources: HDB resale prices (data.gov.sg); SingStat M651121;
cargradient/12_figures.py.

The test compared each HDB resale with a located block with the COE premium in
its quarter and its block's distance from Raffles Place, holding fixed each
block, flat type, storey range and flat model, the floor area, and the lease
left. It asked whether flats near town did better than flats further out in
the quarters when COEs cost more. COE prices also rise in good times, so the
test uses changes in the car quota to pick out the COE moves that good times
did not drive. If the quota did not move with demand for flats near town, the
estimate is the COE's own effect. The test cannot check that assumption, so a
result here is evidence, not proof.

From 2002 to 2015 they did, in dollars per square metre. Across 349,122
resales in 8,400 blocks over 54 quarters, flats nearer Raffles Place gained on
flats further out when the COE rose, and the 95 per cent interval sat wholly
on that side of zero. My first bet held. It held in dollars but not in percentage terms: measured by the log
of price per square metre, the 2002 to 2015 tilt did not show (a check, not
scored).

From 2016 to 2026 there was no clear sign of it. Across 257,854 resales in 9,768 blocks over 42
quarters, the 95 per cent interval ran from a tilt toward town to a tilt away
from it, and so included zero. My second bet failed. In percentage terms the
link since 2016 ran the other way, with flats further out gaining when COEs
rose, and the other checks on these years split both ways.

## Where I was wrong: no sign of a link since 2016

I gave the second bet 40%, and it failed. Between 2020 and 2023 the average COE premium rose from $36,753 to $106,219, a rise of $69,465. Using the estimate
from 2016 onward, that rise implied a change of -79 dollars per square metre in
the gap between a flat 5 km and one 20 km from Raffles Place, with a 95 per
cent interval from -317 to 158. For scale, the median HDB block in Toa Payoh
is 5.9 km from Raffles Place, and in Woodlands 18.4 km.

The share of the actual change in that gap that lined up with the COE, which I
had planned to report, is not meaningful: the actual gap did not clearly change
from 2020 to 2023 (its 95 per cent interval included zero), and the implied
change pointed the other way. My sealed rule then reports the implied change
alone.

The third bet was never scored. It needed a tilt toward town in 2012 to 2017
to weaken. Instead, flats further out gained when COEs rose in those years,
and the interval cleared zero, so my sealed rule takes it out of the count.

So 1 of 2 scored bets held, against the 1.1 I expected for those two. The
Brier score, which measures how far each confidence sat from what happened,
was 0.125, where a forecaster who always says 50 per cent scores 0.25 and lower
is better. Two predictions are far too few to judge anyone's calibration.

## Where the finding flips: 2012, and the checks

Split at 2012, when HDB's records switched from the date a sale was approved
to the date it was registered, the two halves pointed opposite ways. In 2002
to 2011, flats near town gained when COEs rose, and the interval cleared zero.
In 2012 to 2015, flats further out gained, and the interval also cleared zero.

None of the other checks was scored. In percentage terms (the log of price per
square metre), 2002 to 2015 showed no clear link, its interval including zero,
and since 2016 flats further out gained. Since 2016 without 2020 to 2022,
flats near town gained. From 2016 to early 2023, before the COE supply was
redistributed, flats further out gained. Each of these last three intervals
cleared zero. The numbers are in the method notes, and the full set is in
RESULTS.md.

## The obvious objection: isn't this just good times?

If good years lift flats near town more than flats far out, for reasons that
have nothing to do with cars, the 2002 to 2015 result could show up anyway.
Leaning on the car quota helps, but it does not close the door. The sealed limit says so:

> A SURVIVE cannot rule out a slow drift in how much buyers pay to live near
> town that happened to move with the COE premium. In placebo runs with such a
> drift, the scored test found a link about half the time when none existed.

So the bet that held is weaker evidence for the car story than the bet that
failed is against it.

## What it changes: no basis either way

For a buyer weighing a flat near town against one further out, there was no
sign that the gap between them moved with COEs in HDB flats since 2016. But
the estimate since 2016 is too imprecise to rule out a modest link either way:
the COE rise from 2020 to 2023 implied a change of -79 dollars per square
metre in the same 5 km to 20 km gap, with a 95 per cent interval from -317 to
158. For anyone weighing vehicle-quota
policy, this test does not show a side-effect on flat prices for households
that never drive, and it is too imprecise to rule one out. For the pricing of
new flats near town under the Prime Location model, this data gives no basis
for counting COEs in the near-town premium, and none for ruling them out.

At most, this explains part of the near-town premium, not million-dollar flats
as a whole.

## Elsewhere: London charges the trip, not the car

Singapore rations who may own a car. London prices driving into its centre
instead. Transport for London charges a daily fee of GBP 18 to drive within its
Congestion Charge zone, from 7:00 to 18:00 on weekdays and 12:00 to 18:00 at weekends
and on bank holidays. There the cost lands on the trip into town, not on
owning the car.

## What would change my mind

- A tilt toward town since 2016 that survives with the slow drift in
  near-town prices ruled out.
- A record of who gave up a car and where they moved, which this data does not
  have.
- The same test on private homes since 2016, the paper's own market.

## The verdict: no sign of a link since 2016

No sign of a link in HDB flats since 2016. In 2002 to 2015, the paper's years,
the gap widened more when COEs rose. There was no link before 2018 to weaken.

{{< aside title="Method notes" >}}
**The seal.** The three predictions, their pass lines and the confidences were
committed on 12 October 2026 in
[7ee9b91](https://github.com/jacobbuildmodel/hdb-affordability/blob/7ee9b9169c36399a80400b0e2e9ef9bd6b5000af/cargradient/THESIS.md),
before any resale price was opened, and registered on OSF the same day
([osf.io/rntsk](https://osf.io/rntsk)). Anything learned afterwards is in
THESIS_ADDENDUM.md, and none of it changed a score.

**The numbers.** Each estimate is in dollars per square metre, per km from
Raffles Place, per dollar of COE premium; a negative value means prices fell
faster with distance when COEs cost more, and e-04 moves the decimal point four
places left. 2002 to 2015: -9.663e-04 (95 per cent interval -1.370e-03 to
-5.624e-04), first-stage F 86.7, a measure of how strongly the quota moved
the COE (the sealed line was 10). 2016 to 2026:
7.626e-05 (-1.519e-04 to 3.044e-04), F 74.8. 2012 to 2017, before the cut:
1.181e-03 (9.486e-04 to 1.414e-03). Intervals allow for sales in the same
block, and in the same quarter, moving together.

**Checks, not scored (out/sensitivities.csv):** 2002 to 2011, -1.199e-03
(-1.619e-03 to -7.801e-04); 2012 to 2015, 1.456e-03 (8.165e-04 to
2.095e-03); since 2016 without 2020 to 2022, -2.324e-04 (-4.397e-04 to
-2.507e-05); 2016 to early 2023, 2.858e-04 (9.465e-05 to 4.770e-04); in log
prices, 2002 to 2015, -2.939e-09 (-9.776e-08 to 9.188e-08) and since 2016,
1.685e-07 (1.333e-07 to 2.036e-07), in log units.

**Method.** As in the paper, the car quota stands in for the COE: the test
uses only the part of the COE's movement that went with changes in the quota
(two-stage least squares, an instrumental-variables method), to keep good
times alone from setting the estimate. That rests on an assumption the test
does not check: that the quota did not move with near-town demand. An
independent
second script recomputed every scored number and matched it.
{{< /aside >}}

## Sources

- HDB resale flat prices: data.gov.sg collection 189, Housing and Development
  Board, retrieved 6 October 2026, under the Singapore Open Data Licence
  version 1.0.
- COE premium, quota and successful bids: SingStat Table Builder M651121,
  data source Land Transport Authority, retrieved 5 and 6 October 2026.
- Vehicle growth rate cut to 0% from February 2018, and the quota set largely
  by deregistrations: Parliament of Singapore, oral answer by the Senior
  Minister of State for Transport for the Minister for Transport, 6 November
  2017.
- Million-dollar resale counts: Parliament of Singapore, written answer by the
  Minister for National Development, 4 July 2022.
- MRT station exits: data.gov.sg, Land Transport Authority. Block locations:
  contains information from OneMap (Singapore Land Authority), accessed 5 and
  6 October 2026, under the Singapore Open Data Licence version 1.0.
- COE supply redistribution: Ministry of Transport, written reply, 4 November
  2025.
- Town distances (Toa Payoh, Woodlands): median block distance from Raffles
  Place, cargradient/article/town_distances.py, from the geocoded blocks and
  the resale files' town labels.
- Transport for London, "Congestion Charge",
  [tfl.gov.uk/modes/driving/congestion-charge](https://tfl.gov.uk/modes/driving/congestion-charge),
  saved 5 October 2026.
- Huang, Li and Ross, "The impact of the cost of car ownership on the house
  price gradient in Singapore", Regional Science and Urban Economics 68
  (2018), 160-171.

Code, data, the sealed thesis and every number above:
[cargradient/ in hdb-affordability](https://github.com/jacobbuildmodel/hdb-affordability/tree/main/cargradient).

Next: the next open question is posted on the [open questions page](/open/).

*A historical reading of public data, in past tense throughout. It is not
advice, and nothing here is tailored to any reader's own flat or car.*
