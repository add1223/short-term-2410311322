# Gate 2 Design - solo-2410311322-ai-doc-qa-assistant

> 闸门目标: 审计 DESIGN 是否指向 SPEC 每条核心 AC、ADR 是否有真实取舍、测试策略是否呈现红绿、check.sh 是否通过。
> 方法: Loop Engineering,每轮 假设 -> 行动 -> 证据命令 -> 结果 -> 结论 -> 下一轮。

## Loop Engineering Round 1: DESIGN 指向 SPEC 核心 AC + 模块覆盖

- 假设: DESIGN 含 AC 映射表,每条核心 AC 可定位到模块与测试;模块地图覆盖 SPEC 5 端点。
- 行动: 统计 DESIGN 的 AC 映射行数与模块提及;核对 SPEC 端点在 DESIGN 是否有模块承接。
- 证据命令:
  - `grep -c "^| AC-" docs/DESIGN.md`
  - `grep -cE "auth|documents|retrieval|qa|store|llm|chunker|config" docs/DESIGN.md`
  - `grep -E "/health|/login|/documents|/ask" docs/DESIGN.md | head`
- 结果:
  - AC 映射 5 行(AC-1.1/1.3/2.1/2.2/3.1),核心 AC 全部指向模块与测试
  - 8 个模块(auth/documents/retrieval/qa/store/llm/chunker/config)全部在 DESIGN 模块地图出现
  - 端点 /health /login /documents /ask 在 main.py 路由描述中出现,均有模块承接
- 结论: 达标。DESIGN 第 7 节 AC 映射表把核心 AC 追溯到模块与测试;模块地图覆盖全部端点。
- 下一轮: 审计 ADR 真实取舍与红绿证据。

## Loop Engineering Round 2: ADR 真实取舍 + 红绿 + check.sh

- 假设: 3 条 ADR 均含 >=2 候选方案与取舍;红绿证据存在(红 ImportError -> 绿 30 passed);check.sh 通过。
- 行动: 检查 ADR 候选方案数;引用红/绿证据文件与 pytest 输出;引用 check.sh 输出。
- 证据命令:
  - `grep -c "候选方案" docs/adr/*.md`
  - `grep -E "ModuleNotFoundError|3 errors" evidence/W2-1_*red-tests.txt`
  - `grep -E "30 passed" evidence/W3-1_*green-api-tests.txt`
- 结果:
  - ADR-001/002/003 各有 3 候选方案(内存/SQLite/文件; nomic/sentence-transformers/TF-IDF; top_k 3/5/7),取舍真实
  - 红证据: W2-1 "3 errors during collection" + W3-0 "1 error during collection"
  - 绿证据: W3-1 "30 passed in 37.27s"(纯函数 13 + API 17)
  - check.sh: "no whitespace errors" + "local checks passed" exit 0
- 结论: 达标。ADR 有真实取舍;红绿可追溯(W2 红->绿 13, W3 红 dd1e6cb -> 绿 30);check.sh 干净通过。
- 下一轮: 无。进入 W4 UAT + Gate 3。

## 闸门通过判定

| 检查项 | 要求 | 实际 | 结果 |
|---|---|---|---|
| DESIGN 指向 SPEC 核心 AC | AC 映射表 | 5 行映射,核心 AC 全覆盖 | PASS |
| 模块地图 | 覆盖 5 端点 | 8 模块 + 端点路由 | PASS |
| 数据模型/状态机 | 明确 | Document/Chunk/Answer + 文档状态机 | PASS |
| AI 调用边界 | mock 可测 | LLMClient 协议 + OllamaLLMClient + FakeLLMClient | PASS |
| ADR >=2 且有取舍 | 真实候选 | 3 ADR 各 3 候选方案 | PASS |
| 失败路径映射 | E1-E8 + AI 失败 | 10 行(8 SPEC + embed/generate 失败) | PASS |
| 红绿证据 | 可追溯 | W2 红->绿 13, W3 红->绿 30 | PASS |
| check.sh | 通过 | no whitespace errors + local checks passed | PASS |

Gate 2 通过。进入 W3 端点实现(已完成)+ W4 UAT。

## 关联证据

- DESIGN: docs/DESIGN.md
- ADR: docs/adr/ADR-001|002|003
- 红证据: evidence/W2-1_*red-tests.txt, evidence/W3-0_*red-api-tests.txt
- 绿证据: evidence/W2-2_*green-tests.txt, evidence/W3-1_*green-api-tests.txt
- 提交: 34a3d4b(红) -> f2a7048(绿 W2), dd1e6cb(红 W3) -> 绿 W3