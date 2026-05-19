---
icon: truck-fast
---

# Quickstart

### Prerequisites

As this guide utilizes a library published in Gen AI Google Cloud Repository, you will need to fulfill all the setup steps required in [prerequisites.md](../../prerequisites.md "mention"). To summarize, you need the following:

* Python 3.11 or higher
* Access to the **GDP Labs' Gen AI SDK repository** is required to run this program. If you need access, kindly submit a ticket to our DevOps team. Request access to Gen AI Google Cloud repositories by submitting this [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) (alternatively, from your manager or team lead)
* **gcloud CLI:** Please refer to the [installation guide](https://cloud.google.com/sdk/docs/install). After installing, please run `gcloud auth login` to authorize gcloud to access the Cloud Platform with Google user credentials.
* [UV](https://docs.astral.sh/uv/) package manager

### Getting Started

{% stepper %}
{% step %}
**Installation**

Initialize a new project and add the GL Connectors Tools package.

{% code overflow="wrap" lineNumbers="true" %}
```bash
uv init --bare
uv add --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gl-connectors-tools
```
{% endcode %}
{% endstep %}

{% step %}
**Create Your First Tool**

Create a `main.py` file with the following content:

{% code title="main.py" lineNumbers="true" %}
```python
from gl_connectors_tools.tools import BaseTool
from pydantic import BaseModel, Field

class HelloToolInput(BaseModel):
    name: str = Field(description="The name of the person to greet (e.g., 'Alice', 'Bob').")

class HelloTool(BaseTool):
    name: str = "hello_tool"
    description: str = (
        "Greet a person by name. "
        "Takes a name as input and returns a friendly greeting "
        "in the format 'Hello, {name}!'."
    )
    input_schema: type[BaseModel] = HelloToolInput

    def run(self, name: str) -> str:
        return f"Hello, {name}!"

hello = HelloTool()
result = hello.run(name="World")
print(result)  # Hello, World!
```
{% endcode %}

A few things to note:

* **`description`** — This is what the LLM reads to decide whether to call your tool. Be clear and specific about what the tool does, what it accepts, and what it returns.
* **`input_schema`** — Pydantic model that defines the tool's input. Each field's `description` helps the LLM understand what values to pass.
* **`run`** — The actual execution logic. This is called when the LLM invokes the tool.
{% endstep %}

{% step %}
**Run**

```bash
uv run main.py
```

You should see:

```
Hello, World!
```
{% endstep %}

{% step %}
#### Using with Agent

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

{% code title="main.py" lineNumbers="true" %}
```python
from gl_connectors_tools.adapters import to_langchain_tools
from gl_connectors_tools.tools import BaseTool
from pydantic import BaseModel, Field
from glaip_sdk.agents import Agent

class HelloToolInput(BaseModel):
    name: str = Field(description="The name of the person to greet (e.g., 'Alice', 'Bob').")

class HelloTool(BaseTool):
    name: str = "hello_tool"
    description: str = (
        "Greet a person by name. "
        "Takes a name as input and returns a friendly greeting "
        "in the format 'Hello, {name}!'."
    )
    input_schema: type[BaseModel] = HelloToolInput

    def run(self, name: str) -> str:
        return f"Hello, {name}!"

hello = HelloTool()
agent = Agent(
    name="test-agent-with-tools",
    instruction="You are a helpful assistant.",
    tools=to_langchain_tools([hello]),
)
agent.run("say hello to world!")
```
{% endcode %}

**Execution**

Simply run `uv run main.py` again like in Step 3.

You should see an output similar to the following if all the configurations are correct.

```
 ────────────────────────────────────────────────────────────────────────────────────────────────────── Final Result · 7.38s ────────────────────────────────────────────────────────────────────────────────────────────────────── 
  Hello, world!                                                                                                                                                                                                                     
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
```
{% endstep %}
{% endstepper %}
