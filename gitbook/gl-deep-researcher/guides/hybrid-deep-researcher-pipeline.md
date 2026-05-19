# Hybrid Deep Researcher Pipeline

## Overview

This guide demonstrates how to leverage **multiple deep research systems in parallel** within a pipeline.md to obtain comprehensive research results from different sources. By running `OpenAIDeepResearcher` and `GLOpenDeepResearcher` simultaneously, you can combine their unique strengths and produce a more thorough analysis.

The Pipeline orchestrates _when and under what conditions_ parallel deep research is invoked, executes both researchers concurrently, and synthesizes their outputs into a unified response.

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/deep-research/03_hybrid_deep_research_pipeline.py" class="button primary">See complete code in GitHub</a>

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page.

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
   4. [parallel-pipeline-processing.md](../../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/parallel-pipeline-processing.md "mention")
4. Event emitting: [event-emitter.md](../../gen-ai-sdk/tutorials/core/event-emitter.md "mention")

</details>

### Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline gl-odr-sdk
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline gl-odr-sdk
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline gl-odr-sdk
```
{% endtab %}
{% endtabs %}

#### Project Setup

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
</strong>GLODR_API_KEY="..."
</code></pre>
{% endstep %}
{% endstepper %}

### Implementation

In this example, we use **parallel execution** to run two different deep research systems simultaneously. The Pipeline handles routing logic, executes both researchers in parallel when deep research is needed, and then combines their results using a ResponseSynthesizer.

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio

from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import GLOpenDeepResearcher, OpenAIDeepResearcher
from gllm_generation.deep_researcher.gl_open_deep_researcher import ResearchProfile
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.lm_invoker.openai_lm_invoker import OpenAILMInvoker
from gllm_inference.output_parser.json_output_parser import JSONOutputParser
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import LMOutput
from gllm_pipeline.router import LMBasedRouter
from gllm_pipeline.steps import parallel, step, switch
from pydantic import BaseModel


class DeepResearchState(BaseModel):
    """State for the deep research pipeline.

    Attributes:
        user_query (str): The user's research query.
        route (str | None): The routing decision (deep_research or normal).
        openai_result (LMOutput | None): Result from OpenAI deep researcher.
        glopen_result (LMOutput | None): Result from GL Open deep researcher.
        combined_result (str | LMOutput | None): Final combined result.
        event_emitter (EventEmitter): Event emitter for streaming.
    """

    user_query: str
    route: str | None = None
    openai_result: LMOutput | None = None
    glopen_result: LMOutput | None = None
    combined_result: str | LMOutput | None = None
    event_emitter: EventEmitter

    class Config:
        arbitrary_types_allowed = True


# Router LM Request Processor
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
    lm_invoker=OpenAILMInvoker(model_name="gpt-4o-mini"),
    output_parser=JSONOutputParser(),
)

# Step 1: Router
router = step(
    component=LMBasedRouter(
        valid_routes={"deep_research", "normal"},
        lm_request_processor=lmrp,
        default_route="normal",
    ),
    input_map={"text": "user_query"},
    output_state="route",
)

# Step 2a: OpenAI Deep Researcher
openai_deep_researcher = step(
    component=OpenAIDeepResearcher(model_name="o1-mini"),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="openai_result",
)

# Step 2b: GL Open Deep Researcher with GPTR-DEEP profile
glopen_deep_researcher = step(
    component=GLOpenDeepResearcher(profile="INTERNAL"),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="glopen_result",
)

# Step 3: Parallel execution of both deep researchers
parallel_deep_research = parallel(
    [openai_deep_researcher, glopen_deep_researcher],
    name="parallel_deep_research",
)

# Step 4: Response Synthesizer to combine results
reporter = step(
    component=ResponseSynthesizer.stuff_preset(
        model_id="openai/gpt-4o-mini",
        user_template="""
        You are tasked with combining research results from two different deep research systems.

        **OpenAI Deep Research Result:**
        {openai_result}

        **GL Open Deep Research Result:**
        {glopen_result}

        Please synthesize these two research results into a comprehensive, coherent answer that:
        1. Combines insights from both sources
        2. Highlights any complementary information
        3. Notes any contradictions or differences in findings
        4. Provides a unified, well-structured response

        Original Query: {query}
        """,
    ),
    input_map={
        "query": "user_query",
        "openai_result": "openai_result",
        "glopen_result": "glopen_result",
        "event_emitter": "event_emitter",
    },
    output_state="combined_result",
)

# Deep research branch: parallel execution + combination
deep_research_branch = parallel_deep_research | reporter

# Normal response for non-research queries
normal_response_synthesizer = step(
    component=ResponseSynthesizer.stuff_preset(
        model_id="openai/gpt-4o-mini",
        user_template="{query}",
    ),
    input_map={"query": "user_query", "event_emitter": "event_emitter"},
    output_state="combined_result",
)

# Conditional step based on routing
conditional_step = switch(
    condition=lambda input: input["route"],
    branches={
        "deep_research": deep_research_branch,
        "normal": normal_response_synthesizer,
    },
)

# Complete pipeline
deep_research_pipeline = router | conditional_step
deep_research_pipeline.state_type = DeepResearchState


async def main() -> None:
    event_emitter = EventEmitter.with_print_handler()
    state = DeepResearchState(
        user_query="research about the latest trends in AI",
        event_emitter=event_emitter,
    )

    result = await deep_research_pipeline.invoke(state)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```
{% endcode %}

#### Run the script

```bash
uv run 03_hybrid_deep_research_pipeline.py
```

**How it works:**

1. **Router Step**: The Pipeline evaluates the user query and determines whether it requires deep research or a simple response.
2. **Parallel Deep Research**: If deep research is needed, the Pipeline executes both OpenAI Deep Researcher and GL Open Deep Researcher **simultaneously** (not sequentially).
3. **Reporter**: Once both researchers complete, a ResponseSynthesizer combines their outputs into a unified, comprehensive answer.
4. **Normal Response**: For casual queries, the Pipeline routes to a simple response synthesizer.

{% hint style="info" %}
**Parallel Execution Benefits:**

* **Faster Results**: Both researchers run simultaneously, reducing total execution time
* **Diverse Perspectives**: Combines different research approaches and data sources
* **Comprehensive Coverage**: Leverages the unique strengths of each research system
{% endhint %}

### Pipeline Architecture

```
┌─────────────────┐
│     Router      │  ← Determines if deep research is needed
└────────┬────────┘
         │
    ┌────▼────┐
    │ Switch  │
    └─┬─────┬─┘
      │     │
      │     └──────────────────────────┐
      │                                │
┌─────▼──────────────────┐    ┌───────▼────────┐
│  Parallel Execution    │    │ Normal Response│
│  ┌──────────────────┐  │    └────────────────┘
│  │ OpenAI Deep      │  │
│  │ Researcher       │  │
│  └──────────────────┘  │
│  ┌──────────────────┐  │
│  │ GL Open Deep     │  │
│  │ Researcher       │  │
│  └──────────────────┘  │
└─────────┬──────────────┘
          │
    ┌─────▼─────────┐
    │   Reporter    │  ← Combines both results
    │ (Synthesizer) │
    └───────────────┘
```

That's it! You've successfully implemented hybrid deep research with parallel execution!

### Next Steps

1. Explore different [research profiles](https://gdplabs.gitbook.io/gl-open-deepresearch/developers-guide/customization/profiles) for GLOpenDeepResearcher
2. Integrate with RAG pipelines by following [your-first-rag-pipeline.md](../../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md "mention")
3. Explore the [API reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/deep_researcher.html) for advanced features
