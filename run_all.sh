#!/usr/bin/env bash
# Rebuilds every output from raw/. One command, from clean.
#
#   rm -rf out figs && ./run_all.sh
#
# Exits non-zero if any step fails or any checksum does not match.
set -euo pipefail

cd "$(dirname "$0")"

echo "== python and packages"
python3 --version
python3 -c "import pandas, numpy, statsmodels; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| statsmodels', statsmodels.__version__)"

mkdir -p out figs

echo
echo "== 00 grant schedule invariants"
python3 00_validate_schedule.py --selftest
python3 00_validate_schedule.py

echo
echo "== 01 clean"
python3 01_clean.py

echo
echo "== 02 hedonic index"
python3 02_hedonic.py

echo
echo "== 03 fixed-basket index"
python3 03_basket.py

echo
echo "== 02b hedonic, lease spline robustness"
python3 02_hedonic.py --lease-spline

echo
echo "== 04 grants"
python3 04_grants.py

echo
echo "== 05 affordability"
python3 05_affordability.py

echo
echo "== 06 pre-registered tests"
python3 06_tests.py

echo
echo "== 07 figures"
python3 07_figures.py

echo
echo "== 08 number manifest and checksums, verified against the committed file"
python3 08_manifest.py --check

echo
echo "== financing piece =="
mkdir -p financing/out financing/figs

echo
echo "== 20 benchmark and HDB rate table"
python3 financing/20_rates.py

echo
echo "== 21 amortisation and refinancing model, selftest"
python3 financing/21_model.py --selftest

echo
echo "== 22 pre-registered tests T1-T4 and the S1 side comparison"
python3 financing/22_compute.py

echo
echo "== 22b reset-interval sensitivity (AMENDMENT 3)"
python3 financing/22b_reset_sensitivity.py

echo
echo "== 23 charts"
python3 financing/23_figures.py

echo
echo "== 24 scoring against the sealed THESIS.md"
python3 financing/24_results.py

echo
echo "== 25 financing checksums and number manifest, verified"
python3 financing/25_manifest.py --check

echo
echo "run_all.sh completed, all checksums verified"
echo "(CHECKSUMS.md5 is not written here. After an intentional change, regenerate"
echo "it by hand with: python3 08_manifest.py -- see README.md)"
