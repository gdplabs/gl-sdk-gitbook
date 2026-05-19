> This page provides reference for `aip` command-line interface that ships with Python SDK. The CLI exposes same resource coverage as SDK, adds rich terminal renderers and TUI components, and wraps import/export helpers for automation workflows.

{% hint style="info" %}
Need interactive slash palette cheat sheet? Head over to [CLI Slash Command Palette](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-slash-palette).
{% endhint %}

{% hint style="info" %}
**TUI Support**: This CLI includes comprehensive Textual-based TUI components for interactive agent management, configuration, and monitoring. Refer to the TUI foundation spec in the repository for patterns and best practices.
{% endhint %}

{% hint style="info" %}
Multi-account profiles ship in CLI v0.5.0+. Legacy `aip config ...` commands are
deprecated and gated; see the [Legacy Config Commands](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-legacy-config) page for details and migration guidance.
{% endhint %}

## At a glance

- Manage **agents, tools, MCP connections, and language models** without writing code.
- Stream AI agent runs with a live TTY renderer, file attachments, and transcript capture.
- Import/export full resource definitions (JSON or YAML) and sync LangFlow flows into AIP.
- Store multiple credential profiles in `~/.aip/config.yaml` (default + named accounts) and switch output formats (`rich`, `plain`, `json`, `md`).

______________________________________________________________________

## Installation & Quick start

**Install & quick start**

```bash
pipx install glaip-sdk

aip accounts add prod   # interactive credential prompt

aip status              # smoke test connectivity
aip agents list         # browse resources (defaults to active account)
```

{% hint style="info" %}
**Configuration sources** Account selection order is `--account` flag > `active_account` in `~/.aip/config.yaml`. CLI/palette ignore raw credential env vars; Python SDK still honors `AIP_API_URL`/`AIP_API_KEY` for scripts. `AIP_ACCOUNT_FALLBACK` is ignored in the MVP.
{% endhint %}

______________________________________________________________________

## Global options

```bash
aip [GLOBAL OPTIONS] COMMAND [ARGS]...
```

**Global options** (also honored on subcommands)

| Flag              | Description                                                                         |
| ----------------- | ----------------------------------------------------------------------------------- |
| `--api-url TEXT`  | Deprecated: override API endpoint (profiles recommended)                            |
| `--api-key TEXT`  | Deprecated: override API key (profiles recommended)                                 |
| `--account TEXT`  | Target a named account profile for this command (hidden; shown with `--help --all`) |
| `--timeout FLOAT` | Request timeout in seconds (`30` default)                                           |
| `--view`          | Output mode: `rich` (default), `plain`, `json`, `md`                                |
| `--no-tty`        | Disable rich TTY renderer for agent runs                                            |
| `--version`       | Show CLI version                                                                    |
| `--help`          | Show command help                                                                   |

### Output modes

- `--view rich` (default) renders tables/panels using Rich.
- `--view json` emits machine‑friendly JSON.
- `--view md` renders Markdown; `--view plain` prints plain text. All subcommands inherit `--view` from the top-level group.

______________________________________________________________________

## Command Map

| Command            | Description                                                                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `aip status`       | Check connectivity and resource counts                                                                                                          |
| `aip accounts ...` | Manage credential profiles (add/list/show/edit/use/rename/remove)                                                                               |
| `aip configure`    | Legacy configuration wizard (deprecated; gated). Prefer `aip accounts add <name>`                                                               |
| `aip agents ...`   | Agent CRUD, execution, import/export, LangFlow sync                                                                                             |
| `aip tools ...`    | Tool upload/update, metadata, script retrieval                                                                                                  |
| `aip mcps ...`     | MCP configuration management and connection tests                                                                                               |
| `aip models list`  | View available language models                                                                                                                  |
| `aip update`       | Upgrade the installed `glaip-sdk` package                                                                                                       |
| `aip version`      | Show detailed version and environment info                                                                                                      |
| `/transcripts`  | View cached run transcripts and manage local transcript cache                                                                                   |
| `aip config ...`   | Deprecated legacy config helpers (gated); see [Legacy Config Commands](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-legacy-config) |

______________________________________________________________________

## Agents

### List

