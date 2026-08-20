#!/usr/bin/env bash
# 最终提交前自查
cd /mnt/d/trae/work || exit 1
ID=solo-2410311322-ai-doc-qa-assistant
echo "================ 终检 $ID ================"
echo ""
echo "== 1. 提交文件存在性 =="
for f in submissions/$ID-weekly-1.md submissions/$ID-weekly-2.md submissions/$ID-final-report.md; do
  if [ -f "$f" ]; then echo "OK  $f"; else echo "MISSING  $f"; fi
done
echo "note: defense.pptx 按用户要求暂未制作(答辩要点见 PROCESS.md/final-report)"
echo ""
echo "== 2. 本地检查 check.sh =="
. .venv/bin/activate
OLLAMA_HOST=http://127.0.0.1:11435 bash scripts/check.sh 2>&1 | grep -E "passed|whitespace|local checks"
echo ""
echo "== 3. 未填项检查(应无命中) =="
rg -n '<[^>\n]+>|TODO|TBD|待补|your-|changeme|示例项目' README.md docs process PROCESS.md submissions
echo "rg exit: $?"
echo ""
echo "== 4. 密钥扫描(应无命中) =="
rg -n -f scripts/msd-secret-patterns.txt --glob '!scripts/msd-secret-patterns.txt' .
echo "rg exit: $?"
echo ""
echo "== 5. DELIVERY_ID 可定位性 =="
rg -l "$ID|Gate 1|Gate 2|Gate 3|final-uat|secret-scan|最终提交" submissions PROCESS.md process evidence
echo ""
echo "== 6. 最终提交号 =="
git log -1 --oneline
echo ""
echo "================ 终检完成 ================"