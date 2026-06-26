def search(docs, query):
    query_terms = set(query.lower().split())
    scored = []
    for doc in docs:
        terms = set(doc.lower().split())
        score = len(query_terms & terms)
        scored.append((score, doc))
    return [doc for score, doc in sorted(scored, reverse=True) if score > 0]


def llm(prompt):
    return "基于资料回答：" + prompt[:120]


def rag(query, docs):
    related_docs = search(docs, query)
    context = "\n".join(related_docs)
    prompt = f"问题：{query}\n资料：{context}"
    return llm(prompt)


docs = [
    "公司 年假 政策 员工 每年 10 天",
    "报销 需要 发票 和 审批",
    "AI Agent 使用 RAG 查询 私有知识",
]
print(rag("公司 年假 政策", docs))
