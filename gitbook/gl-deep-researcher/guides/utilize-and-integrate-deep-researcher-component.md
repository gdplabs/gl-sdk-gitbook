---
hidden: true
icon: network-wired
---

# Utilize and Integrate Deep Researcher Component

## Overview

This guide shows how to perform **deep research using the** [deep-researcher.md](../../gen-ai-sdk/tutorials/generation/deep-researcher.md "mention") component starting from simple, direct usage and gradually moving toward more advanced orchestration patterns.

Additionally, [component.md](../../gen-ai-sdk/tutorials/core/component.md "mention") can be placed inside a [pipeline.md](../../gen-ai-sdk/tutorials/orchestration/pipeline.md "mention") when you need additional logic such as context preparation or routing decisions. The Pipeline orchestrates _when and under what conditions_ deep research is invoked, but does not define _how deep research itself works internally_.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. completion of all setup steps listed on the [prerequisites.md](../../gen-ai-sdk/prerequisites.md "mention") page.
2. API key for deep researcher component set. Please refer to

You should be familiar with these:

1. [deep-researcher.md](../../gen-ai-sdk/tutorials/generation/deep-researcher.md "mention")
2. Inference:
   1. [lm-invoker](../../gen-ai-sdk/tutorials/inference/lm-invoker/ "mention")
   2. [prompt-builder.md](../../gen-ai-sdk/tutorials/inference/prompt-builder.md "mention")
   3. [lm-request-processor.md](../../gen-ai-sdk/tutorials/inference/lm-request-processor.md "mention")
   4. [mcp-server.md](../../gen-ai-sdk/tutorials/inference/lm-invoker/mcp-server.md "mention")
   5. [mcp-connector.md](../../gen-ai-sdk/tutorials/inference/lm-invoker/mcp-connector.md "mention")
3. Pipeline and orchestration:
   1. [pipeline.md](../../gen-ai-sdk/tutorials/orchestration/pipeline.md "mention")
   2. [component.md](../../gen-ai-sdk/tutorials/core/component.md "mention")
   3. [Routing](../../gen-ai-sdk/tutorials/orchestration/routing/README.md "mention")
