---
icon: comments-question
---

# Component Comparisons for AI Agents

## The Four Approaches at a Glance

There are four main ways to give an agent new capabilities. They solve different problems and work at different layers — but they can also complement each other.

**Skills** are folders of instructions and scripts that teach an agent _how_ to do something. They inject knowledge and procedures into the agent's context. Think of them as an onboarding guide for a new team member.

**Function Calling Tools** structured functions the agent can invoke during a conversation. The agent decides when to call them, fills in the parameters, and receives a result. Think of them as buttons on a control panel.

**MCP Servers** (Model Context Protocol) are long-running services that expose tools, resources, and prompts over a standardized protocol. They act as a bridge between the agent and external systems. Think of them as USB ports — a universal way to plug in any data source or service.

* Typically, MCP Servers utilize APIs behind the scenes; because they are the adaptation layer between AI Agents and APIs.

**Pipelines (and REST APIs)** are deterministic flows that take in an input, go through a certain procedure (including branches) that are fixed, and do not need reasoning to execute. See [pipeline.md](../../gen-ai-sdk/tutorials/orchestration/pipeline.md "mention") for GDP Labs' own Pipeline architecture.

* **REST APIs (Application Programming Interfaces)**: Standardized, deterministic code execution. You call an endpoint, you get a known result. No LLM "decision" is involved in the execution itself. Think of this as **hard-wiring**. They cannot interface directly with LLMs, but with the assistance of Pipelines, REST APIs become extraordinarily cost-effective when determinism is guaranteed.

***

## Comparison Table

<table data-full-width="true"><thead><tr><th></th><th>Skills</th><th>Function Calling Tools</th><th>MCP Servers</th><th>REST APIs (and Pipelines)</th></tr></thead><tbody><tr><td><strong>What it is</strong></td><td>A folder with a <code>SKILL.md</code> file (+ optional scripts and references)</td><td>A function schema the agent can call, defined in your code or API request</td><td>A server process that exposes tools, resources, and prompts over a standard protocol</td><td>A server that exposes endpoints that accepts an input, processes it according to the contract and returns the output.</td></tr><tr><td><strong>Where it lives</strong></td><td>Filesystem (local folder or uploaded zip)</td><td>Defined in the API request or application code</td><td>Runs as a separate process (local or remote)</td><td>Runs on a separate server (remote)</td></tr><tr><td><strong>How the agent uses it</strong></td><td>Reads instructions into context, optionally runs bundled scripts</td><td>Generates a structured function call; your code executes it and returns results</td><td>Discovers available tools at runtime and calls them like regular tools</td><td>Used by deterministic flows such as <strong>Pipelines</strong>. At its raw core, LLMs cannot interact with these directly.</td></tr><tr><td><strong>What it's best at</strong></td><td>Procedural knowledge, workflows, formatting rules, domain expertise</td><td>Discrete actions: fetch data, call an API, perform a calculation</td><td>Aggregating multiple shared tools, ensuring no duplication of works.</td><td>To interface with external services. MCP and Tool tends to interact with these.</td></tr><tr><td><strong>Setup complexity</strong></td><td>Very low — just a folder with a markdown file</td><td>Low to medium — define schemas, write handler code</td><td>Medium to high — run a server, configure transport, manage connections</td><td>Typically, no setup needed. You're interacting with pre-existing services.</td></tr><tr><td><strong>Dependencies</strong></td><td>None required by default (scripts optional). Runtime dependencies are client-dependent.</td><td>Your application code handles execution</td><td>Requires an MCP-compatible client and a running server process</td><td>Third party servers.</td></tr><tr><td><strong>Portability</strong></td><td><strong>Format is high</strong> — the SKILL.md spec works across Claude, Copilot, Codex, etc. <strong>Runtime can be low</strong> — skills with scripts assume the client has the right language, version, and dependencies (Python 3.11? Node 20? <code>pip install pandas</code>?). <strong>The spec does not enforce or validate runtime requirements</strong>. An instructions-only skill is fully portable; a script-heavy skill may break silently on a different machine.</td><td>Platform-specific — each API has its own function calling format</td><td>High — any MCP-compatible client can connect to any MCP server</td><td>High — most sources interact with REST APIs (Skills, Function Calling Tools, MCP Servers).</td></tr><tr><td><strong>Execution model</strong></td><td>Agent reads instructions and may run bundled scripts via bash</td><td>Agent proposes a call → your code executes → result returns to agent</td><td>Agent proposes a call → MCP client routes to server → result returns</td><td>Agent interacts with a deterministic pipeline that will call the APIs for them.</td></tr><tr><td><strong>When it runs</strong></td><td>Activated automatically when the agent matches the skill's description</td><td>Called when the agent decides a function is needed</td><td>Called when the agent decides a discovered tool is needed</td><td>Called by anything.</td></tr><tr><td><strong>Open standard?</strong></td><td>Yes — <a href="https://agentskills.io">Agent Skills spec</a></td><td>No — vendor-specific (though conceptually similar across providers)</td><td>Yes — <a href="https://modelcontextprotocol.io">Model Context Protocol</a></td><td>Yes</td></tr></tbody></table>

***

## Decision Framework

<figure><img src="../../.gitbook/assets/Component Comparisons for AI Agents _ Decision Framework (1).png" alt=""><figcaption><p><a href="https://docs.google.com/drawings/d/17ABCiEmMyCVTnka2T2lzEFOYb1GeTiY0Ch10rHFkvrw/edit?usp=sharing">Diagram Link</a></p></figcaption></figure>

#### The Quick Test

Ask yourself these four questions:

