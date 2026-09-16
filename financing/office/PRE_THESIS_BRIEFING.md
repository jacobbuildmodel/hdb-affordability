# Pre-thesis briefing: the HDB financing piece

Written 16 September 2026, for the checking chat. Nothing has been downloaded and
no THESIS.md exists yet. Answers are in the order asked.

---

# 1. The brief, in full

Reproduced as received. There have been **no amendments from Jacob**. Two things
below the brief are my own proposals and are **not yet accepted**; they are flagged
at the end of this section.

## 0. Who receives this work

The output goes to a coordinating Claude instance that is the single verification
point for the project. Jacob pastes the work there unedited. It has a Linux sandbox
and runs things. It downloads the repository from GitHub, deletes every output, runs
the pipeline from clean and compares MD5s. It recomputes headline figures
independently in pandas rather than trusting the arithmetic. It audits
requirements.txt against every import using the AST. It builds the site with Hugo
and screenshots at 390px in light and dark. It opens the sources cited.

Things this caught before publication on earlier pieces: a headline resting on a
partial year that flattered the comparison; five scripts that failed on a clean
machine because a dependency was undeclared; an income ceiling back-dated by three
years inside a row marked VERIFIED-PRIMARY; a repository pushed one directory too
deep so its README never rendered; a filename collision that would have silently
overwritten a published article.

State uncertainty rather than smoothing it. A stated limitation is treated as good
work. Show which basis or window produced each number.

## 1. The question

**Was the HDB concessionary loan actually the cheaper option?**

It has been fixed at 2.6 per cent since 1999, pegged 0.1 points above the CPF
Ordinary Account rate, and it is presented as the safe, subsidised choice. But
Singapore bank mortgage rates ran well below 2.6 per cent for roughly a decade
before rising sharply from 2022.

So a buyer who chose the HDB loan in, say, 2015 paid above market for years. Whether
they came out ahead over the full loan depends on how long the cheap period lasted,
how far rates rose afterwards, and whether they could have refinanced.

Model it properly. Not a ratio, an actual cash-flow comparison over the life of the
loan.

WHY THIS IS NOT A REPEAT OF THE PUBLISHED PIECE. That one measured affordability as
price over income and found the loan-to-value cap binds by 2025. This one measures
the cost of the financing choice itself, which that piece did not touch. Read it
first and make sure you are answering a different question.

WHAT THIS MUST NOT BECOME. No recommendation about which loan anyone should take.
The site publishes reasoning, never advice, and Jacob is not licensed by MAS. State
what the numbers show and what would change them. Never tell a reader what to do.

## 2. Pre-register before you see the rate data

Write THESIS.md and seal it before downloading anything.

State: the cohorts you compare, meaning which purchase years. The loan terms, tenure
and loan-to-value. The refinancing rule, because a bank borrower can refinance and
an HDB borrower can switch to a bank but not back. The rate path assumption for
years still in the future. And the verdict condition: what total-cost difference
counts as the HDB loan having been cheaper, more expensive, or indistinguishable.

The refinancing rule is the crux and it is where this analysis can be quietly
rigged. A bank borrower who refinances optimally at every opportunity is not a real
person. State your assumption, and run at least one alternative.

Pre-register at least:
  T1  Total nominal cost over full tenure, HDB against bank, for each cohort.
  T2  The crossover year, if any, where the cumulative position flips.
  T3  Sensitivity to the refinancing assumption.
  T4  What happens to a borrower who switched from HDB to bank and could not switch
      back when rates rose.

Each with a fail condition.

## 3. Data, and the hard part

The HDB side is settled. 2.6 per cent throughout, already sourced in the existing
repository. Confirm from the HDB interest rate page already in raw/.

The bank side is the problem and you should solve it before anything else.

