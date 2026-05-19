---
icon: brain
---

# LM-Based Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [lm-based-router.md](lm-based-router.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

The **LM-Based Router** uses a language model to intelligently determine the appropriate route for a given input. This approach leverages the reasoning capabilities of LMs for flexible, context-aware routing decisions.

<details>

<summary>Prerequisites</summary>

This tutorial requires familiarity with these concepts:

1. [lm-invoker](../../inference/lm-invoker/ "mention") - For understanding language model invocation
2. [lm-request-processor.md](../../inference/lm-request-processor.md "mention") - For configuring LM request processing

</details>

## Installation

```bash
pip install gllm-pipeline gllm-inference
```

## Basic Usage

### Step 1: Set up the LM Request Processor

```python
import asyncio
from gllm_inference.request_processor import build_lm_request_processor
from gllm_pipeline.router import LMBasedRouter

# Create an LM request processor
lm_processor = build_lm_request_processor(
    lm_invoker_kwargs={
        "model_id": "openai/gpt-5-nano",
        "credentials": "<YOUR_OPENAI_API_KEY>"
    },
    prompt_builder_kwargs={
        "system_template": "You are a customer support routing assistant.",
        "user_template": "Route this query to the appropriate department: {source}"
    }
)
```

### Step 2: Create the router

```python
router = LMBasedRouter.native(
    lm_request_processor=lm_processor,
    default_route="general",
    valid_routes={"billing", "tech_support", "sales", "general"},
    lm_output_key="route",  # Key in LM output containing the route
)
```

### Step 3: Route queries

```python
# Route a single query
query = "My credit card was charged twice"
route = asyncio.run(router.route(query))
print(f"Selected route: {route}")  # Output: "billing"

# Route with filtering
route = asyncio.run(
    router.route(query, route_filter={"billing", "general"})
)
```

## Advanced Configuration

### Custom Output Parsing

Configure how the LM output is parsed:

```python
lm_processor = build_lm_request_processor(
    lm_invoker_kwargs={
        "model_id": "openai/gpt-5-nano",
        "credentials": "<YOUR_OPENAI_API_KEY>"
    },
    prompt_builder_kwargs={
        "system_template": """You are a routing assistant. Analyze the query and respond with JSON.

Available routes: billing, tech_support, sales, general

Respond in this format:
{
    "route": "<selected_route>",
    "confidence": <0-1>,
    "reason": "<brief explanation>"
}""",
        "user_template": "{source}"
    }
)

router = LMBasedRouter.native(
    lm_request_processor=lm_processor,
    default_route="general",
    valid_routes={"billing", "tech_support", "sales", "general"},
    lm_output_key="route",
)
```

### Multi-Step Routing

Use the LM for more complex routing logic:

```python
lm_processor = build_lm_request_processor(
    lm_invoker_kwargs={
        "model_id": "openai/gpt-5-nano",
        "credentials": "<YOUR_OPENAI_API_KEY>"
    },
    prompt_builder_kwargs={
        "system_template": """You are an intelligent routing assistant.

Step 1: Identify the query type (complaint, question, request)
Step 2: Identify the domain (billing, technical, sales)
Step 3: Select the appropriate route

Routes:
- billing_complaint: For billing complaints
- billing_question: For billing questions
- tech_support: For technical issues
- sales_inquiry: For sales questions
- general: For everything else

Respond with JSON: {"route": "<route>"}""",
        "user_template": "{source}"
    }
)

router = LMBasedRouter.native(
    lm_request_processor=lm_processor,
    default_route="general",
    valid_routes={
        "billing_complaint",
        "billing_question",
        "tech_support",
        "sales_inquiry",
        "general"
    },
    lm_output_key="route",
)
```

## Complete Example

```python
import asyncio
from gllm_inference.request_processor import build_lm_request_processor
from gllm_pipeline.router import LMBasedRouter

async def main():
    # Setup LM processor
    lm_processor = build_lm_request_processor(
        lm_invoker_kwargs={
            "model_id": "openai/gpt-5-nano",
            "credentials": "<YOUR_OPENAI_API_KEY>"
        },
        prompt_builder_kwargs={
            "system_template": """You are a customer support routing assistant.
Analyze the customer query and route it to the appropriate department.

Available routes:
- billing: Payment, invoices, refunds
- tech_support: Technical issues, bugs, errors
- sales: Product questions, pricing, features
- general: General inquiries

Respond with JSON: {"route": "<route>"}""",
            "user_template": "Customer query: {source}"
        }
    )

    # Create router
    router = LMBasedRouter.native(
        lm_request_processor=lm_processor,
        default_route="general",
        valid_routes={"billing", "tech_support", "sales", "general"},
        lm_output_key="route",
    )

    # Test queries
    queries = [
        "My credit card was charged twice for my subscription",
        "The app keeps crashing when I try to upload files",
        "What are the pricing plans for enterprise customers?",
        "How do I contact support?",
    ]

    for query in queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")

asyncio.run(main())
```

## Configuration Options

### LM Model Selection

Choose different models for different routing complexity:

```python
# Fast, cost-effective routing
lm_processor = build_lm_request_processor(
    lm_invoker_kwargs={
        "model_id": "openai/gpt-5-nano",
        "credentials": "<YOUR_OPENAI_API_KEY>"
    },
    prompt_builder_kwargs={...}
)

# More accurate routing with reasoning
lm_processor = build_lm_request_processor(
    lm_invoker_kwargs={
        "model_id": "openai/gpt-4",
        "credentials": "<YOUR_OPENAI_API_KEY>"
    },
    prompt_builder_kwargs={...}
)
```

### Route Filtering

Restrict available routes at runtime:

```python
# Only allow specific routes for this query
route = asyncio.run(
    router.route(
        query,
        route_filter={"billing", "general"}  # Must include default_route
    )
)
```

## Best Practices

1. **Clear Instructions**: Provide explicit routing instructions in the system prompt
2. **Route Descriptions**: Describe each route clearly so the LM understands the distinctions
3. **JSON Responses**: Use structured JSON output for reliable parsing
4. **Fallback Handling**: Set a sensible default route for edge cases
5. **Testing**: Test with diverse queries to ensure consistent routing
6. **Cost Monitoring**: LM-based routing incurs API costs; monitor usage

## Troubleshooting

**Router selecting wrong routes?**
- Improve the system prompt with clearer route descriptions
- Add examples of queries for each route
- Use a more capable model (e.g., GPT-4 instead of GPT-3.5)

**Parsing errors?**
- Ensure LM output format matches `lm_output_key`
- Add explicit format instructions to the prompt
- Use structured output formats (JSON)

**High latency?**
- Use faster models (GPT-3.5-turbo)
- Cache LM responses if routing patterns are repetitive
- Consider hybrid approaches (rules + LM)

## See Also

- [Semantic Router](semantic-router/) - Embedding-based routing
- [Similarity-Based Router](similarity-based-router.md) - Similarity-based routing
- [Rule-Based Router](rule-based-router.md) - Pattern and keyword-based routing

[^1]: This component may involve Language Model (LM). See [lm-request-processor.md](../../inference/lm-request-processor.md "mention") for more information.
