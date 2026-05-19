---
icon: wrench
---

Tools commands help you manage agent capabilities quickly from terminal.

*Use when:* You need to upload, inspect, or promote tools while iterating on agents.

## Placeholders

- `<TOOL_REF>`: tool ID or unique name.
- `<EXPORT_FILE>`: output file path, for example `tool.json`.

## List and Inspect

```bash
aip tools list
aip tools get <TOOL_REF>
```

## Create and Update

```bash
aip tools create tool.py --name "my-tool"
aip tools update <TOOL_REF> --file tool.py
```

View source script:

```bash
aip tools script <TOOL_REF>
```

## Promotion Workflow

```bash
aip tools get <TOOL_REF> --export <EXPORT_FILE>
aip tools create --import <EXPORT_FILE>
```

Related: [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools).
