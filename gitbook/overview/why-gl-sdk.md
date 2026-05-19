---
icon: message-question
---

# Why GL SDK?

In the rapidly evolving landscape of AI development, choosing the right tools can make all the difference between rapid innovation and getting bogged down in complexity. The GL SDK stands out by offering a unique blend of power, simplicity, and unparalleled developer experience, especially when compared to traditional open-source alternatives.

1. **Low Code:** Achieve complex AI tasks in as few as **five lines of code**, drastically **accelerating development and reducing errors**. This principle ensures rapid iteration and a focus on innovation over boilerplate.
2. **Simple, But Flexible:** The SDK offers **straightforward solutions for common tasks** without sacrificing the **granular control** needed for **advanced use cases or customization**. You get both ease of use and the power to adapt to any requirement.
3. **Low Maintenance:** We handle all the **underlying open-source dependency management, updates, and compatibility,** so you gain stability, security, and the latest advancements without the usual headaches. **Your applications simply "just work."**
4. **One-Stop Shop:** The GL SDK provides a **comprehensive, integrated solution for building production-ready** AI applications across the entire development lifecycle. This **eliminates the need to stitch together disparate tools**, streamlining your workflow significantly.
5. **Designed with Developer Experience in Mind:** Meticulously crafted for intuitive use, the SDK combines **clear documentation and tutorials with its low-code approach**, quickly making beginners productive. It’s powerful, yet a joy to use.

## Low Code

The GL SDK adheres to the '**five lines of code'** principle, enabling complex tasks to be achieved with remarkable brevity, often in **five statements or less**. This significantly accelerates development cycles and reduces the potential for errors, allowing you to focus on innovation rather than boilerplate.

Here are some examples across the GL SDK ecosystem.

{% tabs %}
{% tab title="AI Agents Package (AIP)" %}
Learn more about creating AI Agents [here](https://gdplabs.gitbook.io/sdk/gl-aip/tutorials/hands-on-examples).

```python
from glaip_sdk import Client

client = Client()

agent = client.create_agent(
    name="hello-world-agent",
    instruction="You are a friendly AI assistant."
)
agent.run("Hello! How are you today?")

agent.delete()
```
{% endtab %}

{% tab title="GL Connectors" %}
Learn more about authenticating and using connectors here in [Broken link](/broken/pages/A2YFoQ4N2x1TWWoyHz4e "mention")

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_key="GL_CONNECTORS_API_KEY")

response = (connector.connect('google_drive')
    .action('search_files')
    .params({"query": "name contains 'wfo'"})
    .token('GL_CONNECTORS_USER_TOKEN')
    .run())

print(response.get_data())
```
{% endtab %}

{% tab title="GLLM" %}
Learn more about calling language models [here](../gen-ai-sdk/tutorials/inference/lm-invoker/).

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
print(asyncio.run(lm_invoker.invoke("What is the capital city of Indonesia?")))
```
{% endtab %}
{% endtabs %}

## Simple, But Flexible

The GL SDK strives to be **as simple as possible** without sacrificing flexibility.

For instance, compare the following code to create a simple custom RAG pipeline using LangGraph vs. using [GLLM Pipeline](../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/).

{% tabs %}
{% tab title="With LangGraph" %}
```python
import asyncio
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime

from prebuilt.response_synthesizer import response_synthesizer
from prebuilt.retriever import retriever


class State(TypedDict):
    user_query: str
    chunks: list
    response: str


class Context(TypedDict):
    top_k: int


def execute_retrieve(state: State, runtime: Runtime[Context]) -> State:
    top_k = runtime.context["top_k"]
    state_update = {"chunks": asyncio.run(retriever.retrieve(state["user_query"], top_k=top_k))}
    return state_update


def execute_synthesize(state: State) -> State:
    state_update = {"response": asyncio.run(response_synthesizer.synthesize(state["user_query"], state["chunks"]))}
    return state_update


graph = StateGraph(State, context_schema=Context)

graph.add_node("retrieve", execute_retrieve)
graph.add_node("synthesize", execute_synthesize)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "synthesize")
graph.add_edge("synthesize", END)

pipeline = graph.compile()
```
{% endtab %}

{% tab title="With GLLM Pipeline" %}
```python
from gllm_pipeline.steps import step

from prebuilt.response_synthesizer import response_synthesizer
from prebuilt.retriever import retriever

retriever_step = step(
    component=retriever,
    input_map={"query": "user_query", "top_k": "top_k"},
    output_state="chunks",
)

response_synthesizer_step = step(
    component=response_synthesizer,
    input_map={
        "query": "user_query",
        "chunks": "chunks",
    },
    output_state="response",
)

pipeline = retriever_step | response_synthesizer_step
```
{% endtab %}
{% endtabs %}

At GL SDK, **flexibility does not have to come at the expense of simplicity**.

## Low Maintenance

The GL SDK acts as a robust wrapper around **100+ open-source frameworks, packages, and libraries.** This means you gain all the power and flexibility of the open-source ecosystem without the burden of constant maintenance, dependency management, or version conflicts. We handle the upkeep, updates, and compatibility, ensuring your applications remain stable, secure, and performant with the latest advancements.

## One-Stop Shop

The GL SDK is your comprehensive, one-stop solution for building production-ready AI applications, from computer vision to agentic workflows. Explore our extensive [features list](feature-overview/detailed-features.md), containing **100+ features** to unlock the full potential of your projects.

## Designed with Developer Experience in Mind

We believe that a powerful SDK must also be a joy to use. The GL SDK is meticulously designed with developer experience at its core, ensuring it's not just complete but also intuitively easy to navigate. This commitment to usability, combined with our 'Low Code' philosophy, means you'll find comprehensive user guides, practical tutorials, and helpful how-tos that quickly transform beginners into productive developers.

Check out some of our tutorials and how-to guides:

1. [lm-invoker](../gen-ai-sdk/tutorials/inference/lm-invoker/ "mention")
2. [evaluation](../gen-ai-sdk/tutorials/evaluation/ "mention")
3. [build-end-to-end-rag-pipeline](../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/ "mention")
4. [build-document-processing-pipeline](../gen-ai-sdk/guides/build-document-processing-pipeline/ "mention")

<br>
