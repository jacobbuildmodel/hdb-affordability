# Two things, step by step

Written 12 September 2026. Item 1 takes ten seconds. Item 2 has a cheap version
and an expensive version, and the cheap version gets most of the value.

---

## ITEM 1. The MD5 of the resale file, from your download machine

**Why.** The hashes in `raw/RETRIEVED.txt` were computed on the files as they
arrived in the session. They prove the files here are internally consistent. They
prove nothing about what data.gov.sg actually served you. The verifier downloads
the repository and re-runs everything, and this is the first joint it will test.

**Step by step, Windows:**

1. Open the folder where you downloaded the files. Probably `Downloads`.
2. Click once in the address bar at the top of the File Explorer window, so the
   path highlights.
3. Type `cmd` and press Enter. A black Command Prompt window opens, already in
   that folder.
4. Type this and press Enter:

       certutil -hashfile ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv MD5

   If the file has a different name, type `certutil -hashfile ` then drag the file
   from Explorer into the Command Prompt window, which pastes the full path, then
   type ` MD5` and press Enter.
5. It prints three lines. The middle one is a 32-character hash. Send me that line.

**What happens next.** If it reads

    a9e696ef2d4d10e9765eada65fbd50b2

the chain closes and `RETRIEVED.txt` gets upgraded from "internally consistent" to
"matches the source". If it reads anything else, something altered the file between
your disk and here, and I need to know that before the article quotes a single
number from it.

Same command works for any of the other files if you want to do them all. One is
enough; the big file is the one that matters.

---

## ITEM 2. The pre-2019 grant schedule

Here is the honest position. The grant series currently starts in 2019 while the
conventional measure runs from 2013. That asymmetry is stated in the article
rather than hidden, so nothing is broken. But closing it would let me write
something considerably better, and I have found a way to get most of it cheaply.

### What replaced what

Before 11 September 2019, a first-timer family buying a **resale** flat could get:

- the **CPF Housing Grant**, the flat-amount one, which I already have back to
  August 2015 from the Budget 2023 annex
- the **Additional CPF Housing Grant (AHG)**, means-tested, monthly income ceiling
  of about **5,000 dollars**, which ran from March 2006 until the EHG replaced it
- the **Proximity Housing Grant** from August 2015, which I exclude by design
  because it depends on living near a parent rather than on income

The **Special CPF Housing Grant** does not matter here. It applied to new flats
bought from HDB, not to resale, so it never touched this subgroup.

So the whole gap is the AHG.

### 2a. The cheap version, and please do this one

**All I actually need is the AHG income ceiling, with a date.** One number.

Here is why that is nearly enough. The median household earned 7,000 dollars a
month in 2013 and 8,169 in 2018. The AHG ceiling was around 5,000. So the median
household was **above the means-tested grant ceiling in every year from 2013 to
2018**, and got nothing from it. Same for the 80th percentile, by a mile. Only the
20th-percentile buyer, on 3,051 dollars in 2013, was inside.

With the ceiling alone I can extend the median and the 80th-percentile grant series
back to 2013 with a documented zero, which gives the article its spine:

> the median household was outside the means-tested grant until 2019, inside it
> for three years, and outside it again from 2023

That arc is the piece. It needs one sourced number.

**Step by step:**

1. Go to https://web.archive.org
2. Paste this into the search box at the top:

       hdb.gov.sg/cs/infoweb/residential/buying-a-flat/resale/cpf-housing-grants-for-hdb-flats/additional-cpf-housing-grant-ahg

3. A calendar of snapshots appears. Click **2018**, then any date with a blue or
   green circle.
4. The old HDB page loads as it looked then. Ctrl+P, Save as PDF, send it.

If that exact URL has no snapshots, search `web.archive.org` for
`hdb.gov.sg additional cpf housing grant` and take whatever 2016 to 2018 snapshot
comes up. Any of them will state the ceiling.

**Alternative if the Wayback Machine is awkward:** HDB's letter to estate agents
announcing the EHG describes what it replaced.
https://www.hdb.gov.sg/business/estate-agents-and-salespersons/letters-to-keos/enhanced-cpf-housing-grant-and-higher-income-ceiling
Open it, Ctrl+P, Save as PDF. If it names the AHG ceiling, that is a cleaner
source than an archived page and I will use it instead.

### 2b. The expensive version, genuinely optional

The full AHG band table, so the 20th-percentile line also extends back to 2013.
Same Wayback snapshot as above will usually contain it, in which case you get this
for free and there is nothing extra to do.

If the snapshot shows only the ceiling and not the amounts, **stop there**. Do not
go hunting. The 20th-percentile line simply starts in 2019 like it does now, and
the article says so. One line starting later is a footnote. The median arc is the
argument.

### What I will not do

Reconstruct the AHG from a property blog's summary. If the ceiling cannot be
sourced from HDB, archived or current, the grant series stays at 2019 to 2025 and
the article carries one sentence saying the pre-2019 schedule could not be
documented. That is a worse article and an honest one.

---

## Where this leaves the piece

Neither item blocks publication. Item 1 firms up provenance. Item 2a buys a better
section 3. Meanwhile I am building figures, the sources file, the number manifest,
the checksums, the handover brief and the article itself.
