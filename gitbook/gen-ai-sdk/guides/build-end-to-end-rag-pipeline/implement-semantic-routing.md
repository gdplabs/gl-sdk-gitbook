---
icon: compass
---

# Implement Semantic Routing

This guide will walk you through **adding semantic routing to your existing RAG pipeline** to intelligently route different types of queries to specialized handlers.

**Semantic routing** allows your pipeline to automatically decide whether a query needs **knowledge base retrieval** or can be answered with **general knowledge**, making your application more efficient and providing better responses.

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [Routing](../../tutorials/orchestration/routing/README.md "mention") - Overview of available router types
3. [Semantic Router](../../tutorials/orchestration/routing/semantic-router/README.md "mention") - Detailed semantic routing documentation
4. [#switch](../../tutorials/orchestration/steps/#switch "mention") step

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/003_implement_semantic_routing" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```

{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial. You'll extend the project structure as follows:

```
implement-semantic-routing/
├── data/
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py            # 👈 Will be updated with semantic router
├── pyproject.toml
├── route_examples.json
├── setup.bat
├── setup.sh
└── uv.lock
```

{% endstep %}

{% step %}
**Create the route examples file**

Create a new file `route_examples.json` to define your routing categories. This file uses a list of objects with `name` and `utterances` fields:

```json
[
  {
    "name": "knowledge_base",
    "utterances": [
      "What unique feature makes the Luminafox glow in the dark?",
      "How does the Luminafox attract its prey?",
      "Which folklore belief is associated with sighting a Luminafox?",
      "What adaptation allows the Aquaflare to survive near volcanic isles?",
      "What does the Aquaflare feed on in its extreme environment?",
      "Give me 3 aquatic animals",
      "Name 2 nocturnal creatures mentioned in the dataset",
      "List 3 animals that can generate or store electricity",
      "Which 2 creatures are known to glow or emit light?"
    ]
  },
  {
    "name": "general",
    "utterances": [
      "What is the capital of France?",
      "General knowledge question",
      "Tell me about history",
      "What is the meaning of life?",
      "How does photosynthesis work?",
      "What are the benefits of exercise?",
      "Tell me about space exploration",
      "What is machine learning?",
      "How do plants grow?",
      "What is the population of Tokyo?",
      "How do I make a cake?",
      "Why is the sky blue?"
    ]
  }
]
```

{% hint style="info" %}
The route examples define which types of queries should go to your knowledge base vs. general knowledge. The code automatically converts this JSON format to a dictionary mapping route names to utterance lists. Customize these based on your specific use case.
{% endhint %}
{% endstep %}
{% endstepper %}

---

## 1) Build Semantic Routing Components

### Create the Semantic Router

The **semantic router** analyzes incoming queries and determines which specialized handler should process them. It uses embedding similarity to match queries against predefined route examples loaded from your JSON file.

Create `modules/semantic_router.py`:

{% code lineNumbers="true" %}

```python
import os
import json

from dotenv import load_dotenv
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

load_dotenv()

# Create embedding model invoker
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials=os.getenv("OPENAI_API_KEY")
)

# Load route examples from JSON file
with open("route_examples.json", "r", encoding="utf-8") as f:
    route_examples_data = json.load(f)

# Convert JSON format to route_examples dict
route_examples = {
    route["name"]: route["utterances"]
    for route in route_examples_data
}

# Create semantic router with Aurelio backend
semantic_router = SemanticRouter.aurelio(
    default_route="general",
    valid_routes={"knowledge_base", "general"},
    encoder=em_invoker,
    route_examples=route_examples,
    similarity_threshold=0.3,
)
```

{% endcode %}

**Key Components:**

- **Encoder**: Uses the same embedding model as your retriever for consistency (can be any `BaseEMInvoker`)
- **Similarity Threshold**: 0.3 provides balanced routing sensitivity
- **Route Examples**: Dictionary mapping route names to lists of example utterances
- **Default Route**: Falls back to general responses when uncertain

### Create the General Query Handler

For queries that don't need knowledge base retrieval, we'll create a specialized **response synthesizer** that can answer general knowledge questions directly.

Create `modules/handlers.py`:

{% code lineNumbers="true" %}

```python
import os

from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.response_synthesizer import ResponseSynthesizer

response_synthesizer_general = ResponseSynthesizer.stuff(
    lm_request_processor=build_lm_request_processor(
        model_id="openai/gpt-5-nano",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="You are a helpful assistant that answers general knowledge questions.",
        user_template="{query}",
    )

)
```

{% endcode %}

**Key features:**

- Optimized for general knowledge questions
- No retrieval needed - uses the model's built-in knowledge
- Faster responses for queries that don't need your specific data

### Create the Enhanced Pipeline

Now we'll update your existing RAG pipeline to include semantic routing using a **switch step** that intelligently decides between knowledge base retrieval and general responses.

{% stepper %}
{% step %}
**Create the general query step**

This handles queries that don't need knowledge base retrieval:

{% code lineNumbers="true" %}

```python
from gllm_pipeline.steps import step
# Add general query step
synthesize_general_step = step(
    component=response_synthesizer_general,
    input_map={
        "query": "user_query",
    },
    output_state="response",
)
```

{% endcode %}
{% endstep %}

{% step %}
**Create the switch step**

This is the core routing logic that decides which path to take:

{% code lineNumbers="true" %}

```python
from gllm_pipeline.steps import switch

# Implement switch step to wrap the pipeline with semantic router as condition
conditional_step = switch(
    condition = semantic_router,
    branches = {
        "knowledge_base": [retrieve_step, synthesize_step],
        "general": synthesize_general_step,
    },
    default = synthesize_general_step,
    input_map = {"source": "user_query"},
    output_state = "response",
)
```

{% endcode %}

**How it works:**

- **knowledge_base route**: Triggers your full RAG pipeline (retrieval → synthesis)
- **general route**: Uses the general handler for direct responses
- **default**: Falls back to general responses if routing fails
  {% endstep %}

{% step %}
**Define the enhanced state and pipeline**

Extend the RAG state and create the final pipeline:

<pre class="language-python" data-line-numbers><code class="lang-python"># Define state type for the pipeline, extend RAGState
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.pipeline.states import RAGState

<strong>class RouterState(RAGState):
</strong>    route: str
    source: str

# Initialize the pipeline with the conditional step and the state type
e2e_pipeline = Pipeline(steps=[conditional_step], state_type=RouterState)
</code></pre>

This creates a pipeline that:

1. Analyzes the query with semantic routing
2. Either retrieves from your knowledge base OR answers directly
3. Returns the most appropriate response

> 🧠 _The switch step acts as an intelligent dispatcher, seamlessly integrating your existing RAG pipeline with new routing capabilities._
> {% endstep %}
> {% endstepper %}

## 2) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

{% stepper %}
{% step %}
**Configure and invoke the pipeline**

Configure the state and config for direct pipeline invocation:

```python
async def main():
    state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
```

{% endstep %}

{% step %}
**Test with knowledge base queries**

Try these queries with `debug: true` to see the routing in action:

**Knowledge Base Examples:**

```python
"Give me nocturnal creatures from the dataset"
"What unique feature makes the Luminafox glow in the dark?"
"List 3 animals that can generate or store electricity"
```

You should see in the debug logs that these get routed to the `knowledge_base` handler and trigger your RAG pipeline.
{% endstep %}

{% step %}
**Test with general knowledge queries**

Try these general knowledge questions:

**General Knowledge Examples:**

```python
"What is the capital of Japan?"
"How does photosynthesis work?"
"What are the benefits of exercise?"
```

These should be routed to the `general` handler and get direct responses without retrieval.
{% endstep %}

{% step %}
**Verify routing decisions**

With `debug: true`, you should see logs showing:

- Which route was selected
- The similarity scores for each route. Observe how the similarity threshold affects routing decisions.
- Which handler was executed
- The specialized response format
  {% endstep %}
  {% endstepper %}

## Understanding the Flow

Here's what happens when a query comes in:

1. **Query Analysis**: The semantic router compares the incoming query against route examples from your JSON file using embedding similarity
2. **Route Selection**: The route with the highest similarity score (above the threshold) is selected
3. **Switch Execution**: The switch step executes the appropriate pipeline branch based on the selected route:
   - **knowledge_base**: Triggers your full RAG pipeline (retrieval → synthesis)
   - **general**: Uses the general handler for direct model responses
4. **Pipeline Processing**: Either your RAG components or general handler processes the query
5. **Response Generation**: The appropriate pipeline returns a response optimized for the query type

## Troubleshooting

1. **Routes not working as expected**:
   1. Check your route examples - they should be representative and diverse
   2. Verify the similarity threshold isn't too high or too low
   3. Add more examples for better classification
2. **All queries going to default route**:
   1. Lower the similarity threshold
   2. Add more diverse examples to your route categories
   3. Check that your embedding model is working correctly
3. **Queries always going to general route**:
   1. Check your `route_examples.json` - ensure knowledge base examples are specific and diverse and the file is correctly imported
   2. Lower the score threshold in the encoder
   3. Add more knowledge base examples that match your specific use cases
   4. Use debug mode to see similarity scores and understand why routes aren't matching
   5. Check retry configuration (if a APIConnectionError or TimeoutError is raised, it might due to short timeout configuration)
4. **Wrong route selection**:
   1. Review and improve your route examples
   2. Consider adding negative examples or adjusting thresholds
   3. Use debug mode to see similarity scores

---

Congratulations! You've successfully enhanced your RAG pipeline with semantic routing. Your pipeline now intelligently decides between using your knowledge base and providing general responses, making your application more efficient and delivering better user experiences.
