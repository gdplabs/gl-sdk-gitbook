---
icon: folder-open
---

# Agent Filesystem

Give agents a managed filesystem during execution so they can read, write, edit,
and search files as part of a run.

Use this guide when you need stateful file operations across a run, large tool
output capture, or multi-agent workflows that share artifacts.

{% hint style="info" %}
For document ingestion (attachments, chunk IDs, artifact retrieval), use the
[File Processing Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing).
This page focuses on runtime filesystem tooling.
{% endhint %}

## Quick Start

```python
from glaip_sdk import Agent

agent = Agent(
    name="file-agent",
    instruction="Use files to plan, draft, and revise outputs.",
    filesystem=True,  # Defaults to Local Disk
)

agent.run("Create /reports/summary.txt and then read it back.")
```

## Backend Options

| Backend | Best For | Execute Default | Persistence |
|---------|----------|-----------------|-------------|
| `filesystem=True` / `LocalDiskConfig` | Local development | **Disabled** ⚠️ | Yes |
| `InMemoryConfig` | Testing, ephemeral work | N/A | No |
| `SandboxConfig` | Untrusted code, isolation | **Enabled** ✅ | No |

{% hint style="danger" %}
**Critical:** `filesystem=True` uses Local Disk with **execute disabled by default** (security).

- To run commands: Use `SandboxConfig()`
- Or explicitly enable: `LocalDiskConfig(base_directory="/tmp/agent_files", allow_execute=True)`
{% endhint %}

## Usage Examples

### Local Disk (Default)

```python
from glaip_sdk import Agent

# Simple default - file operations only, no execute
agent = Agent(name="docs", instruction="...", filesystem=True)

# Or explicit with custom path
from glaip_sdk.models.filesystem import LocalDiskConfig

agent = Agent(
    name="docs",
    instruction="...",
    filesystem=LocalDiskConfig(base_directory="/tmp/agent_files"),
)
```

### In-Memory (Testing)

```python
from glaip_sdk import Agent
from glaip_sdk.models.filesystem import InMemoryConfig

agent = Agent(
    name="test",
    instruction="...",
    filesystem=InMemoryConfig(),  # Ephemeral, no persistence
)
```

### Sandbox (Isolated Execution)

```python
from glaip_sdk import Agent
from glaip_sdk.models.filesystem import SandboxConfig

# Execute enabled by default - safe for running code
agent = Agent(
    name="secure-runner",
    instruction="Run code safely in isolation.",
    filesystem=SandboxConfig(),  # Uses defaults
)

agent.run("""
Create a Python script that calculates factorial,
run it with execute, and save the result.
""")
```

## Image Inputs And `read_image`

Use this when a run includes image files and the agent needs to inspect visual details. Enable vision for image inspection (filesystem is not required — add it only when the agent also needs runtime file tools):

```python
from glaip_sdk import Agent

agent = Agent(
    name="image-reader",
    instruction="Use read_image when visual details in provided images matter.",
    agent_config={"vision": True},
)

response = agent.run(
    "Inspect the provided image and describe the important details.",
    files=["./images/example.png"],
)
```

Images passed through `Agent.run(..., files=[...])` are registered as image attachments for the run. They are not automatically injected into every model prompt. When visual details are needed, the agent calls `read_image` to turn the selected image into text context. By default, `read_image` uses the same model configured for the agent.

Path semantics:
- `files=["./images/example.png"]` is a host path supplied by the SDK caller.
- Filesystem tool paths such as `/images/example.png` are virtual paths relative to the configured filesystem root.
- `read_file` is for text/code files. Use `read_image` for PNG, JPEG/JPG, or WebP images.

When a tool creates a supported image artifact during a run, the agent can inspect it later with `read_image("chart.png", "What trend does this chart show?")`.

## Available File Tools

When filesystem is enabled, agents receive these file operation tools. Vision-enabled agents can also receive `read_image` for registered image attachments and generated image artifacts.

