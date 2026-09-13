# Sources

Every source behind the article, with its retrieval date and what it is allowed to
support. The article's own Sources section is the reader-facing version; this one is
the register.

Rule in force: news reporting and industry commentary tell you something happened.
They are never the source of a number. Where no primary document exists, the article
says so.

All files were downloaded on **12 September 2026** by Jacob Ong on his own machine,
because data.gov.sg, singstat.gov.sg and hdb.gov.sg all refuse automated requests
from the analysis environment. Byte counts and MD5s are in `raw/RETRIEVED.txt`.

## Transaction and price data

| File | Dataset | Publisher | Vintage | Status |
|---|---|---|---|---|
| `resale_jan2017_onwards.csv` | `d_8b84c4ee58e3cfc0ece0d773c8ca6abc` | HDB | 28 Aug 2026 | PRIMARY |
| `resale_jan2015_dec2016.csv` | `d_ea9ed51da2787afaf8e51f827c304208` | HDB | 28 Aug 2024 | PRIMARY |
| `resale_mar2012_dec2014.csv` | `d_2d5ff9ea31397b66239f245f57751537` | HDB | 28 Aug 2024 | PRIMARY |
| `rpi_quarterly.csv` | `d_14f63e595975691e7c24a27ae4c07c79` | HDB | 24 Jul 2026 | PRIMARY, context only |

The 2017-onwards file was independently hashed on the download machine and matches
the hash computed here: `a9e696ef2d4d10e9765eada65fbd50b2`. The provenance chain is
closed for the file every headline number depends on.

Only files on a **registration-date** basis are used. The 1990-1999 and 2000-Feb 2012
files are on an approval-date basis and are deliberately excluded, because mixing the
two would be a silent break in the series.

## Income data

| File | Dataset | Publisher | Vintage | Status |
|---|---|---|---|---|
| `income_percentiles_excl_cpf.csv` | `d_ff1988785f3e36cfc4757cf604ae0acd` | SingStat | 27 May 2026 | PRIMARY, the series used |
| `income_percentiles_incl_cpf.csv` | `d_dff6b97b7c233917ac8294bd04051486` | SingStat | 26 May 2026 | PRIMARY, sensitivity only |
| `income_resident_vs_employed.csv` | `d_ab4f7ecfc45e0a0eafe4ae4397e77059` | SingStat | 28 Oct 2024 | PRIMARY, ends 2023 |

The excluding-employer-CPF series is the one used, because that is the basis HDB
assesses income on. See the definitions section below.

## Grants

| Document | Date | What it settles | Status |
|---|---|---|---|
| `ehg_amount_families.pdf` | current | the sixteen EHG income bands and amounts | PRIMARY |
| `hdb_20240819_annexA_ehg_structure.pdf` | 19 Aug 2024 | the pre-change and post-change EHG tables printed side by side, which is what makes the 2019-2024 regime sourceable at all | PRIMARY |
| `hdb_20230214_further_support_first_timers.pdf` | 14 Feb 2023 | CPF Housing Grant 50,000 to 80,000 for 2- to 4-room resale; EHG maximum at 80,000 before Aug 2024; PHG at 30,000; family total 160,000 to 190,000 | PRIMARY |
| MOF Budget 2023 Annex E-1 | 14 Feb 2023 | the same grant increase, and the 14,000 income ceiling in force at the time | PRIMARY |
| `hdb_ehg_page.pdf` | page updated 20 Aug 2026 | the EHG household income ceiling of 9,000 | PRIMARY |
| `hdb_mnd_shg_flyer_2011.pdf` | circa 2011 | the AHG applied to resale and maxed at 40,000; the SHG never applied to resale | PRIMARY |

MOF Budget 2023 Annex E-1:
https://isomer-user-content.by.gov.sg/153/5389b2b9-e526-4696-b138-9fcd49096960/annexe1.pdf

## Financing

