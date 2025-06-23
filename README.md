# 易快报API文档-Markdown格式

- `.\ekuaibao_docs\*`包括了所有易快报官方提供的API文档Markdown格式文件明细
- `.\full-md.txt`为聚合了所有的Markdown文档，可以直接用于RAG
- 用于提供给LLM生成相应的MCP代码，或进行FuncCall
- 在`.\ekuaibao_docs\`下的`llm-full.txt`为[Fast-MCP](https://github.com/jlowin/fastmcp)的全量说明文件

## 更新
- 系统中提供了Playwright脚本，可下载脚本`main.py`后，手动运行进行文档更新
- 注意:需要使用Conda先进行导入yml
