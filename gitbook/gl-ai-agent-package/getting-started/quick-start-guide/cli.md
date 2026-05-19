---
icon: terminal
---

*When to use:* You need zero-code validation, quick demos, or scripted runs that operate from any shell.

{% hint style="info" %}
Looking for CLI pages beyond this quick start (accounts, agents, tools, MCPs, transcripts)? Start at the [CLI section](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli).
{% endhint %}

## Step 1: Install or Upgrade the Package

```bash
pip install --upgrade glaip-sdk
```

Or use `uv tool install glaip-sdk` if you prefer uv.

## Step 2: Configure Credentials

```bash
aip accounts add prod
aip accounts use prod
```

## Step 3: Create and Run Your First Agent

```bash
# Create agent
aip agents create \
  --name "hello-world-agent-123" \
  --instruction "You are a friendly AI assistant."

# Run the agent (use the ID or name shown in the create output)
aip agents run 49874068-f2e7-42b4-878d-ef545db5a110 "Hello! How are you today?"
# or
aip agents run "hello-world-agent-123" "Hello! How are you today?"
```

This creates and runs your first agent using the CLI. The `create` output shows both the agent ID and name—use either in the run command.

### Optional: Run from the Slash Command Palette

Launch the palette and select `/agents` to pick and run your new agent:

```bash
aip
```

Inside the palette, choose `/agents`, select your agent, and provide the prompt inline. See the [CLI Slash Palette](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-slash-palette) reference for screenshots and deeper guidance.

{% hint style="info" %}
Screenshot placeholder: palette home screen with `/` completions open.
{% endhint %}

{% hint style="info" %}
Replace the sample ID or name with the values shown in your `aip agents create` output. If you have multiple agents with similar names, use the full ID to avoid confusion.
{% endhint %}

### Optional Next Steps

- Add a tool with `aip tools create` and `aip agents update --tools ...` (details in the [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools)).
- Attach files during runs with `aip agents run <AGENT_REF> --input "Review" --file report.pdf` and consult the [File processing guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing).
- Reuse context by passing `--chat-history` JSON; see the [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) for examples.
- For prompt/export iteration, jump to the [Configuration management guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) which walks through the full export → edit → import loop.
