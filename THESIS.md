# THESIS: has HDB resale affordability actually worsened?

SEALED 11 September 2026, after three review changes and before any transaction
data was downloaded. Not edited after sealing. Anything added later goes in
THESIS_ADDENDUM.md, dated.

Author: Jacob Ong. Repository: hdb-affordability.

---

## 1. The question, and why the obvious answer is not an answer

Resale flat prices have risen. Nobody disputes that and a piece establishing it
would be worthless.

Affordability is a ratio. Three things moved over the period and they moved
independently: the price of a flat, what households earn, and what the state hands
a buyer at the point of purchase. A fourth thing, the cost of borrowing, is the
usual dominant term in any affordability study anywhere in the world, and in
Singapore it is nailed to the floor.

So the question is not whether prices rose. It is what happened to the ratio, and
which of its moving parts did the work.

## 2. What is already known, before any data is touched

Stated here so that it is on the record as an input rather than presented later as
a finding.

**The HDB concessionary loan rate has not moved.** It is pegged at 0.1 percentage
points above the CPF Ordinary Account rate. The OA rate has been 2.5 per cent since
1999, so the concessionary rate has been 2.6 per cent for over two decades.

This is the fact that makes the Singapore case different. In the United States, the
United Kingdom or Australia, an affordability series is dominated by the mortgage
rate, and falling rates have repeatedly rescued affordability measures while prices
climbed. For a Singaporean buyer taking an HDB loan, that rescue is not available
and never was. The financing channel is switched off by design. Whatever happened
to affordability here is price and income and grants, and nothing else.

I verified the rate before sealing this file. It is a design input. Test T2 below
still checks it in code, because a pipeline that assumes a constant is a pipeline
that will not notice when it stops being one.

**Grants moved a great deal.** At least three changes sit inside the likely window:
the Enhanced CPF Housing Grant replacing the AHG and SHG in September 2019, the CPF
Housing Grant for resale rising from 50,000 to 80,000 for 2- to 4-room flats at
Budget 2023, and a further Enhanced CPF Housing Grant increase in August 2024.
Grants are means-tested and steeply tapered by income.

That combination is the reason this question is worth asking. The one lever that
moved is the one that does not apply equally to everyone.

**And the thresholds that decide who gets them did not all move together.** The
Enhanced CPF Housing Grant ceiling has been 9,000 dollars a month since it was
introduced in September 2019. The ceiling for the CPF Housing Grant for resale
flats, and for an HDB loan, went from 14,000 to 16,000 over the same period. A
frozen threshold in a rising income distribution admits fewer households every
year without anyone changing it. That is what T7 tests.

## 3. The lead measure

**Lead: the mortgage servicing ratio for a standardised first-timer buyer, on the
price net of grants.**

    MSR(t, p) = monthly repayment(t, p) / monthly household income(t, p)

where p indexes the buyer's position in the income distribution, and

    purchase price      P*(t)   constant-quality four-room resale price, section 5
    grants              G(t, p) published schedule in force at t, for a first-timer
                                family at income percentile p
    loan                L       = min( LTV(t) x P*(t),  P*(t) - G(t, p) )
    monthly repayment           standard amortisation of L at the HDB concessionary
                                rate in force, over a 300-month tenure
    income                      monthly household income from work EXCLUDING
                                employer CPF contributions, at percentile p

Employer CPF is excluded because that is the basis HDB assesses income on. The
including-CPF series is carried as a sensitivity and both are reported.

Tenure is fixed at 25 years rather than the maximum available, so that a change in
the maximum tenure cannot masquerade as a change in affordability.

**Why this measure leads.** It is the only candidate that composes all four moving
parts into one number, it is what a household actually experiences month to month,
and it is the quantity HDB itself regulates through the mortgage servicing ratio
cap. A reader can recompute it from the formula above.

**Reported alongside, not instead:**

- **Measure 2, price to annual household income**, on the headline constant-quality
  price before grants. The conventional measure, the one everyone quotes. Included
  precisely so that the piece can show whether the conventional measure and the
  lead measure disagree.
- **Measure 3, years of income to accumulate the down payment.** The purchase price
  less the loan, divided by annual household income. This is the constraint buyers
  describe in practice, and it behaves differently from the monthly one because
  grants land on it directly.

