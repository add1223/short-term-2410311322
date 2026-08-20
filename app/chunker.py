"""文档切块(纯函数,无 IO 无模型)。"""


def chunk_text(text, max_chars=200):
    """按段落切,段落超长再按 max_chars 滑动切;跳过空段落。

    返回 list[str],每段长度 <= max_chars。
    """
    chunks = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        start = 0
        while start < len(para):
            chunks.append(para[start:start + max_chars])
            start += max_chars
    return chunks
