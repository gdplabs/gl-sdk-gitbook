# Evaluate Your AI Agent's Q&A Pipeline

This tutorial walks through evaluating a tool-calling agent pipeline using `GEvalGenerationEvaluator`. It follows the [Evals Lifecycle](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle): define the system → prepare a dataset → choose metrics → evaluate → calibrate.

{% hint style="info" %}
**New to GL SDK evaluation?** Read the [Evals Lifecycle](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle) page first. This tutorial is a worked example of that lifecycle for a tool-calling agent.
{% endhint %}

***

## 🚀 Getting Started

{% stepper %}
{% step %}
**Clone the repository & open the directory**

```bash
git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/use-case/agent_qna_evaluations
```
{% endstep %}

{% step %}
**Install dependencies using UV**

```bash
make sync
```
{% endstep %}

{% step %}
**Prepare your `.env` file**

```env
GOOGLE_API_KEY="AIza..."
```
{% endstep %}
{% endstepper %}

***

## Step 1: Define the Target System

> *Before you can measure anything, you need to agree on what you are measuring. Your tech lead opens a doc and asks: "What does this system do, exactly?"*

This step sounds obvious, but writing it down forces a clarification that matters for every step that follows.

| Field | Value |
| --- | --- |
| **System type** | Tool-calling AI agent |
| **Task** | Answer product and order questions by calling internal API tools |
| **Inputs** | A user query sent to the agent |
| **Outputs** | A response that is **grounded** (no hallucinations), **non-redundant**, and covers the key facts |

### Available Tools

The agent has access to three tools. Unlike structured database queries, these tools crawl internal web pages and documentation to fetch data. This distinction matters for evaluation: crawling is non-deterministic — the same query may return different results depending on what pages are currently indexed, accessible, or paginated.

| Tool | What It Does |
| --- | --- |
| `get_product_integrations` | Crawls product pages to find supported platform integrations |
| `get_order_status` | Queries the order management system for order details |
| `get_supported_languages` | Crawls product documentation to find supported programming languages |

***

## Step 2: Prepare the Dataset

> *You ask a domain expert to write down three questions real customers regularly ask, and for each one, write what they consider a correct answer. "Think of it as writing the answer key," you say.*

A dataset is a collection of test cases that represent real usage. Even 3 well-chosen cases written by someone who knows the domain can expose meaningful failure modes. The key insight: the domain expert writes the expected outputs — not an engineer, not the LLM. The CSV stores only fixed reference data — `actual_output` and `retrieved_context` are filled at eval time from the mock agent.

| # | `query` | `expected_output` | `expected_tools` |
| --- | --- | --- | --- |
| 1 | What cloud platforms does CloudDeploy Pro support? | CloudDeploy Pro supports AWS, Google Cloud, Azure, DigitalOcean, and Heroku. | `[{"name": "get_product_integrations", "input_parameters": {"product": "CloudDeploy Pro"}}]` |
| 2 | What is the delivery date for order ORD-7743? | Order ORD-7743 is scheduled for delivery on May 20th, 2025. | `[{"name": "get_order_status", "input_parameters": {"order_id": "ORD-7743"}}]` |
| 3 | What programming languages does CodeScan support? | CodeScan supports Python, JavaScript, TypeScript, Java, Go, Ruby, and Rust. | `[{"name": "get_supported_languages", "input_parameters": {"product": "CodeScan"}}]` |

`expected_tools` is a list of `ToolCall` objects — each can include `name`, `input_parameters`, and optionally `output`. In this dataset we focus on `name` and `input_parameters` to document which tool the agent is expected to call and with what arguments. The tool output is what the agent actually received at runtime, not a fixed reference.

***

## Step 3: Define Metrics and Success Criteria

> *Question: "What makes an agent answer good?" The domain expert says three things: "It should cover the key facts. It shouldn't make things up. And please — no rambling." You write those down. Each one maps directly to a metric.*

