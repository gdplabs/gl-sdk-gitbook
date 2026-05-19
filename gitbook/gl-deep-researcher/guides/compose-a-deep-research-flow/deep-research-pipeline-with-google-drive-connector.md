---
icon: google-drive
---

# Deep Research Pipeline with Google Drive Connector

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
