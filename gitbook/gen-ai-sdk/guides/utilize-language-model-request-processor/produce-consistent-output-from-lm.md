---
icon: brackets-curly
---

# Produce Consistent Output from LM

This guide will walk you through creating structured output responses using LM Request Processor (LMRP) with response schemas.

**Structured output** allows you to receive LM responses in a **predefined, consistent format** (Pydantic BaseModel/JSON). Instead of getting unstructured text, you get validated Python objects that are ready to use in your application.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.
2. A working OpenAI API key configured in your environment variables.

You should be familiar with these concepts and components:

1. [lm-invoker](../../tutorials/inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../../tutorials/inference/lm-request-processor.md "mention")
3. [prompt-builder.md](../../tutorials/inference/prompt-builder.md "mention")
4. Basic understanding of Pydantic models and async Python programming

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/GDP-ADMIN/gl-sdk-cookbook/tree/main/gen-ai/examples/lm_request_processor/lm_request_processor_structured_output" class="button primary" data-icon="github">View full project code on GitHub</a>

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

## Option 1: Using LM Invoker's Response Schema

### 1) Define Your Response Schema

The **response schema** defines the exact structure you want the AI to return. We'll use Pydantic models to define this structure:

{% stepper %}
{% step %}
**Import Required Libraries**

Start by importing the necessary dependencies:

{% code lineNumbers="true" %}

```python
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import asyncio

load_dotenv()
```

{% endcode %}
{% endstep %}

{% step %}
**Create Your Pydantic Models**

Define the structure for individual activities and the complete response:

{% code lineNumbers="true" %}

```python
class Activity(BaseModel):
    type: str
    activity_location: str
    description: str

class ActivityList(BaseModel):
    location: str
    activities: List[Activity]
```

{% endcode %}

> 🧠 _These models define exactly what fields the AI response must include and their data types._
> {% endstep %}
> {% endstepper %}

### 2) Configure the LM Invoker

The **LM invoker** handles communication with the language model and enforces the response schema:

{% stepper %}
{% step %}
**Set up the LM Invoker with Response Schema**

{% code lineNumbers="true" %}

```python
from gllm_inference.lm_invoker import OpenAILMInvoker

lm_invoker = OpenAILMInvoker(
    model_name="gpt-4o-mini",
    response_schema=ActivityList  # This enforces structured output
)
```

{% endcode %}

The `response_schema` parameter ensures the AI response matches your Pydantic model exactly.

{% hint style="info" %}
The response schema acts as a contract between your application and the AI model, guaranteeing consistent output structure.
{% endhint %}
{% endstep %}
{% endstepper %}

### 3) Create the Prompt Builder

The **prompt builder** formats your prompts consistently:

{% stepper %}
{% step %}
**Define Your Prompt Templates**

{% code lineNumbers="true" %}

```python
from gllm_inference.prompt_builder import PromptBuilder

system_template = "You are a helpful assistant who specializes in recommending activities."
user_template = "{question}"

prompt_builder = PromptBuilder(
    system_template=system_template,
    user_template=user_template
)
```

{% endcode %}

> 🧠 _The `{question}` placeholder will be replaced with actual user input when processing requests._
> {% endstep %}
> {% endstepper %}

### 4) Build the LM Request Processor

The **LM request processor** combines your prompt builder and LM invoker into a complete processing pipeline:

{% stepper %}
{% step %}
**Create the Request Processor**

{% code lineNumbers="true" %}

```python
from gllm_inference.request_processor import LMRequestProcessor

lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)
```

{% endcode %}

This creates a complete pipeline that will:

1. Format your prompt using the prompt builder
2. Send it to the LM invoker with schema enforcement
3. Return structured, validated results

> 🧠 _The LM Request Processor automatically handles the entire workflow, making structured output generation seamless._
> {% endstep %}
> {% endstepper %}

### 5) Process Requests and Get Structured Output

Now you can process requests and receive structured responses:

{% stepper %}
{% step %}
**Process a Request**

{% code lineNumbers="true" %}

```python
response = asyncio.run(lm_request_processor.process(
    question="I want to go to Tokyo, Japan. What should I do?"
))

# Access the structured output
print(response.structured_output)
```

{% endcode %}
{% endstep %}

{% step %}
**Expected Output Structure**

The response will be a validated `ActivityList` object:

```python
ActivityList(
    location="Tokyo, Japan",
    activities=[
        Activity(
            type="Cultural",
            activity_location="Senso-ji Temple",
            description="Visit Tokyo's oldest temple in Asakusa district"
        ),
        Activity(
            type="Shopping",
            activity_location="Shibuya Crossing",
            description="Experience the world's busiest pedestrian crossing"
        ),
        # ... more activities
    ]
)
```

{% hint style="info" %}
Notice how every field matches exactly what was defined in your Pydantic models - no parsing or validation needed!
{% endhint %}
{% endstep %}

{% step %}
**Access Individual Fields**

You can access specific data from the structured response:

{% code lineNumbers="true" %}

```python
# Get the location
location = response.structured_output.location
print(f"Destination: {location}")

# Iterate through activities
for activity in response.structured_output.activities:
    print(f"- {activity.type}: {activity.description}")
    print(f"  Location: {activity.activity_location}")
```

{% endcode %}
{% endstep %}
{% endstepper %}

## Option 2: Using Structured Output

This approach uses the **structured output** feature to handle structured output parsing after the LM generates a response. Instead of enforcing the schema at the LM level, it relies on prompt instructions and post-processing.

