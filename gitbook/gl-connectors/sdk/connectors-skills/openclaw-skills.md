---
icon: lobster
---

# OpenClaw Skills

[OpenClaw Skills](https://docs.openclaw.ai/tools/skills) follows the open [Agent Skills](https://agentskills.io/home) standard with runtime automation, environment management, and a community skill registry called [ClawHub](https://clawhub.ai/skills?sort=downloads). For more information regarding Skills, check [.](./ "mention").

At the **installation level**, OpenClaw skills and Agent Skills are identical: both are folders containing a `SKILL.md` file with YAML frontmatter and Markdown instructions. Any tool that can install Agent Skills can install OpenClaw skills.

At the **runtime level**, OpenClaw adds features that only OpenClaw-compatible agents understand: cron scheduling, heartbeat monitoring, hooks, environment injection, gating rules, and multi-agent skill scoping. **These features are not part of the Agent Skills standard and are currently not supported by non-OpenClaw agents.**

{% hint style="info" %}
**In short:** OpenClaw Skills are a superset of Agent Skills. Every OpenClaw skill is a valid Agent Skill, but not every OpenClaw skill will function correctly outside of OpenClaw.
{% endhint %}

***

### OpenClaw Skills: The Extension

OpenClaw skills build on top of the Agent Skills standard. The `SKILL.md` file remains the core, but OpenClaw introduces additional frontmatter fields, a configuration system, and runtime automation features.

#### Extended Frontmatter Fields

Beyond the standard Agent Skills fields, OpenClaw recognizes these additional frontmatter keys:

| Field                      | Default | Description                                                        |
| -------------------------- | ------- | ------------------------------------------------------------------ |
| `homepage`                 | -       | URL displayed in the OpenClaw macOS Skills UI.                     |
| `user-invocable`           | `true`  | Expose the skill as a user-invocable slash command.                |
| `disable-model-invocation` | `false` | Exclude the skill from the model's system prompt.                  |
| `command-dispatch`         | -       | Direct dispatch mode (e.g., `tool`).                               |
| `command-tool`             | -       | Which tool to invoke when dispatched.                              |
| `command-arg-mode`         | `raw`   | How arguments are forwarded to the tool.                           |
| `metadata.openclaw`        | -       | OpenClaw-specific gating, requirements, and presentation metadata. |

#### Metadata Gating (`metadata.openclaw`)

The `metadata.openclaw` object controls **load-time skill eligibility**. If requirements are not met, the skill is silently excluded from the agent's prompt.

```yaml
metadata: {"openclaw": {"requires": {"bins": ["uv", "git"], "env": ["GEMINI_API_KEY"]}, "primaryEnv": "GEMINI_API_KEY", "os": "darwin", "emoji": "star"}}
```

> **Note:** Due to parser limitations, `metadata` must be written as a **single-line JSON object** in OpenClaw `SKILL.md` files.

| Gating Field       | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `requires.bins`    | Binaries that must exist on PATH (all required).                   |
| `requires.anyBins` | At least one of these binaries must exist.                         |
| `requires.env`     | Environment variables that must be set.                            |
| `requires.config`  | OpenClaw config paths that must be truthy.                         |
| `primaryEnv`       | Associated environment variable (used by `apiKey` config).         |
| `os`               | Restrict to `darwin`, `linux`, or `win32`.                         |
| `emoji`            | Icon for the macOS UI.                                             |
| `always`           | Set to `true` to bypass all gating checks.                         |
| `install`          | Array of installer specs (`brew`, `node`, `go`, `uv`, `download`). |

***

### Comparison: Agent Skills vs. OpenClaw Skills

#### Format and Installation

| Aspect                   | Agent Skills                                            | OpenClaw Skills                                       |
| ------------------------ | ------------------------------------------------------- | ----------------------------------------------------- |
| **Core file**            | `SKILL.md` with YAML frontmatter                        | `SKILL.md` with YAML frontmatter                      |
| **Directory structure**  | Folder with `SKILL.md` + optional subdirectories        | Identical                                             |
| **Required frontmatter** | `name`, `description`                                   | `name`, `description`                                 |
| **Optional frontmatter** | `license`, `compatibility`, `metadata`, `allowed-tools` | All standard fields + OpenClaw extensions             |
| **Installation**         | Copy folder to skills directory                         | Identical (also via `clawhub install`)                |
| **Validation**           | `SKILL.md` exists and is non-empty                      | Identical base validation                             |
| **Cross-compatible**     | Yes, by definition                                      | Yes at install time; runtime depends on features used |

#### Runtime Features

| Feature                                            | Agent Skills    | OpenClaw Skills          |
| -------------------------------------------------- | --------------- | ------------------------ |
| **Skill activation via description matching**      | Yes             | Yes                      |
| **Progressive disclosure**                         | Yes             | Yes                      |
| **Metadata gating (bins, env, OS)**                | No              | Yes                      |
| **Environment injection (per-run)**                | No              | Yes                      |
| **Cron scheduling**                                | No              | Yes                      |
| **Heartbeat monitoring**                           | No              | Yes                      |
| **Hooks (event-driven automation)**                | No              | Yes                      |
| **Command dispatch (slash commands)**              | No              | Yes                      |
| **Per-skill configuration (`openclaw.json`)**      | No              | Yes                      |
| **Multi-tier loading (workspace/managed/bundled)** | Agent-dependent | Yes (defined precedence) |
| **Plugin skill bundling**                          | No              | Yes                      |
| **Remote macOS node support**                      | No              | Yes                      |
| **Security scan integration**                      | No              | Yes (via ClawHub)        |

#### Automation: Cron vs. Heartbeat

OpenClaw provides two complementary scheduling mechanisms. Neither exists in the base Agent Skills standard.

| Aspect             | Cron                                           | Heartbeat                                                |
| ------------------ | ---------------------------------------------- | -------------------------------------------------------- |
| **Purpose**        | Run tasks at precise times                     | Periodic monitoring within main session                  |
| **Timing**         | Exact (cron expressions, one-shot, intervals)  | Approximate (drifts with queue load)                     |
| **Session**        | Main or isolated                               | Always main session                                      |
| **Context**        | None (isolated) or full (main)                 | Full conversational history                              |
| **Batching**       | One job per run                                | Multiple checks per turn                                 |
| **Model override** | Yes (per-job)                                  | No (uses session model)                                  |
| **Best for**       | Precise schedules, standalone tasks, reminders | Monitoring, context-aware checks, cost-efficient polling |

Reference: [Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs) | [Cron vs. Heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat)

#### Hooks

OpenClaw [hooks](https://docs.openclaw.ai/automation/hooks) are event-driven scripts that execute when specific events occur (commands, session lifecycle, messages, gateway startup). Hooks are defined in `HOOK.md` files with a `handler.ts` implementation and are discovered from workspace, managed, and bundled directories.

Hooks are entirely an OpenClaw concept and have no equivalent in the Agent Skills standard.

***

### Configuration (`openclaw.json`)

OpenClaw skills can be configured per-user via `~/.openclaw/openclaw.json`. This allows enabling/disabling skills, injecting environment variables, and managing API keys without modifying the skill itself.

```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "MY_API_KEY" },
        "env": { "MY_API_KEY": "sk-..." }
      }
    },
    "allowBundled": ["skill-a", "skill-b"]
  }
}
```

Reference: [Skills Configuration](https://docs.openclaw.ai/tools/skills-config)

This configuration system is specific to OpenClaw. Standard Agent Skills have no equivalent centralized configuration mechanism.

***

### ClawHub: The OpenClaw Skill Registry

{% hint style="danger" %}
**ClawHub skills are community-contributed and should be treated as untrusted code.** Always audit a skill's contents before enabling it, especially if it includes executable scripts. Even skills that pass security scans may contain logic that does not behave as expected.

Our library logs a UGC warning every time a skill is installed from ClawHub, regardless of scan results.
{% endhint %}

[ClawHub](https://clawhub.ai/skills?sort=downloads) is the public, community-driven skill registry for OpenClaw. It provides skill discovery, download tracking, security scanning, and installation tooling.

#### Key Characteristics

* **User-generated content (UGC)**: Anyone can publish skills to ClawHub.
* **Security scanning**: Skills are scanned for malware and suspicious content. Results are available via the API.
* **Sorting and discovery**: Skills can be browsed by downloads, installs, stars, recency, and name.
* **Installation**: `clawhub install <slug>` or programmatically via this library's `ClawHubSource`.

#### Using ClawHub Skills Outside OpenClaw

Skills from ClawHub can be installed into any Agent Skills-compatible agent. However:

* Skills that rely on `metadata.openclaw` gating (binary/env/config requirements) will not be filtered — the skill will load regardless of whether requirements are met, potentially causing runtime errors.
* Skills that depend on cron, heartbeat, hooks, or environment injection will not have those features available.
* Skills that use `command-dispatch` for slash command routing will not be invocable as commands.

**Recommendation:** When installing ClawHub skills for use with non-OpenClaw agents, prefer skills that contain only standard `SKILL.md` instructions without OpenClaw-specific `metadata.openclaw` fields or automation dependencies.

***

### How This Library Handles Both Standards

The GL Connectors Tools supports installing skills from both GitHub (Agent Skills) and ClawHub (OpenClaw Skills) through a unified interface:

```python
from gl_connectors_tools.skills import SkillFactory

# Install a standard Agent Skill from GitHub
github_paths = await SkillFactory.from_github(
    "owner/repo",
    ["/path/to/skills"],
    directory="my-skill",
)

# Install an OpenClaw skill from ClawHub
clawhub_paths = await SkillFactory.from_clawhub(
    "skill-slug",
    ["/path/to/skills"],
)

# Batch installation (parallel, mixed sources)
result = await SkillFactory.create_multiple(
    SkillFactory.from_github("owner/repo", destinations, directory="skill-a"),
    SkillFactory.from_clawhub("skill-b", destinations),
)
```

The tool's responsibility ends at installation. It downloads, validates (`SKILL.md` exists and is non-empty), and copies skill folders. It does **not**:

* Parse or validate OpenClaw-specific frontmatter
* Execute cron, heartbeat, or hook logic
* Inject environment variables
* Evaluate gating rules

These are the consuming application's responsibility.

***

### Summary

|                         | Agent Skills                                                | OpenClaw Skills                                                                  |
| ----------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **What it is**          | Open standard for portable AI agent skills                  | Extension of Agent Skills with runtime automation                                |
| **Core format**         | `SKILL.md` with YAML frontmatter + Markdown                 | Same                                                                             |
| **Unique features**     | None beyond the base spec                                   | Cron, heartbeat, hooks, env injection, gating, config, command dispatch          |
| **Registry**            | GitHub (or any file host)                                   | ClawHub (community UGC registry)                                                 |
| **Agent support**       | 30+ agents (Claude Code, Cursor, Copilot, Gemini CLI, etc.) | OpenClaw-compatible agents only (for extended features)                          |
| **Portability**         | Universal                                                   | Base features portable; extended features require OpenClaw                       |
| **GL Connectors Tools** | Full install support via `GitHubSource`                     | Full install support via `ClawHubSource` (with security scanning + UGC warnings) |

***

### References

* [Agent Skills Specification](https://agentskills.io/specification) - The complete format specification
* [Agent Skills Overview](https://agentskills.io/home) - What Agent Skills are and who supports them
* [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) - OpenClaw's skill system
* [OpenClaw Skills Configuration](https://docs.openclaw.ai/tools/skills-config) - Per-skill configuration via `openclaw.json`
* [OpenClaw Hooks](https://docs.openclaw.ai/automation/hooks) - Event-driven automation
* [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs) - Scheduled task execution
* [OpenClaw Cron vs. Heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat) - When to use each scheduling mechanism
* [ClawHub Skills Registry](https://clawhub.ai/skills?sort=downloads) - Community skill marketplace (UGC)
* [Example Agent Skills](https://github.com/anthropics/skills) - Official example skills on GitHub
* [Agent Skills Reference Library](https://github.com/agentskills/agentskills/tree/main/skills-ref) - Validation tooling
