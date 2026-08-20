import os, sys
import ollama
import numpy as np
host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11435")
c = ollama.Client(host=host)
print("host:", host)
# 1. list
try:
    lst = c.list()
    print("models:", [m.model for m in lst.models])
except Exception as ex:
    print("list FAILED:", type(ex).__name__, str(ex)[:200])
# 2. embed (nomic-embed-text)
try:
    r = c.embed(model="nomic-embed-text", input=["hello world", "TDD red green"])
    e = np.array(r["embeddings"])
    print("nomic-embed-text OK, shape:", e.shape, "dim:", e.shape[1])
except Exception as ex:
    print("embed FAILED:", type(ex).__name__, str(ex)[:200])
    sys.exit(1)
# 3. generate (qwen3.5:4b) - 短prompt 快速验证
try:
    r = c.generate(model="qwen3.5:4b", prompt="用一个词回答:测试驱动开发的颜色顺序是?", stream=False, options={"num_ctx":2048})
    print("qwen3.5:4b generate OK, answer:", r["response"].strip()[:100])
except Exception as ex:
    print("generate FAILED:", type(ex).__name__, str(ex)[:200])
    sys.exit(1)
print("=== ALL CHECKS PASSED ===")
