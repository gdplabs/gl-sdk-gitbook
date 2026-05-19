---
icon: shield-check
---

# Sandbox Filesystem

Run agents in an isolated, ephemeral environment. Perfect for executing untrusted
code, CI/CD pipelines, and security-critical workflows.

{% hint style="success" %}
**Key Benefits:**
- ✅ Isolated execution environment
- ✅ Execute enabled by default (safe in isolation)
- ✅ Automatic cleanup after run
- ✅ Works identically in local and remote execution
{% endhint %}

## Quick Start

```python
from glaip_sdk import Agent
from glaip_sdk.models.filesystem import SandboxConfig

agent = Agent(
    name="secure-runner",
    instruction="Execute code safely in an isolated environment.",
    filesystem=SandboxConfig(),  # Uses defaults
)

result = agent.run("""
Create a Python script that calculates factorial,
run it with the execute tool, and save the result to /workspace/output.txt
""")
```

## When to Use Sandbox

| Use Case | Why Sandbox? |
|----------|--------------|
| **Untrusted Code** | Run arbitrary code without host risk |
| **CI/CD Automation** | Clean environment for each run |
| **Data Processing** | Isolated workspace for sensitive data |
| **Remote Execution** | Same isolation as local |

## Configuration

```python
SandboxConfig(
    base_dir="/workspace",      # Working directory inside sandbox
    timeout_seconds=300,          # Session timeout (default: 300)
    allow_execute=True,          # Enable/disable execute tool
)
```

### Parameters

- **`base_dir`** - Absolute path (e.g., `/workspace`). Auto-created.
- **`timeout_seconds`** - Must be > 0. Session expires after this duration.
- **`allow_execute`** - `True` (default): Agent can run commands. `False`: File operations only.

## Prerequisites

### Local Execution

```bash
# Install with local extras
pip install "glaip-sdk[local]"

# Set sandbox provider API key
export E2B_API_KEY="your-api-key"
```

Get your key from the provider dashboard (e.g., [e2b.dev](https://e2b.dev)).

### Remote Execution

- Platform must support sandbox filesystem backend
- No additional setup needed (platform manages the sandbox)

## Examples

### Run Code Safely

```python
agent = Agent(
    name="code-runner",
    instruction="Execute Python code safely.",
    filesystem=SandboxConfig(base_dir="/workspace"),
)

result = agent.run("""
1. Create a Python script at /workspace/script.py
2. Run it with execute
3. Save output to /workspace/result.txt
""")
```

### File Operations Only

```python
# When you only need file operations, disable execute
agent = Agent(
    name="editor",
    instruction="Edit files.",
    filesystem=SandboxConfig(
        base_dir="/workspace",
        allow_execute=False,  # Extra safety
    ),
)
```

### Long-Running Tasks

```python
# Increase timeout for longer processing
agent = Agent(
    name="processor",
    instruction="Process large dataset.",
    filesystem=SandboxConfig(timeout_seconds=600),  # 10 minutes
)
```

## How It Works

1. **Provisioning** - Isolated environment is provisioned (may take a few seconds on first use)
2. **Execution** - Commands run inside the isolated environment
3. **Cleanup** - Environment is destroyed after run or timeout

{% hint style="warning" %}
**Cold Start:** First sandbox creation may take a few seconds.
Subsequent runs in the same session reuse the environment.
{% endhint %}

## Limitations

- **Ephemeral** - Files lost after run ends
- **Resource Limits** - Subject to provider quotas
- **No Persistence** - Cannot save state between runs

## Troubleshooting

### "ModuleNotFoundError: Sandbox filesystem backend requires..."

**Fix:**
```bash
pip install "glaip-sdk[local]"
```

### "E2B_API_KEY not set" or tests skipped

**Cause:** Sandbox provider API key not configured

**Fix:**
```bash
export E2B_API_KEY="your-api-key"
```

### "base_dir must not contain parent directory traversal"

**Fix:** Use absolute path without `..`:
```python
SandboxConfig(base_dir="/workspace")  # ✅
SandboxConfig(base_dir="/../workspace")  # ❌
```

## Comparison with Local Disk

| Aspect | Local Disk | Sandbox |
|--------|-----------|---------|
| **Execute** | Disabled by default | Enabled by default |
| **Persistence** | Yes | No (ephemeral) |
| **Isolation** | None | Full container |
| **Cleanup** | Manual | Automatic |
| **Best For** | Trusted dev | Untrusted code |

## Related Documentation

- [Agent Filesystem Overview](../agent-filesystem) - All filesystem backends, file tools, and handling large files
- [Sandbox Execution Example](https://github.com/gdplabs/gl-aip-sdk-cookbook/tree/main/examples/filesystem-middleware/07_sandbox_execute.py) - Runnable cookbook example
- [File Processing Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing) - Document ingestion
- [Agents Guide](../agents.md) - Agent configuration
