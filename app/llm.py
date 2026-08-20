"""AI 调用出口:LLMClient 协议 + Ollama 实现 + Fake 测试实现。

设计: 真实模型只在 OllamaLLMClient;测试用 FakeLLMClient,不依赖 Ollama。
"""
from typing import Protocol
import hashlib

import numpy as np

from . import config


class LLMClient(Protocol):
    def embed(self, texts):
        ...

    def generate(self, prompt):
        ...


class OllamaLLMClient:
    def __init__(self, host=None):
        import ollama
        self._c = ollama.Client(host=host or config.OLLAMA_HOST)

    def embed(self, texts):
        r = self._c.embed(model=config.EMBED_MODEL, input=texts)
        return r["embeddings"]

    def generate(self, prompt):
        r = self._c.generate(
            model=config.GEN_MODEL, prompt=prompt, stream=False,
            options={"num_ctx": 4096},
        )
        return r["response"].strip()


class FakeLLMClient:
    """确定性测试客户端:embedding 用 sha256 派生,生成按关键词返回固定文案。"""

    def embed(self, texts):
        out = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            vec = np.array([(b - 128) / 128.0 for b in (h * 48)[:768]], dtype=float)
            out.append(vec.tolist())
        return out

    def generate(self, prompt):
        if "天气" in prompt or "无关" in prompt:
            return "未找到相关内容"
        return "模拟回答(引用 [片段1])"
