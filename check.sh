#!/usr/bin/env bash
# check.sh -- the machine-checkable half of STANDARDS v2.
# Run from the repository root:  ./check.sh            (fast checks only)
#                               ./check.sh --full     (also rebuilds and tests the guard)
# Exits non-zero if any check fails. Every failure prints file and line.
set -uo pipefail
cd "$(dirname "$0")"

FULL=0
[ "${1:-}" = "--full" ] && FULL=1
FAIL=0
note() { printf '%s\n' "$*"; }
fail() { printf 'FAIL  %s\n' "$*"; FAIL=1; }
pass() { printf 'pass  %s\n' "$*"; }

# Files this repository ships as prose or code, excluding vendored data.
TEXT=$(git ls-files '*.md' '*.py' '*.sh' '*.txt' '*.csv' 2>/dev/null | grep -v '^raw/' || true)
ARTICLES=$(git ls-files '*.md' | grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$' || true)
SVGS=$(git ls-files '*.svg' || true)

note "== F5 pure ASCII"
BAD=$(grep -nP '[^\x00-\x7F]' $TEXT 2>/dev/null | head -20 || true)
[ -z "$BAD" ] && pass "no non-ASCII in tracked text" || { fail "non-ASCII found"; printf '%s\n' "$BAD"; }

note "== F3 banned words, articles only"
if [ -n "$ARTICLES" ]; then
  BAD=$(grep -nEi '\b(you should|should buy|recommend|better option|price target|buy the|sell the)\b' $ARTICLES || true)
  [ -z "$BAD" ] && pass "no advice language" || { fail "advice language"; printf '%s\n' "$BAD"; }
  BAD=$(grep -nE '\bwe\b' $ARTICLES || true)
  [ -z "$BAD" ] && pass "no royal we" || { fail "royal we"; printf '%s\n' "$BAD"; }
fi

note "== F5/F6 headline and length"
for a in $ARTICLES; do
  T=$(sed -n 's/^title: *"\(.*\)"/\1/p' "$a" | head -1)
  [ -n "$T" ] && { L=${#T}; [ "$L" -le 60 ] && pass "$a headline $L chars" || fail "$a headline $L chars, over 60"; }
  W=$(python3 -c "
import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
if t.startswith('---'):
    t=t.split('---',2)[2] if t.count('---')>=2 else t
t=re.sub(r'\{\{<\s*aside.*?\{\{<\s*/aside\s*>\}\}',' ',t,flags=re.S)
t=re.sub(r'\{\{<[^>]*>\}\}',' ',t)
t=re.sub(r'!\[[^\]]*\]\([^)]*\)',' ',t)
print(len(t.split()))" "$a")
  if [ "$W" -lt 1200 ] || [ "$W" -gt 1800 ]; then fail "$a $W words, outside 1200-1800"; else pass "$a $W words"; fi
done

note "== E1/E2 charts: dark mode block and 390px legibility"
for s in $SVGS; do
  grep -q 'prefers-color-scheme' "$s" || fail "$s has no prefers-color-scheme block"
  python3 - "$s" <<'PY'
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8',errors='replace').read()
m=re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"',s)
sizes=[float(x) for x in re.findall(r'font-size[:=]"?\s*([\d.]+)',s)]
if not m or not sizes:
    print("      (no viewBox or no font-size found in %s)"%p); sys.exit(0)
scale=390.0/float(m.group(1))
smallest=min(sizes)*scale
print("      %s smallest rendered text at 390px: %.1fpx"%(p,smallest))
sys.exit(1 if smallest < 11.0 else 0)
PY
  [ $? -eq 1 ] && fail "$s text under 11px at 390px"
done

note "== A6 requirements cover every import"
python3 - <<'PY'
import ast,glob,sys,re,os
std=set(sys.stdlib_module_names)
req=set()
for f in glob.glob('requirements.txt')+glob.glob('*/requirements.txt'):
    for l in open(f):
        l=l.split('#')[0].strip()
        if l: req.add(re.split(r'[<>=!\[]',l)[0].lower().replace('-','_'))
missing=set()
for f in glob.glob('*.py')+glob.glob('*/*.py'):
    try: t=ast.parse(open(f,encoding='utf-8').read())
    except SyntaxError: continue
    for n in ast.walk(t):
        if isinstance(n,ast.Import): mods=[a.name.split('.')[0] for a in n.names]
        elif isinstance(n,ast.ImportFrom) and n.level==0 and n.module: mods=[n.module.split('.')[0]]
        else: continue
        for m in mods:
            if m in std or m in req: continue
            if os.path.exists(m+'.py') or os.path.exists(os.path.join(os.path.dirname(f),m+'.py')): continue
            missing.add((f,m))
for f,m in sorted(missing): print("      undeclared import %s in %s"%(m,f))
sys.exit(1 if missing else 0)
PY
[ $? -eq 0 ] && pass "requirements cover every import" || fail "undeclared imports"

note "== A6 versions pinned"
UNPINNED=$(grep -hE '^[A-Za-z]' requirements.txt */requirements.txt 2>/dev/null | grep -v '==' || true)
[ -z "$UNPINNED" ] && pass "all versions pinned" || { fail "unpinned dependencies"; printf '      %s\n' $UNPINNED; }

note "== C1 provenance recorded"
if [ -d raw ]; then
  if [ -f raw/RETRIEVED.txt ]; then
    MISS=0
    for f in raw/*; do b=$(basename "$f"); [ "$b" = "RETRIEVED.txt" ] && continue
      grep -q -- "$b" raw/RETRIEVED.txt || { fail "raw/$b not recorded in RETRIEVED.txt"; MISS=1; }; done
    [ $MISS -eq 0 ] && pass "every raw file recorded"
  else fail "raw/ exists but RETRIEVED.txt does not"; fi
fi

if [ $FULL -eq 1 ]; then
  note "== A2/A3 rebuild from clean, outputs byte-identical"
  git diff --quiet || { fail "working tree dirty before rebuild"; }
  rm -rf out figs */out */figs 2>/dev/null
  if ./run_all.sh > /tmp/check_run.log 2>&1; then pass "run_all.sh exit 0"; else fail "run_all.sh failed, see /tmp/check_run.log"; fi
  if git diff --quiet; then pass "outputs byte-identical"; else fail "rebuild changed committed outputs"; git diff --stat | tail -5; fi

  note "== A5 a corrupted output must fail the rebuild"
  VICTIM=$(git ls-files 'out/*.csv' | head -1)
  if [ -n "$VICTIM" ]; then
    cp "$VICTIM" /tmp/victim.bak; printf 'corrupted\n' >> "$VICTIM"
    if ./run_all.sh > /dev/null 2>&1; then fail "corrupted $VICTIM still passed the rebuild"; else pass "corruption detected"; fi
    cp /tmp/victim.bak "$VICTIM"
  else note "      (no out/*.csv to corrupt; skipped)"; fi
fi

echo
[ $FAIL -eq 0 ] && { echo "ALL CHECKS PASSED"; exit 0; } || { echo "CHECKS FAILED"; exit 1; }