If measure 2 and the lead measure point in different directions, both are reported
with equal prominence and the piece explains the divergence rather than picking a
winner.

## 4. The subgroup

**Four-room resale flats, nationally.**

Defended: the four-room flat is the modal resale flat type and the one a first-time
family buyer typically targets. It exists in both mature and non-mature estates, so
the town controls do real work rather than being collinear with the flat type.
Restricting to one flat type removes the largest single source of composition
drift before any modelling starts.

Not "all HDB resale", for the reason the brief gives: a three-room in Queenstown
and a four-room in Sengkang are not one market and averaging them measures the
basket, not the price.

**Three buyers, fixed in advance:** households at the 20th, 50th and 80th
percentile of resident employed household income from work. Three rather than one,
because the grant schedule is steeply means-tested and the entire question of
whether affordability moved in one direction depends on where in the distribution
you stand. Choosing one buyer after seeing the results would be the exact failure
this file exists to prevent.

**Window: calendar years 2013 to the last complete year, which is expected to be
2025. A 2017 start was considered and rejected.**

The reason matters enough to state. Resale prices fell from 2013 to 2019 and rose
sharply from 2020. A window starting in 2017 therefore starts near a cyclical low
and runs to a high, which flatters any "affordability worsened" finding before a
single number is computed. That the 2017 file is one convenient download is
convenience, not identification, and convenience is not a defence.

Transactions are recorded on a registration-date basis from March 2012 onwards, so
2013 is the first complete calendar year on a consistent basis. That window spans a
peak, a trough and a peak, and the headline comparison is made across it.

Two consequences, both accepted in advance:

- The 2017-to-2025 comparison is still computed and published, labelled as the
  near-trough base. If the two windows give materially different answers, that gap
  is itself reported as a finding about how much the base year does the work.
- The `remaining_lease` column exists only in the January 2017 file onwards. For
  earlier years it is reconstructed as 99 minus the flat's age at sale, from
  `lease_commence_date`. That reconstruction is exact to within a year and the
  cleaning script asserts it reproduces the published column on the overlapping
  period. If it does not reproduce it, the hedonic runs on flat age instead and
  says so.

Partial-year 2026 may be shown, labelled as partial, and appears in no headline
comparison. This is stated in advance because a headline resting on a part year is
a known failure on this site.

The grant-adjusted lead measure runs only over the years for which the grant
schedule can be sourced from primary documents, which may be shorter than 2013 to
2025. Where it is shorter, the chart shows the shorter line and the text says why,
rather than extending a modelled grant back into years I cannot document.

## 5. How composition is handled

This is the largest threat to the result and it is handled in two independent ways,
both reported.

**Method A, hedonic with time dummies.** Regress log resale price on year dummies,
town fixed effects, floor area, storey range, flat model and remaining lease. The
year dummy series is the constant-quality price path. The remaining-lease term is
included because the stock is ageing and lease decay is a real price driver, not
noise.

**Method B, fixed 2017 basket.** Compute median price within each cell defined by
town and floor-area band, then aggregate using each cell's share of 2017
transactions held fixed. A Laspeyres index, which makes no functional-form
assumption at all.

If A and B disagree materially, both are published and the piece says the
composition correction is doing contested work. If they agree, that agreement is
itself evidence the correction is sound.

The raw median four-room price is also shown, so a reader can see exactly how much
the correction moved the answer.

## 6. Pre-registered tests

Each states its own fail condition. All are reported, whichever way they come out.

**T1. The conventional measure worsened.**
The constant-quality four-room price divided by annual median household income
rises by more than 0.5 years of income between the first and last complete year.
- F1: if it changes by less than 0.25 years in absolute value, the conventional
  measure says unchanged, and that becomes the lead finding instead.

**T2. Financing contributed nothing.**
The HDB concessionary rate is 2.6 per cent in every year of the window.
- F2: if the rate moved by more than 0.1 percentage points at any point, the MSR
  change is decomposed into price, income and rate contributions, and section 2 of
  this file is wrong about the Singapore case being different.

