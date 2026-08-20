"""AI ????:LLMClient ?? + Ollama ?? + Fake ?????

??: ?????? OllamaLLMClient;??? FakeLLMClient,??? Ollama?
"""
from typing import Protocol
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
    """????????:embedding ????(????->???),?????????????"""

    def embed(self, texts):
        out = []
        for t in texts:
            vec = np.zeros(768, dtype=float)
            for ch in t:
                vec[hash(ch) % 768] += 1.0
            n = np.linalg.norm(vec) + 1e-9
            out.append((vec / n).tolist())
        return out

    def generate(self, prompt):
        if "??" in prompt or "??" in prompt:
            return "???????"
        return "????(?? [??1])"

