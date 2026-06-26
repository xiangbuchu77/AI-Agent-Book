mcp_server = {
    "name": "company-tools",
    "tools": [
        {"name": "search_docs", "description": "搜索企业文档"},
        {"name": "query_crm", "description": "查询客户系统"},
    ],
    "resources": ["docs://policies", "crm://customers"],
}

for tool in mcp_server["tools"]:
    print(f"MCP Tool: {tool['name']} - {tool['description']}")
