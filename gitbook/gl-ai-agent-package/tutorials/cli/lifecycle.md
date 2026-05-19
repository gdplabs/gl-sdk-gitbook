---
title: CLI Agent Lifecycle
icon: terminal
---

Build, test, and promote one agent end-to-end using only the `aip` CLI.

*When to use:* You want a reproducible terminal workflow for demos, QA validation, or ops handoff without writing Python code.

{% hint style="info" %}
If you are brand new to the CLI, complete [Quick Start (CLI)](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide/cli) first, then return here.
{% endhint %}

## What You Will Do

1. Verify account and connectivity.
2. Create a production-style support triage agent.
3. Run prompts and save transcripts.
4. Iterate instructions with `update`.
5. Export and promote the agent config.
6. Validate the same flow in the slash palette.

## Step 1: Verify Account and Environment

```bash
aip accounts use <ACCOUNT_NAME>
aip status
```

Expected result: status shows valid auth, reachable API, and healthy resource checks.

## Step 2: Create the Agent

```bash
aip agents create \
  --name "support-triage-cli" \
  --instruction "You triage incoming support tickets. Return severity, likely owner, and next action in 3 bullets." \
  --model "openai/gpt-5-mini"
```

Expected result: CLI prints the new agent ID and name. Keep either value for run commands.

## Step 3: Run and Capture a Transcript

```bash
mkdir -p runs
aip agents run support-triage-cli \
  "Customer reports repeated 504 errors on checkout in the last 10 minutes." \
  --save runs/triage-checkout.md
```

Expected result: streamed output in terminal plus a saved transcript at `runs/triage-checkout.md`.

## Step 4: Tighten Behavior with Update

Update the instruction to return strict JSON for downstream automation:

```bash
aip agents update support-triage-cli \
  --instruction "Classify tickets into severity P1-P4 and output valid JSON with keys: severity, owner, next_action, rationale."
```

Re-run to confirm the new format:

```bash
aip agents run support-triage-cli "Payment webhook retries are spiking after deploy." --save runs/triage-webhook.md
```

Expected result: output shape follows the new JSON-oriented instruction.

## Step 5: Export and Promote Configuration

Export the current definition:

```bash
aip agents get support-triage-cli --export support-triage-cli.yaml
```

Create a second environment copy from that file:

```bash
aip agents create --import support-triage-cli.yaml --name support-triage-cli-staging
```

Validate both exist:

```bash
aip agents list
```

Expected result: both `support-triage-cli` and `support-triage-cli-staging` appear in the list.

## Step 6: Validate in Interactive Palette

```bash
aip
```

Then run:

- `/agents` to select `support-triage-cli` and execute a prompt.
- `/runs` to inspect recent executions.

Use the [Slash palette guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/interactive/slash-palette) if you want command discovery screenshots and key bindings.

## Optional Cleanup

```bash
aip agents delete support-triage-cli-staging --yes
```

Keep the main tutorial agent if you want to continue testing export/import and transcript workflows.

## Related Documentation

- [CLI Use Cases](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/use-cases) for compact, task-based command recipes.
- [Agents Commands](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/agents) for full command syntax and flags.
- [CLI Commands Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands) for complete option coverage.
