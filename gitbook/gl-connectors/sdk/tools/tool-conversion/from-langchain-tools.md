---
icon: crow
---

# From Langchain Tools

## From LangChain

This guide walks through converting an existing LangChain tool into a GL Connectors Tools SDK BaseTool.

### Prerequisites

* A working project with `gl-connectors-tools` installed (see [quickstart.md](../quickstart.md "mention"))
* An existing LangChain tool you want to convert (or follow along with the example below)

### Converting a LangChain Tool

{% stepper %}
{% step %}
#### LangChain Conversion Code

Here's a simple LangChain tool that adds two numbers:

<pre class="language-python" data-title="add_tool.py" data-line-numbers><code class="lang-python">from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from gl_connectors_tools.adapters import from_langchain_tool

class AddToolInput(BaseModel):
    """Input schema for the AddTool."""

    a: int = Field(description="The first number.")
    b: int = Field(description="The second number.")


class AddTool(BaseTool):
    """Add two numbers together."""

    name: str = "add_tool"
    description: str = "Add two numbers together and return the sum."
    args_schema: type[BaseModel] = AddToolInput

    def _run(self, a: int, b: int) -> str:
        return str(a + b)

<strong>add_base = from_langchain_tool(AddTool())
</strong>print(add_base.run(a=1, b=1))  # Outputs 2
</code></pre>

The important line is **line 22**, where the conversion happens. That's all you need to do to convert a LangChain Tool to a BaseTool!
{% endstep %}

{% step %}
#### Running with Agent

**Additional Prerequisites**

As we will be using AIP's Local Execution, the following pre-requisites need to be fulfilled:

* Python version 3.11 and 3.12 (AIP currently **does not support Python 3.13** for local execution).
* Install AIP with Local Execution as new dependency:

```shellscript
uv add glaip-sdk[local]
```

* An OpenAI API Key, set via environment variable as follows:

```
OPENAI_API_KEY=
```

**Code**

<pre class="language-python" data-title="main.py" data-line-numbers><code class="lang-python">from gl_connectors_tools.adapters.langchain import to_langchain_tools, from_langchain_tool
from glaip_sdk import Agent
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class AddToolInput(BaseModel):
    """Input schema for the AddTool."""

    a: int = Field(description="The first number.")
    b: int = Field(description="The second number.")


class AddTool(BaseTool):
    """Add two numbers together."""

    name: str = "add_tool"
    description: str = "Add two numbers together and return the sum."
    args_schema: type[BaseModel] = AddToolInput

    def _run(self, a: int, b: int) -> str:
        return str(a + b)

<strong>base_tool = from_langchain_tool(AddTool())
</strong><strong>agent = Agent(
</strong><strong>    name="test-agent-with-tools",
</strong><strong>    instruction="You are a helpful assistant.",
</strong><strong>    tools=to_langchain_tools([base_tool]),
</strong><strong>)
</strong><strong>agent.run("what's 222+333?")  # should be 555
</strong>
</code></pre>

You should see the correct output: `555`, and a log that states the tool `add_tool` has been appropriately called.

You may note that **Line 23** converts the tool to Base Tool first, then **Line 27** converts it back to LangChain tool. You're correct! This demonstrates that the conversion goes both-ways, and it's compatible with no functionality loss!
{% endstep %}

{% step %}
**Use with Any Supported Framework**

Once converted, the BaseTool can be exported to any supported framework:

{% code title="main.py" lineNumbers="true" %}
```python
from gl_connectors_tools.adapters import to_gllm_tool, to_langchain_tool

# Use with a GLLM agent
gllm_tool = to_gllm_tool(add_base)

# Or convert back to LangChain
langchain_tool = to_langchain_tool(add_base)
```
{% endcode %}
{% endstep %}
{% endstepper %}
