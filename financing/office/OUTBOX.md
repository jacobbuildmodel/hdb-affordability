# OUTBOX -- hdb researcher to checker

MSG 002 | from hdb | 2026-09-16
PIECE: hdb-financing
NEED: confirm the T2 fix (point G) is sufficient, or say what more it needs
FILES: 06_tests.py md5 8046d6e528bbc3b3fa21fa5bbcda4b2a
FILES: RESULTS.md md5 a15ce70358bd9aff06b1e0125af67014
FILES: CHECKSUMS.md5 md5 d4c1fa80b558599ee72957767999afc9
BLOCKER: F3 column headings still unchecked; F1-F8 not downloaded; THESIS.md for financing/ not written
---
1. G done, on financing-wip, outside financing/ as you named. 06_tests.py T2 is
   PARTIAL to PASS, citing raw/hdb_interest_rate_page.pdf (the peg formula),
   raw/cpf2.pdf (Q1 2016) and raw/cpf3_q3_2026.pdf (Q3 2026), all three already
   in raw/ before this fix, nothing new downloaded. Basis: two primary CPF
   Board notices a decade apart, both showing the OA rate held at the 2.5pp
   floor and the 2.6pp HDB rate as its direct consequence. Not a monthly
   history, and RESULTS.md says so. This is the same bar TODO_JACOB.md item 4
   set before any data arrived, so nothing here is being loosened to get a
   PASS.
2. Revision note dated in 06_tests.py, per your point G on changelog
   consistency. run_all.sh passes from clean; 08_manifest.py --check reports
   all 60 checksums match; only 06_tests.py and RESULTS.md hashes moved.
   out/index_hedonic.csv and out/index_hedonic_spline.csv regenerated
   byte-different on this machine (floating-point noise past the 10th digit,
   no reported figure moved); reverted to the committed versions rather than
   carry an unrelated diff.
3. Side finding, not acted on: TODO_JACOB.md item 4 already asks Jacob for
   exactly cpf2.pdf and one recent notice, which are already in raw/ and now
   used. The item reads as open but is not. Not edited, since it is outside
   financing/ and you did not name it.
4. A, B, E accepted as design rules for financing/THESIS.md when it is
   written: realised-only headline, verdict restated in break-even terms
   only, headline capped as you specified. Nothing to seal yet, financing/
   has no THESIS.md.
5. C, proposal: drop R1 rather than add a labelled spread step-up. No board
   rate source exists at all for any window (PRE_THESIS_BRIEFING.md section
   2.6), so a step-up would itself be an assumed spread, which is the thing
   this design exists to avoid. Open to override.
6. D and F stay BLOCKED. Both need F1 (SORA), not downloaded.
7. THESIS.md for financing/ is not written. Sealing it is still blocked on
   F3 (MAS Table III.3 column headings), unchanged since MSG 001. Have not
   requested data past F3, per PRE_THESIS_BRIEFING.md section 7.
