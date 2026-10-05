# GEOCODE_REPORT -- HDB blocks, OneMap, 5 October 2026

No resale price was read. Addresses and row counts came from the block,
street_name and month fields only (00_addresses.py, 03_unmatched.py; both
assert it).

## Run

- **01_geocode.py:** OneMap Search with Jacob's token (held in memory,
  never written), at one call per second.
  - Main run: 12:39 to 15:45 UTC, 10,016 pairs.
  - Five transient network errors, each retried after a 5-second back-off.
  - No 429 and no 5xx.
- **Re-query:** 293 matches were tenant records in the right block, such as
  a preschool or public shelter, which OneMap returns with POSTAL "NIL".
  `pick()` now prefers the block's own address record. Those pairs were
  re-queried with `--redo-nil`; see "Postal" below.
- **Matching:** a result is accepted only when BLK_NO equals the block and
  ROAD_NAME equals the expanded street. A nearby block is never taken.
- **Cache:** out/geocode_cache.jsonl, gitignored.

## Results (out/blocks_geocoded.csv)

| match_type | pairs |
|---|---|
| exact | 9,855 |
| expanded | 1 (4C ST. GEORGE'S LANE, matched as SAINT GEORGE'S LANE) |
| none | 160 |

- **Coordinates:** all matched points fall inside latitude 1.270 to 1.457
  and longitude 103.685 to 103.988.
- **Distance to Raffles Place** (mean of exits): 0.59 to 22.41 km.

## Unmatched pairs (out/unmatched.csv)

| | Resale rows unmatched | Of | Share |
|---|---|---|---|
| All years (1990-2026) | 13,628 | 988,123 | 1.38% |
| T1 window (2002-04 to 2015-12, less 2012Q1) | 2,914 | 352,036 | 0.83% |
| T2 window (2016-01 to 2026-09, less 2020Q2) | 0 | 257,856 | 0.00% |

- **The 160 unmatched pairs sit on 55 streets.** The most frequent:
  REDHILL CL (21 pairs), TANGLIN HALT RD (14), TEBAN GDNS RD (7) and
  BOON LAY DR (6).
- **Last sold before 2010: 111 pairs**, flagged "likely SERS or demolished".
  They hold 9,498 resale rows in all, and 1,183 in T1's window.
- **Last sold 2010 or later: 49 pairs**, holding 4,130 rows in all and
  1,731 in T1's window.
  - The latest last sale is 2014-06 (Tanglin Halt Rd blocks 24 to 45 run to
    2013-2014), so none reaches T2.
  - They are likely redeveloped too. That was not checked against an HDB
    source.
- **109 unmatched pairs** have any sale in T1's window.
- **Gate 1 (THESIS section 6, 95 per cent of a window's sales geocoded)
  passes:** T1 99.17 per cent, T2 100 per cent.

## Fallback: proposal for Jacob

- **(A) "HDB Existing Building" GeoJSON via postal code. Not proposed.**
  - The resale files carry no postal code.
  - OneMap returned no record, so there is no postal code to join on.
  - The layer lists current buildings only (coverage from 2025-11-04), so
    a demolished block is not in it.
- **(B) One point per estate, from a scripted OneMap Search on the street
  name alone** (the road's point), labelled match_type "street".
  - It is reproducible and sourced.
  - Its error is the distance from the block to that point. That is
    typically a few hundred metres, against a mean distance of several
    kilometres. Hand-entered points are not proposed: they cannot be
    reproduced.
- **(C) Recommended: leave the 160 pairs out of the scored runs, and report
  (B) as a sensitivity.**
  - Reasons:
    - They are 0.83 per cent of T1's rows and none of T2's, and gate 1
      passes by a wide margin.
    - Most were demolished, so their late sales carry redevelopment hopes
      that are not the COE story.
    - An approximate point adds measurement error exactly where the
      blocks are oldest and closest to town.
  - The cost: dropping them removes some central, older blocks from T1, a
    small selection on location. The sensitivity shows whether it matters.

## Station points (out/station_points.csv)

- **Raffles Place MRT:** 10 exits. The mean of the exits (i) is 9.7 m from
  the nearest exit, Exit D (ii).
- **City Hall MRT:** 4 exits. (i) is 54.7 m from Exit B (ii).
- Across all blocks, km to Raffles Place differs by at most 9.8 m between
  (i) and (ii).
- Which point is used is sealed later.

## Postal

- The 293 tenant-record matches were re-queried at 15:46 to 15:52 UTC.
  - All 293 matched again on block and street.
  - 284 now carry the block's own address record and a real postal code.
- 9 matched pairs still have POSTAL "NIL": OneMap holds only tenant records
  for them.
- The re-picked points moved a median of 0.2 m and at most 93.2 m. So the
  distances were barely affected, but the postal codes are now the
  block's own.

Contains information from OneMap (Singapore Land Authority), accessed 5
October 2026, under the Singapore Open Data Licence version 1.0.
