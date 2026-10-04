# PAPER_NOTES -- Huang, Li and Ross (2018)

Status: BLOCKED. The paper has not been read. Every field below is empty on
purpose: nothing here is filled from memory, because a specification written
from memory would be an unsourced claim.

## The paper, as given in the brief

- Huang, Li and Ross (2018), "The impact of the cost of car ownership on the
  house price gradient in Singapore", Regional Science and Urban Economics 68.
- Their data: URA REALIS private homes (paid). This piece uses public HDB
  resale data instead, so it is a conceptual replication, not a replication,
  and the piece must say so.
- Public copy named in the brief:
  https://liberalarts.tulane.edu/sites/default/files/sites/default/files/Ross_Ownership.pdf

## Why it is blocked

Checked 4 October 2026, 10:12 UTC, from the research session:
- liberalarts.tulane.edu: CONNECT refused with 403 by the session's network
  policy. Stopped there, as instructed.
- doi.org and www.sciencedirect.com (the publisher copy) are refused the same
  way. While testing hosts for the world-view source, one request also went
  to ideas.repec.org (a bibliographic listing for the paper); it was refused
  too. No other copy or mirror of the paper was tried, and none will be.

## To unblock (either)

1. Jacob downloads the PDF on his own machine into cargradient/raw/ and
   records bytes and md5 in cargradient/raw/RETRIEVED.txt (the same route as
   the 12 September 2026 downloads in SOURCES.md), or
2. Jacob adds liberalarts.tulane.edu to the environment's allowed domains.

## What to extract once the PDF is in raw/ (each with page and table number)

1. The estimating equation, written out, with every term defined.
2. The dependent variable (price level, log price, per square metre?).
3. The sample: property types, how many transactions, which years exactly,
   any filters (new sale vs resale, tenure, size).
4. How distance is measured: to what point (the CBD point, with coordinates or
   name), straight line or travel, kilometres or log.
5. The COE series: which category (A, B, E, or an average), and which
   averaging (per bidding exercise, monthly, quarterly, annual, any lag or
   moving average).
6. The fixed effects and controls (project, building, time; MRT distance?).
7. How standard errors are clustered.
8. The headline coefficients: value, standard error, table and page.
9. What they say the mechanism is: a short quote of one line, with page.
10. Any test of a policy change, and how the dates were set.

Quotes are kept to single short lines.
