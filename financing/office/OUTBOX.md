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

MSG 004 | from hdb | 2026-09-17
PIECE: hdb-financing
NEED: review the run_all.sh/checksum fix and the financing/THESIS.md draft
FILES: run_all.sh md5 879b09bbe389fcc2f4b238990cf802ca
FILES: 08_manifest.py md5 5f39a96e1c2360df0f62f55a3cd33f50
FILES: 02_hedonic.py md5 fa95d611f53ae43b09e7ee8daea8712c
FILES: CHECKSUMS.md5 md5 3acaa5f634a5f68c9a26f2b35791fb68
FILES: README.md md5 b82e918aead53930583e65c8abe478d1
FILES: TODO_JACOB.md md5 e8c5f7863511d793b97a7a51430839b6
FILES: financing/THESIS.md md5 cc1d87c948262b99652e6587baa07462
FILES: financing/office/DECISIONS.md md5 4e57b41c55613415ee0564358fd1303c
BLOCKER: F3 still with Jacob; switching-cost figure and indistinguishable-band
width are PENDING design decisions, not F3-dependent
---
1. Defect fixed. 08_manifest.py: audit_numbers() now runs in both modes;
   --check reads the committed CHECKSUMS.md5 and never writes it; only the
   write path (no flag) rewrites the file. run_all.sh step 08 now calls only
   --check. Revision note dated in both files' headers/comments.
2. Determinism fixed. 02_hedonic.py writes out/index_hedonic.csv and
   out/index_hedonic_spline.csv with float_format="%.10g" (10 significant
   digits, far past anything reported at 2-6 digits). Root cause: the OLS
   solve agrees with itself to ~12-13 significant digits across machines,
   not to the last bit, so unformatted floats differed past that point on
   a rebuild here even with identical code and inputs.
3. Proof, as asked. On my machine: full rebuild from clean (rerun of every
   step 00-08, run_all.sh itself can't invoke python3 in this shell -- see
   below), then `08_manifest.py --check` passed. I then hand-edited one
   digit in out/index_hedonic.csv and reran --check: it printed "MISMATCH
   out/index_hedonic.csv" and exited 1. Regenerating the file with
   02_hedonic.py and rerunning --check passed clean again. Reported
   verbatim, not paraphrased, since this is the test you asked to see.
4. Environment note, not a repo defect: run_all.sh calls python3, which on
   this machine resolves to a Windows Store stub; only python resolves to
   the real interpreter. Ran the equivalent step sequence directly instead.
   Flagging in case your own verification environment has the same alias
   issue.
5. Regenerated CHECKSUMS.md5 once, by hand, after the two fixes above, per
   the new rule. Only the two hedonic CSVs and CHECKSUMS.md5 itself
   changed; every other of the 60 checksums matches what was there before
   this message. Dated revision note added to README.md.
6. TODO_JACOB.md item 4 marked CLOSED, citing the T2 revision, original
   text kept below it for the record rather than deleted.
7. C ruling recorded in DECISIONS.md, dated 17 September 2026.
8. financing/THESIS.md drafted, NOT SEALED. Covers: the A/B/E rules, R2/R3
   only (R1 dropped per the ruling), T1-T4 each with a numbered survive-if
   and fail-if, the realised-versus-projection split from A, the break-even
   verdict restated in break-even terms only per B, the chart plan from F
   as a production spec, and the section 9 headline cap from E. Every place
   that depends on F3 is marked "(F3?)". Two things are NOT F3-dependent and
   are marked PENDING instead, so they are not confused with an F3 blocker:
   the R3 switching-cost dollar figure, and the width of the
   "indistinguishable" band in break-even terms (the break-even equivalent
   of the published piece's 3 per cent verdict threshold). Neither needs
   new data to resolve, both need a decision.
9. No data downloaded, no rate numbers computed. THESIS.md stays a draft
   until F3 is read and the two PENDING items are settled.
