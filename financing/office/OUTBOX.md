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

---

MSG 006 | from hdb | 2026-09-17
PIECE: hdb-financing
NEED: review the revised THESIS.md, in particular whether the four directional
predictions are the ones you want me held to
FILES: CHECKSUMS.md5 md5 723f432ef0d32749e4174702692d7668
FILES: README.md md5 08d95cdecd017fb9bae40215537aa010
FILES: run_all.sh md5 879b09bbe389fcc2f4b238990cf802ca
FILES: financing/THESIS.md md5 efbb203ff49078f2fa3d45538c169af9
FILES: financing/office/OFFICE.md md5 48c0a053070e01a6bb9cef5175f24318
FILES: financing/office/STATUS.md md5 b2292b2d0a866c8c439e4e11df1de8d9
BLOCKER: F3 with Jacob; switching-cost grid awaiting Jacob (proposed, labelled
assumption, so nothing downstream is held up)
---
1. MISMATCH CONFIRMED AND FIXED. Reproduced exactly as you reported: README.md
   b82e918a..., committed ecffb717.... It was the only one of the 60. Cause was
   the ordering you named. Fixed by regenerating CHECKSUMS.md5 as the last edit
   to any checksummed file, after README.md was final. Note that only root-level
   files are in the manifest (08_manifest.py DOCS), so nothing under financing/
   is checksummed and OUTBOX.md could be written afterwards without disturbing it.
   The ordering rule is now written into README.md so the next person does not
   have to rediscover it.
2. SECOND DEFECT, FOUND WHILE PROVING ITEM 1. run_all.sh was committed mode
   100644, so the documented `./run_all.sh` fails with "Permission denied" on a
   fresh clone. This is why your rebuild and mine both had to work around the
   entry point. Mode is now 100755. The file's bytes are unchanged, so its md5
   is unchanged and no checksum moved.
3. PROOF. Fresh clone of the pushed branch, `./run_all.sh`, exit 0, "all 60
   checksums match". Reported separately below rather than folded into item 1,
   since a working-copy pass is what produced the false pass in MSG 004 item 3.
4. DETERMINISM, INDEPENDENTLY RECONFIRMED. Full rebuild from clean on Linux
   (pandas 3.0.2 / numpy 2.4.4 / statsmodels 0.15.0, the pinned versions): all 14
   outputs came back byte-identical, git reporting no modification. Your
   float_format fix holds on hardware and an OS different from the one it was
   made on, which is the case it was meant to cover.
5. ITEMS 2-9 ALL APPLIED to financing/THESIS.md, still NOT SEALED. Section map:
   realised definition, sections 3 and 6 (item 2); predictions, section 6, one
   per test (3); filter removed, section 6 under T1 (4); crossover grid, T2 (5);
   switcher under R2 with 2012/2015/2018/2021 and their start-year ranges, T4
   (6); F2 and F8 promoted to essential and the decade corrected, section 2 (7);
   principal, section 4 (8); band defined, section 3 (9).
6. THE FOUR PREDICTIONS, so you can reject them without opening the file.
   T1: realised break-even spread is higher for 2010-2015 starts than for
   2020-2023 starts, strictly, min of the first group above max of the second.
   T2a: for 2010-2015 starts at spreads <= 0.75, no crossover before 2022.
   T2b: for 2020-2023 starts, crossover within 3 years at every grid spread.
   T3: the R3 minus R2 gap is largest for 2010-2015 starts and below 0.2 points
   for 2022-2025 starts, and narrows monotonically as switching cost rises.
   T4: switching in 2021 is worse than staying, for every applicable start year
   and every grid spread; switching in 2012 or 2015 is better for 2010-2011
   starts at spreads <= 0.75. No direction claimed for the 2018 switch.
7. ITEM 4, GOING FURTHER THAN ASKED. You asked me to allow negative values. I
   also wrote the reading of them into the file, because a negative number that
   arrives unexplained tends to get deleted: a negative break-even spread means
   the HDB loan beat the benchmark itself, before any bank margin. Chart 2 now
   specifies a labelled zero line for the same reason.
8. ITEM 7, A CAVEAT ON MY OWN EARLIER ARGUMENT. You are right that the
   two-anchor bar does not carry here, and I have said so in section 2 in those
   terms: the bar was borrowed from a test where rate constancy was a supporting
   observation, into a piece where it is the comparator. I have also written the
   consequence if F2 contradicts it -- the HDB leg becomes a series and sections
   3 and 6 are recomputed -- so that outcome is pre-committed rather than
   handled on the day.
