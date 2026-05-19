---
icon: user-hat-tie
---

# Implementing with Agent

This guide demonstrates how to build your own agent that supports Skills using LangChain's DeepAgents.

## Prerequisites

As this guide utilizes a library published in Gen AI Google Cloud Repository, you will need to fulfill all the setup steps required in Gen AI's [prerequisites.md](../../../../gen-ai-sdk/prerequisites.md "mention"). To summarize, you need the following:

* Python 3.11 or higher
* [UV](https://docs.astral.sh/uv/) package manager

{% stepper %}
{% step %}
**Installation**

{% code overflow="wrap" lineNumbers="true" %}
```bash
uv init --bare
uv add langchain-openai deepagents gl-connectors-tools-binary
```
{% endcode %}

{% hint style="warning" %}
**Note:** To use Anthropic models, install `langchain-anthropic` instead of `langchain-openai`.
{% endhint %}
{% endstep %}

{% step %}
**Example Code**

{% hint style="info" %}
The skill we're using is LangChain DeepAgent's skill for LangGraph Documentation. The skill can be found here. You are very much welcome to experiment and try out the skill yourself to check!

[https://github.com/langchain-ai/deepagentsjs/blob/main/examples/skills/langgraph-docs](https://github.com/langchain-ai/deepagentsjs/blob/main/examples/skills/langgraph-docs)
{% endhint %}

Create a `main.py` file with the following content:

{% code title="main.py" lineNumbers="true" %}
```python
import asyncio
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langchain.chat_models import init_chat_model

from gl_connectors_tools.skills import SkillFactory

async def main():
    await SkillFactory.from_github(
        source="https://github.com/langchain-ai/deepagentsjs/blob/main/examples/skills/langgraph-docs",
        destination=[".deepagents/skills"],
    )

    agent = create_deep_agent(
        model=init_chat_model("openai:gpt-5-mini"),
        backend=FilesystemBackend(root_dir=str(Path(__file__).parent.absolute())),
        skills=[".deepagents/skills/"],
        system_prompt="You are a LangGraph documentation assistant. You can use the LangGraph documentation skill to help the user with their questions.",
    )
    result = agent.invoke({
        "messages": [{"role": "user", "content": "What are agent skills and how to create them?"}],
    })
    print(result["messages"][-1].content)

asyncio.run(main())
```
{% endcode %}
{% endstep %}

{% step %}
**Running the Program**

As with before, you can run the program with the following:

```bash
uv run main.py
```
{% endstep %}
{% endstepper %}

## Observing Skill Impact

To see the difference skills make, try commenting out the `skills` parameter (line 19 on `main.py`):

```python
agent = create_deep_agent(
    model=init_chat_model("openai:gpt-5-mini"),
    backend=FilesystemBackend(root_dir=current_dir),
    # skills=[".deepagents/skills/"],
    system_prompt="You are a LangGraph documentation assistant. You can use the LangGraph documentation skill to help the user with their questions.",
)
```

Without the skill, the agent will hallucinate or provide generic responses. With the skill enabled, the agent has access to the actual LangGraph documentation and responds accurately. The following is the example response (your mileage will vary) side-by-side for comparison.

{% columns %}
{% column %}
<details>

<summary>With Skill</summary>

**Agent skills in LangGraph** are modular, reusable code components that encapsulate specialized capabilities, such as domain-specific workflows, integrations with external systems, or complex logic. Skills empower agents to perform advanced tasks beyond simple prompt-response behavior, fostering modularity and reusability.

Let me break down both core concepts and the process of creating agent skills:

***

**What are Skills in LangGraph?**

* **Skills** are self-contained packages containing code, configuration, and documentation that extend agent capabilities.
* They are often stored in `.deepagents/skills/` directories within your project.
* Skills can include:
  * Python scripts (for logic, API integrations, custom reasoning)
  * Workflows, patterns, templates
  * Documentation (`SKILL.md`) describing purpose, usage, and best practices
  * Helper files, configs, etc.
* Skills follow a progressive disclosure pattern: agents discover a skill by name and description, then read `SKILL.md` for detailed use.
* Skills can be shared and reused across different agents and projects, promoting maintainability.

***

**Why Use Skills?**

* **Separation of concerns:** Skills centralize complex logic apart from core agent code.
* **Reusability:** One skill can power multiple agents.
* **Maintainability:** Change or upgrade skill logic without touching the agent’s main workflow.
* **Progressive Disclosure:** Only load code and knowledge when needed—efficient for large projects.

***

**How to Create a Skill**

**1. Create a Skill Directory**

*   Place your skill under `.deepagents/skills/` using a descriptive folder name, for example:

    ```
    /my-project/
    └── .deepagents/
        └── skills/
            └── my-custom-skill/
    ```

**2. Provide a `SKILL.md` File**

* This is the “manifest” for your skill—describe:
  * What the skill does
  * When to use it
  * Configuration required
  * Usage examples
  * Any helper files/scripts

Example `SKILL.md`:

```
# My Custom Skill

## Description
This skill enables agents to interact with the Acme Weather API.

## When to Use
- When user asks for weather forecast, current conditions, etc.

## How to Use
- Read `weather_client.py` for usage.
- Use the `get_weather(city)` function.

## Examples
User: "What's the weather in Paris?"
-> Use this skill to fetch and return the result.

## Files
- weather_client.py: API logic
```

**3. Write Your Logic (e.g., `weather_client.py`)**

* Place reusable functions, classes, or workflows in Python files.
* Use clear interfaces so agent code can call into them easily.

**4. (Optional) Add Helper Files**

* Configuration files
* Data schemas
* API credentials (never hard-coded!)

**5. Use within the Agent**

* The agent discovers and reads available skills using the progressive disclosure pattern.
* At runtime, the agent can load the skill, read `SKILL.md`, and execute code as per the defined workflow.

***

**Example Skill Structure**

```
.deepagents/skills/
└── langchain-weather/
    ├── SKILL.md
    ├── weather_client.py
    └── config.yaml
```

***

**Best Practices**

* Keep skills focused: do one thing well.
* Document usage and interface clearly.
* Separate external dependencies/configs from logic.
* Use consistent structure for easy discovery.

***

**Summary:**\
Skills make agents smarter and more maintainable by letting you plug in new abilities as reusable modules. Create your skill with documentation and code, add it to `.deepagents/skills/`, and agents can invoke it dynamically as needed.

***

Would you like a code example of a simple skill, or guidance on how to load/use a skill from an agent?

</details>
{% endcolumn %}

{% column %}
<details>

<summary>Without Skill</summary>

In LangGraph, **Agent Skills** are modular, reusable units of tool-based logic and state that agents can leverage within a graph. They enable you to encapsulate functionality (tools, chains, memory, retrieval components, etc.) and expose it in a standardized way, so different agents or nodes can use these “skills” interchangeably.

**What Are Agent Skills?**

* **Skills**: Encapsulate a set of tools, chains, or capabilities (e.g., search, summarization, code execution).
* **Reusable**: Define once, use across multiple agents or nodes.
* **Compositional**: Skills can be combined to build more sophisticated agents.

Agent Skills make it easy to share capabilities between nodes or graphs, leading to more maintainable and modular architectures.

***

**How to Create an Agent Skill**

**1. Define Tools or Chains**

First, define the tools (usually functions) you want to expose. Example with LangChain:

```python
from langchain.tools import tool

@tool
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y
```

**2. Create a Skill Object**

LangGraph provides a `Skill` class to wrap your tools. Example:

```python
from langgraph.skills import Skill

# Wrap your tool(s) in a skill
math_skill = Skill([add])
```

You can include any callable (tools, chains, runnable components, even retrievers).

**3. Add the Skill to Your Agent/Node**

When constructing your agent or node, provide the skill as part of its toolset:

```python
from langgraph.graph import StateGraph, END
from langgraph.graph.utils import add_agent_node

# Build graph, then add agent node
graph = StateGraph(...)
add_agent_node(graph, "math_agent", skills=[math_skill])
```

Now, `math_agent` can use any tool inside `math_skill`.

***

**Example: Creating and Registering a Custom Skill**

Here’s a more complete example:

```python
from langchain.tools import tool
from langgraph.skills import Skill
from langgraph.graph import StateGraph

# 1. Define custom tool
@tool
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

# 2. Create the skill
greet_skill = Skill([greet])

# 3. Register skill with agent node
graph = StateGraph(input_type=..., output_type=...)
graph.add_node("greeter", skills=[greet_skill])
```

***

**Why Use Skills?**

* DRY code: Define and update logic in one place.
* Share skills across many nodes or agents.
* Simplifies agent composition for large or complex graphs.

***

**References:**

* [LangGraph Skills Documentation](https://langgraph.readthedocs.io/en/latest/concepts/skills/)
* [Example: Creating and Registering a Skill](https://langgraph.readthedocs.io/en/latest/concepts/skills/#creating-skills)

If you want a hands-on code sample or to see how skills can expose retrievers, memory, or other complex components, let me know!

</details>
{% endcolumn %}
{% endcolumns %}

As you can see, the response **with** the Skill correctly captures the skill's essence and the requirements needed. The one **without** hallucinates quite heavily. This perfectly demonstrates what skill can do to assist LLMs as they provide not only guidance but the capabilities as well.
