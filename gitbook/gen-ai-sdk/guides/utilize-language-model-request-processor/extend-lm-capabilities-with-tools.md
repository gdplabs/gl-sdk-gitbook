---
icon: toolbox
---

# Extend LM Capabilities with Tools

This guide will walk you through implementing tool calling in your applications using two different approaches.

**Tool calling** enables language models to **execute external functions** during conversations, allowing dynamic computation, data retrieval, and complex workflows beyond simple text generation.

For example, when asked _"What is 15 + 25 then multiply by 2?"_, instead of guessing, the model calls your `add` and `multiply` functions to provide accurate results.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.
2. A working OpenAI API key configured in your environment variables.

You should be familiar with these concepts and components:

1. [lm-invoker](../../tutorials/inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../../tutorials/inference/lm-request-processor.md "mention")
3. [prompt-builder.md](../../tutorials/inference/prompt-builder.md "mention")
4. [#tool-calling](../../tutorials/inference/lm-invoker/#tool-calling "mention")

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/inference/lm_request_processor/lm_request_processor_tool_calling" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference
```

{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Environment Configuration**

Ensure you have a file named `.env` in your project directory with the following content:

```env
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

{% hint style="info" %}
Replace `<YOUR_OPENAI_API_KEY>` with your actual OpenAI API key.
{% endhint %}
{% endstep %}
{% endstepper %}

---

There are two approaches to implement tool calling:

1. **LM Request Processor**: Simplified approach with built-in tool execution handling
2. **LM Invoker with Execution Loop**: Direct control over the tool calling process

Choose the approach that best fits your use case and complexity requirements.

## Option 1: LM Request Processor

This approach simplifies tool calling by using the LM Request Processor, which handles tool execution automatically.

### 1) Define Tools and Components

Set up your tools and LMRP components:

{% stepper %}
{% step %}
**Import Libraries and Define Tools**

{% code lineNumbers="true" %}

```python
from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.prompt_builder import PromptBuilder
from gllm_core.schema import tool
import asyncio

load_dotenv()

# Define tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

{% endcode %}
{% endstep %}

{% step %}
**Configure LM Invoker with Tools**

{% code lineNumbers="true" %}

```python
# Define the LM invoker with tools
lm_invoker = OpenAILMInvoker(
    model_name="gpt-4o-mini",
    tools=[add, subtract, multiply]
)
```

{% endcode %}

The LM invoker automatically handles tool registration and execution when using LMRP.
{% endstep %}
{% endstepper %}

### 2) Set Up Prompt Builder and LMRP

Create the prompt builder and request processor:

{% stepper %}
{% step %}
**Create Prompt Builder**

{% code lineNumbers="true" %}

```python
# Define the prompt templates
system_template = "You are a helpful assistant. Use tool for performing math operations. Output the final answer only."
user_template = "{question}"

prompt_builder = PromptBuilder(
    system_template=system_template,
    user_template=user_template
)
```

{% endcode %}
{% endstep %}

{% step %}
**Initialize LM Request Processor**

{% code lineNumbers="true" %}

```python
# Define the LM request processor
lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)
```

{% endcode %}

{% hint style="info" %}
The LMRP automatically handles the tool calling execution loop, making implementation much simpler than Option 2.
{% endhint %}
{% endstep %}
{% endstepper %}

### 3) Process Requests with Tool Calling

Execute tool calling with a single method call:

{% stepper %}
{% step %}
**Process the Request**

{% code lineNumbers="true" %}

```python
# Invoke the LM request processor
response = asyncio.run(lm_request_processor.process(
    question="What is 10 + 20 * 0 - 4?"
))

print(response)
```

{% endcode %}
{% endstep %}

{% step %}
**Expected Output**

The LMRP will automatically:

1. Format the prompt using the prompt builder
2. Send the request to the LM invoker
3. Handle any tool calls the model makes
4. Return the final response after all tool executions

For the query "What is 10 + 20 \* 0 - 4?", the model will use the mathematical tools to calculate the correct result: `6`
{% endstep %}
{% endstepper %}

## Option 2: LM Invoker with Execution Loop

This approach gives you full control over the tool calling execution flow and conversation management.

### 1) Define Your Tools

First, create the tools that your AI can use:

{% stepper %}
{% step %}
**Import Required Libraries**

{% code lineNumbers="true" %}

```python
from gllm_core.schema import tool
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import ToolResult, Message
from dotenv import load_dotenv
import asyncio

load_dotenv()
```

{% endcode %}
{% endstep %}

{% step %}
**Create Tool Functions**

Define your tools using the `@tool` decorator:

{% code lineNumbers="true" %}

```python
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

{% endcode %}

{% hint style="info" %}
The `@tool` decorator automatically generates the schema that the model needs to understand and call your functions.
{% endhint %}
{% endstep %}
{% endstepper %}

### 2) Set Up the LM Invoker

Configure the LM invoker with your tools:

{% stepper %}
{% step %}
**Initialize the Invoker with Tools**

{% code lineNumbers="true" %}

```python
# Initialize the invoker with tools
tools = [add, subtract, multiply]
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", tools=tools)
```

