# W1 Environment Record - solo-2410311322-ai-doc-qa-assistant

## 运行环境

- 宿主: Windows + WSL2 Ubuntu-24.04
- Python: 3.12.3 (/usr/bin/python3)
- 虚拟环境: .venv (ollama 0.6.2, numpy 2.5.2)
- Ollama: 0.32.14

## Ollama 部署方式(关键)

系统服务 ollama.service 以 ollama 用户运行,OLLAMA_MODELS=/usr/share/ollama/.ollama/models(空)。
为避免 sudo 操作,本项目以当前用户身份在 11435 端口运行独立的 ollama serve,指向用户模型目录:

- OLLAMA_HOST=http://127.0.0.1:11435
- OLLAMA_MODELS=/home/add1223/.ollama/models
- 启动命令: OLLAMA_HOST=127.0.0.1:11435 OLLAMA_MODELS=/home/add1223/.ollama/models ollama serve
- blobs=6, models=3

## 模型

| 模型 | 用途 | 维度/参数 |
|---|---|---|
| nomic-embed-text:latest | embedding(检索) | 768 维 |
| qwen3.5:4b | 生成(回答) | thinking 模型,response 字段取最终答案 |
| qwen3.5:9b | 备用(不用于本项目) | - |

注: qwen3.5:4b 不支持 embeddings 接口(返回 501),故 embedding 必须用 nomic-embed-text。
注: qwen3.5:4b 是 thinking 模型,生成时 thinking 内容在 thinking 字段,最终答案在 response 字段。

## spike 结论

- 检索+生成链路可行: 是
- 无相关内容拒绝分支: 是
- 详见 evidence/W1-1_..._ai-capability-spike.txt

## 已知问题(供 W3 实现参考)

- top_k=3 时关键定义片段未被召回,导致严格模型拒绝回答;top_k=5 召回正确。W3 需调参 chunk size 与 top_k。
