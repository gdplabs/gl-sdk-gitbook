---
icon: arrow-progress
---

Use this checklist whenever you bump GL AIP or deploy a new version of
the platform.

> **Success**
>
> **When to use this guide:** Plan upgrades, communicate timelines, or document migrations between AIP releases.
>
> **Who benefits:** Release managers, platform engineers, and PMs coordinating customer rollouts.

For the latest release notes and migration deltas, follow your GL AIP platform
release channel. For runnable implementation examples during migrations, use the
[GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip).

______________________________________________________________________

## Quick Checklist

1. **Review release notes** – capture breaking changes or behavioural updates.
1. **Export state** – back up agents, tools, and MCP configs as JSON/YAML if you
   manage them manually.
1. **Update the SDK/CLI** – on each machine or runner execute `aip update`
   (use `--check-only` to verify availability or `--force` to reinstall).
1. **Smoke test**
   - `aip status`
   - representative `aip agents run` / `aip tools get` commands
   - `client.ping()` from a Python shell
1. **Deploy backend changes** (if applicable) – pull the corresponding AIP
   release and restart services.
1. **Verify MCP and tool integrations** – run one workflow that exercises each
   connector you depend on.
1. **Communicate** – note the versions installed and any follow-up tasks (e.g.,
   feature flag toggles, configuration updates).

______________________________________________________________________

## Tips

- Keep a copy of exported agent/tool JSON in version control; it simplifies
  rollback and lets you diff changes across upgrades.
- Automate `aip update` via CI jobs so runners stay in sync with PyPI releases.
- When the REST API introduces new endpoints or payloads, the
  [REST API Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/README)
  is updated automatically and should be consulted for schema details.

Future breaking changes will re-use this page—add concise “Before / After” code
snippets when they land so the checklist stays actionable.

## Related playbooks

- [Configuration management guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) — Export/import workflows for pre- and post-upgrade backups.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — Schedule `aip update` checks and regression runs.
- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — Validate run history and streaming behaviour after upgrades.
- [Security & privacy](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/security-and-privacy) — Confirm PII mappings and token scopes did not regress.
