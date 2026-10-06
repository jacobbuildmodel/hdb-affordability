# cargradient

Does a dearer COE tilt HDB resale prices toward the city centre? A conceptual
replication, on public HDB resale data, of Huang, Li and Ross (2018), who
studied private homes. Pre-seal: THESIS.md is an UNSEALED draft, and no
resale price has been opened. Run `bash cargradient/run_all.sh`.

| Path | What it is |
|---|---|
| THESIS.md | the tests, windows, gates and verdict rule (unsealed draft) |
| office/ | paper notes, Rule 0, feasibility, design sketch, titles |
| 00_coverage.py | labels and counts of the five resale files; the price column is never parsed -> out/coverage.txt |
| 00_addresses.py | block, street and month from the five resale datasets (no price field) -> out/addresses.csv |
| 01_coe_ranges.py | quarterly COE premium, categories A and B, as the paper builds it -> out/coe_ranges.txt |
| 04_coe_crossings.py | when the A and B premiums were at or above $100,000, bidding by bidding -> out/coe_crossings.txt |
| 01_geocode.py | OneMap Search for each block -> out/blocks_geocoded.csv (cache out/geocode_cache.jsonl is not committed) |
| 02_distance.py | great-circle km to Raffles Place and City Hall MRT -> out/block_distance.csv, out/station_points.csv |
| 03_unmatched.py | resale rows per pair (counts only) and the unmatched pairs -> out/address_rowcounts.csv, out/unmatched.csv |
| 05_street_points.py | OneMap street points for the streets of the unmatched pairs (sensitivity J) -> out/street_points.csv |
| cglib.py | shared windows, thresholds, the seal guard and the outcome rules |
| 10_load.py | the analysis panel; refuses raw/ until SEALED exists -> out/panel.csv.gz, coe_quarterly.csv, geocode_coverage.csv |
| 11_tests.py | T1-T3, both gates, the sensitivities, section 7A and the verdict -> out/tests.csv and others |
| 12_figures.py | two charts with finding titles -> figs/ |
| 13_results.py | RESULTS.md, failures first |
| 14_manifest.py | checksums, number check, and --seal for SEAL_MANIFEST.md |
| 15_reproduce.py | independent route (numpy only) to every scored number |
| tests/ | invented-data fixtures and the suite that forces every outcome branch and checks the guard |
| run_all.sh | the suite always; the real run only after the seal |
| raw/ | sources, with URL, date and md5 in raw/RETRIEVED.txt; raw/hansard/ holds the Parliament records |

Run from the repository root. 01_geocode.py needs ONEMAP_EMAIL and
ONEMAP_PASSWORD in the environment. The token is held in memory only, and
calls are limited to one per second.

## Attribution

Contains information from OneMap (Singapore Land Authority), accessed 5
October 2026, under the Singapore Open Data Licence version 1.0.

Resale, COE and MRT exit data: data.gov.sg and SingStat (data source LTA),
under the Singapore Open Data Licence version 1.0.