**T3. Grants moved enough to matter.**
For the 20th-percentile buyer, the increase in total grants between the first and
last complete year exceeds 40 per cent of the increase in the constant-quality
price over the same period.
- F3: if that figure is below 10 per cent, grants are a footnote rather than a
  mechanism, and the piece drops the divergence argument.

**T4. How far apart did the two ends of the distribution move. This is the headline
test, and it is about magnitude, not sign.**

The direction is expected by construction and the piece must not present it as a
discovery. The CPF Housing Grant for resale flats carries a household income
ceiling and the Enhanced CPF Housing Grant carries a lower one. An 80th-percentile
household sits above both in every year of the window, so it receives no
means-tested grant at any point, so its effective mortgage servicing ratio is
whatever the headline one is. That the low-income buyer does better is what
means-testing is for. Finding it in the data would be finding that the policy
works as written, which is not a finding.

The open questions are how much, and whether it was enough:

- **T4a.** The change in effective mortgage servicing ratio between the first and
  last complete year is at least 5 percentage points smaller for the
  20th-percentile buyer than for the 80th-percentile buyer.
- **T4b, the one that carries the piece.** For the 20th-percentile buyer, the
  effective mortgage servicing ratio in the last complete year is no higher than in
  the first. That is full offset: grants rose by enough to absorb the entire price
  rise for that buyer. Partial offset is the middle case and is reported as a
  percentage of the gap closed.

Fail conditions, covering all three outcomes so none is left undefined:
- F4a: the two buyers' changes are within 2 percentage points of each other. Then
  means-testing did not bite in practice despite being written into the schedule,
  the piece reports one number for all buyers, and says so.
- F4b: both move in the same direction but differ by more than 5 percentage points.
  Then the result is heterogeneity without sign divergence. Reported in those
  words. This is the most likely outcome and the piece is written to survive it.
- F4c: the changes carry opposite signs. Reported as full offset and better, with
  the explicit caveat that the sign is a property of the grant schedule rather than
  a discovery about the housing market.

**T5. Composition mattered.**
The constant-quality index and the raw median four-room price differ by more than 3
percentage points cumulatively over the window.
- F5: if they differ by less than 1 percentage point, the piece states that
  composition did not matter here and shows the two lines on top of each other.

**T6. The two composition methods agree.**
Methods A and B differ by less than 2 percentage points cumulatively.
- F6: if they differ by more than 5 percentage points, no single constant-quality
  number is published. A range is published instead.

**T7. The median household crossed the Enhanced CPF Housing Grant income ceiling
inside the window.**

The Enhanced CPF Housing Grant carries a household income ceiling of 9,000 dollars
a month. It was introduced at 9,000 in September 2019 and is still 9,000 in 2026,
so it has not moved in seven years. Over the same seven years the ceiling for the
CPF Housing Grant for resale flats, and for an HDB loan, went from 14,000 to
16,000, and household incomes rose.

The test: the median of resident employed household monthly income from work
excluding employer CPF sits below the Enhanced CPF Housing Grant ceiling in force
in an early year of the window and above it in the last complete year.

If it holds, the typical household stopped qualifying for the Enhanced CPF Housing
Grant at some point inside the window, while the maximum Enhanced CPF Housing Grant
was being raised from 80,000 to 120,000. The piece reports the crossing year. A
grant got larger and the median household became ineligible for it, in the same
period, and I have not seen anyone write that up.

- F7a: the median is below the ceiling in every year. No crossing. Report the
  margin in the last complete year, and how many years of income growth at the
  trailing five-year rate would close it.
- F7b: the median is above the ceiling in every year. Then the median household
  never qualified at any point in the window, which is a different statement and
  also worth publishing.
- F7c: the ceiling turns out not to have been constant at 9,000 across the window.
  Then it is recomputed against the ceiling actually in force each year, and the
  seven-year-freeze framing is withdrawn.

Reported alongside T7, whichever way it goes: the Enhanced CPF Housing Grant
ceiling as a ratio of median household income, one figure per year. A single line
that shows whether the freeze is biting.

**What T7 is not.** SingStat's percentile series covers resident employed
households, not flat buyers, who are younger and differently distributed. HDB
assesses the average gross monthly household income over the preceding twelve
months, which is not the same construct. So T7 says where the typical household
sits relative to the threshold. It does not count buyers who lost eligibility, and
the piece must not let a reader think it does.

