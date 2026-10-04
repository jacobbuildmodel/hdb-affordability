# PAPER_NOTES -- Huang, Li and Ross (2018)

Read from cargradient/raw/huang_li_ross_2018.pdf (md5
b74310b9081111c3c8a179ec5bce842d, see cargradient/raw/RETRIEVED.txt).

**Which version this is.** The public copy is a WORKING PAPER dated
"December 26th, 2016" (p. 1), 38 pages. The published article is Regional
Science and Urban Economics 68 (2018), pp. 160-171,
doi:10.1016/j.regsciurbeco.2017.10.009 (volume, pages and DOI from the RePEc
listing, https://ideas.repec.org/a/eee/regeco/v68y2018icp160-171.html). The
published text was not read: www.sciencedirect.com answers automated requests
with a 403 page, and no other copy was tried. Every page and table number
below is the working paper's. The published coefficients may differ; check
before any number is quoted in public.

Their data: URA REALIS private non-landed homes (paid). This piece uses HDB
resale data, so it is a conceptual replication, and the piece says so.

## 1. The specification (Section 4, pp. 11-13)

Equation (1), p. 11:

    P_it = b1 COEP_t + b2 DD_i x COEP_t + b3 PPI_t + g_i + u_it

- P_it: "median area-adjusted house price in housing project i in quarter t"
  (p. 11). Area-adjusted means transaction price divided by floor area, then
  the median over all sales in that project and quarter (p. 14, note 27). In
  LEVELS, not logs. The area unit (sq ft or sq m) is not stated.
- COEP_t: quarterly COE premium (see section 4 below).
- DD_i: distance in kilometres from project i to the city centre (p. 11).
- PPI_t: price index for the national non-landed private market (p. 11), in
  columns (2) and (3) only.
- g_i: project fixed effects (p. 11).
- Time controls by column (p. 16; Table 2 rows, p. 28): (1) none; (2) PPI;
  (3) PPI plus a yearly linear trend; (4) year x quarter fixed effects (b1
  and the PPI drop out); (5) adds a planning-area linear trend.
- Estimation: OLS (Table 2) and IV, the headline. COE quota COEQ_t and
  DD_i x COEQ_t instrument COEP_t and DD_i x COEP_t (p. 13; Tables 3a, 3b).
- Standard errors clustered by project; t statistics in parentheses
  (p. 16; table headers).

## 2. The sample and years (Section 5, pp. 13-15)

- Private non-landed homes (apartments and condominiums) only (p. 9). HDB
  flats excluded "due to the high subsidy received" (p. 9). Landed homes
  excluded (p. 9, note 15).
- 2002Q2 to 2015Q4 (p. 4 and p. 15). COE data April 2002 to December 2015
  (p. 14).
- Project-quarter cells with at least three transactions (p. 14, note 27).
  En bloc (collective) sales excluded (p. 14).
- 2,543 projects (p. 15); 43,073 project-quarter observations (Table 1,
  p. 27); 30 of 55 planning areas (p. 16, note 33).

## 3. How distance is measured (pp. 11, 14-15)

- City centre: Raffles Place MRT station (p. 11, note 19). Robustness: City
  Hall MRT station (Table 5, p. 32).
- Each building's postal code is matched to MapInfo, a GIS product, which
  gives the distance from each building to 141 MRT stations (pp. 14-15).
  Distance to Raffles Place MRT is taken from that. A project with several
  buildings gets the average of its buildings (p. 15). Kilometres. Whether
  it is straight-line or along a network is not stated.
- MRT control: distance to the nearest station, using "all 2015 proposed and
  existing stations" (p. 15). Used only in the robustness check that keeps
  projects more than 1,000 m from the nearest station (Table 4, p. 31).

## 4. The COE series and its averaging (p. 11, p. 14)

- Categories A and B (cars). Category E (open) is added in a robustness check
  (Table 6, p. 33).
- Per auction, the A and B premiums are weighted by successful bids in each
  category. Then the auctions in a quarter are averaged (p. 14). (p. 11
  says "weighted by the quarterly COE quota"; p. 14 says "by the number of
  successful bids". The two descriptions differ; the p. 14 one is the more
  detailed.)
- The quota is aggregated the same way (p. 14). Source: LTA bidding results
  PDFs (p. 14, note 29).

## 5. Headline coefficients (the interaction is the gradient)

| Table, page | Estimator | Coefficient on COE premium x distance, columns (1) to (5) | t stats |
|---|---|---|---|
| Table 2, p. 28 | OLS | -0.0018, -0.0021, -0.0022, -0.0022, -0.0029 | -10.25 to -13.91 |
| Table 3b, p. 30 | IV (headline) | -0.0032, -0.0034, -0.0034, -0.0034, -0.0037 | -10.07 to -17.98 |
| Table 4, p. 31 | IV, more than 1 km from MRT | -0.0041, -0.0040, -0.0041, -0.0040, -0.0035 | -6.03 to -11.65 |
| Table 5, p. 32 | IV, City Hall centre | -0.0032, -0.0033, -0.0033, -0.0034, -0.0036 | -9.75 to -17.48 |
| Table 6, p. 33 | IV, categories A, B and E | -0.0032, -0.0035, -0.0035, -0.0035, -0.0036 | -9.92 to -18.47 |

The main COE premium coefficient (columns 1 to 3 only): OLS 0.0947, 0.0309,
0.0298; IV 0.1196, 0.0447, 0.0454. All coefficients carry three stars.

The sign tested here: a negative interaction. When COEs cost more, prices
rise more near Raffles Place and less further out.

**In words** (p. 17): a COE rise of S$30,000 (the 2009-2010 rise, p. 16)
goes with "approximately 8.37%" higher prices at the centre and 2.19% at 10
km. **Checker note:** the text attributes these to "column (3)" while
discussing the IV results (p. 16). Recomputed from the printed tables against
the Table 1 mean price (10,677.39), Table 2 OLS column (3) gives 8.37% and
2.19%. Table 3b IV column (3) gives 12.76% and 3.20%. So the quoted
percentages are the OLS ones. This is arithmetic on printed coefficients; no
model was fitted.

## 6. The stated mechanism (Section 3, pp. 10-11)

Two modes of transport, two bid-rent curves; prices follow the outer
envelope. People near the CBD, "where the subway system is the most
extensive, do not need a car" (p. 10). Those further out "are more likely to
need to purchase a car" (p. 10). A cheaper car moves some households between
X1 and X2 from public transport to cars, changing both the level and the
slope of prices (pp. 10-11). Their conclusion: costlier cars mean people
"pay more to locate closer to the CBD" (p. 18).

## 7. What does not carry over to HDB data (for DESIGN_SKETCH)

- Project fixed effects become block fixed effects. HDB flats in a block are
  not identical units, so flat type, area, storey and lease controls are
  needed.
- The PPI becomes the HDB Resale Price Index, or month fixed effects.
- Quarterly project medians: HDB blocks trade less often, and three sales a
  quarter would drop many blocks. Whether to aggregate is a design choice to
  seal.
- HDB buyers face eligibility rules and grants (their p. 9 reason for leaving
  HDB out). That is the main threat to a conceptual replication and is
  stated in the piece.

## Exposure, disclosed

Reading the paper exposed the researcher to its COE premium summary for
2002Q2-2015Q4 (Table 1, p. 27, mean and range), its Figure 3 (premiums and
quotas from 2004Q1, p. 26), and the average 2012 premium (Table A2, p. 35).
These are COE values over test 1's window, not HDB prices, and they come from
the paper's private-housing sample. Recorded here so the checker can rule on
them before the seal.