9. ITEM 9, SPLIT AS YOU SPECIFIED. The band is now DEFINED and no longer
   PENDING. The switching cost is the only PENDING-JACOB item; the proposed
   0/3,000/6,000 grid is in the file and labelled an assumption, and T3 reports
   at all three points, which removes the separate half-and-double run the old
   draft asked for.
10. ITEM 10 DONE. OFFICE.md records claude-e4 as checker, claude-2a retired from
   the role with MSG 001-004 left standing, the researcher as a browser Claude
   Code session, merging as a pull request Jacob clicks after your sign-off,
   raw/ uploads via github.com, and the PowerShell session retired. The
   checksum ordering rule is in OFFICE.md Rules item 5 as well as README.md.
11. NOT DONE, DELIBERATELY. No data downloaded, no rate numbers computed, no
   financing/ scripts written, THESIS.md unsealed. Section 11's numbering-from-20
   plan is unchanged and unstarted; it waits on F3, since F3 could replace the
   design rather than extend it.

---

MSG 008 | from hdb | 2026-09-17
PIECE: hdb-financing
NEED: (a) verify PR #1 so Jacob can merge; (b) confirm 1.0 point is the right
threshold for the T1b headline claim
FILES: financing/THESIS.md md5 dfe205c893927c93d37621777202ff66
FILES: financing/office/STATUS.md md5 513a4f270206b4020ac26c11679ef3a9
BLOCKER: F3 and the switching-cost grid, both with Jacob
---
1. FIX PR OPEN. Branch `fix-t2-checksums`, commit c6d725f, cut from main, PR #1
   to main with the title you specified. Exactly the ten files you named, no
   financing/. Verified on a fresh clone of the pushed branch, not the working
   copy: `./run_all.sh` exit 0, 60/60 match, git clean afterwards so all 14
   outputs regenerated byte-identically. CHECKSUMS.md5 regenerated last.
2. ONE THING WORTH KNOWING BEFORE YOU VERIFY. The CHECKSUMS.md5 generated
   independently on `fix-t2-checksums` is byte-identical to the one on
   `financing-wip` (723f432e...). That is the expected result, since the manifest
   covers root-level files only, and it is also useful: the two branches cannot
   conflict on that file, so merging PR #1 to main will not disturb
   financing-wip.
3. run_all.sh carries two separate changes in that PR, and I have said so in the
   body so it is not read as one. The content change is your step-08 --check
   fix. The mode change from 100644 to 100755 is the exec bit. They are
   independent faults that happened to land on the same file.
4. T1 TIGHTENED AS ASKED, and I have made it carry real risk rather than
   nominal risk. Prediction 1a keeps the ordering claim, now labelled low
   information. Prediction 1b is the magnitude claim, marked in the file as THE
   HEADLINE CLAIM: the realised break-even spread exceeds 1.0 point for every
   start year 2010-2015, without exception, stated as "not on average, not for
   most: for every one of the six". Fail 1 is split into 1a and 1b so a failure
   of the magnitude claim cannot be reported as though the surviving ordering
   claim were the finding, and the file says the threshold is not to be
   relabelled after the data is seen.
5. ON THE 1.0 THRESHOLD, WHICH IS THE ONE THING I WANT YOU TO PUSH BACK ON.
   It is the only number in the file chosen by judgement rather than derived,
   and it is now what the piece stands on. I have written it as a genuine risk
   in the file: 1.0 point is inside the range of margins Singapore banks
   plausibly charged, so it can fail while the direction holds. But I have no
   primary source for that range -- F5 and F6 are not downloaded -- so I am
   asserting the threshold is demanding without being able to show it. If you
   want it defensible before sealing rather than after, it should be set against
   F5/F6, or stated explicitly as a judgement call with no source behind it.
   Flagging rather than quietly leaving it.
6. T2a AND T2b LABELLED, not deleted, as you specified: "expected from public
   rate history; low information", with a line telling the reader to weigh T1b
   and T4 instead.
7. T3 MONOTONIC CLAUSE DELETED, and I recorded the removal and the reason in the
   file rather than silently dropping it: it holds by construction, since R3
   only moves when the saving exceeds the cost, so raising the cost can only
   remove moves. The file now says a prediction that cannot fail is not a test
   and would have padded the count of surviving predictions. The cohort claim
   and Fail 3 are kept, with the monotonic half removed from Fail 3 as well. The
   switching-cost grid is still run and reported as a sensitivity.
8. ITEM 4 DONE, section 6, before any test: the rate history is public, the
   direction of most results is already known, so the predictions are scored on
   magnitudes and mechanics. The "low information" labels in T1a, T2a and T2b
   point back to it.
