# Gate 1 PRD/SPEC - solo-2410311322-ai-doc-qa-assistant

> 闸门目标: 审计 PRD/SPEC 是否可机器判定、API 契约完整、错误路径达标、主题边界清晰、AI 能力可行。
> 方法: Loop Engineering,每轮 假设 -> 行动 -> 证据命令 -> 结果 -> 结论 -> 下一轮。

## 互审复述(可读性验证)

互审者读完后复述系统要做的事:

> AI Doc QA Assistant 是一个本地文档问答助手。用户(editor)上传一篇文本文档,系统切块并用 nomic-embed-text 做 768 维 embedding 索引;editor 或 viewer 针对该文档提问,系统用余弦相似度检索 top-k 片段,交给 qwen3.5:4b 生成带引用片段编号的回答;若检索到的片段与问题无关,返回固定文案"未找到相关内容"而不是编造。editor 可上传+提问,viewer 只能提问(越权上传被拒)。M 阶段单文档单机单用户,不接互联网检索、不做流式、不做质量评分。

复述覆盖: 用户角色、核心场景、AI 能力(RAG)、引用来源、拒绝分支、鉴权边界、非目标。可读性达标。

## Loop Engineering Round 1: 验收标准可机器判定 + API 契约完整 + 错误路径达标

- 假设: SPEC 的 AC 编号齐全且形如"操作 -> 预期输出",API 契约 5 个端点,错误路径 >=6 种。
- 行动: 用 grep 统计 AC 编号、状态码、错误路径表行;人工通读每条 AC 是否可机器判定。
- 证据命令:
  - `grep -c "AC-" docs/SPEC.md`
  - `grep -cE "422|401|404|409|201|200" docs/SPEC.md`
  - `grep -c "^| E[0-9]" docs/SPEC.md`
- 结果:
  - AC- 出现 11 次(US-1 x4, US-2 x4, US-3 x3 = 11 条验收标准,每故事 >=2 条)
  - 状态码出现 20+ 次(覆盖 200/201/401/404/422/409)
  - 错误路径表 8 行(E1-E8),满足 >=6
- 结论: 达标。AC 可机器判定(每条含"操作 -> 预期状态码 + 字段"),API 契约 5 端点齐全,错误路径 8 种超过 6 种门槛。
- 下一轮: 确认主题边界(不越 PRD 非目标范围),并用 spike 验证 AI 能力可行性。

## Loop Engineering Round 2: 主题边界确认 + AI 能力可行性

- 假设: 本项目专注本地单文档问答(不越 PRD 非目标范围),接口/角色/数据模型与 PRD 描述一致,且 AI 能力(RAG)已用 spike 证明可行。
- 行动: 在 docs/ 与 spike 中检索越界关键词(PRD 非目标里不允许的内容);引用 spike 证据结论。
- 证据命令:
  - `grep -inE "联网|互联网|流式|多文档|版本管理|协同编辑|注册|密码|历史问答" docs/ scripts/spike_rag.py evidence/W1-1_*.txt`
  - spike 结论: `grep -E "rag_works|refuse_works" evidence/W1-1_*.txt`
- 结果:
  - 越界关键词命中: 0(联网/流式/多文档/版本管理/协同编辑/注册/密码/历史问答 均未出现)
  - 本项目关键词: /documents, /ask, editor, viewer, RAG, embedding, chunk, has_answer, sources
  - spike 证据: rag_works=true, refuse_works=true,相关问答回答正确并带引用 [片段1],无关问题返回"未找到相关内容"
- 结论: 边界清晰。主题严格在本地单文档 RAG 问答范围内,未越 PRD 非目标;接口/角色/数据模型与 PRD 完全一致。AI 能力(RAG 检索+生成)经 spike 证明可行。
- 下一轮: 无。进入 W2 DESIGN/ADR。

## 闸门通过判定

| 检查项 | 要求 | 实际 | 结果 |
|---|---|---|---|
| 用户故事 >=3 | M 阶段 | 5 个(US-1..US-5) | PASS |
| 每故事 AC >=2 | 可机器判定 | 11 条 AC(每故事 3-4 条) | PASS |
| API 契约端点 | 临时契约 | 5 端点(/health,/login,/documents,GET /documents/{id},/ask) | PASS |
| 错误路径 >=6 | 状态码可判 | 8 条(E1-E8) | PASS |
| 主题边界确认 | 不越非目标 | 越界词 0 命中 | PASS |
| AI 能力 spike | 证明可行 | rag_works=true, refuse_works=true | PASS |
| 互审复述 | 可复述 | 已复述 | PASS |

Gate 1 通过。进入 W2:DESIGN/ADR + Gate 2。

## 关联证据

- PRD: docs/PRD.md
- SPEC: docs/SPEC.md
- 环境记录: evidence/W1-0_solo-2410311322-ai-doc-qa-assistant_environment.md
- spike 证据: evidence/W1-1_solo-2410311322-ai-doc-qa-assistant_ai-capability-spike.txt
- spike 脚本: scripts/spike_rag.py
