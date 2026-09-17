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
echo "run_all.sh completed, all checksums verified"
echo "(CHECKSUMS.md5 is not written here. After an intentional change, regenerate"
echo "it by hand with: python3 08_manifest.py -- see README.md)"
