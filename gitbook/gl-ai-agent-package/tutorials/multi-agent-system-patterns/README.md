---
icon: arrow-progress
---

Explore runnable templates for orchestrating multiple agents with GL AIP.

> **Success**
>
> **When to use this section:** You need proven coordination patterns before
> customising them for production.
>
> **Audience:** Engineers designing workflows and PMs creating workflows from requirements.

Use these examples to compare architectures (sequential, parallel, router,
hierarchical, aggregator, loop) and understand when to apply each one.

## Prerequisites

- Python 3.11 or 3.12

- [uv](https://docs.astral.sh/uv/) package manager installed

- The public cookbook repository cloned locally:

  ```bash
  git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
  ```

- Environment variables defined in `.env`:

  ```bash
  OPENAI_API_KEY=your-openai-key-here
  ```

## Getting Started

Ready-to-run implementations of these patterns are available in the [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns).

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gl-aip/examples/multi-agent-system-patterns
uv sync
cp .env.example .env  # then edit with your credentials
```

Run any pattern example with uv, for example the sequential workflow:

```bash
uv run sequential/main.py
```

## Orchestration Approaches

These patterns demonstrate two orchestration approaches, each suited for different workflow types:

### gllm-pipeline (Linear Workflows)

Patterns with **linear, non-cyclic workflows** use `gllm-pipeline` for orchestration. gllm-pipeline provides a declarative API with features like:

- **Parallel execution** - Run multiple agents simultaneously
- **Sequential workflows** - Chain agents where output flows to the next
- **Conditional routing** - Direct queries to specialized agents based on logic
- **State management** - Track data flow through the pipeline using Pydantic models

**Patterns using gllm-pipeline:**

- Sequential, Parallel, Router, Aggregator

To use these patterns, install `gllm-pipeline-binary` version 0.4.13:

```bash
uv add gllm-pipeline-binary==0.4.13
```

### Sub-Agent Delegation (Cyclic Workflows)

Patterns with **cyclic workflows or feedback loops** use sub-agent delegation instead. This approach allows parent agents to:

- Make autonomous decisions based on sub-agent responses
- Loop back to previous steps for refinement
- Implement quality checks and conditional branching
- Control iteration limits to prevent infinite loops

**Patterns using sub-agent delegation:**

- Hierarchical (coordinator decides based on sub-agent outputs)
- Loop (optimizer iterates based on executor feedback)

These patterns define sub-agents via the `agents` parameter when creating the coordinator/optimizer agent.

## AgentComponent Wrapper

Patterns using gllm-pipeline (Sequential, Parallel, Router, Aggregator) use the `AgentComponent` wrapper to integrate `glaip_sdk.Agent` with gllm-pipeline. This wrapper is now built into the SDK and can be accessed via the `.to_component()` method.

**Note:** Sub-agent delegation patterns (Hierarchical, Loop) do not use this wrapper - they use the native `agents` parameter instead.

### Usage

```python
from glaip_sdk import Agent

# Create an agent
assistant_agent = Agent(
    name="assistant_agent",
    instruction="Be helpful",
    model="openai/gpt-5-mini"
)

# Convert it to a pipeline-compatible component
component = assistant_agent.to_component()
```

The `AgentComponent` handles:

- Converting agents to pipeline-compatible components
- Compiling structured pipeline state (context, history) into a cohesive prompt
- Executing agents asynchronously within the pipeline
- Managing runtime configuration overrides

For more details on advanced usage, see the [Agent as Component](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/agent-component) guide.

## Example Structure

Every pattern page shares the same layout so you can skim quickly:

1. Overview of when the pattern works best
1. Demo scenario you can run immediately
1. Diagram showing agent relationships
1. Implementation steps with code snippets
1. Run commands and required environment variables
1. Sample output for validation
1. Notes and related documentation

## Pattern Library

| Pattern                                                                                                              | When to use                                                   | Orchestration | Cookbook Example                                                                                                               |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **[Aggregator](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/aggregator)**     | Combine specialist insights into one briefing.                | gllm-pipeline | [aggregator](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns/aggregator)     |
| **[Hierarchical](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/hierarchical)** | Delegate tasks through supervisors for complex workflows.     | Sub-agent     | [hierarchical](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns/hierarchical) |
| **[Loop](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/loop)**                 | Iterative optimization with feedback loops.                   | Sub-agent     | [loop](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns/loop)                 |
| **[Parallel](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/parallel)**         | Execute independent tasks simultaneously or compare variants. | gllm-pipeline | [parallel](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns/parallel)         |
| **[Router](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/router)**             | Direct each request to the right specialist.                  | gllm-pipeline | [router](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns/router)             |
| **[Sequential](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns/sequential)**     | Refine answers step-by-step with predictable stages.          | gllm-pipeline | [sequential](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns/sequential)     |

## Related Documentation

- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents)
  — Agent lifecycle, nesting, and runtime overrides.
- [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools)
  — Upload Python tools and reuse catalog assets.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting)
  — Run pattern scripts inside CI pipelines or cron jobs.
- [Security & privacy](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/security-and-privacy)
  — Apply memory, PII, and artifact-sharing controls across agents.