You need a Singapore housing loan rate series covering roughly 2010 to 2025.
Candidates to investigate:
  - MAS Monthly Statistical Bulletin, which publishes domestic banks' housing loan
    rates
  - SORA and its predecessor SIBOR, published by MAS, plus the spread banks charged
    over it
  - Published board rates or fixed-rate packages, which are harder to source
    historically

MAS and data.gov.sg return 403 to sandboxes. Identify exactly what you need with
URLs and ask Jacob in ONE consolidated message. Include the file size and a fallback
if it is large.

If no defensible bank rate series exists publicly, say so before investing time.
That is a valid outcome and the piece becomes about why the comparison cannot be
made honestly, which is still publishable here.

Every figure traces to a named document with a date. Never invent one. Show the
arithmetic.

## 4. Where this lives

Extend the existing repository rather than creating a new one. One raw data set, one
cleaning step, many analyses. A second repository means a second copy of the raw
files to keep identical, and they drift.

  github.com/jacobbuildmodel/hdb-affordability

Add a subdirectory, for example financing/, with scripts numbered continuing from
the existing sequence so run order across the whole repository stays unambiguous.
Its own README, its own checksums covering inputs and outputs, its own manifest.
Update the top-level README to list the new subdirectory, because that was missed
once before and a reader could not tell the new scripts existed.

Before handing over: delete the outputs, run from clean, confirm every checksum
still matches including the existing analysis you did not touch.

## 5. The article

Same structure and house style as the published pieces. Hook, unheaded
introduction, headings that read as a storyline, what would prove this wrong, what
this does not explain, what to take from this, sources.

Pure ASCII. No em dashes, no Unicode minus, no multiplication sign. Plain English.
Headline is the finding, under 60 characters. No royal "we". 1,200 to 1,800 words
of linear read.

Figures as SVG with a prefers-color-scheme block so they work in dark mode.

IMPORTANT ON FILENAMES. Pick a date that is not already used. Currently taken:
2026-08-22, 2026-08-29, 2026-09-05, 2026-09-08, 2026-09-12, 2026-09-19. A collision
would silently overwrite a published article.

## 6. How to present the work

Five things, clearly separated, not interleaved with commentary.

(1) The article, one markdown file, draft: true, front matter matching the
    published pieces including repo and dataset fields.
(2) The repository additions as a zip.
(3) The number manifest.
(4) What you could not verify.
(5) An honest note: did the data support the argument or did you soften a claim;
    did the pre-registered tests survive; how sensitive is the answer to the
    refinancing rule; which figures are load-bearing.

## 7. Start here

Do not write and do not request data yet.

1. Read the published HDB piece and the repository.
2. Establish whether a defensible public bank mortgage rate series exists. This
   decides whether the piece is possible. Report what you found before anything
   else.
3. Then write THESIS.md and show it before requesting files.

## Later instruction added by Jacob, 16 September 2026

Additional standing rules for this piece:

- This is a historical comparison by loan start year. Never write "choose X" or
  anything aimed at one reader's situation. The Financial Advisers Act rules apply
  in full.
- Pure ASCII: no em dashes, no Unicode minus signs, no multiplication signs.
- Do not touch any data until THESIS.md is sealed with numbered survive-if and
  fail-if conditions.

## Changelog since the brief was first sent

**No changes to the brief itself.** Two items are my proposals, reported to Jacob on
15 September 2026 and **not yet accepted**:

1. A design pivot: solve for the break-even spread rather than assume a spread. See
   section 2 below.
2. An article date of **2026-09-26**, chosen to avoid the six taken dates.

Neither is in force. Both need Jacob's agreement before THESIS.md is sealed.

---

# 2. Does a public bank mortgage rate series exist for 2010 to 2025?

**No.** Not one that measures what borrowers actually paid.

The short version: the benchmark is public, the mortgage rate is not, and the gap
between them is a bank's commercial margin that no Singapore authority publishes.

## Candidates, one by one

### 2.1 SORA and Compounded 3-Month SORA

