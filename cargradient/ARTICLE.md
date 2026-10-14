---
# DRAFT for Checkpoint 2. The title is a proposal: Jacob decides titles.
# Other proposals: "Since 2016, no sign COEs tilted HDB prices toward town"
# (54 characters, the lead chart's title). The date is a proposal, not agreed:
# 2026-10-31 and 2026-11-14 are taken in content/economics/.
title: "Flats near town gained when COEs rose. Not since 2016."
question: "Million-dollar flats came with $100,000 COEs. Coincidence?"
date: 2026-11-28
draft: true
showToc: true
summary: "Does a dearer COE make a flat near town worth more, even to a family with no car? Three predictions were sealed before the HDB resale prices were opened. From 2002 to 2015 flats near Raffles Place gained on flats further out when COEs rose; since 2016 there was no sign of it."
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
> **Key number:** the COE rise from 2020 to 2023 implied a change of -79 dollars per square metre in the price gap between a flat 5 km and one 20 km from Raffles Place (95 per cent interval -317 to 158), from 257,854 resales since 2016.\
> **My confidence going in:** 70%, 40% and 15% on three predictions, 1.25 expected to hold.\
> **Scored:** 1 of 2 held; the third was not scored.\
> **What would change it:** a near-town tilt since 2016 that holds up with the drift in near-town prices ruled out.

In the first bidding of June 2022, the COE for larger cars closed at or above
$100,000 for the first time. The year before, 259 HDB resale flats had sold for
$1 million or more, up from 46 in 2017. Two headlines, argued about
separately. Could they be one story?

Most people would say no. A COE is a car-owner's problem. A family with no car
pays nothing for it. But one study of private condos found that when COEs cost
more, homes near the city centre gained on homes further out. I put the same
question to HDB resale flats and wrote down my bets before I opened the price
data. The tilt was there from 2002 to 2015. Since 2016 there was no sign of it.

## The argument: two separate prices, or one story

**Separate stories.** A COE is the price of the right to own a car. What a flat
costs is about its size, its lease and where it is. A family that will never
drive has no stake in the COE, so there is no reason the two would move
together.

**One story.** Huang, Li and Ross (2018) argued the opposite for private homes.
Some households sit on the edge of owning a car. When the COE rises, some of
them go without one, and a household without a car values a short train ride
to work more than one with a car does. So part of what a home near town costs
moves with the COE, whoever buys it. They found that tilt in private condos
from 2002 to 2015.

## Pushed to the extreme: the last bus home

These are thought experiments, not claims about the data.

Picture cars costing almost nothing. Every family drives, a flat at the end of
the line is a short drive from anywhere, and a change in the price of cars
barely moves what a flat near town is worth. Now picture cars out of reach.
Nobody drives, every family lives by the train timetable, and nearness to town
is everything. Singapore sits between the two, where a dearer COE can tip a
few households from one side to the other.

It works like the last bus home. When it stops running, the room nearest the
office is worth more, to everyone who has no other way back. Call it the
last-bus premium: the extra a home near town is worth when getting around
without a car gets harder. The question here is whether that premium showed up
in HDB prices, and moved with the COE.

## My bets: a tilt in both periods, weaker after 2018

I sealed three predictions on 12 October 2026, before opening the resale
prices, and posted them on an
[open question page](/open/2026-10-12-million-dollar-flats/). This study
applies the method of Huang, Li and Ross (2018) to HDB resale flats.

1. **Their years** (70%). From 2002 to 2015, when COEs cost more, HDB flats
   near Raffles Place gained relative to flats further out. Why, in my words
   at the seal: "Same city, same years and same COE swings as a paper that
   found the effect strongly in condos, and the central HDB premium widened
   over most of those years."
2. **Since then** (40%). The same was true from 2016 to 2026. Why: "COEs
   tripled in 2021-23, but outer towns kept pace with central ones, and the
   only clear tilt toward far-out flats came just as COEs started rising."
3. **After the 2018 cut** (15%). After growth in the car quota was cut to zero
   in February 2018, the tilt got weaker. My Why began: "I'd lean weaker, but
   not by much."

