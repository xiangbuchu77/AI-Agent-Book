def ecommerce_agent(data):
    rag_context = "行业经验：提升转化率，优化商品标题和主图"
    analysis = f"店铺数据：{data}; 参考：{rag_context}"
    strategy = "建议：优化爆款商品详情页，并针对低转化流量做人群分层。"
    return {"analysis": analysis, "strategy": strategy, "output": "运营报告"}


result = ecommerce_agent("访客上涨，转化率下降")
print(result["strategy"])
