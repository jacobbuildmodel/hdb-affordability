# STATUS -- hdb-financing

Updated 17 September 2026, MSG 006 (researcher `hdb` to checker `claude-e4`).

| Item | State | Blocker | Next action by |
|---|---|---|---|
| Rate-series question | answered: no public mortgage rate series | F3 column headings unchecked | Jacob |
| Design | break-even spread; A/B/E accepted; C ruled -- R1 dropped (DECISIONS.md 17 Sep) | none | -- |
| THESIS.md | DRAFT revised against MSG 005 points 2-9, financing/THESIS.md, NOT SEALED | F3 headings; switching-cost grid awaiting Jacob | claude-e4 to review, Jacob for the grid |
| MSG 005 item 1, CHECKSUMS mismatch | FIXED and proved from a fresh clone of the pushed branch | none | claude-e4 to confirm |
| run_all.sh executable bit | FIXED, mode now 100755; was 100644 so documented `./run_all.sh` failed on a fresh clone | none | claude-e4 to confirm |
| Headline definition (item 2) | done: realised break-even spread is the definition, full tenure is a labelled projection | none | -- |
| Directional predictions (item 3) | done: T1-T4 each carry a falsifiable prediction | none | claude-e4 to review the predictions themselves |
| Plausibility filter (item 4) | done: 0-5 filter removed, negative spreads valid, non-convergence is the only unreliability | none | -- |
| T2 crossover (item 5) | done: crossover year per start year x grid spread, side-note table/heatmap, not a headline | none | -- |
| T4 switcher (item 6) | done: modelled under R2; switch years 2012/2015/2018/2021 with applicable start years fixed | none | -- |
| F2 and F8 (item 7) | promoted to ESSENTIAL in THESIS section 2; "decade and a half" corrected to ten years | F2 and F8 not downloaded | Jacob |
| Principal (item 8) | done: S$400,000 stated; spread principal-free, switching cost is not | none | -- |
| Indistinguishable band (item 9) | DEFINED, no longer PENDING: abs(bank - HDB) / HDB total interest <= 3% | none | -- |
| Switching-cost grid (item 9) | PENDING-JACOB: proposed S$0 / 3,000 / 6,000, labelled assumptions | Jacob's confirmation | Jacob |
| OFFICE.md (item 10) | updated: checker claude-e4, browser researcher session, PR merge route, raw/ uploads via github.com, PowerShell retired | none | -- |
| Data F1-F8 | not downloaded | THESIS not sealed; F3 headings first | Jacob |
| RESULTS.md T2 fix | done on financing-wip, pushed, G ACCEPTED (MSG 003) | none | -- |
| Determinism fix (float_format) | independently reverified on Linux: all 14 outputs byte-identical on a clean rebuild | none | -- |
| TODO_JACOB.md item 4 | closed 17 Sep, citing the T2 revision | none | -- |
| Article | provisional date 2026-09-26 | charts and numbers first, blocked on F1 | hdb |

## What is waiting on whom

- **Jacob:** F3 column headings (the one thing that could replace the design); F2
  and F8, now essential rather than supporting; confirm or replace the
  switching-cost grid.
- **claude-e4:** review the revised THESIS.md, in particular whether the four
  directional predictions are the right ones to be held to.
- **hdb:** nothing until one of the above lands. No data downloaded, no rate
  numbers computed, THESIS.md still unsealed.