{% endcode %}

The LM invoker will automatically register your tools with the model for calling.
{% endstep %}
{% endstepper %}

### 3) Implement the Execution Loop

Create the execution loop that handles tool calling:

{% stepper %}
{% step %}
**Create the Execution Function**

{% code lineNumbers="true" %}

```python
async def execute_tool_calling(lm_invoker, query, tools, prompt_builder):
    # Create a lookup dictionary for quick tool access
    tool_dict = {t.name: t for t in tools}

    # Format the initial prompt
    messages = prompt_builder.format(query=query)

    # Main execution loop (max 5 iterations)
    for _ in range(5):
        # Get response from the model
        result = await lm_invoker.invoke(messages)

        # Check if model wants to call tools
        if isinstance(result, str) or not result.tool_calls:
            # No tool calls - return the final response
            return result if isinstance(result, str) else result.text

        # Model wants to call tools - prepare assistant message
        assistant_content = []
        if result.text:
            assistant_content.append(result.text)
        assistant_content.extend(result.tool_calls)
        messages.append(Message.assistant(assistant_content))

        # Execute each tool call
        for call in result.tool_calls:
            try:
                # Execute the tool
                output = await tool_dict[call.name].ainvoke(call.args)
            except Exception as e:
                # Handle tool execution errors
                output = f"Error: {e}"

            # Add tool result back to conversation
            messages.append(Message.user(ToolResult(id=call.id, output=str(output))))

    return "Max iterations reached"
```

{% endcode %}

{% hint style="info" %}
The execution loop handles multiple rounds of tool calling, allowing the model to use tool results for further reasoning and additional tool calls.
{% endhint %}
{% endstep %}

{% step %}
**Set Up Prompt Builder**

Configure the prompt builder to guide the model:

{% code lineNumbers="true" %}

```python
prompt_builder = PromptBuilder(
    system_template="You are a helpful assistant. Use tool for performing math operations. Output the final answer only.",
    user_template="Calculate: {query}"
)
```

{% endcode %}

The system message is crucial for encouraging proper tool usage.
{% endstep %}
{% endstepper %}

### 4) Execute Tool Calling

Run the complete tool calling example:

{% stepper %}
{% step %}
**Run the Example**

{% code lineNumbers="true" %}

```python
# Run the tool calling example
query = "What is 15 + 25 then multiply by 2?"
result = asyncio.run(execute_tool_calling(lm_invoker, query, tools, prompt_builder))
print(f"Result: {result}")
```

{% endcode %}
{% endstep %}

{% step %}
**Expected Flow**

The execution will follow this pattern:

1. **User Query**: "What is 15 + 25 then multiply by 2?"
2. **Model Analysis**: Identifies need for addition and multiplication
3. **First Tool Call**: `add(15, 25)` → Returns `40`
4. **Second Tool Call**: `multiply(40, 2)` → Returns `80`
5. **Final Response**: "The result is 80"
{% endstep %}
{% endstepper %}

## 📂 Complete Guide Files

### Option 1 Implementation

{% code lineNumbers="true" %}

```python
from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.prompt_builder import PromptBuilder
from gllm_core.schema import tool
import asyncio

load_dotenv()

# Define tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Setup components
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", tools=[add, subtract, multiply])
system_template = "You are a helpful assistant. Use tool for performing math operations. Output the final answer only."
user_template = "{question}"
prompt_builder = PromptBuilder(system_template=system_template, user_template=user_template)

# Create and execute LMRP
lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)

response = asyncio.run(lm_request_processor.process(
    question="What is 10 + 20 * 0 - 4?"
))

print(response)
```

{% endcode %}

### Option 2 Implementation

{% code lineNumbers="true" %}

```python
from gllm_core.schema import tool
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import ToolResult, Message
from dotenv import load_dotenv
import asyncio

load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def execute_tool_calling(lm_invoker, query, tools, prompt_builder):
    tool_dict = {t.name: t for t in tools}
    messages = prompt_builder.format(query=query)

    for _ in range(5):
        result = await lm_invoker.invoke(messages)

        if isinstance(result, str) or not result.tool_calls:
            return result if isinstance(result, str) else result.text

        assistant_content = []
        if result.text:
            assistant_content.append(result.text)
        assistant_content.extend(result.tool_calls)
        messages.append(Message.assistant(assistant_content))

        for call in result.tool_calls:
            try:
                output = await tool_dict[call.name].ainvoke(call.args)
            except Exception as e:
                output = f"Error: {e}"

            messages.append(Message.user(ToolResult(id=call.id, output=str(output))))

    return "Max iterations reached"

# Setup and execution
tools = [add, subtract, multiply]
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", tools=tools)
prompt_builder = PromptBuilder(
    system_template="You are a helpful assistant. Use tool for performing math operations. Output the final answer only.",
    user_template="Calculate: {query}"
)

query = "What is 15 + 25 then multiply by 2?"
result = asyncio.run(execute_tool_calling(lm_invoker, query, tools, prompt_builder))
print(f"Result: {result}")
```

{% endcode %}
