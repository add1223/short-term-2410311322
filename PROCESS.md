# PROCESS - solo-2410311322-ai-doc-qa-assistant

> 本文件是过程资产索引:5 分钟内能定位全部过程资产。对应提交期"推荐目录"合同。

## 交付标识

- MSD_GROUP_ID: solo-2410311322
- MSD_PROJECT_ID: ai-doc-qa-assistant
- MSD_DELIVERY_ID: solo-2410311322-ai-doc-qa-assistant
- 主题: AI 文档问答助手(RAG:切块 -> nomic-embed-text 768 维检索 -> qwen3.5:4b 生成带引用回答)

## 阶段进度

- W1: PRD/SPEC + AI spike + Gate 1 (完成, commit 048dd33/732edb5)
- W2: DESIGN/ADR + 红绿 + Gate 2 + weekly-1 (完成, commit f2a7048/3104056)
- W3: 端点实现 + test_api + 红绿 (完成, commit dd1e6cb/a324eb0)
- W4: UAT + Gate 3 + 安全扫描 + weekly-2 + final-report + defense.pptx (待办)

## 过程资产索引

- PRD: docs/PRD.md
- SPEC: docs/SPEC.md
- DESIGN: docs/DESIGN.md
- ADR: docs/adr/ADR-001|002|003
- 任务卡: process/task_cards/solo-2410311322-ai-doc-qa-assistant-project-cards.md
- 周志 1: submissions/solo-2410311322-ai-doc-qa-assistant-weekly-1.md
- Gate: process/gate/solo-2410311322-ai-doc-qa-assistant-gate-1-prd-spec.md, -gate-2-design.md
- 环境记录: evidence/W1-0_solo-2410311322-ai-doc-qa-assistant_environment.md
- spike 证据: evidence/W1-1_solo-2410311322-ai-doc-qa-assistant_ai-capability-spike.txt
- 红绿证据: evidence/W2-1,W2-2,W3-0,W3-1
- check.sh 证据: evidence/W3-2_solo-2410311322-ai-doc-qa-assistant_check-sh.txt
- 本地检查脚本: scripts/check.sh
- RAG spike 脚本: scripts/spike_rag.py

## 关键演示信息

- 启动: wsl -d Ubuntu-24.04, cd /mnt/d/trae/work, . .venv/bin, uvicorn app.main:app --port 8000
- Ollama: OLLAMA_HOST=127.0.0.1:11435 OLLAMA_MODELS=/home/add1223/.ollama/models ollama serve
- 测试: OLLAMA_HOST=http://127.0.0.1:11435 python -m pytest -q
- 检查: bash scripts/check.sh
- 环境变量: OLLAMA_HOST=http://127.0.0.1:11435

## 答辩要点

- One decision changed during implementation（实现中变更过的一项决策）: top_k 3 -> 5(spike 证明 3 漏召回关键定义片段,见 ADR-003)
- One test that best proves quality（最能证明质量的一项测试）: tests/test_api.py::test_ask_with_answer(端到端:上传->检索->生成->带 sources)
- One AI-generated change reviewed manually（人工复核过的一项 AI 生成修改）: spike prompt 调优(严格指令+引用编号要求,人工验证拒绝分支)
- Latest passing commit（最近通过的提交）: a324eb0 (W3 green API tests 30 passed, check.sh pass)

## 已知限制

- 内存存储(ADR-001):重启丢失,UAT 演示前需现传文档
- SCORE_THRESHOLD=0.6:W4 UAT 需验证调参
- 单机单用户,不处理高并发(非目标)
- 真实模型仅在 spike/UAT,自动测试用 FakeLLMClient