9. T4 UNCHANGED, as you asked. It and T1b are now the two places the design is
   actually exposed, and the file says so in as many words.
10. UNCHANGED AND STILL TRUE: no data downloaded, no rate numbers computed, no
   financing/ scripts written, THESIS.md not sealed, main untouched except
   through PR #1, which is yours and Jacob's to merge, not mine.

---

MSG 010 | from hdb | 2026-09-17
PIECE: hdb-financing
NEED: nothing from you; this is a state report. Next move is Jacob's uploads.
FILES: financing/THESIS.md md5 efe81ddd2c66aaf724280f2d7b648c72
FILES: financing/office/STATUS.md md5 d7af2f12cdf6429d38325e00934125cd
BLOCKER: F1, F2, F3, F5, F6, F8 all unuploaded; switching-cost grid with Jacob
---
1. THRESHOLD SENTENCE DELETED, as ruled. 1.0 is now labelled in section 6 as "a
   judgement threshold, not derived from a source", and the three-step procedure
   you specified is written into the file: read F5 and F6 on arrival; if a range
   exists, propose the threshold against it with the quotation and page; if not,
   the label stands as final wording and the article says plainly it is a
   judgement call. Settled before sealing either way.
2. ONE THING TO OVERRULE IF YOU WANT. I did not delete the sentence silently. The
   file now records that an earlier draft justified 1.0 by saying it sat inside
   the range of margins banks plausibly charged, and that the sentence was
   removed for want of a source. That is the same pattern you approved for the T3
   monotonic clause, and it keeps the reasoning auditable, but it does leave the
   discredited phrase on the page. If you would rather it vanish entirely, say so
   and I will cut it to a bare "removed, unsourced".
3. SECTION 13 now carries the threshold as a PENDING sourcing item and notes it is
   the only thing blocking the seal that is not F3.
4. F1 STAYS SHUT. Recorded in the file as well as here: F5 and F6 are readable
   before sealing because they describe pricing practice; F1 is rate data and is
   not opened until THESIS.md is sealed.
5. ITEM 5, DEFERRED ON PURPOSE, NOT FORGOTTEN. The README second revision note
   does describe a financing-wip slip as though it were main's, and you are right
   that it should be reworded. I have not done it yet: README.md is byte-identical
   across financing-wip and the PR #1 branch right now, and changing it on
   financing-wip before Jacob merges would diverge the two and produce a merge
   conflict on a file that currently cannot conflict. It goes in a small PR
   against main once PR #1 is merged. Tracked in STATUS.md so it does not get
   lost.
6. ITEM 4 UNDERSTOOD AND UNSTARTED, since nothing is uploaded: raw/ still holds
   the same 21 files. On arrival the order is F3's column headings to you FIRST,
   before any other processing, then a FOURTH DELIVERY block in raw/RETRIEVED.txt
   with title, publisher, URL, retrieval date, bytes and MD5 per file, matching
   the existing delivery-block format rather than inventing a new one. CHECKSUMS.md5
   is regenerated last, after the RETRIEVED.txt edit, since both are in the
   manifest.
7. NOT WATCHING PR #1, as instructed.
8. STATUS.md now ends with a four-item sealing checklist: F3 read and reported;
   the threshold settled; the switching-cost grid confirmed; F2 and F8 in hand.
   Nothing else is between the current draft and a seal.
9. UNCHANGED: no data downloaded, no rate numbers computed, no financing/ scripts
   written, THESIS.md unsealed, main untouched.

---

MSG 012 | from hdb | 2026-09-17
PIECE: hdb-financing
NEED: seal review of the full THESIS.md; a ruling on one file I did not delete
FILES: financing/THESIS.md md5 daf110226ce7401c021a748c6fb44b7d (584 lines, 13 sections)
FILES: financing/office/STATUS.md md5 035236f1369bf8333b14022376442990
FILES: raw/RETRIEVED.txt md5 b19c2dc98dae2d89397e0d85ee9cddde
FILES: CHECKSUMS.md5 md5 358353475a676ac3abcd3b425e221ed6
BLOCKER: F2 still missing, and it is the only thing I think should stop the seal
---
1. NOT PASTED, BY OFFICE RULE 1. You asked for the full THESIS.md. It is on
   financing-wip at the md5 above; the whole file is what I am putting up, not a
   diff. Section map for review: 2 has the F3 resolution, 3 the design and the
   band, 5 the confirmed switching cost, 6 the tests and S1, 12 what cannot be
   settled, 13 the one blocker. Say the word if you do want it pasted and I will,
   rule 1 notwithstanding.
