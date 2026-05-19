---
icon: flag-pennant
---

# Your First RAG Pipeline

This guide will walk you through setting up a basic RAG pipeline.

<details>

<summary>Prerequisites</summary>

This example specifically requires you to complete all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") and [index-your-data-with-vector-data-store.md](../index-your-data-with-vector-data-store.md "mention") page.

You should be familiar with these concepts and components:

1. [introduction-to-rag.md](../introduction-to-rag.md "mention")
2. [data-store](../../tutorials/data-store/ "mention")
3. [lm-invoker](../../tutorials/inference/lm-invoker/ "mention")
4. [em-invoker.md](../../tutorials/inference/em-invoker.md "mention")
5. [retriever](../../tutorials/retrieval/retriever/ "mention")
6. [repacker.md](../../tutorials/generation/repacker.md "mention")
7. [response-synthesizer.md](../../tutorials/generation/response-synthesizer.md "mention")
8. [orchestration](../../tutorials/orchestration/ "mention")

</details>

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/001_your_first_rag_pipeline" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-datastore
```
{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Folder Structure**

Start by organizing your files (if you have downloaded the Complete Guide Files, you can proceed to the next step). This is the minimal folder structure you can follow, yet you may adjust to your need.

```
<project-name>/
├── data/
│   ├── chroma.sqlite3
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```

{% hint style="info" %}
Don’t worry about creating all these files yourself — we’ll provide the content for each file throughout the tutorial.
{% endhint %}
{% endstep %}

{% step %}
**Prepare your `.env` file**:

Ensure you have a file named `.env` in your project directory with the following content:

```env
EMBEDDING_MODEL="text-embedding-3-small"
LANGUAGE_MODEL="openai/gpt-5-nano"
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

{% hint style="info" %}
This is an example .env file. You may adjust the variables according to your need.
{% endhint %}
{% endstep %}
{% endstepper %}

***

## 1) Index Your Data

{% stepper %}
{% step %}
**Download the database**

For this guide, we provide a preset SQLite database that is loaded with chunks from `imaginary_animals.csv` . You can download them here.

{% file src="../../../.gitbook/assets/database-imaginary-animals-250826 (1).zip" %}
{% endstep %}

{% step %}
**Arrange the files**