- **Publisher:** SingStat, sourced from MAS. Dataset "Current Banks Interest Rates
  (End Of Period), Monthly".
- **ID:** `d_5fe5a4bb4a1ecc4d8a56a095832e2b24`
- **URL:** https://data.gov.sg/datasets/d_5fe5a4bb4a1ecc4d8a56a095832e2b24/view
- **Frequency:** monthly, end of period. Dataset last updated 8 September 2026.
- **Coverage:** the dataset runs Jul 2005 to Jul 2026, but the two SORA series start
  around **2009**, not 2005. No gaps found inside their own span. That covers 2010
  to 2025 in full.
- **What it measures:** a **benchmark**. SORA is the volume-weighted average rate of
  unsecured overnight interbank SGD transactions. The compounded 3-month version is
  the backward-looking average used to price floating mortgages after 2020.
- **Housing loans specifically:** no.
- **Fixed or floating:** neither; it is the reference rate a floating package is
  priced against.
- **Indicative levels seen on the dataset page:** about 0.24 to 0.37 per cent in
  2015, about 0.06 to 0.45 in 2020, about 3.35 to 3.77 in 2023, about 1.77 to 2.29
  in 2026. Read off the page, not from a downloaded file, so INDICATIVE only.

### 2.2 MAS Monthly Statistical Bulletin, Table III.3

- **Publisher:** MAS. "III.3 Interest Rates of Banks and Finance Companies
  (Monthly)".
- **URL of the historical CSV:**
  https://www.mas.gov.sg/-/media/mas-media-library/statistics/monthly-statistical-bulletin/msb-historical/interest-rates-of-banks-and-finance-companies---monthly.csv
- **Frequency:** monthly.
- **Coverage and contents: UNVERIFIED.** The CSV, the MSB landing page and the
  eServices table all return **403** to this environment. I could not read the
  column list, so I cannot tell you whether it contains a housing loan rate.
- **What I expect, and expectation is not evidence:** prime lending rate, savings
  and fixed deposit rates, and possibly a finance-company housing loan rate.
  Finance companies are a small segment and not the banks the question is about.
- **This is the single highest-value file to check.** If it contains a banks'
  housing loan rate for 2010 to 2025, the whole design below changes and the piece
  becomes a direct comparison. It needs a human to open it.

### 2.3 MAS, Data on Housing and Bridging Loans

- **Publisher:** MAS, part of the MSB.
- **URL:** https://www.mas.gov.sg/statistics/monthly-statistical-bulletin/data-on-housing-and-bridging-loans
- **Coverage and contents: UNVERIFIED, 403.** The title implies loan volumes and
  outstanding amounts rather than rates. Worth one look for the same reason as 2.2.

### 2.4 ABS Prime Lending Rates

- **Publisher:** Association of Banks in Singapore.
- **URL:** https://www.abs.org.sg/benchmark-rates/prime-lending-rates
- **Frequency:** weekly.
- **Coverage:** **current snapshot only.** ABS states on the page that "this
  publication page is overwritten weekly and no historical PLR data is archived."
  The latest snapshot seen was 11 September 2026.
- **What it measures:** "the lowest lending rate which a Bank or Institution is
  prepared to lend in Singapore dollars to its clients on an overdraft or demand
  basis." Not a mortgage rate, and Singapore mortgages are not priced off prime.
- **Verdict:** unusable. No history, wrong instrument.

### 2.5 SIBOR

- **Publisher:** ABS Benchmarks Administration, with MAS oversight.
- **Status:** discontinued. ABS ran a SOR and SIBOR transition to SORA; SIBOR was
  retired at the end of 2024.
- **Coverage:** no official downloadable historical archive found. ABS's transition
  FAQ is about the transition, not the history.
- **What exists instead:** third-party charts, for example housingloansg.com and
  moneylobang.com. These are commercial sites with no stated methodology or
  provenance and are **not usable** under the rules this project works to.
