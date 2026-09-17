# STATUS -- hdb-financing

Updated 17 September 2026, MSG 012 (researcher `hdb` to checker `claude-e4`).

**THESIS.md is proposed for sealing. One blocker remains: F2.**

| Item | State | Blocker | Next action by |
|---|---|---|---|
| Rate-series question | CLOSED. F3 read: no banks' housing loan rate, design stands | none | -- |
| F3 side comparison S1 | added: finance-company 15-yr rate vs HDB 2.6%, labelled non-headline non-proxy, coverage 2010-01 to 2022-06 | none | claude-e4 |
| F4 | no longer needed; F3 closed the question it existed for | none | -- |
| Design | break-even spread; A/B/E accepted; C ruled -- R1 dropped (DECISIONS.md 17 Sep) | none | -- |
| THESIS.md | revised against MSG 011; PROPOSED FOR SEAL, still NOT SEALED | F2 missing | claude-e4 to rule on the seal |
| MSG 005 items 1-11 | ACCEPTED at cb7c941 (MSG 007 item 1) | none | -- |
| Fix PR against main | VERIFIED by claude-e4 (MSG 009 item 1); open and unmerged | none | Jacob to merge PR #1 |
| T1 magnitude claim (MSG 007 item 3) | added: realised spread exceeds 1.0 point for every 2010-2015 start, flagged as the headline claim | none | -- |
| 1.0 threshold basis | SETTLED. F5 and F6 read 17 Sep; neither publishes a spread or a rate level; 1.0 kept, labelled a judgement threshold, quotes and pages recorded in section 6 | none | -- |
| README second revision note (MSG 009 item 5) | DEFERRED deliberately, not forgotten: rewording it now would diverge financing-wip from the in-flight PR #1 and conflict on merge | PR #1 unmerged | hdb, once PR #1 merges |
| T2a/T2b labelling (MSG 007 item 3) | done: both labelled "expected from public rate history; low information" | none | -- |
| T3 monotonic clause (MSG 007 item 3) | deleted; holds by construction. Removal recorded in the file with the reason | none | -- |
| Public-knowledge sentence (MSG 007 item 4) | done, section 6: predictions test magnitude and mechanics, not direction | none | -- |
| Headline definition (item 2) | done: realised break-even spread is the definition, full tenure is a labelled projection | none | -- |
| Directional predictions (item 3) | done: T1-T4 each carry a falsifiable prediction | none | claude-e4 to review the predictions themselves |
| Plausibility filter (item 4) | done: 0-5 filter removed, negative spreads valid, non-convergence is the only unreliability | none | -- |
| T2 crossover (item 5) | done: crossover year per start year x grid spread, side-note table/heatmap, not a headline | none | -- |
| T4 switcher (item 6) | done: modelled under R2; switch years 2012/2015/2018/2021 with applicable start years fixed | none | -- |
| F2 and F8 (item 7) | promoted to ESSENTIAL in THESIS section 2; "decade and a half" corrected to ten years | F2 and F8 not downloaded | Jacob |
| Principal (item 8) | done: S$400,000 stated; spread principal-free, switching cost is not | none | -- |
| Indistinguishable band (item 9) | DEFINED, no longer PENDING: abs(bank - HDB) / HDB total interest <= 3% | none | -- |
| Switching-cost grid | CONFIRMED by Jacob 17 Sep at S$0 / 3,000 / 6,000; PENDING-JACOB removed | none | -- |
| OFFICE.md (item 10) | updated: checker claude-e4, browser researcher session, PR merge route, raw/ uploads via github.com, PowerShell retired | none | -- |
| Data F1, F3, F5, F6, F8 | IN raw/, renamed, recorded in RETRIEVED.txt FOURTH DELIVERY with bytes and MD5 | none | -- |
| F2 (CPF rate history) | MISSING. Not in the delivery; direct fetch refused, 403 at CONNECT to cpf.gov.sg | blocks the seal | Jacob |
| raw/ tidy | done in one commit: 5 renames, cpff2.pdf removed as a proven duplicate, cpff1.pdf KEPT and renamed | ruling wanted on keeping cpff1 | claude-e4 |
| F1 values | UNOPENED by design; only column headings and series labels read, to identify the file | seal | claude-e4 confirms seal first |
| RESULTS.md T2 fix | done on financing-wip, pushed, G ACCEPTED (MSG 003) | none | -- |
| Determinism fix (float_format) | independently reverified on Linux: all 14 outputs byte-identical on a clean rebuild | none | -- |
| TODO_JACOB.md item 4 | closed 17 Sep, citing the T2 revision | none | -- |
| Article | provisional date 2026-09-26 | charts and numbers first, blocked on F1 | hdb |

## What is waiting on whom

- **Jacob:** F2, the CPF interest rate history, which this environment cannot
  fetch. Also merge PR #1, still open and verified.
- **claude-e4:** rule on the seal; rule on whether cpf_faq_interest_rates_page.pdf
  stays or goes.
- **hdb:** nothing until the seal is ruled on. F1 values stay unopened. Owed once
  PR #1 merges: the README revision-note reword.

## Sealing checklist

1. ~~F3 read and its column headings reported.~~ DONE. No banks' housing loan
   rate; design stands; F4 dropped.
2. ~~The 1.0 threshold settled against F5/F6, or labelled a judgement call.~~
   DONE. Neither publishes a spread or a level; labelled a judgement threshold.
3. ~~The switching-cost grid confirmed by Jacob.~~ DONE, S$0 / 3,000 / 6,000.
4. **F2 in hand. NOT DONE, and it is the only remaining blocker.** F8 is in and
   closes the late end, but the HDB leg still rests on four dated anchors rather
   than a continuous series, and in this piece the flat 2.6 per cent is the
   comparator itself.

## Known risk, deliberately not investigated before sealing

The start date of compounded 3-month SORA inside F1, and whether the pre-2020
window is official or back-calculated. Checking it needs F1 values, which stay
shut until the seal is confirmed. If the compounded series begins around 2020,
every 2010-2019 cohort depends on the F7 SIBOR substitution, which is unsourced.
This is the first thing examined after the seal.
