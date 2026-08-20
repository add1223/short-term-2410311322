# AI Doc QA Assistant - solo-2410311322

自选项目:AI 文档问答助手(基于检索增强生成 RAG)。
用户上传文档,系统基于检索增强生成回答;与集中期 arena-lite(对战/ELO/排行榜)主题、接口、角色完全不同。

## 标识

- MSD_GROUP_ID: solo-2410311322
- MSD_PROJECT_ID: ai-doc-qa-assistant
- MSD_DELIVERY_ID: solo-2410311322-ai-doc-qa-assistant

## 快速开始

> 启动/测试/演示命令将在 W1 PRD/SPEC 完成后补齐。评审者应能凭本节独立启动项目。

```bash
# 环境变量
export MSD_GROUP_ID="solo-2410311322"
export MSD_PROJECT_ID="ai-doc-qa-assistant"
export MSD_DELIVERY_ID="${MSD_GROUP_ID}-${MSD_PROJECT_ID}"

# 虚拟环境
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

# 本地检查
scripts/check.sh
```

## 文档索引

- 过程索引: PROCESS.md
- PRD/SPEC/DESIGN: docs/
- Gate 记录: process/gate/
- UAT: process/uat/
- 最终提交: submissions/
