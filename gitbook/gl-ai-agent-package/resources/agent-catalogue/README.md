---
icon: robot
---

Browse built-in specialist agents and planned agents.

## Available Agents

| Agent Name | Agent Description | Remarks / Notes |
| --- | --- | --- |
| Browser Use Agent | Executes end-to-end web automation: navigate sites, fill forms, click actions, extract content, and summarize results. | Requires Steel account/integration for browser sessions. |
| Code Interpreter Agent | Processes natural-language analysis tasks and direct code snippets in a secure sandbox, including visualization and file outputs. | Requires E2B account/integration. |
| Data Analysis Agent | Performs SQL-backed analysis, generates visualizations, and produces formatted insights. | Requires database configuration. |
| SQL Query Agent | Handles SQL query generation and related data retrieval flows. | Requires database configuration. |
| Pandas Data Processing Agent | Processes and transforms data with pandas for analysis/aggregation. | Internal availability can vary by environment. |
| Table Generation Agent | Generates formatted tables from analysis outputs. | Internal availability can vary by environment. |
| Graph Generation Agent | Produces visual charts from analysis outputs. | Can often be substituted by Code Interpreter Agent. |
| Research Agent | Coordinator agent for research and communication workflows. | Internal availability can vary by environment. |
| Research Compiler Agent | Performs web research and document workflows (for example Google Docs), and can integrate with email delivery flows. | Requires search + connector integrations (for example Serper, Google connectors). |
| Email Assistant Agent | Reads and sends email via connector-backed integrations. | Requires email connector configuration. |
| GitHub Agent | Provides cross-repository insights across PRs, issues, commits, and metadata. | Requires GitHub integration for full access. |
| GitHub Commits Agent | Specialized analysis over repository commit histories. | Requires GitHub integration/key setup. |
| GitHub Contributions Agent | Specialized contributor-activity analysis across repositories. | Requires GitHub integration/key setup. |
| GitHub Issues Agent | Specialized issue analysis across repositories. | Requires GitHub integration/key setup. |
| GitHub Projects Agent | Specialized analysis for GitHub Projects and project items. | Requires GitHub integration/key setup. |
| GitHub PRs Agent | Specialized pull-request analysis across repositories. | Requires GitHub integration/key setup. |
| Calendly Agent | Finds availability and assists meeting setup workflows. | Requires calendar MCP/integration setup. |
| Data Analysis RAG Agent | Combines SQL analysis, charting, and vector retrieval in one flow. | Requires SQL and vector DB connector configuration. |
| Meemo Chat Agent | Answers questions from meeting transcription context. | Internal availability can vary by environment. |
| GitBook Agent | Answers questions grounded on connected GitBook content. | Requires MCP GitBook connection. |
| Report Automation Sync Agent | Syncs report configuration from Google Sheets to deployed agents and schedules. | Internal availability can vary by environment. |
| [SS v2] GitHub Agent | Smart Search connector for GitHub search workflows. | Requires Smart Search integration. |
| [SS v2] Google Calendar Agent | Smart Search connector for Google Calendar search workflows. | Requires Smart Search integration. |
| [SS v2] Google Drive Agent | Smart Search connector for Google Drive search workflows. | Requires Smart Search integration. |
| [SS v2] Google Mail Agent | Smart Search connector for Google Mail search workflows. | Requires Smart Search integration. |
| Release Notes Beautifier Agent | Beautifies release-note draft content from GitHub title + "What's Changed" PR list. | Internal availability can vary by environment. |

## Upcoming Agents

| Agent Name | Agent Description | Remarks / Notes |
| --- | --- | --- |
| Observability Agent | Correlates Sentry traces, ELK logs, and Prometheus metrics for unified root-cause analysis and action recommendations. | On-trial mode |
| ELK Log Retrieval Agent | Retrieves logs from ELK sources. | On-trial mode |
| Sentry Traces Retriever Agent | Retrieves traces from Sentry sources. | On-trial mode |
| Prometheus Metrics Retrieval Agent | Retrieves metrics from Prometheus sources. | On-trial mode |
| Data Crawling Agent | Crawls data from internet sources. | Planned (Q1 2026) |
| RegTech Agent | Extracts/summarizes regulation documents and supports compliance comparison workflows. | Planned (Q1 2026) |
| PR Code Review Agent | Analyzes PR quality/activity metrics (for example merge duration, comment volume, change size). | Planned (Q1 2026) |

## Related Pages

- [Browser Use Agent](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/agent-catalogue/browser-use-agent)
- [Code Interpreter Agent](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/agent-catalogue/code-interpreter-agent)
- [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools)
