---
icon: location-check
---

# Public Skills

GL Connectors has not created any Agent Skills yet. However, the SDK supports the open [Agent Skills](https://agentskills.io/) standard, and since Skills are simply folders containing a `SKILL.md` file alongside optional scripts and resources, sourcing them from GitHub repositories is straightforward. Getting started with Skills is a matter of **curation, not creation**.

The Agent Skills format was originally developed by [Anthropic](https://www.anthropic.com/), released as an open standard, and has since been adopted by a growing number of agent products including Claude Code, OpenAI Codex, GitHub Copilot, Gemini CLI, Cursor, VS Code, and others. Skills give agents access to procedural knowledge and domain-specific context they can load on demand — think of them as onboarding guides for AI agents.

Below is a curated set of the best repositories and directories for discovering ready-to-use Agent Skills.

***

### Standard & Specification

| Resource                  | Link                                                                             |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Agent Skills Standard** | [agentskills.io](https://agentskills.io/home)                                    |
| **Specification**         | [agentskills.io/specification](https://agentskills.io/specification)             |
| **Spec Repository**       | [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills) |

***

### Official Vendor Skill Repositories

{% hint style="warning" %}
While these repositories are officially curated by the respective companies (Anthropic, Microsoft, etc.), before using, please check the code first as we have not yet validated their security or their behavior.
{% endhint %}

These are first-party Skills maintained by the companies behind major agent platforms and cloud services.

#### Anthropic

The creators of the Agent Skills standard. This repository contains example skills across creative, technical, enterprise, and document workflows — including the popular `docx`, `pdf`, `pptx`, `xlsx`, and `frontend-design` skills.

* **Repository:** [github.com/anthropics/skills](https://github.com/anthropics/skills)
* **68k+ stars** — the reference implementation for the ecosystem.

#### OpenAI

Skills catalog for Codex. Organized into three tiers: `.system` (auto-installed), `.curated` (installable by name), and `.experimental` (community/in-progress).

* **Repository:** [github.com/openai/skills](https://github.com/openai/skills)
* **Docs:** [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)

#### Microsoft

132 skills for Azure SDKs and Microsoft AI Foundry, spanning Python, .NET, TypeScript, and Java. Includes agent persona definitions, prompt templates, and a daily-updated documentation pipeline.

* **Repository:** [github.com/microsoft/skills](https://github.com/microsoft/skills)
* **Skill Explorer:** [microsoft.github.io/skills](https://microsoft.github.io/skills/)
* **Blog Post:** [Context-Driven Development: Agent Skills for Microsoft Foundry and Azure](https://devblogs.microsoft.com/all-things-azure/context-driven-development-agent-skills-for-microsoft-foundry-and-azure/)

#### Vercel

Official skills for React/Next.js best practices, web design guidelines, React Native patterns, and Vercel deployment. Vercel also maintains the `skills` CLI — the primary package manager for the Agent Skills ecosystem.

* **Skills Repository:** [github.com/vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
* **Skills CLI (`npx skills`):** [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills)
* **Skills Directory & Leaderboard:** [skills.sh](https://skills.sh/)

#### GitHub

Community-contributed skills, custom agents, instructions, and prompts for GitHub Copilot.

* **Repository:** [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)
* **Skills Index:** [docs/README.skills.md](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)
* **Copilot Skills Docs:** [docs.github.com — About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

#### Hugging Face

Skills for ML workflows — model training (TRL/SFT/DPO/GRPO), dataset creation, evaluation, experiment tracking, and Hugging Face Hub CLI operations.

* **Repository:** [github.com/huggingface/skills](https://github.com/huggingface/skills)

#### Supabase

PostgreSQL performance optimization guidelines from Supabase, with references across 8 categories prioritized by impact.

* **Repository:** [github.com/supabase/agent-skills](https://github.com/supabase/agent-skills)

#### Google

Skills for the Gemini API/SDK and Google Labs Stitch project (design-to-code workflows, Remotion video generation, shadcn/ui components).

* **Gemini Skills:** [github.com/google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills)
* **Stitch Skills:** [github.com/google-labs-code/stitch-skills](https://github.com/google-labs-code)

***

### OpenClaw Skills

OpenClaw Skills are a superset of Agent Skills. Every OpenClaw skill is a valid Agent Skill, but not every OpenClaw skill will function correctly outside of OpenClaw.

[OpenClaw Skills](https://docs.openclaw.ai/tools/skills) follows the open [Agent Skills](https://agentskills.io/home) standard with runtime automation, environment management, and a community skill registry called [ClawHub](https://clawhub.ai/skills?sort=downloads). For more information regarding Skills, check [.](./ "mention"), and for OpenClaw specifically, it can be accessed in [openclaw-skills.md](references/openclaw-skills.md "mention").

#### ClawHub: The OpenClaw Skill Registry

{% hint style="danger" %}
**ClawHub skills are community-contributed and should be treated as untrusted code.** Always audit a skill's contents before enabling it, especially if it includes executable scripts. Even skills that pass security scans may contain logic that does not behave as expected.
{% endhint %}

[ClawHub](https://clawhub.ai/skills?sort=downloads) is the public, community-driven skill registry for OpenClaw. It provides skill discovery, download tracking, security scanning, and installation tooling.

**Using ClawHub Skills Outside OpenClaw**

Skills from ClawHub can be installed into any Agent Skills-compatible agent. However:

* Skills that rely on `metadata.openclaw` gating (binary/env/config requirements) will not be filtered — the skill will load regardless of whether requirements are met, potentially causing runtime errors.
* Skills that depend on cron, heartbeat, hooks, or environment injection will not have those features available.
* Skills that use `command-dispatch` for slash command routing will not be invocable as commands.

**Recommendation:** When installing ClawHub skills for use with non-OpenClaw agents, prefer skills that contain only standard `SKILL.md` instructions without OpenClaw-specific `metadata.openclaw` fields or automation dependencies.

### Community-Curated "Awesome" Lists

{% hint style="danger" %}
Be very careful when using community-managed skills. They can be useful, but they may hide implementation behind scripts — ensure you check the code before you actually use them!
{% endhint %}

These repositories aggregate skills from across the ecosystem and are excellent starting points for discovery.

#### Awesome Agent Skills (by skillmatic-ai)

The most comprehensive meta-resource — covers platforms, catalogs, tutorials, research papers, tools, and individual skills.

* **Repository:** [github.com/skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills)

#### Awesome Agent Skills (by VoltAgent)

300+ skills from official dev teams and the community. Compatible with Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, and more.

* **Repository:** [github.com/VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)

#### Awesome Agent Skills (by heilcheng)

Curated list covering skills, tools, tutorials, and capabilities across agents.

* **Repository:** [github.com/heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)

#### Awesome Agent Skills (by libukai)

Chinese/English bilingual guide with quick-start instructions, recommended skills, and practical case studies.

* **Repository:** [github.com/libukai/awesome-agent-skills](https://github.com/libukai/awesome-agent-skills)

***

### Discovery Platforms

| Platform      | Description                                                        | Link                                  |
| ------------- | ------------------------------------------------------------------ | ------------------------------------- |
| **skills.sh** | Leaderboard and directory by Vercel. Install via `npx skills add`. | [skills.sh](https://skills.sh/)       |
| **SkillsMP**  | Marketplace for discovering and sharing Agent Skills.              | [skillsmp.com](https://skillsmp.com/) |

***

### How Skills Work

An Agent Skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code (Python, Bash, etc.)
├── references/       # Optional: detailed documentation
└── assets/           # Optional: templates, icons, fonts
```

The `SKILL.md` file uses YAML frontmatter for discovery and Markdown for instructions:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
---
# My Skill

Instructions the agent follows when this skill is activated.
```

Skills use **progressive disclosure** — agents see only the name and description until a task matches, then load the full instructions, and finally access scripts/resources only as needed. This keeps the context window efficient even with many skills installed.

***

### Skills vs MCP

Agent Skills and the Model Context Protocol (MCP) solve different but complementary problems:

|                    | Agent Skills                     | MCP Servers                    |
| ------------------ | -------------------------------- | ------------------------------ |
| **Purpose**        | Procedural knowledge & workflows | Tool execution & data access   |
| **Format**         | Folders of Markdown + scripts    | Running servers exposing tools |
| **Loaded when**    | Agent decides it's relevant      | Agent needs to call a tool     |
| **Think of it as** | An onboarding guide              | An API integration             |

Skills teach agents _how_ to approach a task. MCP gives agents _tools_ to execute it. Many real-world setups use both together.
