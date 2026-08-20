"""????:?? + embedding ?? + ???"""
from datetime import datetime, timezone

from . import chunker, config, store
from .models import Chunk, Document

_seq = 0


def upload(title, content, llm):
    """?????????? Document???: ValueError(?) / FileExistsError(??)?"""
    if not title.strip():
        raise ValueError("empty title")
    if not content.strip():
        raise ValueError("empty content")
    if store.has_content(content):
        raise FileExistsError("duplicate content")

    global _seq
    _seq += 1
    doc_id = f"doc-{config.STUDENT_ID}-{_seq:03d}"

    texts = chunker.chunk_text(content, config.CHUNK_SIZE)
    if not texts:
        raise ValueError("content empty after chunking")
    embs = llm.embed(texts)
    chunks = [
        Chunk(doc_id=doc_id, chunk_index=i, text=t, embedding=e)
        for i, (t, e) in enumerate(zip(texts, embs))
    ]
    doc = Document(
        doc_id=doc_id, title=title, content=content, chunks=chunks,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    store.put(doc)
    store.add_content(content)
    return doc


def get(doc_id):
    return store.get(doc_id)