- **Why it matters anyway:** before 2020 floating mortgages priced off SIBOR, not
  SORA, and SIBOR sat above SORA by a term and credit premium. Any result expressed
  over SORA therefore misstates what a pre-2020 borrower faced, in a known
  direction. See section 4.

### 2.6 Bank board rates and fixed-rate packages

- **Publisher:** none. Each bank sets its own.
- **The authoritative statement is MAS's own.** Information Paper on Residential
  Mortgage Pricing and Disclosure Practices, November 2021:
  https://www.mas.gov.sg/-/media/MAS/News-and-Publications/Monographs-and-Information-Papers/INFORMATION-PAPER-ON-RESIDENTIAL-MORTGAGE-PRICING-AND-DISCLOSURE-PRACTICES.pdf
  It says variable-rate mortgages reference either a public indicator, "Singapore
  Interbank Offered Rate (SIBOR), Singapore Swap Offer Rate (SOR), Singapore
  Overnight Rate Average (SORA)", or "an administered rate which is determined by
  each FI (e.g. fixed deposit rate or internal board rate)". It says banks set the
  rate from "the cost to the FI of granting the mortgage (which includes the cost of
  funding and other costs), competitors' pricing and other strategic
  considerations". And it states that MAS "does not intervene directly in mortgage
  pricing".
- **Read plainly: the regulator supervises the practice and publishes none of the
  numbers.** This is the paper that closes the question.

### 2.7 Singapore Government Securities yields

Same data.gov.sg dataset as 2.1. Benchmarks, not mortgage rates. Useful only as
context on the level of rates.

### 2.8 Third-party aggregators

FRED, CEIC, TradingEconomics, FocusEconomics. Each mirrors official series such as
the interbank rate or the prime lending rate, or sells a derived one. None
originates a Singapore housing loan rate, and a mirror inherits the gap it is
mirroring. FRED's search is robots-disallowed to this environment in any case.

## Plain verdict

For 2010 to 2025 there is **no public series of the interest rate Singapore
borrowers actually paid on housing loans**, from any official source, for either
fixed or floating packages.

What is public and primary and continuous is a **benchmark**: SORA from about 2009.
The bank-side rate is benchmark plus a commercial margin, and the margin is exactly
the number that decides the answer.

Two caveats on my own verdict, stated because they could overturn it:

- MSB Table III.3 and the housing and bridging loans page are **403 to me and
  therefore unchecked.** If either carries a banks' housing loan rate, my verdict is
  wrong and the design should change. A human should open both before THESIS.md is
  sealed.
- I searched in English on the open web. A series behind a MAS login, in a
  discontinued publication, or in a printed MSB issue would not have surfaced.

## What the piece should become instead

Not "the comparison cannot be made". Invert it.

**Solve for the break-even spread.** For each loan start year, compute the constant
margin over compounded 3-month SORA at which a bank borrower would have ended the
full tenure exactly level with an HDB borrower on 2.6 per cent. Report that number
per cohort.

Why this is the honest design:

- The undocumented quantity becomes the **output**, not a hidden input. No spread is
  ever assumed, so there is nothing to rig.
- A reader who knows what they actually paid can locate their own cohort without
  being told anything about their situation.
- If the break-even spread for a cohort comes out at, say, 1.8 points, then only
  borrowers who got an unusually wide margin lost, and the piece says so with a
  number instead of an adjective.
- The result is a function, not an opinion, and it survives the fact that nobody
  publishes spreads.

All four pre-registered tests survive in this form. T1 becomes the break-even spread
by cohort. T2 is the crossover year, unchanged. T3 becomes sensitivity to the
refinancing rule rather than to an assumed level. T4, the borrower who switched from
HDB to a bank and could not switch back, is unchanged and is probably the sharpest
part of the piece.

---

# 3. The 2.6 per cent claim, and a correction you should know about

## The answer to the question asked

**CPF Board publishes the complete quarterly Ordinary Account rate history in one
document.**

