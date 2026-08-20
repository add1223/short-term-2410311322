"""配置:全部可由环境变量覆盖(见 DESIGN 第 6 节)。"""
import os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11435")
EMBED_MODEL = os.environ.get("DOCQA_EMBED_MODEL", "nomic-embed-text")
GEN_MODEL = os.environ.get("DOCQA_GEN_MODEL", "qwen3.5:4b")
TOP_K = int(os.environ.get("DOCQA_TOP_K", "5"))
CHUNK_SIZE = int(os.environ.get("DOCQA_CHUNK_SIZE", "200"))
SCORE_THRESHOLD = float(os.environ.get("DOCQA_SCORE_THRESHOLD", "0.6"))
