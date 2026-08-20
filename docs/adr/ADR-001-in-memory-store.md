# ADR-001: 使用内存存储而非持久化存储

- 状态: Accepted
- 日期: 2026-08-20

## 背景(Context)

M 阶段需要存储 Document、Chunk(含 768 维 embedding)、Answer。SPEC 非目标明确"不持久化大量历史问答""单机单用户"。

## 候选方案(Options considered)

1. **内存字典 store(dict by doc_id)**: 最简,启动即空,重启丢失。
2. **SQLite 持久化**: 重启不丢,支持查询,但 embedding 以 BLOB 存取增加序列化代码与测试成本。
3. **文件持久化(JSON/pickle 落盘)**: 介于两者之间,需处理并发与原子写。

## 决策(Decision)

选 1 内存字典。理由:
- 非目标已声明可重启丢失、单机单用户,持久化属过度设计。
- 降低 W3 实现与测试复杂度,内存 store 易注入易测。
- L 阶段若需持久化,可替换 store 接口实现而不动上层。

## 后果(Consequences)

- 正面: 实现快、测试简单、无迁移/序列化 bug。
- 负面: 重启丢失文档,需重新上传;多实例不共享。
- 缓解: UAT 文档演示前现传,非生产级。