Together the percentages put the expected number holding at 1.25 of 3. The
exact wording, the gates and the full Why lines are in the
[sealed thesis](https://github.com/jacobbuildmodel/hdb-affordability/blob/7ee9b9169c36399a80400b0e2e9ef9bd6b5000af/cargradient/THESIS.md).

## What the data said: a tilt to 2015, none since

![Change in the price gap between a flat 5 km and one 20 km from Raffles Place for each COE rise, by period](/figs/cargradient_chart1_tests.svg)

*How to read it: a dot right of zero means flats near town gained on flats far
out when COEs rose; the line is the 95 per cent interval. A line that crosses
zero is no clear link. Muted rows were not scored.*

The test compared every HDB resale with the COE premium in its quarter and its
block's distance from Raffles Place, holding fixed each block, each flat type,
each storey range and the lease left. It asked whether flats near town did
better than flats further out in the quarters when COEs cost more. It is a test
of whether the two moved together, not of what caused what.

From 2002 to 2015 they did. Across 349,122 resales in 8,400 blocks over 54
quarters, flats nearer Raffles Place gained on flats further out when the COE
rose, and the 95 per cent interval sat wholly on that side of zero. My first
bet held.

From 2016 to 2026 they did not. Across 257,854 resales in 9,768 blocks over 42
quarters, the 95 per cent interval ran from a tilt toward town to a tilt away
from it, and so included zero. My second bet failed.

## Where I was wrong: no link since 2016

I gave the second bet 40%, and it failed. The clearest way to see its size is
the calculation I sealed for this. Between 2020 and 2023 the average COE
premium rose from $36,753 to $106,219, a rise of $69,465. Using the estimate
from 2016 onward, that rise implied a change of -79 dollars per square metre in
the gap between a flat 5 km and one 20 km from Raffles Place, with a 95 per
cent interval from -317 to 158. That interval runs from the near-town flat
losing ground to it gaining ground.

I had also planned to say what share of the actual change in that gap lined up
with the COE. That share is not meaningful here. The actual gap moved by 67
dollars per square metre from 2020 to 2023, but with an interval from -58 to
193, so it did not clearly change at all, and the implied change pointed the
other way. My own rule, written before the data, says to report the implied
change alone in that case.

The third bet was never tested. It needed a tilt toward town in 2012 to 2017
to weaken after 2018. There was none: in those years the estimate pointed the
other way, with flats further out gaining when COEs rose, and its interval
cleared zero. With no tilt before 2018, there was nothing to weaken, and my
sealed rule takes it out of the count.

So 1 of 2 scored bets held, against the 1.1 I expected for those two. The
Brier score, which measures how far each confidence sat from what happened,
was 0.125, where a forecaster who always says 50 per cent scores 0.25 and lower
is better. Two predictions are far too few to judge anyone's calibration.

## Where the finding flips: around 2012

Split at 2012, when HDB's records switched from the date a sale was approved
to the date it was registered, the years 2002 to 2011 showed the tilt toward
town, and the years 2012 to 2015 showed the opposite. Checks on the years since
2016 pointed both ways. Leaving out 2020 to 2022 showed a tilt toward town;
ending in early 2023, before the COE supply was redistributed, showed a tilt
the other way. None of these checks was
scored, and the full set is in RESULTS.md.

## The obvious objection: isn't this just good times?

COE prices rise in good years. If good years also lift flats near town more
than flats far out, for reasons that have nothing to do with cars, the 2002 to
2015 result would show up anyway. The test leans on the car quota, set mostly
from the number of cars taken off the road, as the thing that moves the COE.
That helps, but it does not close the door. The sealed limit says so:

> A SURVIVE cannot rule out a slow drift in how much buyers pay to live near
> town that happened to move with the COE premium. In placebo runs with such a
> drift, the scored test found a link about half the time when none existed.

So the bet that held is weaker evidence for the car story than the bet that
failed is against it.

## What it changes: no case for counting the COE

For a buyer weighing a flat near town against one further out, there was no
sign that the gap between them moved with COEs in HDB flats since 2016.
Whatever moved the near-town premium in those years, this test found no sign
that the COE was part of it. For anyone weighing vehicle-quota policy, there
is no evidence here of a side-effect on flat prices for households that never
drive. For the pricing of new flats near town under the Prime Location model,
this data makes no case for counting COEs in the near-town premium.

## Elsewhere: London charges the trip, not the car

Singapore rations who may own a car. London prices driving into its centre
instead. Transport for London charges a daily fee of GBP 18 (GBP 21 if paid
by midnight of the third day after travel) to drive within its Congestion
Charge zone, from 7:00 to 18:00 on weekdays and 12:00 to 18:00 at weekends
and on bank holidays. There the cost
lands on the trip into town, not on owning the car.

## What would change my mind

- A tilt toward town since 2016 that survives with the slow drift in
  near-town prices ruled out.
- A record of who gave up a car and where they moved, which this data does not
  have.
- The same test on private homes since 2016, the paper's own market.

## The verdict: no sign of a link since 2016

No sign of a link in HDB flats since 2016. In 2002 to 2015, the paper's years,
the gap widened more when COEs rose. There was no link before 2018 to weaken.

At most, this explains part of the near-town premium, not million-dollar flats
as a whole.

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
1.181e-03 (9.486e-04 to 1.414e-03). Intervals are clustered by block and by
quarter.

**Method.** As in the paper, the car quota stands in for the COE: the test
uses only the part of the COE's movement that went with changes in the quota
(two-stage least squares, an instrumental-variables method), so that good
times alone do not set the estimate. An independent
second script recomputed every scored number and matched it.
{{< /aside >}}

## Sources

- HDB resale flat prices: data.gov.sg collection 189, Housing and Development
  Board, retrieved 6 October 2026, under the Singapore Open Data Licence
  version 1.0.
- COE premium, quota and successful bids: SingStat Table Builder M651121,
  data source Land Transport Authority.
- Million-dollar resale counts: Parliament of Singapore, written answer by the
  Minister for National Development, 4 July 2022.
- MRT station exits: data.gov.sg, Land Transport Authority. Block locations:
  contains information from OneMap (Singapore Land Authority), accessed 5 and
  6 October 2026, under the Singapore Open Data Licence version 1.0.
- COE supply redistribution: Ministry of Transport, written reply, 4 November
  2025.
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