1. **Is the flow deterministic and requiring no reasoning?** → **Pipeline and REST API**. You're trying to execute a standardized procedure. You don't need LLMs to deal with this. Just pure pipeline and REST API.
2. **Does the agent need to&#x20;**_**know**_**&#x20;something it doesn't currently know?** → **Skill.** You're adding knowledge — procedures, formats, rules, or expertise.
3. **Does the agent need to&#x20;**_**do**_**&#x20;something it can't currently do?** → **Function Calling Tools** or **MCP Server.** You're adding capability — API calls, data retrieval, external actions.
4. **Does the agent need to know&#x20;**_**how**_**&#x20;to use a tool it already has access to?** → **Skill + Function Calling Tool/MCP.** The tool provides the capability; the skill teaches the workflow around it.

***

### When They Work Together

Skills, Function Calling Tools, REST API and Pipelines, and MCP Servers aren't competing choices — they're layers. The most powerful setups combine them.

#### Example: Analytics Processing

| Layer        | Component             | Role                                                                                                                                                                                                                                 |
| ------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Pipeline** | GL Pipeline           | <p>Orchestrates the flow from:<br>1. Gathering the data from Github<br>2. Process the data into a well-structured format.<br>3. Handles all post-processing and flows to ensure that data can be understood by subsequent steps.</p> |
| **REST API** | Github API            | Retrieves all the necessary data from Github.                                                                                                                                                                                        |
| **Skill**    | `data-analysis` skill | Allows the formatted data to follow the required and requested human-readable format.                                                                                                                                                |

#### Example: Code Review Workflow

| Layer          | Component           | Role                                                                                |
| -------------- | ------------------- | ----------------------------------------------------------------------------------- |
| **MCP Server** | GitHub MCP Server   | Provides access to PRs, diffs, and comments                                         |
| **MCP Server** | Sentry MCP Server   | Provides access to error data and stack traces                                      |
| **Skill**      | `code-review` skill | Teaches the agent your team's review checklist, severity ratings, and comment style |

Without the skill, the agent can read PRs and Sentry data — but it doesn't know your team's standards. Without the MCP servers, the skill has great instructions but no access to the actual code. Together, the agent reviews PRs the way your senior engineers do.

#### Example: Invoice Generator

| Layer     | Component               | Role                                                                                      |
| --------- | ----------------------- | ----------------------------------------------------------------------------------------- |
| **Tool**  | `generate_pdf` function | Creates a PDF from structured data                                                        |
| **Skill** | `invoice-format` skill  | Defines your company's invoice template, required fields, tax rules, and numbering scheme |

The tool handles the mechanics of PDF creation. The skill ensures every invoice follows your company's exact format and business rules.

#### Example: Data Analysis Pipeline

| Layer                   | Component             | Role                                                                                                         |
| ----------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ |
| **MCP Server**          | Database MCP Server   | Provides SQL query access to your data warehouse                                                             |
| **Skill** (with script) | `data-analysis` skill | Includes instructions for your team's analysis methodology, plus Python scripts for statistical calculations |

The MCP server connects to the data. The skill's instructions define what analyses to run and how to interpret results. The skill's scripts handle the actual statistical computations.

***

### Common Pitfalls

| Pitfall                                                 | Problem                                                                                  | Better Approach                                                                                 |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Building an MCP server just to format output            | Over-engineering — MCP is for external connections, not formatting                       | Use a **Skill** with output templates in the instructions                                       |
| Writing a tool for something the agent already knows    | Adding complexity without value — the agent can already write code, summarize text, etc. | Only add tools for capabilities the agent genuinely lacks (external API access, real-time data) |
| Using a skill for live data retrieval                   | Skills are static instructions — they can't fetch real-time data on their own            | Use a **Tool** or **MCP Server** for the data, plus a **Skill** for the workflow                |
| Putting complex business logic in SKILL.md instructions | LLMs can misinterpret nuanced logic; long instructions bloat context                     | Move deterministic logic into a **script** inside the skill's `scripts/` folder                 |
| Building a separate tool for every API endpoint         | Leads to tool sprawl — the agent has too many options and picks the wrong one            | Group related endpoints into an **MCP Server** with well-named tools                            |
| Skipping the skill when you already have MCP/tools      | The agent has access but doesn't know your team's _way_ of using the tools               | Add a **Skill** that documents the workflow and best practices                                  |

***

### Summary: Pick Your Starting Point

| You are...                                                                        | Start with                    | Then consider adding                                                           |
| --------------------------------------------------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------ |
| A non-developer who wants consistent AI output                                    | **Skill** (instructions only) | Nothing — this may be all you need                                             |
| A developer who wants to give customized instructions to handling certain inputs. | **Skill** (with scripts)      | The script can execute certain things perfectly to adhere to the instructions. |
| A developer who wants the agent to call your API                                  | **Tool** (function calling)   | A **Skill** if the workflow around the API is complex                          |
| A team that wants to connect the agent to Slack, GitHub, Jira, etc.               | **MCP Server**                | A **Skill** to teach the agent your team's workflows with those tools          |
| A team building a production agent with multiple data sources                     | **All three**                 | Skills for knowledge, MCP for connections, Tools for custom actions            |

Start with the simplest approach that solves your problem. You can always layer on more later.

***

### Further Reading

* [creating-a-skill](connectors-skills/creating-a-skill/ "mention") — build a skill with just instructions
* [skill-with-scripts.md](connectors-skills/creating-a-skill/skill-with-scripts.md "mention") — add executable code to a skill
* [Agent Skills Specification](https://agentskills.io/) — the open standard
* [Model Context Protocol](https://modelcontextprotocol.io/) — the MCP standard
