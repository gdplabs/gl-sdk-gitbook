---
icon: messages-question
---

Use models commands to discover available language models before assigning them to agents.

*Use when:* You are choosing or validating model IDs for agent updates.

## Commands

```bash
aip models list
aip models list --view json
```

## Expected Result

- Model IDs/providers are visible for the current account.

## Next Step

- Set model on agent config, then validate with `aip agents run <AGENT_REF> "..."`.
- Model selection guidance: [Language models guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/language-models).
