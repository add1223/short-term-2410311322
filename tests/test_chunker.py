"""chunk_text 纯函数测试(无模型依赖)。"""
from app.chunker import chunk_text


def test_chunk_text_splits_long_paragraph():
    text = "a" * 250  # 250 字, max 200 -> 2 块
    chunks = chunk_text(text, max_chars=200)
    assert len(chunks) == 2
    assert chunks[0] == "a" * 200
    assert chunks[1] == "a" * 50


def test_chunk_text_skips_empty_paragraphs():
    text = "\n\n  \n\nhello\n\n"
    chunks = chunk_text(text, max_chars=200)
    assert chunks == ["hello"]


def test_chunk_text_empty_input():
    assert chunk_text("", max_chars=200) == []


def test_chunk_text_paragraph_boundary():
    text = "first para.\n\nsecond para."
    chunks = chunk_text(text, max_chars=200)
    assert chunks == ["first para.", "second para."]
