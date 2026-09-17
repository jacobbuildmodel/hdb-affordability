# STATUS -- hdb-financing

Updated 17 September 2026, MSG 010 (researcher `hdb` to checker `claude-e4`).

| Item | State | Blocker | Next action by |
|---|---|---|---|
| Rate-series question | answered: no public mortgage rate series | F3 column headings unchecked | Jacob |
| Design | break-even spread; A/B/E accepted; C ruled -- R1 dropped (DECISIONS.md 17 Sep) | none | -- |
| THESIS.md | DRAFT revised against MSG 005 points 2-9, MSG 007 points 3-4 and MSG 009 point 3, NOT SEALED | F3 headings; 1.0 threshold basis; switching-cost grid | Jacob (uploads and grid) |
| MSG 005 items 1-11 | ACCEPTED at cb7c941 (MSG 007 item 1) | none | -- |
| Fix PR against main | VERIFIED by claude-e4 (MSG 009 item 1); open and unmerged | none | Jacob to merge PR #1 |
| T1 magnitude claim (MSG 007 item 3) | added: realised spread exceeds 1.0 point for every 2010-2015 start, flagged as the headline claim | none | -- |
| 1.0 threshold basis (MSG 009 item 3) | unsourced justification DELETED; 1.0 now labelled "a judgement threshold, not derived from a source"; three-step procedure for settling it fixed in section 6 | F5 and F6 not uploaded | Jacob, then hdb reads F5/F6 |
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
| Switching-cost grid (item 9) | PENDING-JACOB: proposed S$0 / 3,000 / 6,000, labelled assumptions | Jacob's confirmation | Jacob |
| OFFICE.md (item 10) | updated: checker claude-e4, browser researcher session, PR merge route, raw/ uploads via github.com, PowerShell retired | none | -- |
| Data F1-F8 | not uploaded; raw/ still holds the same 21 files | THESIS not sealed; F3 headings first | Jacob |
| On-upload procedure (MSG 009 item 4) | agreed and unstarted: record each file in raw/RETRIEVED.txt (title, publisher, URL, retrieval date, bytes, MD5) as a FOURTH DELIVERY block, and report F3's column headings before anything else | uploads | Jacob, then hdb |
| RESULTS.md T2 fix | done on financing-wip, pushed, G ACCEPTED (MSG 003) | none | -- |
| Determinism fix (float_format) | independently reverified on Linux: all 14 outputs byte-identical on a clean rebuild | none | -- |
| TODO_JACOB.md item 4 | closed 17 Sep, citing the T2 revision | none | -- |
| Article | provisional date 2026-09-26 | charts and numbers first, blocked on F1 | hdb |

## What is waiting on whom

- **Jacob:** F3 column headings (the one thing that could replace the design); F2
  and F8, now essential rather than supporting; confirm or replace the
  switching-cost grid.
- **claude-e4:** nothing outstanding. PR #1 is verified, MSG 008 accepted, and the
  threshold pushback was upheld and applied.
- **hdb:** blocked on uploads. On arrival, in this order: report F3's column
  headings, record every file in raw/RETRIEVED.txt, then read F5 and F6 for a
  margins range and settle the 1.0 threshold. F1 stays unopened until THESIS.md is
  sealed. Also owed, once PR #1 merges: the README revision-note reword.

## Sealing checklist

THESIS.md cannot be sealed until all four are closed:

1. F3 read and its column headings reported. If it carries a banks' housing loan
   rate, the design is replaced rather than sealed.
2. The 1.0 threshold settled against F5/F6, or explicitly labelled a judgement
   call with no source.
3. The switching-cost grid confirmed or replaced by Jacob.
4. F2 and F8 in hand, since the flat 2.6 per cent is the comparator.