### `read_file` - Read File Contents

**Purpose:** Read all or part of a file.

**When to use:** Inspecting file contents, reading configuration, examining logs, accessing evicted tool outputs.

**Examples:**

```python
# Read entire file (small files only)
read_file(path="/config/app.yaml")

# Read specific lines
read_file(path="/logs/server.log", line_offset=100, limit=50)

# Read by character offset (for large files)
read_file(path="/data/large.json", char_offset=0, max_chars=20000)
```

**Key parameters:**
- `path` - Absolute file path (required)
- `line_offset` + `limit` - Line-based pagination
- `char_offset` + `max_chars` - Character-based pagination

See [Reading Large Files](#reading-large-files--outputs) for pagination details.

### `read_image` - Inspect Images

**Purpose:** Analyze a registered image attachment or generated image artifact and return text context.

**When to use:** A user provides an image file (via `files=[]`) or a tool creates an image artifact, and the agent needs to describe its visual content.

**Examples:**
```python
# Inspect an image by its registered filename
read_image(image="example.png", query="What does this image show?")

# Inspect by artifact filename (from a tool output)
read_image(image="chart.png", query="What trend does this chart show?")
```

**Key parameters:**
- `image` - Registered filename, artifact name, or image attachment ID (required)
- `query` - Optional targeted question about the image

**Behavior:**
- `read_image` is only available when `agent_config={"vision": True}` is set
- It does not have access to raw file bytes — it receives a safe data URL resolved from the attachment registry
- By default it uses the same model configured for the agent

### `write_file` - Create New Files

**Purpose:** Create a new file. Errors if the destination already exists.

**When to use:** Creating new files, writing initial content, saving outputs that don't exist yet.

**Examples:**

```python
# Create a new file
write_file(
    path="/workspace/output.txt",
    content="Hello, this is the result of my analysis."
)

# Write JSON data
write_file(
    path="/data/results.json",
    content='{"status": "success", "count": 42}'
)
```

**Important:** This tool creates new files only. It will error if the file already exists. Use `edit_file` to modify existing files.

### `edit_file` - Modify Existing Files

**Purpose:** Make targeted changes to specific parts of a file using exact string replacement.

**When to use:** Fixing bugs, updating values, refactoring code, making surgical edits without rewriting the whole file.

**Examples:**

```python
# Replace a specific line
edit_file(
    path="/config/app.yaml",
    old_string="debug: false",
    new_string="debug: true"
)

# Update a function
edit_file(
    path="/src/main.py",
    old_string="def calculate(x):\n    return x * 2",
    new_string="def calculate(x):\n    return x * 3"
)
```

**Key points:**
- Uses exact string matching
- Errors if multiple matches found unless `replace_all=True` is provided
- Must match exactly (including whitespace)

### `ls` - List Directory Contents

**Purpose:** List files and directories at a given path.

**When to use:** Exploring directory structure, finding files, checking what exists, understanding the workspace layout.

**Examples:**

```python
# List current directory
ls(path="/workspace")

# List specific directory
ls(path="/workspace/src")

# Check if directory exists (and see its contents)
ls(path="/data/processed")
```

**Output:** Returns a Python list-style string of absolute file paths (e.g., `['/workspace/file1.txt', '/workspace/file2.txt']`).

### `grep` - Search File Contents

**Purpose:** Search for text patterns within files.

**When to use:** Finding specific text across multiple files, searching logs for errors, locating code patterns, filtering large files.

**Examples:**

```python
# Search for "error" in log files
grep(pattern="ERROR", path="/logs")

# Search for a function definition
grep(pattern="def calculate", path="/workspace/src")

# Search in a specific file
grep(pattern="TODO", path="/workspace/notes.txt")
```

**Key points:**
- `pattern` supports basic text matching
- `path` can be a directory (searches recursively) or specific file
- Filesystem tools (`ls`, `grep`, `read_file`, `write_file`, `edit_file`) are excluded from auto-eviction and always return inline

---

All paths must be **absolute** (start with `/`).

## Reading Large Files & Outputs

### Pagination Strategy

When reading files, agents can use **line-based** or **character-based** pagination. Choose one mode per file and never mix them.

#### Line-Based (Default)
Best for normal code/text files with reasonable line lengths:

```
# Read first 100 lines
read_file(path="/src/main.py", line_offset=0, limit=100)

# Read next 100 lines
read_file(path="/src/main.py", line_offset=100, limit=100)
```

**Use case:** Reading source code, logs, configuration files.

#### Character-Based
Best for large/long-line files (JSON, minified JS, CSV, database query results):

```
# Read first 20,000 characters
read_file(path="/data/large.json", char_offset=0, max_chars=20000)

# Read next 20,000 characters
read_file(path="/data/large.json", char_offset=20000, max_chars=20000)
```

**Use case:** GL Connectors SQL MCP results that return as single-line JSON blobs, minified JavaScript bundles, or large CSV files where lines exceed typical limits.

{% hint style="danger" %}
**Never mix modes:** Once you pick a mode for a file, continue with that mode until done.
{% endhint %}

### Tool Output Auto-Eviction

When tool outputs exceed **~80,000 characters**, they're automatically saved to `/tool_outputs/<tool_call_id>.txt`.

**Applies to:** Non-filesystem tools (e.g., `execute` tool output, large API responses)

**Excluded from eviction:** Filesystem tools (`read_file`, `write_file`, `edit_file`, `ls`, `grep`) always return inline

**Why this matters:**
- Large command outputs from `execute` tool
- Big API responses that would overflow context window
- Long-running command results

**What the agent receives:**
- File path where content was saved
- Preview (first 500 chars + last 500 chars)
- Instructions to use `read_file` for full access

**Example scenario:**
```
# Agent runs: execute("find /var -name '*.log' | head -1000")
# Returns 100K characters of output
# Automatically saved to: /tool_outputs/call_abc123.txt
# Agent gets preview + instruction to use read_file with pagination
```

See [Sandbox Filesystem](./sandbox) for detailed sandbox configuration and use cases.

## When to Use Each Backend

### Local Disk
- ✅ Local development and debugging
- ✅ Need persistence across runs
- ✅ Working with existing files
- ⚠️ Execute disabled by default

### In-Memory
- ✅ Unit testing
- ✅ Ephemeral operations
- ❌ No execute capability
- ❌ Files lost after run

### Sandbox
- ✅ Running untrusted code
- ✅ CI/CD automation
- ✅ Security-critical workflows
- ✅ Execute enabled by default

{% hint style="warning" %}
**Remote Mode Note:** In remote execution, `LocalDiskConfig.base_directory` is
platform-managed. Use explicit paths only for local expectations.
{% endhint %}

## Troubleshooting

### "Why can't I run commands with `filesystem=True`?"

**Cause:** Local Disk defaults to `allow_execute=False`.

**Fix:**
```python
# Option 1: Use Sandbox (recommended)
filesystem=SandboxConfig()

# Option 2: Explicitly enable on Local Disk
filesystem=LocalDiskConfig(
    base_directory="/tmp/agent_files",
    allow_execute=True
)
```

### Sandbox Not Available

**Cause:** Missing E2B API key or `glaip-sdk[local]` extras.

**Fix:**
```bash
export E2B_API_KEY="your-key"
pip install "glaip-sdk[local]"
```

## Cookbook

See the [Filesystem Middleware Cookbook](https://github.com/gdplabs/gl-aip-sdk-cookbook/tree/main/examples/filesystem-middleware) for runnable examples of common patterns including file discovery, lifecycle management, data pipelines, codebase analysis, and security auditing.

## Related Documentation

- [Sandbox Filesystem Deep Dive](./sandbox) - Detailed sandbox guide
- [File Processing Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing) - Document ingestion
- [Agents Guide](../agents.md) - Agent configuration
