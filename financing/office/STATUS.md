# STATUS -- hdb-financing

Updated 17 September 2026, MSG 016 (researcher `hdb` to checker `claude-e4`).

**THESIS.md is SEALED (43bd0a0). Build done. 5 predictions passed, 3 FAILED.**

| Item | State | Blocker | Next action by |
|---|---|---|---|
| Rate-series question | CLOSED. F3 read: no banks' housing loan rate, design stands | none | -- |
| F3 side comparison S1 | added: finance-company 15-yr rate vs HDB 2.6%, labelled non-headline non-proxy, coverage 2010-01 to 2022-06 | none | claude-e4 |
| F4 | no longer needed; F3 closed the question it existed for | none | -- |
| Design | break-even spread; A/B/E accepted; C ruled -- R1 dropped (DECISIONS.md 17 Sep) | none | -- |
| THESIS.md | SEALED 17 Sep at 43bd0a0, sealed on its own commit before F1 was opened; two AMENDMENT blocks appended | none | claude-e4 to rule on AMENDMENT 1 |
| Predictions | T1a PASS, T1b PASS (weak evidence), T2a PASS, T2b FAIL, T3 FAIL, T4a FAIL, T4b PASS, S1 PASS | none | claude-e4 |
| financing/ scripts 20-25 | built; selftest, compute, charts, scoring, own CHECKSUMS and number manifest; wired into run_all.sh | none | claude-e4 |
| Charts 1 and 2 | built as SVG, dark mode, checked in Chromium at 390px in both schemes; two rendering defects found and fixed | none | -- |
| R3 implementation | CHANGED, recorded as AMENDMENT 1 (written AFTER results). Literal sealed rule made R3 cost more than R2, contradicting its own upper-bound description | none | claude-e4 to rule |
| SGS forward-curve projection | NOT built, recorded as AMENDMENT 2. Two other labelled paths are built | none | claude-e4 |
| MSG 005 items 1-11 | ACCEPTED at cb7c941 (MSG 007 item 1) | none | -- |
| Fix PR against main | VERIFIED by claude-e4 (MSG 009 item 1); open and unmerged | none | Jacob to merge PR #1 |
| T1 magnitude claim (MSG 007 item 3) | added: realised spread exceeds 1.0 point for every 2010-2015 start, flagged as the headline claim | none | -- |
| 1.0 threshold basis | SETTLED. F5 and F6 read 17 Sep; neither publishes a spread or a rate level; 1.0 kept, labelled a judgement threshold, quotes and pages recorded in section 6 | none | -- |
| README second revision note | PR #1 merged (main a7bed51); reword PR opened against main | none | Jacob to merge |
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
| F2 (CPF rate history) | IN raw/, VERIFIED: OA 2.50% in all 59 quarters 2010-Q1 to Jul-Sep 2024, and in all 109 quarters 1999-2026. HDB leg is a verified constant | none | -- |
| SIBOR bias on T1b | added: pass is weak evidence, fail is strong evidence, for 2010-2015 starts; section 7 item 6 tied to 1b; sentence goes next to the headline number | none | claude-e4 |
| F1 date coverage | recorded from checker's check: compounded 3M SORA 2005-10 to 2026-07, whole window covered. No values opened | none | -- |
| F7 SIBOR history | OPTIONAL. Would turn the bias direction into a measured size | none | -- |
| raw/ tidy | done; cpff1 keep RULED CORRECT by claude-e4, recorded in DECISIONS.md | none | -- |
| F1 values | UNOPENED by design; only column headings and series labels read, to identify the file | seal | claude-e4 confirms seal first |
| RESULTS.md T2 fix | done on financing-wip, pushed, G ACCEPTED (MSG 003) | none | -- |
| Determinism fix (float_format) | independently reverified on Linux: all 14 outputs byte-identical on a clean rebuild | none | -- |
| TODO_JACOB.md item 4 | closed 17 Sep, citing the T2 revision | none | -- |
| Article | provisional date 2026-09-26 | charts and numbers first, blocked on F1 | hdb |

## What is waiting on whom

- **Jacob:** merge PR #2 (README wording, corrected per MSG 015 item 3).
- **claude-e4:** rule on AMENDMENT 1, the R3 implementation change; review the
  three failures; say whether the piece proceeds to prose.
- **hdb:** no prose written and none starting until told. Nothing else pending.

## Sealing checklist

1. ~~F3 read and its column headings reported.~~ DONE. No banks' housing loan
   rate; design stands; F4 dropped.
2. ~~The 1.0 threshold settled against F5/F6, or labelled a judgement call.~~
   DONE. Neither publishes a spread or a level; labelled a judgement threshold.
3. ~~The switching-cost grid confirmed by Jacob.~~ DONE, S$0 / 3,000 / 6,000.
4. ~~F2 in hand.~~ DONE and verified row by row: OA 2.50% in all 59 quarters of
   the window and all 109 in the document. The HDB leg is a constant, read from
   the series rather than inferred from anchors.

**All four are closed. THESIS.md is proposed for seal.**

## What the seal does not make safe

The benchmark substitution. Pre-2020 mortgages were priced off SIBOR, which ran
above SORA, so a break-even spread measured over SORA overstates the
SIBOR-equivalent margin for 2010-2015 starts and biases prediction 1b toward
passing. This is now written into 1b and tied to section 7 item 6, and the
sentence travels with the headline number into the article: for those cohorts a
pass is weak evidence and a fail is strong evidence. F7 would measure the size of
it; it is optional and not sourced.
