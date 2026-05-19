---
icon: comment-dots
---

Use runs and transcripts to debug agent behavior and share reproducible outputs.

*Use when:* You need evidence for prompt quality, tool failures, or regression checks.

## Placeholders

- `<AGENT_REF>`: agent ID or unique name.
- `<RUN_ID>`: run ID from transcripts listing.

## Run and Save Output

```bash
aip agents run <AGENT_REF> "Hello" --save run.md
aip agents run <AGENT_REF> "Hello" --save run.json --view json
```

In `--view rich` mode, the CLI also captures a local transcript and may open the post-run transcript viewer automatically when running in a TTY.

## Transcript Commands

```bash
/transcripts
```

Inside the command palette (run `aip`), press `Ctrl+T` after a run to open the transcript viewer for the most recent execution.

Use `/transcripts` to browse and open local cached runs.

Cache location defaults to `~/.config/glaip-sdk/transcripts/`. Override with `AIP_TRANSCRIPT_CACHE_DIR` when you need a custom path (for example on CI machines).

There is currently no dedicated cleanup command; remove the cache directory manually if you need to clear transcript files.

## Interactive Remote Run Debugging

```bash
aip
```

Inside palette: `/agents` -> select agent -> `/runs` -> open run details.

Related: [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents).
