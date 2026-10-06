#!/usr/bin/env bash
# cargradient piece. One command, from the repository root or anywhere:
#
#   bash cargradient/run_all.sh
#
# 1. Always: the synthetic test suite (cargradient/tests/, invented data
#    only). It builds invented raw files, runs steps 10-15 end to end on them,
#    forces every outcome branch, and checks the seal guard.
# 2. Only once the thesis is sealed (cargradient/SEALED exists): steps 10-15
#    on the real data, then every checksum verified. Before the seal the real
#    steps are skipped, and 10_load.py would refuse cargradient/raw/ anyway.
#
# Exits non-zero if any test or step fails or any checksum does not match.
# CHECKSUMS.md5 is never written here; regenerate it by hand, last, with
#   python3 cargradient/14_manifest.py
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== cargradient: python and packages"
python3 --version
python3 -c "import pandas, numpy, scipy, pyfixest; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| scipy', scipy.__version__, '| pyfixest', pyfixest.__version__)"

echo; echo "== synthetic test suite (invented data only; no real price is read)"
python3 -W ignore -m unittest discover -s cargradient/tests -p "test_*.py" -v

if [ ! -f cargradient/SEALED ]; then
  echo; echo "== cargradient/SEALED absent: THESIS.md is not sealed, so no real price is read."
  echo "cargradient run_all.sh completed: synthetic tests only"
  exit 0
fi

mkdir -p cargradient/out cargradient/figs
echo; echo "== 10 panel";            python3 cargradient/10_load.py
echo; echo "== 11 tests, gates, sensitivities, 7A, verdict"; python3 cargradient/11_tests.py
echo; echo "== 12 charts";           python3 cargradient/12_figures.py
echo; echo "== 15 independent reproduction"; python3 cargradient/15_reproduce.py
echo; echo "== 13 RESULTS.md";       python3 cargradient/13_results.py
echo; echo "== 14 checksums and number manifest, verified"; python3 cargradient/14_manifest.py --check
echo; echo "cargradient run_all.sh completed, all checksums verified"
