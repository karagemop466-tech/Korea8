#!/usr/bin/env bash
# Resolve the recurring concurrent-merge conflicts on the canonical dashboard branch.
# Generated artifacts are regenerated from data; COORDINATION.md keeps both sessions' text.
set -euo pipefail
cd /home/user/Korea8

git fetch origin -q
if git merge origin/main --no-edit >/tmp/merge.log 2>&1; then
  echo "merge clean"
else
  echo "merge had conflicts:"; git diff --name-only --diff-filter=U
fi

GEN="overflow-integration/build-report.json overflow-integration/verification-report.json site-data/build-report.json site-data/verification.json verification.html flagged-for-review.html index.html sources.html audit/independent_audit_report.json overflow-integration/EXECUTIVE_SUMMARY.md OVERFLOW_EXECUTIVE_SUMMARY.md"

for f in $(git diff --name-only --diff-filter=U); do
  case " $GEN " in
    *" $f "*) git checkout --theirs -- "$f"; echo "took upstream generated: $f" ;;
    *)
      python3 - "$f" <<'PY'
import re,sys
p=sys.argv[1]
t=open(p).read()
n=len(re.findall(r'^<<<<<<<',t,re.M))
t=re.sub(r'<<<<<<< [^\n]*\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n',lambda m:m.group(1).rstrip('\n')+'\n\n'+m.group(2).rstrip('\n')+'\n',t,flags=re.S)
assert '<<<<<<<' not in t and '>>>>>>>' not in t, p
open(p,'w').write(t)
print(f'merged both sides ({n} blocks): {p}')
PY
      ;;
  esac
done

git add -A
python3 -c "import ast;ast.parse(open('scripts/build_overflow_site.py').read())" && echo "generator syntax OK"
python3 scripts/build_overflow_site.py >/tmp/build.log 2>&1 && tail -n 6 /tmp/build.log
python3 scripts/verify_overflow_site.py 2>&1 | tail -n 2
python3 -m unittest discover -s tests -p 'test_overflow*.py' 2>&1 | tail -n 2
python3 audit/independent_audit.py 2>&1 | tail -n 1
python3 scripts/wording_guard.py 2>&1 | tail -n 1
python3 scripts/stage_overflow_pages.py 2>&1 | tail -n 1
git diff --check && echo "diff-check clean"