Arrange them in your project. You can follow the structure in [#project-setup](your-first-rag-pipeline.md#project-setup "mention") section.
{% endstep %}
{% endstepper %}

You may use another knowledge base file and adjust accordingly. For more information about how to index data to data store, you can visit this page [index-your-data-with-vector-data-store.md](../index-your-data-with-vector-data-store.md "mention").

## 2) Build Core Components of Your Pipeline

### Create the Retriever

The [retriever](../../tutorials/retrieval/retriever/ "mention") finds and pulls useful information from your ChromaDB database. Create `modules/retriever.py`:

{% code lineNumbers="true" %}
```python
import os

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

embedding_model = OpenAIEMInvoker(
    model_name=os.getenv("EMBEDDING_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

data_store = ChromaDataStore(
    collection_name="documents",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=embedding_model)

retriever = VectorRetriever(data_store=data_store)
```
{% endcode %}

**Key Components Explained:**

1. **Environment Loading**: Load settings from your `.env` file
2. **Embedding Model**: `OpenAIEMInvoker` converts text into vector embeddings for similarity search
3. **Data Store**: `ChromaDataStore` connects to your local ChromaDB with persistent storage and vector capability
4. **Retriever**: `VectorRetriever` performs vector similarity search to find relevant documents

{% hint style="info" %}
The embedding model used here must match the one used when indexing the data for proper retrieval functionality..
{% endhint %}

### Create the Response Synthesizer

The [**response synthesizer**](https://gdplabs.gitbook.io/sdk/tutorials/generation/response-synthesizer) generates the final answer using the retrieved context and user query.

Create `modules/response_synthesizer.py`:

{% code lineNumbers="true" %}
```python
import os

from dotenv import load_dotenv
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.repacker import Repacker

load_dotenv()

SYSTEM_PROMPT = """
- Use only the information provided in the context below to answer the user's question.
You may infer simple, logical conclusions based on the context, but do not introduce
new facts or external knowledge.
- If the context does not contain enough information to answer the user's question, respond with:
"Sorry, I don't have enough information to answer that."

Context:
{context}
"""
USER_PROMPT = "Question: {query}"

lm_request_processor = build_lm_request_processor(
    model_id=os.environ["LANGUAGE_MODEL"],
    credentials=os.environ["OPENAI_API_KEY"],
    system_template=SYSTEM_PROMPT,
    user_template=USER_PROMPT,
)

response_synthesizer = ResponseSynthesizer.stuff(
    lm_request_processor=lm_request_processor,
    chunks_repacker=Repacker(mode="chunk"),
)
```
{% endcode %}

**Key Components:**

1. **System Prompt**: Instructs the model to use only provided context and handle insufficient information gracefully
2. **User Prompt**: Templates the user's question for the model
3. **LM Request Processor**: Built using the `build_lm_request_processor()` helper function for simplified setup
4. **Response Synthesizer**: ResponseSynthesizer.static\_list combines all given chunks into a single prompt for response generation

## 3) Build the Pipeline

We'll build the full process in your `pipeline.py` file using GL SDK's [pipeline](https://gdplabs.gitbook.io/sdk/tutorials/orchestration). Open the file and follow these instructions to create [steps](../../tutorials/orchestration/steps/) and compose them:

{% hint style="info" %}
Note that in this guide, the states used as input state and output state are only `user_query`, `chunks`, `context`, `state_variables`, and `response`. The full state structure is defined in [#default-state-ragstate](../../tutorials/orchestration/state.md#default-state-ragstate "mention").\
\
For each step, you can pass state variables as parameters to their corresponding components. For example, [vector-retriever.md](../../tutorials/retrieval/retriever/vector-retriever.md "mention") accepts `query` as parameter, thus you can pass the `"query"` state and takes value from another state (i.e. `"user_query"`) to be mapped.
{% endhint %}

{% stepper %}
{% step %}
**Import the helpers and components**

```python
import asyncio
from gllm_pipeline.steps import step
from modules.retriever import retriever
from modules.response_synthesizer import response_synthesizer
```
{% endstep %}

{% step %}
**Create the Retriever Step**

This [component step](../../tutorials/orchestration/steps/#step) searches for relevant chunks based on the user's query.

```python
retriever_step = step(
    component=retriever,
    input_map={"query": "user_query", "top_k": "top_k"},
    output_state="chunks",
)
```

{% hint style="info" %}
We use `input_map` to map inputs from the pipeline state (or fixed values) to the component's arguments. This is the recommended way to configure steps.
{% endhint %}

Here, the `query` input takes its value from the user input (`user_query`). We also configure `top_k` to control how many results are retrieved.
{% endstep %}

{% step %}
**Create the Response Synthesizer Step**

```python
response_synthesizer_step = step(
    component=response_synthesizer,
    input_map={"query": "user_query", "chunks": "chunks"},
    output_state="response",
)
```

**Key Components:**

1. **System Prompt**: Instructs the model to use only provided context and handle insufficient information gracefully
2. **User Prompt**: Templates the user's question for the model
3. **LM Request Processor**: Built using the `build_lm_request_processor()` helper function for simplified setup
4. **Response Synthesizer**: `ResponseSynthesizer.stuff()` combines all context into a single prompt for response generation.

Note:

1. `"chunks": "chunks"` is the primary data flow in the state.
2. `"kwargs": "chunks"` is for validation compatibility since kwargs should not be empty.
{% endstep %}

{% step %}
**Connect Everything into a Pipeline**

Finally, use the [pipe operator](../../tutorials/orchestration/pipeline.md#the-pipe-operator) (`|`) to chain all steps in order:

```python
e2e_pipeline = retriever_step | response_synthesizer_step
```
{% endstep %}
{% endstepper %}

## 4) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

{% stepper %}
{% step %}
**Configure and invoke the pipeline**

Configure the state and config for direct pipeline invocation:

```python
state = {
    "user_query": "Give me nocturnal creatures from the dataset",  # Replace with your actual query
    "event_emitter": None,
}

config = {
    "top_k": 5,
    "debug": True,  # Set to True to look at the pipeline execution flow
}

result = asyncio.run(e2e_pipeline.invoke(state, config))
print(f"Pipeline result: {result['response']}")
```
{% endstep %}

{% step %}
**Run `pipeline.py` file**

```
python pipeline.py
```
{% endstep %}

{% step %}
**Observe output**

If you successfully run all the steps, you will see something like this:

```
Building 'OpenAILMInvoker' with config:
  {'model_name': 'gpt-5-nano'}

[Start 'VectorRetriever'] Processing input:
    - query: 'Give me nocturnal creatures from the dataset'
    - top_k: 5
    - embeddings: POST /v1/embeddings → 200
    - vector search: ES /data/_search → 200
[Finished 'VectorRetriever'] Retrieved 5 chunks
    1) Nightwhisper Owl (score 0.7234)
    2) Shadowpounce Lynx (0.6987)
    3) Glowfin Eel (0.6812)
    4) Moonscale Serpent (0.6745)
    5) Stargazer Bat (0.6698)

[Start 'StuffResponseSynthesizer'] Processing query
    - LM invoke: POST /v1/responses → 200
[Finished 'StuffResponseSynthesizer'] Response:
    Here are nocturnal creatures from the dataset:
      1. Nightwhisper Owl
      2. Shadowpounce Lynx
      3. Glowfin Eel

Pipeline result: Here are nocturnal creatures from the dataset:
1. Nightwhisper Owl
2. Shadowpounce Lynx
3. Glowfin Eel
```
{% endstep %}
{% endstepper %}

Congratulations! You've successfully built your first RAG pipeline.