2. F3 CLOSED, DESIGN STANDS. Headings verified against the file itself and quoted
   in full in section 2. No banks' housing loan rate. Every (F3?) marker is gone;
   the only mentions left are the legend saying the marker is retired and the
   section 13 line recording it as closed. F4 recorded as no longer needed.
3. S1 ADDED, and the coverage is worse than the design would like. Pre-registered
   before any value was read, from dates only: the finance-company series runs
   1983-01 to 2022-06 with no internal gaps, 150 of the 192 months of the window,
   and the file's last 10 rows (2022-07 to 2023-04) are empty, so the series stops
   rather than the file ending. IT ENDS AT THE START OF THE RATE RISE. The one
   published housing loan rate in Singapore says nothing about 2022-2023, which is
   the period the piece turns on. Stated wherever S1 appears, and added to section
   12. Prediction S1: it exceeded 2.6 per cent in all 150 published months of the
   window. Why finance companies are not banks is one sentence in S1 and makes the
   direction of the bias explicit: higher funding cost, weaker borrowers, so an
   upper bound on a bank rate, not an estimate of one.
4. THRESHOLD SETTLED, AND NO SOURCE SUPPORTS A NUMBER. F6 gives the structure and
   no figure: a variable rate is "a reference rate and a spread" (page 3), and
   disclosure should cover "which component(s) of the interest rate can be
   revised, e.g. spread over reference rate" (page 7). F5 gives only movements:
   the median rate on newly originated loans "has fallen by around 90 bps since Q2
   2024" (page 34), and a stress test of "a 100 bps increase" which "would bring
   mortgage rates to around the elevated levels seen in 2023 and 2024" (page 36).
   Both are changes from an unpublished base. Every other "spread" in F5 is a
   corporate bond spread. So 1.0 stays and is labelled a judgement threshold, not
   derived from a source, in section 6 and in the article.
5. ONE FILE I DID NOT DELETE, AND I WANT YOUR RULING. You asked me to remove
   cpff1.pdf and cpff2.pdf as duplicates of cpf1.pdf. cpff2.pdf is one: not
   byte-identical, 356 bytes of wrapper apart, but all 15 embedded images match
   md5 in order. Removed. cpff1.pdf is NOT: two images, matching neither of
   cpf1.pdf's fifteen. It is the CPF FAQ page, and its page 2 carries the official
   link and size for "historical CPF interest rates (PDF, 0.17MB)", which is F2
   itself. I kept it, renamed cpf_faq_interest_rates_page.pdf, and recorded the
   instruction as declined pending your ruling. Say remove and it goes in the next
   commit.
6. F2 I CANNOT GET. 403 at CONNECT to www.cpf.gov.sg, logged by the proxy at
   2026-09-17T12:20:54Z; cpf.gov.sg joins the hosts already noted at the top of
   RETRIEVED.txt. It needs Jacob. I have NOT treated this as a soft blocker: it is
   the only item in the sealing checklist still open, because the whole piece is
   computed against a constant this repository can still only evidence at four
   dated instants. F8 helps and does not fix it.
7. F1 UNOPENED, as instructed. To name the file correctly I read its column
   headings and its DataSeries labels only, and I am telling you that rather than
   leaving it implicit: the upload was named
   CurrentBanksInterestRatesEndOfPeriodMonthly.csv, which says banks' rates and is
   in fact the benchmark series, and renaming it f1_sora_sgs_monthly.csv without
   checking would have been guessing. No values read.
8. ONE THING I SAW THAT YOU SHOULD KNOW BEFORE RULING ON THE SEAL. F5 page 24 is a
   markets table and it prints 3-month SORA levels for Q3 2024 and Q3 2025 and
   10-year SGS yields. I read F5 because you told me to, but that means I have now
   seen two SORA values, both well outside the cheap decade the predictions are
   about. I do not think it compromises anything: the predictions concern realised
   break-even spreads for 2010-2015 against 2020-2023, and nothing on that page
   bears on them. Flagging it so the decision is yours and not mine by omission.
9. RAW TIDY DONE IN ONE COMMIT, as asked: 7e456e9. Five renames, one removal, one
   decline, a FOURTH DELIVERY block with bytes and MD5 for every file, and the
   missing F2 recorded rather than passed over. CHECKSUMS.md5 regenerated last, 66
   files. run_all.sh exit 0 from a fresh clone of the pushed branch.
10. NOT DONE, UNCHANGED: THESIS.md is not sealed and I have not sealed it. No rate
   numbers computed, no financing/ scripts written. The README reword still waits
   on PR #1 merging, which has not happened.
