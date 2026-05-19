# Deep Research in a Pipeline with Routing

## Overview

This guide shows how to perform **deep research using the** [deep-researcher.md](../../gen-ai-sdk/tutorials/generation/deep-researcher.md "mention") [component.md](../../gen-ai-sdk/tutorials/core/component.md "mention") placed inside a [pipeline.md](../../gen-ai-sdk/tutorials/orchestration/pipeline.md "mention") when you need additional logic such as context preparation or routing decisions. The Pipeline orchestrates _when and under what conditions_ deep research is invoked, but does not define _how deep research itself works internally_.

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/deep-research/01_deep_research_pipeline.py" class="button primary">See complete code in GitHub</a>

{% include "../../.gitbook/includes/how-to-use-this-guide.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page

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

{% code expandable="true" %}
```
╭────────────────────────╮
│     THINKING START     │
╰────────────────────────╯
**Explaining banana ripening**

The user has asked for a short and concise report on why bananas are yellow, which relates to the science of botany. Bananas start off green and turn yellow as they ripen due to the breakdown of chlorophyll. This process reveals yellow pigments such as xanthophylls and carotenoids. I’ll focus on summarizing this pigment change, discussing how these compounds affect the color of bananas as they reach ripeness, and I'll ensure it's clear and concise.
╭──────────────────────╮
│     THINKING END     │
╰──────────────────────╯

╭────────────────────────╮
│     THINKING START     │
╰────────────────────────╯
**Focusing on textual explanation**

The user wants a "short and concise report" about why bananas are yellow. A textual explanation should suffice for this, and though I considered including an image, it's likely unnecessary for a straightforward answer. I’ll focus on gathering information about the pigments that contribute to the yellow color of bananas, particularly as they ripen. My aim will be to provide a clear and engaging textual report without the need for images, sticking closely to the user’s request.
╭──────────────────────╮
│     THINKING END     │
╰──────────────────────╯

╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: search
>>> query: "why banana is yellow"
>>> sources: None

╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: search
>>> query: banana color pigments chlorophyll carotenoids
>>> sources: None

╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: search
>>> query: "banana" chlorophyll breakdown yellow pigment
>>> sources: None

╭────────────────────────╮
│     THINKING START     │
╰────────────────────────╯
**Exploring banana coloration**

I’ve come across research articles about chlorophyll breakdown in banana leaves or fruits. While they might have relevant information, they could be too technical if the user expects a short answer. I’ll still need references to support a concise explanation. I wonder if I should focus on the scientific reasons behind why bananas are yellow, such as carotenoids and ripening. So, let’s search specifically for phrases like "banana why yellow carotenoids."
╭──────────────────────╮
│     THINKING END     │
╰──────────────────────╯

...

╭────────────────────────╮
│     THINKING START     │
╰────────────────────────╯
**Structuring the report on bananas**

I’m planning to create a report titled “Why Bananas Are Yellow.”

I’m thinking about using bullet points to outline key concepts like the differences between unripe and ripe bananas, the breakdown of chlorophyll, and what pigments contribute to the yellow color.

While I could use subheadings like “Chlorophyll vs. Carotenoids” or “Ripening Process,” I believe a simple bullet list under the main title is also effective. This should clearly present the information while adhering to the guidelines.
╭──────────────────────╮
│     THINKING END     │
╰──────────────────────╯
# Why Bananas Are Yellow

- **Chlorophyll in young bananas – green color:** Unripe bananas appear green because their peel contains chlorophyll pigment ((https://www.scribd.com/document/949965573/Yellow-Wikipedia#:~:text=Bananas%20are%20green%20when%20they,enzymes%20continue%20their%20work%2C%20
the)).
- **Ripening breaks down chlorophyll:** As bananas ripen they produce ethylene, triggering enzymes that degrade chlorophyll ((https://pubmed.ncbi.nlm.nih.gov/21160159/#:~:text=The%20ripening%20of%20bananas%20is,to%20their%20fascinating%20blue%20luminescence)) ((https://www.scribd.com/document/949965573/Yellow-Wikipedia#:~:text=Bananas%20are%20green%20when%20they,enzymes%20continue%20their%20work%2C%20
the)). This causes the green pigment to fade.
- **Carotenoids give the yellow color:** Once the green chlorophyll is gone, yellow-orange carotenoid pigments remain in the peel. Ripe bananas accumulate xanthophylls (a type of carotenoid) so that the peel reflects yellow light ((https://wentbananas.com/why-banana-are-yellow/#:~:text=The%20specific%20type%20of%20carotenoid,yellow%20or%20orange%20fruits%20and)) ((https://foodcrumbles.com/colours-in-fruits-vegetables/#:~:text=The%20same%20applies%20to%20a,the%20underlying%20colors%20become%20visible)). These carotenoids dominate the peel’s color, making ripe bananas look yellow.

**Sources:** The color change is explained by plant pigment chemistry: ripening bananas lose green chlorophyll and reveal underlying yellow carotenoids ((https://pubmed.ncbi.nlm.nih.gov/21160159/#:~:text=The%20ripening%20of%20bananas%20is,to%20their%20fascinating%20blue%20luminescence)) ((https://foodcrumbles.com/colours-in-fruits-vegetables/#:~:text=The%20same%20applies%20to%20a,the%20underlying%20colors%20become%20visible)). For example, one source notes that “the green chlorophyll supply is stopped and the yellow color of the carotenoids replaces it” during banana ripening ((https://www.scribd.com/document/949965573/Yellow-Wikipedia#:~:text=Bananas%20are%20green%20when%20they,enzymes%20continue%20their%20work%2C%20
the)), and specifically cites xanthophyll pigments as responsible for the yellow hue ((https://wentbananas.com/why-banana-are-yellow/#:~:text=The%20specific%20type%20of%20carotenoid,yellow%20or%20orange%20fruits%20and)).
```
{% endcode %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/generation/deep_researcher" class="button primary">See more examples on GitHub</a>

That’s it! You've just successfully used the deep researcher module!

## Next Step

1. Combine in an end-to-end RAG pipeline by following the guides in [your-first-rag-pipeline.md](../../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md "mention")
2. Explore more about deep researcher subclasses and features in [API reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/deep_researcher.html)