For a tool-calling agent answering factual questions, four metrics cover the failure modes identified earlier:

| Metric | What It Measures | `higher_is_better` | Default Threshold |
| --- | --- | --- | --- |
| `tool_correctness` | The agent called the right tool with the right input arguments | `true` | `0.5` |
| `completeness` | All key facts from `expected_output` are present in `actual_output` | `true` | `1.0` |
| `groundedness` | Every claim in `actual_output` is supported by `retrieved_context` | `true` | `1.0` |
| `redundancy` | `actual_output` does not contain unnecessary repetition | `false` | `0.5` |

`tool_correctness` is included from the start — not as a calibration step — because the dataset already has `expected_tools`. It gives an early signal on whether the agent routed correctly, independently of generation quality.

***

## Step 4: Evaluate and Improve

### The Evaluation Script

> *With dataset and metrics defined, you open `eval.py` and write the evaluation. The goal: run every test case through the mock agent, collect the outputs, then hand everything to the judge in one call.*

This example uses `MOCK_AGENT_OUTPUTS` to simulate agent responses without running a live agent — it simplifies the setup so you can focus on the evaluation logic. When writing your own evals, replace `run_agent()` with your actual agent invocation.

{% code title="eval.py" lineNumbers="true" %}
```python
MOCK_AGENT_OUTPUTS: dict[str, tuple[str, list[dict]]] = {
    "What cloud platforms does CloudDeploy Pro support?": (
        "CloudDeploy Pro supports AWS, Google Cloud, and Azure.",
        [
            {
                "name": "get_product_integrations",
                "input_parameters": {"product": "CloudDeploy Pro"},
                "output": {
                    # Note: DigitalOcean and Heroku absent — tool retrieval gap
                    "supported_platforms": ["AWS", "Google Cloud", "Azure"],
                },
            }
        ],
    ),
    # ... (Cases 2 and 3 follow the same structure)
}


def run_agent(query: str) -> tuple[str, list[dict], str]:
    actual_output, tools_called = MOCK_AGENT_OUTPUTS[query]
    return actual_output, tools_called, json.dumps(tools_called)


async def main():
    agent_results = [run_agent(row["query"]) for row in DATASET]

    # CSV provides input/expected_output/expected_tools;
    # agent mock provides actual_output/tools_called/retrieved_context.
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=actual_output,
            expected_output=row["expected_output"],
            retrieved_context=retrieved_context,
            tools_called=ToolCall.from_dicts(tools_called_list),
            expected_tools=ToolCall.from_dicts(json.loads(row["expected_tools"])),
        )
        for row, (actual_output, tools_called_list, retrieved_context) in zip(DATASET, agent_results)
    ]

    # tool_correctness checks agent routing; completeness/groundedness/redundancy
    # check generation quality. evaluation_params limits to name + args only.
    experiment_result = await evaluate(
        data=data,
        evaluators=[
            GEvalGenerationEvaluator(
                models=judge_model,
                metrics=[
                    DeepEvalToolCorrectnessMetric(
                        evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
                    ),
                    GEvalCompletenessMetric(),
                    GEvalGroundednessMetric(),
                    GEvalRedundancyMetric(),
                ],
            )
        ],
        experiment_tracker=tracker,
    )
```
{% endcode %}

Run the evaluation:

```bash
make run-eval
```

### First Run Results

> *The results come in. Case 2 passes cleanly. Then you see Cases 1 and 3: `aggregate_success: False`. You read the judge explanations.*