```bash
aip agents list [OPTIONS]
```

Options:

- `--simple` — skip interactive fuzzy picker; always show a table
- `--type TEXT` — filter by agent type (`config`, `code`, `a2a`, `langflow`)
- `--framework TEXT` — filter by orchestration framework (`langchain`, `langgraph`, `google_adk`)
- `--name TEXT` — filter by partial name (case-insensitive)
- `--version TEXT` — filter by agent version
- `--sync-langflow` — pull latest flows from the configured LangFlow server before listing (honours `LANGFLOW_BASE_URL`/`LANGFLOW_API_KEY`)
- `--view` / `--json` — override output format

When you run the command on an interactive terminal in Rich mode it opens the picker **only** if no filters are supplied and `--simple` is omitted.
Supplying any filter (`--name`, `--type`, `--framework`, `--version`) or switching to the simple/plain/JSON views skips the picker and prints the table immediately.
Selecting an agent in the picker still shows complete metadata and suggested follow-up commands (`run`, `update`, `delete`).

### Get

```bash
aip agents get AGENT_REF [OPTIONS]
```

Options:

- `--select INTEGER` — choose among ambiguous name matches (1-based)
- `--export PATH` — export the full agent definition to `.json` or `.yaml`
- `--view` / `--json`

`AGENT_REF` accepts either an ID or a name. The command resolves ambiguity using fuzzy search or the `--select` flag. Exported files include `agent_config`, tool associations, MCP references, and metadata.

### Create

```bash
aip agents create [OPTIONS]
```

Required flags:

- `--name TEXT`
- `--instruction TEXT`

Optional flags:

- `--model TEXT` — override the base model (omit to use your workspace’s AIP default); pass `language_model_id` inside `--import` payload for catalogue models
- `--tools TOOL_REF` — attach tools by name or ID (multi-use option)
- `--agents AGENT_REF` — attach sub-agents by name or ID (multi-use)
- `--mcps MCP_REF` — attach MCP connections by name or ID (multi-use)
- `--timeout INTEGER` — execution timeout per run (seconds, default `300`)
- `--import PATH` — bootstrap from an exported agent JSON/YAML file (CLI merges CLI flags over imported data)
- `--view` / `--json`

References accept either UUIDs or human-friendly names; ambiguity raises unless unique. Import files can include `metadata`, `agent_config` (memory, tool sharing, PII tags), and runtime defaults. Secret fields should be re-supplied manually post-import.

### Run

```bash
aip agents run AGENT_REF [INPUT] [OPTIONS]
```

Parameters:

- Positional `INPUT` or `--input TEXT` — required prompt if not provided positionally
- `--select INTEGER` — disambiguate name matches
- `--chat-history JSON` — pass prior turns as JSON array (`[{"role": "user", "content": "..."}, ...]`)
- `--file PATH` — attach one or more files (repeatable)
- `--timeout INTEGER` — execution timeout for this run (defaults to agent timeout)
- `--save PATH` — persist transcript and full debug log (supports `.md` or `.json`)
- `--verbose` — deprecated; use the transcript viewer (Ctrl+T) for detailed events
- `--view` / `--json`

Note: top-level `aip --timeout` controls HTTP request timeout; `aip agents run --timeout` controls agent execution timeout. If you need both, pass the request timeout before the subcommand (for example: `aip --timeout 60 agents run <AGENT_REF> "Hello" --timeout 600`).

The command streams SSE responses using the Rich renderer (progress panels, tool call summaries, usage stats) and stores a structured transcript locally. In an interactive terminal with `--view rich` the CLI may open the post-run transcript viewer automatically; you can also press `Ctrl+T` during streaming to toggle transcript mode. Runtime overrides such as `pii_mapping`, `runtime_config`, or per-tool settings are currently only available via SDK/REST — the CLI forwards the fixed set above.

### Update

```bash
aip agents update AGENT_REF [OPTIONS]
```

Options:

- `--name TEXT`
- `--instruction TEXT`
- `--tools TOOL_REF`
- `--agents AGENT_REF`
- `--timeout INTEGER`
- `--import PATH` — merge updates from exported definition (CLI sanitises language model fields automatically)
- `--view` / `--json`

