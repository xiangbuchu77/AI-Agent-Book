import json

server = {
    "name": "knowledge-base",
    "tools": [{"name": "search_docs", "input_schema": {"query": "string"}}],
    "resources": [{"uri": "kb://policies", "description": "Company policies"}],
}
print(json.dumps(server, ensure_ascii=False, indent=2))
