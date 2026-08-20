# Final Report - solo-2410311322-ai-doc-qa-assistant

## 1. 交付标识与仓库

- MSD_DELIVERY_ID: solo-2410311322-ai-doc-qa-assistant
- 仓库: 本地 git 仓库 D:\trae\work(单人提交,未推远程)
- 最终提交号: 见 evidence/W4-3_solo-2410311322-ai-doc-qa-assistant_final-check.txt 的 git log -1

## 2. 启动 / 测试 / 演示命令

```bash
cd /mnt/d/trae/work && . .venv/bin/activate
# Ollama(11435)
OLLAMA_HOST=127.0.0.1:11435 OLLAMA_MODELS=/home/add1223/.ollama/models ollama serve &
# 应用(8000)
OLLAMA_HOST=http://127.0.0.1:11435 uvicorn app.main:app --host 127.0.0.1 --port 8000
# 测试
OLLAMA_HOST=http://127.0.0.1:11435 python -m pytest -q     # 30 passed
bash scripts/check.sh                                        # 本地 CI
python scripts/uat_run.py                                    # UAT 7 PASS
bash scripts/scan_run.sh                                     # 安全扫描
```

## 3. PRD/SPEC/DESIGN/ADR 摘要

- PRD(docs/PRD.md): AI 文档问答助手,目标用户学生/研究者;5 用户故事;非目标(注册/联网/流式/评分);成功指标(有答带引用、无关拒绝、错误路径状态码正确)
- SPEC(docs/SPEC.md): 11 AC、5 端点(/health /login /documents /documents/{id} /ask)、8 错误路径(E1-E8)
- DESIGN(docs/DESIGN.md): 8 模块单向依赖、Document/Chunk/Answer 数据模型、文档状态机、LLMClient 协议(Ollama+Fake)、10 行失败路径映射、AC 映射
- ADR(docs/adr/): ADR-001 内存存储、ADR-002 nomic-embed-text、ADR-003 top_k=5(各 3 候选方案与取舍)

## 4. 过程资产索引

- 任务卡: process/task_cards/solo-2410311322-ai-doc-qa-assistant-project-cards.md(TC-W3-1..5)
- Gate: process/gate/...-gate-1-prd-spec.md, -gate-2-design.md, -gate-3-delivery.md
- UAT: process/uat/solo-2410311322-ai-doc-qa-assistant-final-uat.md
- 环境记录: evidence/W1-0_*environment.md
- spike: evidence/W1-1_*ai-capability-spike.txt + scripts/spike_rag.py
- 红绿: evidence/W2-1(red), W2-2(green 13), W3-0(red api), W3-1(green 30), W3-2(check.sh)
- UAT: evidence/W4-1_*uat.txt; 安全: evidence/W4-2_*secret-scan.txt; final-check: evidence/W4-3
- 周志: submissions/*weekly-1.md, *weekly-2.md

## 5. 测试与 UAT 结论

- 自动测试: 30 passed(纯函数 13 + API 17),mock LLM,不依赖 Ollama
- UAT: 7 PASS / 0 FAIL,真实 Ollama(nomic-embed-text + qwen3.5:4b)
- 主路径有答带 sources;无关问题拒绝;错误路径 401/404/422/409 正确

## 6. 安全与隐私

- 密钥扫描: 无真实凭据(rg exit 1)
- 占位符: 无未填残留(rg exit 1)
- 无截图,文本输出已脱敏
- 代码无硬编码 Key/Token(鉴权用运行时 issue_token 随机生成)

## 7. 分工

- 单人提交(solo-2410311322),全部工作由提交者完成;互审复述见 Gate 1

## 8. 已知限制与后续

- 内存存储重启丢失(ADR-001,L 阶段可换 SQLite)
- SCORE_THRESHOLD=0.6 / top_k=5(UAT 验证有效,可按语料调)
- 单机单用户(非目标)
- 真实模型仅在 spike/UAT
- 答辩 PPT 按用户要求暂未制作,答辩要点见 PROCESS.md"答辩要点"节
- 后续: 持久化、流式回答、多文档检索、回答质量评分(L 阶段)

## 9. 答辩要点(供 Q&A)

- 系统服务谁: 学生/研究者上传讲义,基于文档提问
- 最小可用场景: 上传一篇文档 -> 提问 -> 带引用回答;无关问题拒绝
- 被修正的决策: top_k 3 -> 5(ADR-003,spike 证明 3 漏召回关键定义片段)
- 最能证明质量的测试: tests/test_api.py::test_ask_with_answer(端到端)
- AI 生成修改: spike prompt(严格指令+引用编号),人工验证拒绝分支
- 密钥保护: 运行时随机 token,无硬编码
- 再给一周: 加持久化 + 多文档检索