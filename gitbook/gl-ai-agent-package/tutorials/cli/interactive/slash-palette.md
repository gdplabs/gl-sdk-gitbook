---
icon: terminal
---

Use the slash palette for guided CLI operations with less typing.

*Use when:* You want discoverable commands while debugging or operating agents.

## Start Palette

```bash
aip
```

<figure><img src="../../../resources/ux/agent-workspace-shell.svg" alt=""><figcaption>Agent workspace shell screenshot captured from the Textual TUI flow.</figcaption></figure>

<figure><img src="../../../resources/ux/aip-help.svg" alt=""><figcaption>CLI command screenshot captured from `aip --help`.</figcaption></figure>

## Core Flows

From the palette home screen:

- `/accounts`: manage credential profiles (add/switch).
- `/agents`: pick an agent and enter a focused run prompt.
- `/transcripts`: browse cached local transcripts and open the viewer.

Inside an agent session (after `/agents`):

- `/runs`: browse remote run history for the active agent.
- `/schedules`: manage recurring schedules for the active agent.
- `/prompt`: edit the agent instruction in a TUI.
- `/details`: view the agent export/config.

## Suggested Debug Loop

1. `/agents` -> select target agent.
2. `/runs` -> open latest failed or suspicious run.
3. Inspect tool calls and final output.
4. `/transcripts` -> open the cached transcript viewer when you need detailed local evidence.

Tip: after an agent run, press `Ctrl+T` to open the transcript viewer for the most recent execution.

Reference details: [CLI Slash Palette Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-slash-palette).