```python
{
  'run_id': 'agent-qna-eval_...',
  'num_samples': 3,
  'results': [
    [{'generation': {'aggregate_success': False, 'aggregate_score': 0.88,
        'tool_correctness': {'score': 1.0, 'success': True,  ...},
        'completeness':     {'score': 0.5, 'success': False, 'threshold': 1.0, ...},
        'groundedness':     {'score': 1.0, 'success': True,  ...},
        'redundancy':       {'score': 0.0, 'success': True,  ...}}}],
    [{'generation': {'aggregate_success': True, 'aggregate_score': 1.0, ...}}],
    [{'generation': {'aggregate_success': False, 'aggregate_score': 0.88,
        'tool_correctness': {'score': 1.0, 'success': True,  ...},
        'completeness':     {'score': 0.5, 'success': False, 'threshold': 1.0, ...},
        'groundedness':     {'score': 1.0, 'success': True,  ...},
        'redundancy':       {'score': 0.0, 'success': True,  ...}}}],
  ],
}
```

Cases 1 and 3 fail `completeness` — but `tool_correctness` passes for both. The agent called the right tool with the right arguments. The failure is in the generation metric, not the agent's routing.
- Case 1 explanation: *"The minimum key facts are: [AWS], [Google Cloud], [Azure], [DigitalOcean], and [Heroku]. The Generated Response matches three but is missing [DigitalOcean] and [Heroku]. Partial coverage."*
- Case 3 explanation: *"The minimum key facts include [Ruby] and [Rust]. The Generated Response matches five but is missing Ruby and Rust. Partial coverage."*
- Case 2 passes. The tool call outputs confirm why: `get_product_integrations` returned only 3 of 5 platforms; `get_supported_languages` returned only 5 of 7 languages. `groundedness: 1.0` for all — the agent reported exactly what the tools returned.

***

## Step 5: Calibrate the Evals

> *Before closing the laptop, your tech lead asks the second uncomfortable question: "The completeness score says the agent failed — but `tool_correctness` passes. The agent called the right tool. So why does completeness fail?" You look at the tool outputs and realize: these tools crawl product pages. They don't query a structured database. The crawler returned what it found — not necessarily everything that exists.*

Calibration answers one question: **can I trust what these scores tell me?** `tool_correctness` already confirmed the agent routed correctly. So the completeness failure must come from the eval metric comparing against a static reference — not from the agent's behavior.

The problem is structural:
1. The crawler may not find all items depending on page structure, indexing state, or pagination.
2. `completeness` compares the response against a fixed `expected_output`. If the crawler returns fewer items, the agent faithfully reports fewer — and `completeness` penalizes it for the crawler's gap.
3. The correct question is: *was the context the crawler returned sufficient to answer the query?* That is what `context_sufficiency` measures.

### Why `completeness` Is the Wrong Metric Here

Reviewing the failures with domain experts surfaces a structural problem with using `completeness` for these queries — not just a one-time tool gap:

**1. The tool uses web crawling, not structured queries.** `get_product_integrations` and `get_supported_languages` crawl product pages to find data. Crawling is non-deterministic: the same query may return different results depending on which pages are indexed, accessible, or paginated at the time. A fixed `expected_output` is not a reliable reference for crawler output.

**2. Catalog data grows continuously.** Supported platforms and languages expand with each product release. A fixed `expected_output` becomes stale independently of crawler behavior — today it lists 5 platforms, next quarter it should list 7. Every release requires manually updating the reference, or `completeness` will flag a correct answer as failure.

**3. The meaningful question is different.** For web-crawled results, the right diagnostic is: *did the crawler return sufficient context to answer the query?* — not *did the response match a fixed reference?* `GEvalContextSufficiencyMetric` directly measures whether `retrieved_context` contained enough information to fully answer `input`, independent of `expected_output`.

### Calibration: Replace `completeness` with `context_sufficiency` for Cases 1 and 3

> *You bring the Case 1 and Case 3 results to the domain expert. They read the eval output: `tool_correctness` passes, `completeness` fails. "The agent called the right tool. So completeness is failing because of the crawler, not the agent," they say. "We need a metric that evaluates what the crawler actually returned — not what a fixed reference says it should have returned."*

This is the calibration trigger. `tool_correctness` in the initial eval already ruled out agent routing as the cause. The remaining question is: was the crawler's output sufficient to answer the query? That is exactly what `GEvalContextSufficiencyMetric` measures — independent of any fixed reference.