- **Name:** "CPF Interest Rates", a table of Ordinary, Special, MediSave and
  Retirement Account rates.
- **Publisher:** Central Provident Fund Board.
- **URL:** https://www.cpf.gov.sg/content/dam/web/member/faq/documents/InterestRate.pdf
- **Coverage:** 1955 to September 2024, quarterly for recent decades.
- **What it shows:** the Ordinary Account rate at **2.50 per cent in every quarter
  from January 2010 onwards**. A footnote marks calculated rates with an asterisk,
  meaning the rate that would have applied with no legislated minimum, which is how
  a reader can see the floor binding rather than take it on trust.
- **Reachable:** yes. This PDF is readable from the analysis environment, unusually
  for a government PDF. It should still be downloaded and checksummed into `raw/`.

That single file covers January 2010 to September 2024. The tail is already in the
repository:

- `raw/cpf2.pdf`, CPF announcement for 1 Jan to 31 Mar 2016: the OA rate "will be
  maintained at 2.5% per annum ... as the computed rate of 0.21% is lower than the
  legislated minimum interest rate", and the HDB concessionary rate "will remain
  unchanged at 2.6% per annum".
- `raw/cpf3_q3_2026.pdf`, the announcement for 1 Jul to 30 Sep 2026: the same two
  sentences, computed rate 0.32 per cent.
- `raw/hdb_interest_rate_page.pdf`: the peg, "0.10% above the prevailing CPF
  Ordinary Account (OA) interest rate".

Between them: the mechanism, the full history to Sep 2024, and two anchor points
either side. October 2024 to mid-2026 is covered by the Q3 2026 announcement plus
the CPF rates page in `raw/cpf1.pdf`. If you want it airtight, one more quarterly
announcement from late 2024 or 2025 closes the last gap, and I have listed it as
optional in section 5.

## The correction

You are right that RESULTS.md said the history "is not yet sourced from a primary
document", and you are right to have flagged it. **That text was stale and it was my
error.**

The sequence: RESULTS.md is generated by `06_tests.py`, which hard-coded the T2
verdict as PARTIAL. When the CPF announcements arrived on 12 September I filed them
into `raw/` and wrote the correct account into the article, but I did not update the
hard-coded verdict and did not regenerate. So for four days the repository contained
two files that contradicted each other. The article was always right. RESULTS.md was
wrong.

Fixed on 16 September 2026. `06_tests.py` now reports T2 as **PASS**, lists the three
primary documents, and carries a dated revision note saying the earlier verdict was
stale and why. `RESULTS.md` and `CHECKSUMS.md5` have been regenerated; all 60
checksums verify.

**The published bundle therefore needs the updated `RESULTS.md`, `06_tests.py` and
`CHECKSUMS.md5`.** If the checking chat has the 12 September zip, it has the stale
version.

## What this means for the new piece

The new piece depends on the flat rate far more heavily than the published one did,
so it gets its own verification rather than inheriting one. The CPF history PDF goes
into `raw/`, gets a checksum, and the financing analysis asserts against it in code
rather than trusting a constant written into a script.

---

# 4. How I would define "cheaper"

Nothing here is settled. This is the proposal THESIS.md would formalise.

## 4.1 The comparison unit

**Primary: total nominal interest paid over the full tenure, by loan start year, on
an identical principal.** That is what the brief asks for and it is the number a
reader can hold.

**Reported beside it, not instead:**

- **Cumulative interest paid at each elapsed year**, which is what T2 needs. The
  crossover is only visible in the cumulative path.
- **Present value of the interest stream**, discounted at the CPF Ordinary Account
  rate of 2.5 per cent. This matters more than it looks. The HDB borrower pays more
  in the early years and the bank borrower more in the late years, and a nominal
  total treats a dollar in 2012 as a dollar in 2037. Reporting only the nominal
  total would flatter whichever loan back-loads its cost. Both get published, and if
  they disagree the article says so and explains which question each answers.