Updating fetches the latest copy, merges defaults, and issues a full PUT. Passing empty lists (e.g. `--tools` omitted) keeps current associations; supplying an empty list in an import file clears them.

### Delete

```bash
aip agents delete AGENT_REF [-y/--yes]
```

Soft-deletes the agent after confirmation (or immediately with `--yes`). Use the SDK/REST to restore soft-deleted agents if needed.

### Sync LangFlow

```bash
aip agents sync-langflow [--base-url URL] [--api-key KEY]
```

Fetches all flows from the configured LangFlow instance and upserts matching agents. Credentials fall back to `LANGFLOW_BASE_URL` / `LANGFLOW_API_KEY` environment variables.

______________________________________________________________________

## Tools

### List

```bash
aip tools list [--type TYPE]
```

- `--type TEXT` — filter by backend tool type (`custom`, `native`, etc.)
- `--view` / `--json`

### Create

```bash
aip tools create [FILE] [OPTIONS]
```

Options:

- Positional `FILE` or `--file PATH` — path to the plugin Python file
- `--name TEXT` — override inferred plugin name (must match the class `name` attribute)
- `--description TEXT`
- `--tags TEXT` — comma-separated tags
- `--import PATH` — import metadata from exported tool definition (merges with CLI flags)
- `--view` / `--json`

If a file is provided, the CLI validates the plugin `name` attribute, checks for duplicates, and uploads via `/tools/upload`. Metadata-only creation is reserved for imports or native catalog entries.

### Get

```bash
aip tools get TOOL_REF [OPTIONS]
```

Options:

- `--select INTEGER` — disambiguate by name
- `--export PATH` — export JSON/YAML definition
- `--view` / `--json`

### Update

```bash
aip tools update TOOL_ID [OPTIONS]
```

Options:

- `--file PATH` — upload new plugin code (only valid for custom tools)
- `--description TEXT` — metadata update (only valid for native tools)
- `--tags TEXT` — comma-separated tags (native tools only)
- `--view` / `--json`

Custom tools support code updates via file upload; native tools support metadata updates. The command enforces these constraints before calling the backend.

### Delete

```bash
aip tools delete TOOL_ID [-y/--yes]
```

Deletes the tool after confirmation. The underlying API performs a soft delete.

### Script

```bash
aip tools script TOOL_ID [--view VIEW]
```

Fetches and prints the stored plugin source (`json` view wraps it under `{"script": ...}`).

______________________________________________________________________

## MCPs (Model Context Protocol)

### List

```bash
aip mcps list
```

Shows stored MCP connections.

### Create

```bash
aip mcps create --name NAME --transport TRANSPORT [OPTIONS]
```

Options:

- `--description TEXT`
- `--config JSON` — inline JSON payload (e.g. `'{"url": "https://..."}'`)
- `--view` / `--json`

### Get

```bash
aip mcps get MCP_REF [--export PATH] [--view VIEW]
```

Resolves names/IDs, optionally exports the definition.

### Tools

```bash
aip mcps tools MCP_REF
```

Lists tools discovered from a stored MCP connection.

### Connect (ad-hoc test)

```bash
aip mcps connect --from-file CONFIG.json
```

Loads JSON config from disk, calls `/mcps/connect`, and prints the result. Uses Rich panels unless `--view json` is active.

### Update

```bash
aip mcps update MCP_REF [OPTIONS]
```

Options:

- `--name TEXT`
- `--description TEXT`
- `--config JSON`
- `--view` / `--json`

The underlying SDK escalates to a full PUT when `name`, `transport`, and `config` are supplied together; the CLI currently exposes `name`, `description`, and `config`, so updates are submitted as partial PATCH requests.

### Delete

```bash
aip mcps delete MCP_REF [-y/--yes]
```

Soft-delete after confirmation.

______________________________________________________________________

## Language Models

```bash
aip models list [--view VIEW]
```

Displays available language models for the current API key, including provider and optional base URL overrides. Use this list to locate `language_model_id` values for agent creation.

______________________________________________________________________

## Configuration & Status

### Interactive setup

1. **Prompt for API URL and key**

The wizard prompts for API URL and key (with masked input).

2. **Persist to disk**