4. Event emitting: [event-emitter.md](../../gen-ai-sdk/tutorials/core/event-emitter.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline
```
{% endtab %}
{% endtabs %}

## Utilize Deep Research as a single Component

See [#quickstart](../../gen-ai-sdk/tutorials/generation/deep-researcher.md#quickstart "mention") for the simplest way to perform deep research using the GL SDK, which is by invoking deep research directly **without any Pipeline orchestration**.

## Integrate in a Research Pipeline with Routing

This section demonstrates how to place DeepResearcher **Component** inside a **Pipeline** to orchestrate _when_ it is invoked, based on the characteristics of a user query.

Here, the Pipeline is responsible for:

* inspecting the incoming request
* deciding whether deep research is required
* routing execution accordingly

The Pipeline does **not** define how deep research is executed internally. Deep research is invoked as an encapsulated step, and its internal reasoning remains provider-defined.

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/deep-research/01_deep_research_pipeline.py" class="button primary">See complete code in GitHub</a>

### Project Setup

{% stepper %}
{% step %}
**Clone the repository**

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/deep-research
```
{% endstep %}

{% step %}
**Set UV authentication and install dependencies**

Unix-based systems (Linux, macOS):

```bash
./setup.sh
```

For Windows:

```cmd
setup.bat
```
{% endstep %}

{% step %}
**Prepare `.env` file**

<pre class="language-env"><code class="lang-env"><strong>OPENAI_API_KEY="..."
</strong></code></pre>
{% endstep %}
{% endstepper %}

### Implementation

In this example, DeepResearcher Component is used as one step within a Pipeline. The Pipeline handles routing logic and context preparation, while deep research itself remains a standalone invocation.

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio

from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import OpenAIDeepResearcher
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.lm_invoker.openai_lm_invoker import OpenAILMInvoker
from gllm_inference.output_parser.json_output_parser import JSONOutputParser
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import LMOutput
from gllm_pipeline.router import LMBasedRouter
from gllm_pipeline.steps import step, switch
from pydantic import BaseModel


class DeepResearchState(BaseModel):
    user_query: str
    route: str | None
    result: str | LMOutput | None
    event_emitter: EventEmitter

    class Config:
        arbitrary_types_allowed = True

lmrp = LMRequestProcessor(
    prompt_builder=PromptBuilder(
        user_template="""
        Based on the following user query, determine if it is a deep research query or a normal query.

        - **normal**: Casual greetings, small talk, or simple conversational queries that do not require
          in-depth research. Examples: "hello", "how are you", "what's the weather", "thanks", "goodbye".

        - **deep_research**: Queries that require comprehensive research, multi-source analysis, or
          in-depth exploration of a topic. Examples: "research the latest AI trends", "compare X vs Y",
          "analyze the market for...", "what are the pros and cons of...".

        Output the answer in JSON format with "route" as the key. For example:
        {{"route": "deep_research"}} or {{"route": "normal"}}

        Query: {text}
        """
    ),
    lm_invoker=OpenAILMInvoker(model_name="gpt-5-nano"),
    output_parser=JSONOutputParser(),
)

router = step(
    component=LMBasedRouter(
        valid_routes={"deep_research", "normal"},
        lm_request_processor=lmrp,
        default_route="normal",
    ),
    input_map={"text": "user_query"},
    output_state="route",
)

deep_researcher = step(
    component=OpenAIDeepResearcher(model_name="o4-mini-deep-research"),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="result",
)

normal_response_synthesizer = step(
    component=ResponseSynthesizer.stuff_preset(
        model_id="openai/gpt-5-nano",
        user_template="{query}",
    ),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="result",
)

conditional_step = switch(
    condition=lambda input: input["route"],
    branches={"deep_research": deep_researcher, "normal": normal_response_synthesizer},
)

deep_research_pipeline = router | conditional_step
deep_research_pipeline.state_type = DeepResearchState


async def main() -> None:
    event_emitter = EventEmitter.with_print_handler()
    state = DeepResearchState(
        user_query="research about the latest trends in AI",
        event_emitter=event_emitter,
        route=None,
        result=None,
    )

    result = await deep_research_pipeline.invoke(state)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```
{% endcode %}

#### Run the script

```bash
uv run 01_deep_research_pipeline.py
```

**How it works:**

1. The Pipeline evaluates the user query and determines the appropriate execution path.
2. If deep research is required, the Pipeline invokes the deep research step.
3. Otherwise, the Pipeline routes the request to a simpler response path.
4. The Pipeline returns the final result produced by the selected path.

{% hint style="info" %}
The deep research step is treated as an encapsulated unit; the Pipeline does not break down or modify its internal execution.
{% endhint %}

## Deep Research Pipeline with Google Drive Integration

This section demonstrates Pipeline orchestration with **additional data sources**, using Google Drive as an example.

In this setup:

* the Pipeline controls routing and execution flow
* Google Drive access is provided via an MCP connector
* Deep research is invoked as an encapsulated step with additional data available during execution

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/deep-research/02_deep_research_google_drive_pipeline.py" class="button primary">See complete code in GitHub</a>

### Project Setup

{% stepper %}
{% step %}
**Clone the repository**

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/deep-research
```
{% endstep %}

{% step %}
**Set UV authentication and install dependencies**

Unix-based systems (Linux, macOS):

```bash
./setup.sh
```

For Windows:

```cmd
setup.bat
```
{% endstep %}

{% step %}
**Prepare `.env` file with Google Drive authentication**

Get the auth token from [OpenAI Connector Guide](https://platform.openai.com/docs/guides/tools-connectors-mcp?quickstart-panels=connector#authorizing-a-connector)

When generating the token, make sure to enable the following scopes:

* `userinfo.email`
* `userinfo.profile`
* `drive.readonly`

Add to `.env`:

```env
OPENAI_API_KEY="..."
GOOGLE_DRIVE_AUTH_TOKEN="..."
```
{% endstep %}
{% endstepper %}

### Implementation

In this example, Google Drive is made available to deep research through an MCP connector, while the Pipeline determines when deep research should be invoked.

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
import os

from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import OpenAIDeepResearcher
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.lm_invoker.openai_lm_invoker import OpenAILMInvoker
from gllm_inference.output_parser.json_output_parser import JSONOutputParser
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import LMOutput, NativeTool
from gllm_pipeline.router import LMBasedRouter
from gllm_pipeline.steps import step, switch
from pydantic import BaseModel


class DeepResearchState(BaseModel):
    user_query: str
    route: str | None
    result: str | LMOutput | None
    event_emitter: EventEmitter

    class Config:
        arbitrary_types_allowed = True

lmrp = LMRequestProcessor(
    prompt_builder=PromptBuilder(
        user_template="""
        Based on the following user query, determine if it is a deep research query or a normal query.

        - **normal**: Casual greetings, small talk, or simple conversational queries that do not require
          in-depth research. Examples: "hello", "how are you", "what's the weather", "thanks", "goodbye".

        - **deep_research**: Queries that require comprehensive research, multi-source analysis, or
          in-depth exploration of a topic. Examples: "research the latest AI trends", "compare X vs Y",
          "analyze the market for...", "what are the pros and cons of...".

        Output the answer in JSON format with "route" as the key. For example:
        {{"route": "deep_research"}} or {{"route": "normal"}}

        Query: {text}
        """
    ),
    lm_invoker=OpenAILMInvoker(
        model_name="gpt-5-nano",
    ),
    output_parser=JSONOutputParser(),
)

router = step(
    component=LMBasedRouter(
        valid_routes={"deep_research", "normal"},
        lm_request_processor=lmrp,
        default_route="normal",
    ),
    input_map={"text": "user_query"},
    output_state="route",
)

connector = NativeTool.mcp_connector(
    name="google_drive",
    connector_id="connector_googledrive",
    auth="<google_auth_token>",
)

deep_researcher = step(
    component=OpenAIDeepResearcher(
        model_name="o4-mini-deep-research",
        tools=[connector]
    ),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="result",
)

normal_response_synthesizer = step(
    component=ResponseSynthesizer.stuff_preset(
        model_id="openai/gpt-5-nano",
        user_template="{query}",
    ),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="result",
)

conditional_step = switch(
    condition=lambda input: input["route"],
    branches={"deep_research": deep_researcher, "normal": normal_response_synthesizer},
)

deep_research_pipeline = router | conditional_step
deep_research_pipeline.state_type = DeepResearchState


async def main() -> None:
    event_emitter = EventEmitter.with_print_handler()
    state = DeepResearchState(
        user_query="research information from my Google Drive about AI trends",
        event_emitter=event_emitter,
        route=None,
        result=None,
    )

    result = await deep_research_pipeline.invoke(state)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```
{% endcode %}

The Google Drive connector extends the data available during research, but does not change the execution flow or reasoning strategy of deep research itself.

#### Run the script

```bash
uv run 02_deep_research_google_drive_pipeline.py
```

**Benefits:**

* Make documents stored in Google Drive available as research context
* Combine private documents with public information during research
* Integrate external data sources without changing research execution logic