- **Monthly repayment paths**, shown in a figure but never as the headline, because
  comparing a flat repayment against a moving one is what makes people reach for the
  wrong conclusion.

Everything is in nominal Singapore dollars unless labelled as present value. No
inflation adjustment; stated.

## 4.2 What the bank borrower does when a fixed period ends

This is the crux and it is where the analysis can be quietly rigged, so it gets
three rules run side by side, all published.

- **R1, never act.** At the end of the fixed or teaser period the borrower rolls on
  to the bank's floating rate and never moves again. The realistic pessimistic case,
  and the one that describes a borrower who was busy.
- **R2, reprice on schedule. This is the base case.** Every three years the loan
  reprices to the then-prevailing benchmark plus the same spread, with no shopping
  around and no change of bank. It is the closest thing to a neutral assumption.
- **R3, refinance whenever it pays.** Move every time the saving over the remaining
  tenure exceeds the switching cost. Reported explicitly as **not a real person**
  and treated as an upper bound on what the bank route could have delivered.

Switching is not free, so R3 carries a cost per move: legal and valuation fees net
of any subsidy, plus clawback of subsidies if the move happens inside a lock-in. I
will set a single dollar figure, state it, and test the result against it. If the
break-even spread is insensitive to that figure the article says so; if it is not,
that sensitivity becomes a finding.

The HDB borrower has no equivalent choice. A borrower on an HDB loan may refinance
to a bank, but **cannot return to an HDB loan**. That asymmetry is the whole of T4
and it is modelled rather than described.

## 4.3 The bank's margin, when only a benchmark is public

Not assumed. Solved for.

**The break-even spread is the headline output**: the constant margin over compounded
3-month SORA that makes total cost equal. Computed per cohort and per refinancing
rule.

Alongside it, a **grid of fixed spreads**, say 0.25 to 1.50 points in steps of 0.25,
so a reader can find the row nearest what they actually paid. The grid is a table of
outcomes, not a recommendation, and it is described in the past tense.

Two things this does not fix, both stated in the piece:

- **Benchmark substitution.** Before 2020 mortgages priced off SIBOR, which ran
  above SORA. A break-even quoted over SORA therefore **overstates** the margin a
  pre-2020 borrower needed over their actual benchmark. If a SIBOR history can be
  sourced, the pre-2020 cohorts get recomputed on it; if not, the direction of the
  bias is stated and the pre-2020 numbers carry a health warning.
- **Fixed-rate packages.** A borrower on a two or three year fixed rate was not on
  benchmark plus spread at all. The model treats a fixed period as a constant rate
  equal to the benchmark plus spread at inception, which is an approximation and is
  labelled as one.

## 4.4 Loan limits and the stress rate

**Hold the principal identical across both routes.** The comparison is of the cost
of the financing choice, not of how much each route lets you borrow.

The reason is not convenience. The published piece already measured the loan-size
channel and found the loan-to-value cap binding by 2025. Letting principal differ
here would mix that finding back in and the two pieces would answer the same
question badly instead of different questions well.

So the loan-to-value schedules, the 30 per cent mortgage servicing ratio, the 55 per
cent total debt servicing ratio and the stress rates **do not enter the headline
calculation at all**. They are described in the article as the reason the two routes
are not interchangeable in practice, and they appear in one sensitivity where
principal is allowed to differ by the cap in force.

For the record, and only used in that sensitivity: HDB introduced a 3 per cent
interest rate floor for sizing eligible loan amounts on 30 September 2022, sourced
in `ltv_schedule.csv` from the MAS release. Banks size against a separate
medium-term rate under MAS rules. I have not verified the bank figure and will not
use it until I have.

## 4.5 Sensitivities

Every one pre-registered with a threshold before any data is touched.

1. Refinancing rule: R1 against R2 against R3.
2. Start year: every cohort from 2010 to 2025, so the answer is a curve rather than
   an anecdote.