Persists values to `~/.aip/config.yaml` (0600 permissions).

3. **Test the connection**

Tests the connection by listing agents/tools/MCPs.

### Legacy config commands (deprecated)

Use `aip accounts ...` for credentials. If you still need the
legacy `aip config ...` commands (for example, global settings like
`history_default_limit`), see
[Legacy Config Commands](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-legacy-config)
for gated usage and migration guidance.

### Status

```bash
aip status
```

Displays the resolved account + source (`flag`/`account:<name>`/`active_profile:<name>`), masks the key, pings the API, and counts agents/tools/MCPs. Useful for smoke tests in CI.

### Accounts command group

```bash
aip accounts list [--json]
aip accounts show <name> [--json]
aip accounts add <name> [--url URL] [--key [KEY|-]] [--yes]
aip accounts edit <name> [--url URL] [--key [KEY|-]]
aip accounts use <name>
aip accounts rename <current_name> <new_name> [--yes]
aip accounts remove <name> [--yes]
```

- `aip accounts list` renders a table with an active badge; `--json` returns `[{name, api_url, has_key, active}]` (keys are never printed).
- `aip accounts show` prints one profile with masked key and config path; `--json` returns a single object and omits empty metadata fields.
- `aip accounts add` is interactive by default; `--url` + `--key <value>` accepts inline keys, and `--url` + `--key -` (or no value) reads from stdin for scripts. Use `--yes` to overwrite without prompting. Add does not validate connectivity; validation happens when you switch.
- `aip accounts edit` updates an existing profile, prompting for missing fields; `--url` or `--key` can be supplied non‑interactively.
- `aip accounts use` validates connectivity before switching and then sets `active_account` (no offline bypass).
- `aip accounts rename` renames a profile; pass `--yes` to overwrite an existing target name.
- `aip accounts remove` refuses to delete the last profile; if the active profile is removed, the CLI auto-selects `default` (or the next alphabetical) and prints a notice.
- The global `--account <name>` override is available on all commands (hidden; visible via `--help --all`) so you can target a profile without switching it.

______________________________________________________________________

## Transcripts

### Transcripts command group

```bash
/transcripts
```

- `/transcripts` shows cached run history captured from `aip agents run` in the local transcript cache.
- In TTY environments, `/transcripts` opens the local transcript browser so you can pick and inspect a run.
- There is currently no dedicated transcript-cleanup command; remove `~/.config/glaip-sdk/transcripts/` manually when you need to clear local cache data.

______________________________________________________________________

## Import & Export Workflow Tips

- Use `aip agents get <ref> --export agent.yaml` or `aip tools get <ref> --export tool.json` to version configurations alongside code.
- Imported agent files can carry `agent_config` settings for **memory scopes**, **PII mappings**, and **tool output sharing** described in the AIP REST reference. The CLI sanitises language model fields so you can swap between named models and catalogue IDs safely.
- `aip agents run ... --save transcript.md` captures the Rich stream plus final answer; JSON saves include captured debug events for replaying pipelines.
- When scripting, prefer `--view json` to capture machine-friendly responses and avoid control characters from the Rich renderer.

______________________________________________________________________

## Examples

### Run an agent with attachments and save the transcript

**Run an agent with attachments**

```bash
aip agents run agent-123 \
  "Summarise the incident and propose mitigation" \
  --file incident-report.pdf \
  --timeout 900 \
  --save incident-summary.md
```

Replace `agent-123` with the ID you captured from `aip agents list`.

### Import agent configuration from Git

**Import agent from repo**

```bash
# Assuming agent.yaml lives in your repo
aip agents create --import agent.yaml --name "prod-coordinator"
```

### Sync LangFlow and inspect

**Sync LangFlow and inspect (JSON view)**

```bash
export LANGFLOW_BASE_URL=https://flows.example.com
export LANGFLOW_API_KEY=lfk-123

aip agents list --type langflow --sync-langflow --view json | jq '.[] | {id, name, metadata}'
```

______________________________________________________________________

## Related documentation

- [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk) — low‑level control with code
- [REST API Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api) — authoritative endpoint catalogue

> The CLI shares the same backend guarantees as the Python SDK. Consult the REST reference for the full payload schema.
