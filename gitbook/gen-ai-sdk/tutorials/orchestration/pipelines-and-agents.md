---
icon: user-robot-xmarks
---

# Pipelines and Agents

In the GL SDK ecosystem, workflows are orchestrated using two complementary primitives: **Pipelines** and **Agents**. While they often work together in hybrid systems, they serve fundamentally different roles.

In general:

1. **Use Pipelines** when you need predictable, auditable, and repeatable data processing (e.g., "Always search the database, then summarize").
2. **Use Agents** when the workflow depends on complex reasoning or dynamic decision-making (e.g., "Figure out if the user needs a search or a calculation, and do it").

{% hint style="info" %}
This page covers integration patterns between Pipelines and Agents. If you are looking for ways to create an Agent, refer to the [AIP documentation](https://gdplabs.gitbook.io/sdk/gl-aip/guides/agents-guide).
{% endhint %}

## Integration Patterns

Most production systems are **hybrid**. You can integrate Pipelines and Agents in two primary ways:

1. **Pipeline-as-a-Tool**: Giving an Agent the ability to run a Pipeline.
2. **Agent-as-a-Step**: embedding an Agent inside a deterministic Pipeline.

### Pipeline-as-a-Tool

<figure><img src="../../../.gitbook/assets/Copy of Diagram Color Guide (4).png" alt=""><figcaption><p>Pipeline can be integrated into an Agent by having it act as a tool.</p></figcaption></figure>

You can expose a deterministic Pipeline as a callable **Tool**. This allows an AI Agent to "decide" when to invoke a complex workflow (like a RAG search) treating it as a single atomic action. Every `Component` and `Pipeline` in the SDK has an `.as_tool()` method.

```python
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
# 1. Define a deterministic RAG Pipeline
retrieval_step = step(retrieval_component, name="retrieve")
generation_step = step(generation_component, name="generate")
rag_pipeline = Pipeline([retrieval_step, generation_step])
# 2. Convert the Pipeline into a Tool
rag_tool = rag_pipeline.as_tool(
    name="rag_search",
    description="Retrieves relevant context and generates answers for factual queries."
)
# 3. Give the Tool to an Agent
agent = Agent(
    name="rag-agent",
    instruction="Use rag_search for factual questions.",
    tools=[rag_tool],
)
# The Agent decides when to call the pipeline!
print(agent.run("What is LangGraph?"))
```

### Agent-as-a-Step

<figure><img src="../../../.gitbook/assets/Copy of Diagram Color Guide (6).png" alt=""><figcaption><p>An Agent can be integrated as a step in the Pipeline.</p></figcaption></figure>

Conversely, you can wrap an Agent as a Pipeline Step. This allows you to build a structured workflow where specific steps require reasoning or adaptive behavior, but the overall flow remains controlled.

You can wrap an agent using a custom `Component` or `BasePipelineStep`.

```python
from gllm_core.schema import Component, main
from gllm_pipeline.steps import step

# 1. Define an Agent
refiner_agent = Agent(
    name="refiner",
    instruction="Rewrite the user request to be precise and unambiguous."
)

# 2. Wrap Agent in a Component
class AgentComponent(Component):
    def __init__(self, agent):
        self.agent = agent

    @main
    async def run_agent(self, task: str) -> str:
        # Agent.run() returns the final answer string
        return await self.agent.run(task)

# 3. Use in a Pipeline Step
refine_step = step(
    component=AgentComponent(refiner_agent),
    input_map={"task": "user_query"}, # Map pipeline state 'user_query' to agent 'task'
    output_state="refined_query"      # Store result in 'refined_query'
)

# The pipeline executes the agent as just another step
pipeline = refine_step | next_step
```

## When to Use Each

Use the following decision matrix to choose the right primitive for your task.

| Need                                                                           | Component                              | Reason                                                                                                                                     |
| ------------------------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Deterministic, auditable, repeatable data processing**                       | **Pipeline**                           | Explicit graph of steps with predictable state transitions; supports observability, visualization, caching, and replay.                    |
| **Open-ended reasoning with dynamic decision making**                          | **Agent**                              | Agent behavior adapts at runtime based on context and intermediate outcomes; suitable for interactive and exploratory workflows.           |
| **Deterministic workflow with one or more reasoning stages**                   | **Hybrid: Pipeline + Agent-as-Step**   | Pipeline controls execution order, validation, and branching; agent steps handle interpretation, synthesis, and localized decision-making. |
| **Open-ended reasoning with conditional access to deterministic capabilities** | **Hybrid: Agent + Pipeline-as-a-Tool** | Agent controls invocation timing and task routing; pipeline provides a reliable, testable workflow for ETL, RAG, or domain-specific logic. |
