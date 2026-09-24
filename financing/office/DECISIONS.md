# DECISIONS -- hdb-financing

| Date | Decision | By |
|---|---|---|
| 2026-09-16 | Break-even spread design accepted | Jacob |
| 2026-09-16 | Article date 2026-09-26, provisional; moves if F3 changes the design | Jacob |
| 2026-09-16 | Pilot: researcher runs as a Claude Code session and talks to the checker directly | Jacob |
| 2026-09-17 | R1 (never act) dropped from the refinancing rules; only R2 and R3 modelled, since no board-rate source exists to give R1 a labelled spread step-up | claude-2a |
| 2026-09-17 | cpf_faq_interest_rates_page.pdf (was cpff1.pdf) is KEPT, not removed: it is not a duplicate of cpf1.pdf and its page 2 is the provenance trail for F2 | claude-e4 |
| 2026-09-17 | F5 SORA exposure ACCEPTED. Reading F5 as instructed exposed the researcher to two compounded 3-month SORA values (Q3 2024 and Q3 2025) and 10-year SGS yields, printed in the markets table on page 24. Both are outside the 2010-2015 and 2020-2023 groups the predictions concern, and neither bears on any prediction. Recorded rather than left implicit, at the researcher's flag | claude-e4 |
| 2026-09-17 | Switching-cost grid CONFIRMED at S$0 / S$3,000 / S$6,000, still labelled assumptions | Jacob |
| 2026-09-17 | F3 carries no banks' housing loan rate, so the break-even design stands and is not replaced. F4 no longer needed | claude-e4 |
| 2026-09-17 | The 1.0 point threshold in prediction 1b is kept and labelled a judgement threshold, not derived from a source, no primary source publishing a bank mortgage spread having been found in F5 or F6 | claude-e4 |
| 2026-09-17 | THESIS.md SEALED. Sealed content is the file at commit 0ed509e, md5 7eaf10ff2ea96d4fd73503d849699411. With the SEALED header added (the only post-ruling change) the file is md5 af585c3a7a922818dfd632fdc9694e49. Sealed before any F1 rate value was read; the seal is committed on its own so the ordering is visible in the history. From here THESIS.md changes only by appended, dated AMENDMENT blocks stating whether they were written before or after seeing results | claude-e4 |
| 2026-09-17 | AMENDMENT 1 (R3 as hindsight trigger grid) ACCEPTED. R3 is implemented as the cheapest outcome over a grid of constant refinancing triggers, chosen with hindsight, rather than the literal monthly re-evaluation the sealed wording would produce, so that R3 <= R2 holds by construction and the "upper bound, not a real person" property in THESIS.md section 5 is real rather than asserted | claude-e4 |
