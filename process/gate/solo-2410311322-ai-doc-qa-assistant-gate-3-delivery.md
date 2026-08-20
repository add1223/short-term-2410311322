# Gate 3 Delivery - solo-2410311322-ai-doc-qa-assistant

> 闸门目标: 审计交付完整性。本地检查通过、UAT 覆盖主路径+>=2 错误路径、密钥扫描无凭据、README 可独立启动、架构决策可解释。
> 方法: Loop Engineering,每轮 假设 -> 行动 -> 证据命令 -> 结果 -> 结论 -> 下一轮。

## Loop Engineering Round 1: 本地检查通过 + UAT 覆盖

- 假设: check.sh 通过(pytest + 语法 + 空白);UAT 真实模型覆盖主路径 + >=2 错误路径。
- 行动: 跑 check.sh;引用 UAT 文档与证据。
- 证据命令:
  - `bash scripts/check.sh`
  - `grep -E "7 PASS|0 FAIL" evidence/W4-1_*uat.txt`
  - `grep -E "主路径|错误路径" process/uat/*final-uat.md`
- 结果:
  - check.sh: "30 passed" + "no whitespace errors" + "local checks passed" exit 0
  - UAT: 7 PASS / 0 FAIL(真实 Ollama nomic-embed-text + qwen3.5:4b)
  - UAT 覆盖: 主路径(health/login/upload/ask 有答)+ 3 条错误路径(无关问题 has_answer=false、viewer 越权 401、不存在 doc 404)
- 结论: 达标。本地检查通过;UAT 真实模型运行,主路径 + 3 条错误路径(>=2)。
- 下一轮: 安全与可启动性。

## Loop Engineering Round 2: 密钥扫描 + README 独立启动 + 架构决策解释

- 假设: 密钥扫描无真实凭据;占位符无残留;README 含完整启动/测试/演示命令;架构决策可解释(被推翻或修正过)。
- 行动: 跑密钥扫描与占位符检查;通读 README 快速开始;引用 ADR-003 作为被修正决策。
- 证据命令:
  - `bash scripts/scan_run.sh`
  - `grep -cE "ollama serve|uvicorn|pytest|uat_run" README.md`
  - `grep -E "top_k 3 -> 5|被推翻|修正" PROCESS.md docs/adr/ADR-003-top-k-5.md`
- 结果:
  - 密钥扫描: rg exit 1(无命中)
  - 占位符检查: rg exit 1(无命中)
  - README: 含 ollama serve/uvicorn/pytest/uat_run 完整命令,4 节(前置依赖/快速开始/测试/演示流程)
  - 架构决策: ADR-003 记录 top_k 3 -> 5 的修正(spike 证明 3 漏召回关键定义片段),PROCESS.md 答辩要点同步
- 结论: 达标。无真实凭据、无未填占位符;README 可让评审者独立启动;架构决策可解释且有证据。
- 下一轮: 无。交付。

## 闸门通过判定

| 检查项 | 要求 | 实际 | 结果 |
|---|---|---|---|
| 本地检查 | check.sh 通过 | 30 passed + no whitespace | PASS |
| UAT 主路径 | 真实模型 | 7 PASS(health/login/upload/ask 有答) | PASS |
| UAT 错误路径 | >=2 | 3 条(无关/越权/不存在) | PASS |
| 密钥扫描 | 无真实凭据 | rg exit 1 无命中 | PASS |
| 占位符 | 无残留 | rg exit 1 无命中 | PASS |
| README 独立启动 | 完整命令 | 4 节启动/测试/演示 | PASS |
| 架构决策可解释 | 被修正过 | ADR-003 top_k 3->5 | PASS |

Gate 3 通过。交付完成(答辩 PPT 按用户要求暂不制作,答辩要点见 PROCESS.md 与 final-report)。

## 关联证据

- UAT 文档: process/uat/solo-2410311322-ai-doc-qa-assistant-final-uat.md
- UAT 原始输出: evidence/W4-1_*uat.txt
- 安全扫描: evidence/W4-2_*secret-scan.txt
- check.sh 证据: evidence/W3-2_*check-sh.txt
- ADR-003: docs/adr/ADR-003-top-k-5.md
- README: README.md