**The grant parameters this test rests on, and their status.** Enhanced CPF Housing
Grant for families, up to 120,000, income ceiling 9,000 a month. CPF Housing Grant
for resale flats, up to 80,000 for 2- to 4-room and up to 50,000 for 5-room and
larger, income ceiling 16,000 a month, raised from 14,000 on 24 August 2026.
Proximity Housing Grant, 30,000 living with a parent or child and 20,000 within
four kilometres, no income test. Maximum combined 230,000. Taken from CPF Board's
own guide and from HDB's MyNiceHome, both read on 11 September 2026. They are
requested again as saved PDFs in DATA_REQUEST.md because both pages render their
tables in JavaScript and only the prose could be read from here. If a saved PDF
contradicts any figure above, the PDF wins and this paragraph is corrected in the
addendum, not here.

## 7. What counts as an answer

On the lead measure, for the median buyer, between the first and last complete
year:

- **Worsened** if the effective mortgage servicing ratio rises by more than 3
  percentage points.
- **Improved** if it falls by more than 3 percentage points.
- **Unchanged** if it moves by less than 3 percentage points either way.

Three percentage points is chosen because it is roughly a tenth of the 30 per cent
mortgage servicing ratio cap HDB applies, so a movement of that size changes what a
household can actually borrow. It is set now so that it cannot be set later.

## 8. The headline I expect to be able to write

Stated in advance so that a different outcome is visibly a different outcome.

If T7 holds, it is the headline, because it is the only result here that nobody has
already written: **"The grant grew. The median household aged out of it."** (54
characters), or **"A bigger grant the middle stopped qualifying for"** (47).

If T7 fails and T4b holds, the headline is about full offset for the low-income
buyer: **"Grants absorbed the whole price rise, for some buyers"** (52).

If T7 fails and T4b fails, which is the most likely single outcome, the honest
headline is about partial offset and the size of the gap closed. Something shaped
like **"The grants covered about half of it"**, with the actual fraction in place
of "about half".

If F1 triggers, the headline is that the conventional measure moved less than
everyone assumes, and the piece is shorter.

Four outcomes, four headlines, written down before the data arrives so that
whichever one gets used is visibly the one the data produced. Only the first two
are interesting. That is precisely why they are named now rather than chosen later.

## 9. What this design cannot settle, known in advance

- **Why** prices moved. Cooling measures, the wait-out rule, pandemic construction
  delays and BTO supply all push demand between the new and resale markets inside
  this window. They are confounds, they are not identified here, and the piece
  makes no causal claim about the cause of the price path.
- Anything at month-level timing. The transaction file is by registration date, not
  by the date a price was agreed. All analysis is annual, with quarterly shown only
  for context.
- The experience of buyers who are not first-timer families. Second-timers, singles
  and non-citizen households face different grants or none, and are out of scope.
- Whether a buyer takes an HDB loan or a bank loan. The lead measure assumes an HDB
  concessionary loan throughout. A bank-loan buyer faced a very different rate path
  after 2022, and that is named as a limitation rather than modelled.

## 10. Conditions under which I abandon or reshape the piece

- If the grant schedule cannot be sourced from primary documents for every year in
  the window, measure 1 is dropped entirely and the piece runs on measures 2 and 3
  with an explicit statement that grants are omitted and what that omits.
- If the household income series is not available at the 20th and 80th percentile
  on a consistent basis, the three-buyer design collapses to the median alone and
  T3 and T4 are reported as untestable rather than quietly dropped.
- If the hedonic year dummies are not identified, or method A and method B diverge
  past the F6 threshold, no constant-quality number is published.
- If the history of the Enhanced CPF Housing Grant income ceiling cannot be
  established from primary documents for every year since September 2019, T7 is
  reported against the ceiling only for the years that can be sourced, and the
  seven-year-freeze claim is not made. The claim rests on the ceiling having stayed
  at 9,000, and one undocumented year is enough to withdraw it.
- If the earlier transaction files cannot be obtained, the window falls back to
  2017 to 2025 and the piece states in its own text that the base year sits near a
  cyclical low, what that does to the headline, and that the longer window was
  attempted and not available.
