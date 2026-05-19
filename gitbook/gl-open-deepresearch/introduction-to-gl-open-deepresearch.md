---
icon: lightbulb-on
---

# Introduction to GL Open DeepResearch

GL Open DeepResearch is a **centralized deep research service**. You ask a question, choose how deep or fast you want the research (via a **profile**), and get a sourced, structured answer. The service runs proven research engines for you so you don’t have to host or tune them.

#### What it does

* **Accepts a question** — You send a natural-language query (e.g. “What are the latest developments in quantum computing?”).
* **Runs multi-step research** — The service uses a research engine to decompose the question, gather information from multiple sources, and synthesize an evidence-based answer.
* **Returns a structured result** — You get a final answer plus (depending on the profile and API) thinking steps, tool usage, and sources.
* **Supports different “modes”** — Profiles control speed vs depth (e.g. quick vs comprehensive) and which research engine is used.

#### What it doesn’t do

* **It is not a chat interface** — You send a query and get a result (or stream); there is no multi-turn conversation in the API.
* **It does not replace real-time or live data** — Research is based on the engine’s tools (e.g. search, retrieval); freshness depends on those tools.
* **It does not guarantee a single “correct” answer** — Outputs are synthesized from available sources and can vary by run and profile.

