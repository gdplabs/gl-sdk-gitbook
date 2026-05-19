---
icon: puzzle-piece-simple
---

In modular AI systems, the **Pipeline** serves as the core orchestration component, managing the execution of modular units called **Components**. While a Pipeline manages structured data flow (retrieval results, metadata, and state), an **Agent** typically operates on natural language instructions.

The `AgentComponent` standardizes this interaction by wrapping a GL Agent into a basic executable unit. It compiles structured pipeline state into a cohesive prompt, allowing Agents to be seamlessly orchestrated alongside other components.

______________________________________________________________________

## The `to_component()` Pattern

To simplify integration, any `Agent` instance can be converted into a reusable `Component` using the built-in `.to_component()` method. This abstraction ensures that the Pipeline can treat the Agent as a uniform executable unit, regardless of its underlying reasoning engine.

```python
from glaip_sdk import Agent

# 1. Initialize your agent
my_agent = Agent(
    name="Researcher",
    instruction="You are a research assistant."
)

# 2. Convert to a Component
# This returns an AgentComponent instance
agent_component = my_agent.to_component()
```

______________________________________________________________________

## Pipeline Integration

Once converted, the Agent becomes a standard building block that can be inserted into any `gllm-pipeline` step. The component automatically handles the mapping between the pipeline's **State** and the agent's **Prompt**.

### Supported Input Mapping

The `AgentComponent` exposes a standardized interface for common orchestration needs:

| Argument         | Type                     | Description                                                                       |
| :--------------- | :----------------------- | :-------------------------------------------------------------------------------- |
| `query`          | `str`                    | The primary user question or instruction.                                         |
| `context`        | `list[Chunk\|str\|dict]` | Background data (e.g., retrieval results). Automatically formats `Chunk` objects. |
| `chat_history`   | `list[Message\|dict]`    | Prior conversation turns. Supports `Message` objects and raw dictionaries.        |
| `runtime_config` | `dict`                   | Execution-time overrides (e.g., planning, tool settings).                         |
| `run_kwargs`     | `dict`                   | Payload for advanced agent execution parameters (e.g., `local: True`).            |

### Advanced Execution Control

The `AgentComponent` supports fine-grained control over execution, allowing you to switch between local and remote runners or pass runtime-specific execution parameters dynamically through the pipeline state.

#### Local Execution

To force a pipeline step to run locally, pass `local: True` inside the `run_kwargs` payload:

```python
# state['params'] = {"local": True}
agent_step = step(
    component=my_agent.to_component(),
    input_state_map={
        "query": "user_query",
        "run_kwargs": "params"
    },
    output_state="answer"
)
```

#### Robust Argument Passthrough

Any key provided in the `run_kwargs` dictionary is passed directly to the underlying `agent.run()` call. This is useful for passing per-step configuration that should not be baked into the agent's static definition.

### Example Workflow

```python
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

# Define the pipeline step
# mapping shared state keys ('user_query', 'docs') to component arguments
agent_step = step(
    component=my_agent.to_component(),
    input_state_map={
        "query": "user_query",
        "context": "retrieved_docs",
        "chat_history": "history"
    },
    output_state="agent_answer"
)

pipeline = Pipeline(steps=[agent_step], state_type=MyState)
```

______________________________________________________________________

## How Prompt Compilation Works

The `AgentComponent` follows the GLLM Core standard of encapsulating business logic. During execution, it automatically transforms heterogeneous inputs into a structured prompt:

1. **Conversation History**: Formats messages into a readable dialogue (e.g., "User: ... \\n Assistant: ...").
1. **Relevant Context**: flattens background data into a clear reference list.
1. **User Query**: Positions the primary instruction at the end of the prompt for optimal model attention.

This ensures that the Agent receives all necessary state in a format optimized for reasoning, without bloating the Pipeline definition with string manipulation logic.

______________________________________________________________________

## Installation

The `AgentComponent` is enabled via the `pipeline` extra:

```bash
pip install glaip-sdk[pipeline]
```
