This directory collects the definitive reference material for GL AIP: low-level REST endpoints, the Python SDK surface, and the companion CLI. Each page is derived from the live sources in `aip_readme.md` and kept in lockstep with the SDK and CLI implementations, so you can rely on it when building or automating against the platform.

## What's Included

- [**Python SDK Reference**](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk) — client architecture, method signatures, data models, streaming behaviour, and error handling patterns.
- [**CLI Commands Reference**](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands) — every `aip` subcommand with flags, interactive behaviour, import/export flows, and workflow tips.
- [**CLI Slash Command Palette**](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-slash-palette) — interactive palette shortcuts (`/help`, `/agents`, `/details`) with keyboard hints, completions, and agent-context actions.
- [**REST API Reference**](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api) — endpoint catalogue aligned with AIP features (agents, tools, MCP, schedules, language models, accounts, utilities) plus sample payloads.
- [**HITL REST Workflow**](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl) — end-to-end walkthrough of the Human-in-the-Loop approval flow with example payloads and cURL snippets.

## Source of Truth

- The Python reference mirrors the SDK client architecture, models, and utilities.
- CLI coverage reflects the Click command tree and the behaviours validated by the unit tests in the repository.
- REST endpoints, configuration subsystems, and security notes are summarised from `aip_readme.md` and the FastAPI routers that power the platform.

Whenever you ship new SDK features, CLI flags, or backend endpoints, update the corresponding reference page alongside the code change.

## How to Use This Section

- **Developers** — Jump into the Python SDK reference for method signatures and streaming examples, then the REST catalogue when you need to craft custom requests or runtime overrides.
- **Operators** — Lean on the CLI guide for day-to-day management (status checks, imports, scripted runs) and the REST guide for automation or monitoring hooks.
- **Integrators** — Start with the REST API page to understand available capabilities (memory, PII mapping, tool output sharing, MCP overrides), then pick the SDK or CLI depending on your execution environment.

## Keeping Docs Fresh

### 1) When you add or change SDK methods

Update the Python SDK reference and include illustrative snippets so consumers can rely on accurate method signatures and examples.

### 2) When you extend CLI commands

Keep the CLI commands reference in sync with new flags, default behaviours, and examples so operators and automation scripts behave as expected.

### 3) When backend routers change

Refresh the REST API reference so it reflects the latest endpoints, payload shapes, and security guarantees.

Related sections worth bookmarking:

- [Guides](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides) — task-oriented walkthroughs
- [Resources overview](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources) — upgrade notes and release checklists

Keeping these three reference pages aligned with the codebase ensures SDK consumers, CLI users, and API integrators share a single, up-to-date source of truth.