### 1) Define Your Response Schema

The response schema definition remains the same as Option 1:

{% stepper %}
{% step %}
**Import Required Libraries**

{% code lineNumbers="true" %}

```python
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import asyncio

load_dotenv()
```

{% endcode %}
{% endstep %}

{% step %}
**Create Your Pydantic Models**

{% code lineNumbers="true" %}

```python
class Activity(BaseModel):
    type: str
    activity_location: str
    description: str

class ActivityList(BaseModel):
    location: str
    activities: List[Activity]
```

{% endcode %}

> 🧠 _The same Pydantic models work for both approaches - the difference is in how they're applied._
> {% endstep %}
> {% endstepper %}

### 2) Configure the LM Invoker

Unlike Option 1, the LM invoker doesn't need a response schema parameter:

{% stepper %}
{% step %}
**Set up the LM Invoker**

{% code lineNumbers="true" %}

```python
from gllm_inference.lm_invoker import OpenAILMInvoker

lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", output_transformer="json")
```

{% endcode %}

> 🧠 _Notice there's no `response_schema` parameter - the structure is enforced through prompting and parsing._
> {% endstep %}
> {% endstepper %}

### 3) Create the Prompt Builder with Schema Instructions

The prompt must instruct the model to return JSON in the expected format:

{% stepper %}
{% step %}
**Define Your Prompt Templates with Schema**

{% code lineNumbers="true" %}

```python
from gllm_inference.prompt_builder import PromptBuilder

system_template = """You are a helpful assistant who specializes in recommending activities.
Return the response in JSON format with the schema: {schema}."""

user_template = "{question}"

prompt_builder = PromptBuilder(
    system_template=system_template,
    user_template=user_template
)
```

{% endcode %}

> 🧠 _The `{schema}` placeholder will be filled with the actual JSON schema at runtime._
> {% endstep %}
> {% endstepper %}

### 4) Build the LM Request Processor

Include the prompt builder and LM invoker in the request processor configuration:

{% stepper %}
{% step %}
**Create the Request Processor**

{% code lineNumbers="true" %}

```python
from gllm_inference.request_processor import LMRequestProcessor

lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)
```

{% endcode %}

This creates a pipeline that will:

1. Format your prompt with schema instructions
2. Send it to the LM invoker
3. Parse and validate the JSON response using structured output

> 🧠 _The structured output transformer handles both JSON parsing and optional Pydantic model validation._
> {% endstep %}
> {% endstepper %}

### 5) Process Requests with Schema Parameter

Pass the schema as a prompt parameter when processing requests:

{% stepper %}
{% step %}
**Process a Request with Schema**

{% code lineNumbers="true" %}

```python
response = asyncio.run(lm_request_processor.process(
    question="I want to go to Tokyo, Japan. What should I do?",
    schema=str(ActivityList.model_json_schema())
))

# Access the parsed output
print(response.structured_output)
```

{% endcode %}
{% endstep %}

{% step %}
**Expected Output Structure**

The response will contain parsed JSON data that matches your schema structure:

```python
{
    "location": "Tokyo, Japan",
    "activities": [
        {
            "type": "Cultural",
            "activity_location": "Senso-ji Temple",
            "description": "Visit Tokyo's oldest temple in Asakusa district"
        },
        # ... more activities
    ]
}
```

{% hint style="info" %}
The output is parsed JSON data, ready for further processing or conversion to Pydantic models if needed.
{% endhint %}
{% endstep %}
{% endstepper %}

## 📂 Complete Guide Files

### Option 1: Using LM Invoker's Response Schema

{% code lineNumbers="true" %}

```python
from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from pydantic import BaseModel
from typing import List
from gllm_inference.prompt_builder import PromptBuilder
import asyncio

load_dotenv()

# Define the response schema
class Activity(BaseModel):
    type: str
    activity_location: str
    description: str

class ActivityList(BaseModel):
    location: str
    activities: List[Activity]

# Define the LM invoker with response schema
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", response_schema=ActivityList)

# Define the prompt
system_template = "You are a helpful assistant who specializes in recommending activities."
user_template = "{question}"

prompt_builder = PromptBuilder(system_template=system_template, user_template=user_template)

# Define the LM request processor
lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)

# Invoke the LM request processor
response = asyncio.run(lm_request_processor.process(
    question="I want to go to Tokyo, Japan. What should I do?"
))

print(response.structured_output)
```

{% endcode %}

### Option 2: Using JSON Output Parser

{% code lineNumbers="true" %}

```python
from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from pydantic import BaseModel
from typing import List
from gllm_inference.prompt_builder import PromptBuilder
import asyncio

load_dotenv()

# Define the response schema
class Activity(BaseModel):
    type: str
    activity_location: str
    description: str

class ActivityList(BaseModel):
    location: str
    activities: List[Activity]

# Define the LM invoker (no response schema)
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", output_transformer="json")

# Define the prompt with schema instruction
system_template = "You are a helpful assistant who specializes in recommending activities. Return the response in JSON format with the schema: {schema}."
user_template = "{question}"

prompt_builder = PromptBuilder(system_template=system_template, user_template=user_template)

# Define the LM request processor
lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)

# Invoke the LM request processor with schema parameter
response = asyncio.run(lm_request_processor.process(
    question="I want to go to Tokyo, Japan. What should I do?",
    schema=str(ActivityList.model_json_schema())
))

print(response.structured_output)
```

{% endcode %}

---