3. Tenure: 25 years base, 30 years alternative. The published piece fixed 25 so that
   a change in maximum tenure could not masquerade as a change in affordability; the
   same logic applies.
4. Nominal against present value at 2.5 per cent.
5. Switching cost in R3.
6. Benchmark: SORA throughout, against SIBOR before 2020 if it can be sourced.
7. Rate path for years still in the future. Cohorts from about 2001 onwards on a
   25-year tenure do not complete inside the data, so the remaining years need an
   assumption. Base case is the forward path implied by the SGS curve; alternatives
   are the last observed rate held flat, and the long-run average. All three
   published, with the point where the assumption starts to bite marked on the
   figure.

## 4.6 Verdict condition

Stated before the data, per cohort, on total nominal interest at the base case R2:

- **HDB cheaper** if HDB total interest is more than 3 per cent below the bank
  route.
- **Bank cheaper** if it is more than 3 per cent above.
- **Indistinguishable** in between, and the word used is indistinguishable, not
  "similar".

Three per cent because it is comfortably larger than the rounding in a 25-year
amortisation and small enough to detect a real difference. The equivalent statement
in break-even terms is that a cohort's break-even spread is reported with the range
of spreads that would leave the two routes indistinguishable.

## 4.7 The compliance line

The piece is a historical comparison by loan start year and nothing else. It will
not contain "choose", "should", "better option", "recommend", or any second-person
construction aimed at a decision. Findings are past tense and cohort-level. The
article will carry an explicit line saying it is not advice and that Jacob is not
licensed by MAS. I will grep the finished text for a banned-word list before
handing it over.

---

# 5. Files needed, one list

Download date and any "last updated" date, please, for each.

## Essential

**F1. SORA and SGS yields, monthly.**
https://data.gov.sg/datasets/d_5fe5a4bb4a1ecc4d8a56a095832e2b24/view
Small, well under 100 KB. The only public benchmark covering the window.

**F2. CPF interest rate history, 1955 to 2024.**
https://www.cpf.gov.sg/content/dam/web/member/faq/documents/InterestRate.pdf
About 100 to 300 KB. This is the answer to your question 3 and it is what the whole
piece rests on.

**F3. MAS Monthly Statistical Bulletin, Table III.3, Interest Rates of Banks and
Finance Companies, monthly historical CSV.**
https://www.mas.gov.sg/-/media/mas-media-library/statistics/monthly-statistical-bulletin/msb-historical/interest-rates-of-banks-and-finance-companies---monthly.csv
Size unknown, probably under 1 MB. **This is the file that could overturn my verdict
in section 2.** Please open it and tell me the column headings even before sending
it. If it contains a banks' housing loan rate, say so immediately and I will rewrite
the design before sealing anything.

## Wanted

**F4. MAS, Data on Housing and Bridging Loans.**
https://www.mas.gov.sg/statistics/monthly-statistical-bulletin/data-on-housing-and-bridging-loans
Same reason as F3. Probably volumes, not rates. One look settles it.

**F5. MAS Financial Stability Review 2025.**
https://www.mas.gov.sg/-/media/mas-media-library/publications/financial-stability-review/2025/financial-stability-review-2025.pdf
Likely 5 to 10 MB. If it is too large to upload, the two things I need from it are
the share of outstanding housing loans on floating rather than fixed rates, and any
chart of average housing loan rates. A screenshot of those pages would do.

**F6. MAS Information Paper on Residential Mortgage Pricing and Disclosure
Practices, November 2021.**
https://www.mas.gov.sg/-/media/MAS/News-and-Publications/Monographs-and-Information-Papers/INFORMATION-PAPER-ON-RESIDENTIAL-MORTGAGE-PRICING-AND-DISCLOSURE-PRACTICES.pdf
Small. I can already read this one, but it needs to be in `raw/` with a checksum
because it is the document that establishes why no mortgage rate series exists.

