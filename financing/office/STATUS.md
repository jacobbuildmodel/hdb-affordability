# STATUS -- hdb-financing

Updated 17 September 2026, MSG 008 (researcher `hdb` to checker `claude-e4`).

| Item | State | Blocker | Next action by |
|---|---|---|---|
| Rate-series question | answered: no public mortgage rate series | F3 column headings unchecked | Jacob |
| Design | break-even spread; A/B/E accepted; C ruled -- R1 dropped (DECISIONS.md 17 Sep) | none | -- |
| THESIS.md | DRAFT revised against MSG 005 points 2-9 and MSG 007 points 3-4, NOT SEALED | F3 headings; switching-cost grid awaiting Jacob | claude-e4 to review, Jacob for the grid |
| MSG 005 items 1-11 | ACCEPTED at cb7c941 (MSG 007 item 1) | none | -- |
| Fix PR against main | OPEN, PR #1, branch `fix-t2-checksums`, root-level only, proved from a fresh clone | none | claude-e4 to verify, then Jacob merges |
| T1 magnitude claim (MSG 007 item 3) | added: realised spread exceeds 1.0 point for every 2010-2015 start, flagged as the headline claim | none | claude-e4 |
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
- **claude-e4:** verify PR #1 against main so Jacob can merge it; and confirm the
  tightened predictions, in particular whether 1.0 point is the right threshold
  for the T1b headline claim. It is the one number in the file chosen by judgement
  rather than derived, and it is now what the piece stands on.
- **hdb:** nothing until one of the above lands. No data downloaded, no rate
  numbers computed, THESIS.md still unsealed.
