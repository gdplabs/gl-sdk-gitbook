---
icon: flag-checkered
---

# Getting Started

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [lm-invoker](../gen-ai-sdk/tutorials/inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../gen-ai-sdk/tutorials/inference/lm-request-processor.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-generation"
```
{% endtab %}
{% endtabs %}

## Quickstart

Let’s jump into a basic example of using the deep researcher. In this example, we'll use an event emitter with a print event handler, which allows us to see the deep research progress in real time.

{% hint style="info" %}
Each example uses the same `research()` interface while swapping out the underlying deep research provider. This allows different providers to be used interchangeably, without changing the calling logic that invokes the Component.

Each example follows the same flow:

1. define a research query;
2. invoke deep research using the same `research()` call;
3. receive streamed progress and final results via an event emitter.
{% endhint %}

Below are minimal examples that perform deep research using the GL SDK:

{% tabs %}
{% tab title="GL-ODR" %}
1. Obtain API Key (Contact the GL Open DeepResearch Team to obtain your API key). Configure it via the `api_key` argument or the environment variable.

```bash
export GLODR_API_KEY=...
```

2. Run this code:

```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import GLOpenDeepResearcher

query = "Create a concise report about why bananas are yellow."
event_emitter = EventEmitter.with_print_handler()

deep_researcher = GLOpenDeepResearcher()
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endtab %}

{% tab title="Google" %}
1. Obtain API Key and configure it via the `api_key` argument or the environment variable.

```bash
export GOOGLE_API_KEY=...
```

2. Run this code:

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import GoogleDeepResearcher

query = "Create a concise report about why bananas are yellow."
event_emitter = EventEmitter.with_print_handler()

deep_researcher = GoogleDeepResearcher()
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}
{% endtab %}

{% tab title="Parallel.ai" %}
1. Obtain API Key and configure it via the `api_key` argument or the environment variable.

```bash
export PARALLEL_API_KEY=...
```

2. Run this code:

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import ParallelDeepResearcher

query = "Create a concise report about why bananas are yellow."
event_emitter = EventEmitter.with_print_handler()

deep_researcher = ParallelDeepResearcher()
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}
{% endtab %}

{% tab title="Perplexity" %}
1. Obtain API Key and configure it via the `api_key` argument or the environment variable.

```bash
export PERPLEXITY_API_KEY=...
```

2. Run this code:

<pre class="language-python" data-line-numbers data-expandable="true"><code class="lang-python">from dotenv import load_dotenv
<strong>load_dotenv()
</strong>
import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import PerplexityDeepResearcher

query = "Create a concise report about why bananas are yellow."
event_emitter = EventEmitter.with_print_handler()

deep_researcher = PerplexityDeepResearcher()
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
</code></pre>
{% endtab %}

{% tab title="OpenAI" %}
1. Obtain API Key and configure it via the `api_key` argument or the environment variable.

```bash
export OPENAI_API_KEY=...
```

2. Run this code:

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import OpenAIDeepResearcher

query = "Create a concise report about why bananas are yellow."
event_emitter = EventEmitter.with_print_handler()

deep_researcher = OpenAIDeepResearcher()
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}
{% endtab %}
{% endtabs %}

**Expected Output**

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

1. Take a look into some additional capabilities of the deep researcher components in [customization-and-capability.md](tutorials/customization-and-capability.md "mention")
2. Integrate deep research in a pipeline in [Broken link](/broken/pages/dQgNdO39jrtktDUX5sHh "mention")
3. Explore more about deep researcher subclasses and features in [API reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/deep_researcher.html)