| Document | Date | What it settles | Status |
|---|---|---|---|
| MOF, Measures to Cool the Property Market | 15 Dec 2021 | loan-to-value 90 to 85 per cent, effective 16 Dec 2021 | PRIMARY |
| MAS, Measures to Promote Sustainable Conditions | effective 30 Sep 2022 | loan-to-value 85 to 80 per cent, and the 3 per cent stress rate | PRIMARY |
| `hdb_interest_rate_page.pdf` | page updated 15 Jul 2026 | the 0.1 point peg above the CPF Ordinary Account rate, and 2.60 per cent currently | PRIMARY |
| `cpf2.pdf` | Q1 2016 | Ordinary Account at the 2.5 per cent floor, HDB rate 2.6 per cent, computed rate 0.21 per cent | PRIMARY |
| `cpf3_q3_2026.pdf` | Q3 2026 | the same two numbers ten years later, computed rate 0.32 per cent | PRIMARY |

The August 2024 loan-to-value cut from 80 to 75 per cent is **NEEDS-PRIMARY**. The
HDB release is not reachable from this environment and the press release archive does
not go back far enough. It is carried in `ltv_schedule.csv` with that status and the
article does not lean on it.

## Definitions, and why they decided the analysis

- **HDB**, ask.gov.sg, "How does HDB determine my average gross monthly household
  income?", retrieved 12 September 2026.
  https://ask.gov.sg/hdb/questions/clxsp9q6x0029df0en2tm8ch3
  > "The income considered refers to the total gross income earned including
  > employee's CPF deductions and excluding employer's CPF contributions and
  > bonuses."

- **SingStat**, Key Household Income Trends glossary, retrieved 12 September 2026.
  https://www.singstat.gov.sg/-/media/files/publications/households/khitglossary.pdf
  > "Monthly household employment income includes one-twelfth of the annual bonus."

These two sentences settle the choice of income series and force one caveat. HDB
excludes the employer's CPF contribution, so the excluding-CPF series is correct.
HDB also excludes bonuses and SingStat includes a twelfth of them, so the series sits
**above** HDB's assessed basis. Every income-threshold result is therefore a bound,
not a point.

- **MOM**, Gross Monthly Income from Employment: Concepts and Definitions, and
  Average (Mean) Monthly Earnings, both retrieved 12 September 2026, which agree with
  SingStat on the bonus treatment.

## Used to find things, never cited for a figure

AsiaOne, EdgeProp, PropertyGuru, Stacked Homes, The Financial Coconut, 99.co, a
People's Action Party news page, and Wikipedia. Each was useful for learning that
something happened or for locating a primary document. None supports a number in the
article.

The PAP page gives the Additional CPF Housing Grant income ceiling as 5,000 dollars.
That figure is not used anywhere, because a party website is not a source.

## Not obtained

- **The Additional CPF Housing Grant income ceiling.** Three routes were tried on
  12 September 2026 and all failed: the Wayback Machine has no snapshot of HDB's AHG
  page, HDB's press release archive does not reach September 2019, and the 2011
  flyer's table stops at 2,250 dollars a month because that was the Special CPF
  Housing Grant's ceiling rather than the AHG's. Consequence: no pre-2019 grant is
  modelled and the grant measures run from 2019 while the price measure runs from
  2013. Stated in the article.
- **The August 2024 loan-to-value release.** See above.
- **A MOM bonus share for a lower bound on the crossing year.** The Report on Wage
  Practices 2025 is in `raw/` and gives variable wages as about 13 per cent of total
  wages, but it is an establishment-based private-sector series rather than a
  household one, so it is not used to adjust the household income series. The 2022
  crossing is published as an upper bound only.

## Technique

Borrowed for craft, not content. The Pudding on data-essay structure, the UK
Government Analysis Function on writing about statistics, and Our World in Data on
letting the figure carry the argument and the prose carry the caveat.