`context_sufficiency` replaces `completeness` for Cases 1 and 3 (web-crawled, enumerable catalog queries). `tool_correctness` stays because the dataset has `expected_tools` and routing correctness remains a valid ongoing check.

Case 2 (single-value lookup) keeps the default evaluator — `completeness` is appropriate for stable, single-source facts like an order delivery date.

{% code title="eval_calibrated.py" %}
```python
# LLMTestCase now includes tools_called and expected_tools for tool_correctness.
data = [
    LLMTestCase(
        input=row["query"],
        actual_output=actual_output,
        expected_output=row["expected_output"],
        retrieved_context=retrieved_context,
        tools_called=ToolCall.from_dicts(tools_called_list),
        expected_tools=ToolCall.from_dicts(json.loads(row["expected_tools"])),
    )
    for row, (actual_output, tools_called_list, retrieved_context) in zip(DATASET, agent_results)
]

# Cases 1 and 3: tool_correctness checks agent routing, context_sufficiency
# checks tool data quality. Together they attribute failures to the right layer.
result_multi = await evaluate(
    data=[data[0], data[2]],
    evaluators=[
        GEvalGenerationEvaluator(
            models=judge_model,
            metrics=[
                DeepEvalToolCorrectnessMetric(
                    evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
                ),  # verify tool name + args only (expected_tools has no output)
                GEvalContextSufficiencyMetric(),  # tool data sufficiency check
                GEvalGroundednessMetric(),
                GEvalRedundancyMetric(),
            ],
        )
    ],
    experiment_tracker=tracker,
)

# Case 2: single-value lookup — default (completeness + groundedness + redundancy).
result_single = await evaluate(
    data=[data[1]],
    evaluators=[GEvalGenerationEvaluator(models=judge_model)],
    experiment_tracker=tracker,
)
```
{% endcode %}

Run the calibrated evaluation:

```bash
make run-eval-calibrated
```

### Calibrated Results

Cases 1 and 3 now **pass** with the calibrated metrics. All four metrics succeed:

```python
# Case 1 result (calibrated)
{
  'generation': {
    'aggregate_success': True,
    'tool_correctness':    {'score': 1.0, 'success': True,  ...},
                            # agent called get_product_integrations with correct args
    'context_sufficiency': {'score': 1.0, 'success': True,
                            'explanation': 'The retrieval context provides a direct list of '
                                           'supported platforms for CloudDeploy Pro, mentioning '
                                           'AWS, Google Cloud, and Azure.'},
    'groundedness':        {'score': 1.0, 'success': True,  ...},
    'redundancy':          {'score': 0.0, 'success': True,  ...},
  }
}
```

This is the key insight from calibration: the `completeness` failures in `eval.py` were **false negatives**. The fixed `expected_output` listed 5 platforms — but the tool returned 3, and the agent faithfully reported those 3. `context_sufficiency` confirms the tool's output was sufficient to answer the query as posed. The agent was not broken; the eval metric was comparing against a stale reference.

### What Calibration Is Not

Calibration is not adjusting configuration until all cases pass. The test is: **does the calibrated metric set reflect what domain experts actually care about?**

- **`completeness`** is correct for stable, single-source facts (Case 2). The expected answer is fixed and definitive.
- **`tool_correctness`** is correct when you need to verify the agent's routing decision — that it called the right tool with the right input arguments.
- **`context_sufficiency`** is correct when you need to verify the tool's data quality — that what the tool returned was sufficient to answer the query. Together with `tool_correctness`, it enables root cause attribution: agent failure vs tool failure.

Calibration decisions should be reviewed and sign-off documented — otherwise they are score manipulation, not measurement improvement.

See the [Calibrate the Evals](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/calibrate-the-evals) guide for the systematic calibration workflow.

***

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation Evals Lifecycle page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle).