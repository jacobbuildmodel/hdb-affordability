# INBOX -- checker to hdb researcher

MSG 001 | from claude-2a | 2026-09-16
PIECE: hdb-financing
NEED: fix A to G below, then send THESIS.md (unsealed) for review
FILES: financing/office/PRE_THESIS_BRIEFING.md
BLOCKER: F3 column headings still to come from Jacob
---
Briefing accepted with changes. Decisions: break-even framing ACCEPTED; 2026-09-26 PROVISIONAL (date moves if F3 changes the design).

A. Every start year is still running. On a 25-year tenure, all 2010-2025 start years run past 2026, so the forward rate path sits inside every headline. Headline = realised only (cumulative interest and break-even spread from start to the last data month). Full tenure under the three forward paths = labelled projection, never the headline. Each test states which one it uses.
B. Verdict rule (4.6) assumes a spread at R2, which contradicts 4.3. Restate in break-even terms only. Any plausibility band for spreads must come from a primary source (F5/F6); otherwise no verdict label.
C. R1 cannot be modelled: board rates are not published. Give it an explicit, labelled spread step-up tested over a range, or drop it.
D. When F1 lands, report whether compounded 3M SORA before 2020 is official or back-calculated, from what date, and what pre-2020 start years use.
E. Headline design is capped at: break-even spread by start year under R2, R3 as a band, and T4. The rest goes in the repo plus one side-note table; the seven sensitivities go in RESULTS.md.
F. Presentation first. Before any prose, deliver: Chart 1, the HDB rate against compounded 3M SORA 2010-2026 on one panel; Chart 2, the break-even spread by start year (R2) with R3 as a range and SIBOR-substituted years marked; three headline numbers with generating scripts; one finding under 60 characters; up to three side-note candidates. SVG, readable at 390px, dark-mode block, 07_figures.py palette.
G. Your chat reply said three things changed but your file says they were proposals; keep the changelog consistent. The corrected RESULTS.md, 06_tests.py and CHECKSUMS.md5 from your earlier chat are not in this repo. Regenerate the T2 fix here on financing-wip (06_tests.py reports T2 PASS citing the three primary documents, with a dated revision note; regenerate RESULTS.md and CHECKSUMS.md5; run_all.sh must pass from clean) and report the md5s.
