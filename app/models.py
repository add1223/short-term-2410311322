"""数据模型(dataclass)。对应 DESIGN 第 2 节。"""
from dataclasses import dataclass, field


@dataclass
class Chunk:
    doc_id: str
    chunk_index: int
    text: str
    embedding: list = None


@dataclass
class Document:
    doc_id: str
    title: str
    content: str
    chunks: list = field(default_factory=list)
    created_at: str = ""


@dataclass
class Source:
    chunk_index: int
    text: str
    score: float


@dataclass
class Answer:
    doc_id: str
    question: str
    answer: str
    has_answer: bool
    sources: list = field(default_factory=list)
