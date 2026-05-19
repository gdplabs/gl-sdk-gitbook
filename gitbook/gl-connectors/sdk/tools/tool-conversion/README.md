---
icon: comment-waveform
---

# Tool Conversion

### The Vendor Lock-In Problem

Every agentic framework defines its own tool interface. LangChain tools look different from CrewAI tools, which look different from GLLM tools. The core logic might be identical — call an API, run a query, format a result — but the wrapping is framework-specific.

This creates **vendor lock-in at the tool level**. Once you've built a library of tools for one framework, migrating to another means rewriting every tool to match the new interface. The cost scales with the number of tools you maintain, and it discourages teams from experimenting with alternative frameworks even when they'd be a better fit.

### BaseTool as the Common Layer

The GL Connectors Tools addresses this with **BaseTool** — a framework-agnostic base class that your tools inherit from. Instead of writing tools _for_ a specific framework, you write them once against BaseTool, and the adapters we provide handle conversion to and from supported frameworks.

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontFamily": "Arial, sans-serif",
    "primaryColor": "#00A0DF",
    "primaryBorderColor": "#00A0DF",
    "primaryTextColor": "#FFFFFF",
  }
}}%%

graph LR
    classDef default fill:#00A0DF,stroke:#00A0DF,color:#FFFFFF,stroke-width:2px;
    classDef emphasis fill:#306FB7,stroke:#306FB7,color:#FFFFFF,stroke-width:2px;

    LC[LangChain Tool]
    GLLM[GLLM Tool]
    BT[BaseTool]
    LCOut[LangChain Agent]
    GLLMOut[GLLM LMRP]

    class LC,GLLM,LCOut,GLLMOut default;
    class BT emphasis;

    LC -->|"from_langchain_tool()"| BT
    GLLM -->|"from_gllm_tool()"| BT
    BT -->|"to_langchain_tool()"| LCOut
    BT -->|"to_gllm_tool()"| GLLMOut
```

This means:

* **Existing tools can be brought in.** If you already have tools written for a supported framework, you can convert them to BaseTool without rewriting the underlying logic.
* **New tools are portable from day one.** Tools authored against BaseTool can be converted to any supported framework through a single adapter call.
* **Migration is incremental.** You don't need to convert everything at once. BaseTool and framework-native tools can coexist in the same project.

### Supported Frameworks

| Framework | Import From                                                                          | Export To               |
| --------- | ------------------------------------------------------------------------------------ | ----------------------- |
| LangChain | <p>✅ <code>from_langchain_tool()</code><br>✅ <code>from_langchain_tools()</code></p> | ✅ `to_langchain_tool()` |
| GLLM      | <p>✅ <code>from_gllm_tool()</code><br>✅ <code>from_gllm_tools()</code></p>           | ✅ `to_gllm_tool()`      |

{% hint style="info" %}
Support for additional frameworks may be added over time. We will keep this list updated as we support more.
{% endhint %}

### Framework-Specific Guides

For step-by-step instructions on converting tools from a specific framework:

* [from-langchain-tools.md](from-langchain-tools.md "mention")
