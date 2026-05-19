---
icon: book-open
---

Key concepts and terminology used throughout the GL AIP package and its Python
SDK.

## A

**Agent** – A configured AI worker that executes instructions, invokes tools,
processes attached files, and produces responses. Agents are stored per account
and exposed via `/agents`.

**Agent Config** – Structured settings that tune an agent’s behaviour at rest
and runtime (memory backend, tool-output sharing, temperature overrides, etc.).
Persisted under `agent_config` in agent records and extended dynamically via
`runtime_config` during runs.

**Agent Run** – A single execution of an agent triggered via the REST API, SDK,
or CLI. Runs can stream Server-Sent Events (SSE) and optionally attach files.

## B

**GL Connectors** – A curated set of tools packaged by GDP Labs that connect agents to
third-party services (e.g., GitHub, Google Workspace, HR systems). GL Connectors appear with `gl_connector_` prefixes in `/tools` listings.

## C

**CLI (`aip`)** – The command-line interface bundled with the SDK. Provides
commands for managing agents, tools, MCPs, language models, and configuration.
Supports Rich output (default), JSON (`--view json`), and Markdown.

## L

**LangFlow Sync** – A synchronisation endpoint (`POST /agents/langflow/sync`)
that imports LangFlow flows into AIP agents. Exposed via `client.sync_langflow_agents`
and `aip agents sync-langflow`.

## M

**Memory Scope** – Identifier used by the `mem0` backend to persist conversation
state across runs. Controlled through `agent_config.memory` and
`agent_config.agent_id`.

**MCP (Model Context Protocol)** – A protocol allowing agents to interact with
external systems. MCP configurations live under `/mcps` and can be overridden at
runtime via `runtime_config.mcp_configs`.

## P

**PII Mapping** – A dictionary mapping placeholders (e.g., `<EMAIL_1>`) to
actual sensitive values. Passed during runs so secrets remain client-side while
the backend receives fully resolved inputs.

## R

**Runtime Config** – A payload supplied with `POST /agents/{id}/run` that applies
in-memory adjustments for a single execution (tool-specific overrides, MCP
credentials, agent settings per delegate).

## T

**Tool** – A reusable capability (custom or native) that agents can invoke.
Tools are uploaded via `/tools/upload`, and each stores metadata, optional
configuration schemas, and versioning information.

**Tool Config** – Structured parameters stored alongside an agent to customise
a tool’s behaviour (e.g., chart format, API mode). Not to be confused with
`runtime_config.tool_configs`, which applies per run.

## W

**Workspace (Account)** – A logical tenant boundary. API keys, agents, tools,
and schedules are scoped per account. Master keys bypass scoping for operator
workflows.