## Optional

**F7.** Any official SIBOR history, if one exists. Try ABS at
https://www.abs.org.sg and the SOR and SIBOR to SORA section. If there is no
official archive, say so and I will state that the pre-2020 cohorts are quoted over
the wrong benchmark in a known direction.

**F8.** One CPF quarterly interest rate announcement from late 2024 or any quarter of
2025, from https://www.cpf.gov.sg/member/infohub/news/news-releases, to close the
gap between the end of F2 and the Q3 2026 announcement already in `raw/`.

## Fallback if anything is too large

Gzip it. A 22 MB CSV went to about 4 MB last time and lost nothing. If gzip still
will not upload, put the file in a public GitHub repository and send the raw URL;
github.com is reachable from here.

---

# 6. Reuse from the existing repository, with flags

## Reusing

| Item | Where from | Risk |
|---|---|---|
| `amortise()` | `05_affordability.py` | None. Five lines of standard annuity maths, no source dependency. It will be lifted into the financing module rather than imported across directories, so each directory stays independently runnable. |
| SVG helpers | `07_figures.py` | None. Layout code only. Same validated palette, same dark-mode block. |
| Validator pattern | `00_validate_schedule.py` | None. The idea is reused, not the file: a new `rate_schedule.csv` with the same `status` and `source_quote` columns and the same fatal invariants, including a selftest that reintroduces a known error and fails unless it is caught. |
| HDB concessionary rate, 2.6 per cent | `ltv_schedule.csv`, row `HDB_CONCESSIONARY_RATE`, currently LEVEL-VERIFIED-PRIMARY | **Upgrading, not inheriting.** With F2 the whole quarterly history becomes primary and the row moves to VERIFIED-PRIMARY. Until F2 lands, flagged. |
| `raw/hdb_interest_rate_page.pdf`, `raw/cpf1.pdf`, `raw/cpf2.pdf`, `raw/cpf3_q3_2026.pdf` | existing `raw/` | None. Already checksummed. The financing analysis reads the rate from `rate_schedule.csv`, which cites them. |

## Not reusing, and why

- **`grant_schedule.csv` and `ehg_bands.csv`.** Grants change the principal, not the
  cost per dollar borrowed. At constant principal they do not enter. Keeping them
  out also keeps the NOT-OBTAINED rows, such as the Additional CPF Housing Grant
  income ceiling, from touching this piece at all.
- **The resale transaction data and `01_clean.py`.** No transaction data is needed.
  The financing comparison is on a stated principal.
- **`out/affordability.csv` and the hedonic index.** Different question.

## Flagged, and the flags matter

- **`ltv_schedule.csv`, the 20 August 2024 cut to 75 per cent, status
  NEEDS-PRIMARY.** The HDB release is not reachable from this environment. Because
  the headline holds principal constant, **this row does not enter any headline
  number.** It appears only in the optional sensitivity where principal is allowed
  to vary with the cap. If that sensitivity runs, the article marks the 2024 point
  as resting on an unverified source, or the sensitivity is dropped.
- **`PURCHASE_AND_CPFHG_CEILING` rows at 12,000 and 16,000, both NEEDS-PRIMARY.**
  Not used here at all.
- **`AHG_INCOME_CEILING`, NOT-OBTAINED.** Not used here at all.
- **The bank medium-term stress rate.** Not in the repository, not verified, and I
  will not use it until it is.

## Repository placement

New subdirectory `financing/`, scripts numbered from 20 so there is no ambiguity
about run order against the existing 00 to 08. Its own README, its own
`CHECKSUMS.md5` covering its inputs and outputs, its own number manifest, its own
`THESIS.md`. The top-level README gains a section pointing at it. `run_all.sh` at
the top level gains a step that runs the financing pipeline, so one command still
rebuilds everything.

Before handover: delete every output in both directories, run from clean, and
confirm the existing analysis still reproduces byte-identically alongside the new
one.
