---
icon: arrow-progress
---

# Evals Lifecycle

## Evals Lifecycle

The lifecycle is iterative, not a waterfall. Most real evaluation work happens inside the feedback loops, not in the first pass through the steps.

## Overview

<figure><img src="../../../.gitbook/assets/Evals Lifecycle.png" alt=""><figcaption></figcaption></figure>

{% stepper %}
{% step %}
## Step 1: Define the Target System

The target system is the AI application, pipeline, agent, or model you want to evaluate. This step answers one question: what exactly are we measuring?

Be clear about the following before moving on.

1. **System type:** the architectural pattern of your system -- RAG, AI agent, classifier, summarizer, or other. This determines which evaluator and metrics apply in gllm-evals..
2. **Task**: what the system is supposed to do in one sentence.
3. **Inputs**: what the system receives (user query, document, conversation history, tool outputs).
4. **Outputs**: what the system produces (text answer, action taken, structured JSON, classification label).

### Why it matters

Without a clear target definition, every downstream decision gets fuzzy. Dataset rows will be missing columns. Metrics will not map to real failure modes. Improvements will be hard to attribute.

The target system itself is not a `gllm-evals` object. It is whatever your application exposes. `gllm-evals` evaluates the outputs your system already produced -- it does not call your system during evaluation. By Step 2, each row in your dataset must include the actual\_output your system generated.

### Example

```
System type: RAG chatbot
Task:        Answer questions about investment, generate consisce title from conversation transcript
Inputs:      user_query, conversation_history
Outputs:     text response grounded in retrieved HR policy documents
```
{% endstep %}

{% step %}
## Step 2: Prepare Dataset

A dataset is a collection of test cases that represent what the target system must handle.

### Start small

Do not wait until you have a large dataset. Start with 20 to 50 cases. A small, representative dataset catches more real failures than a large synthetic one.

### What to include

At minimum, every row needs an `input`. For most tasks, also include `expected_output`, the reference answer the system should produce.

That is all you need at this step. Other fields like `actual_output`, `retrieved_context`, and `tools_called` are generated when your system runs. They are added to the dataset before you run evaluation, not here.

### How to source test cases

Sources in priority order:

1. **Production traffic and support tickets**: real user failures are the highest-signal source.
2. **Internal dogfooding**: engineers and PMs using the product.
3. **Error analysis**: patterns you already know the system struggles with.
4. **SME review**: domain experts identify gaps users cannot articulate.
5. **Red teaming**: adversarial inputs designed to break the system.
6. **Synthetic generation**: LLM-generated inputs around known weak spots.

### Examples

**QnA Chatbot** -- input is a question, expected output is the reference answer.

<table><thead><tr><th width="69">no</th><th>input</th><th>expected_output</th></tr></thead><tbody><tr><td>1</td><td>Kapan Strategi Nasional Kecerdasan Artifisial (Stranas KA) resmi diluncurkan?</td><td>Stranas KA resmi diluncurkan pada 10 Agustus 2020.</td></tr></tbody></table>

**Conversation Title Generator** -- input is a full conversation transcript, expected output is the title the system should produce.

<table data-header-hidden><thead><tr><th width="71">no</th><th>input</th><th>expected_output</th></tr></thead><tbody><tr><td>1</td><td><p>| Entity | Owner | Event Message | Consumer | Reason for Use | Release Date (YYYY-MM-dd) |</p><p>&#x3C;long table content></p><p><br></p><p>Convert that table into html</p></td><td>Table Conversion into HTML</td></tr></tbody></table>

The column names in your CSV do not need to match `input` and `expected_output` exactly. Map them explicitly when constructing `LLMTestCase` (see code below).

### Using gllm-evals

`gllm-evals` represents each row as an LLMTestCase object. The example below loads from CSV, but any dataset source works. Load your data, run your target system to generate `actual_output`, then construct the list:

```python
data = [
    LLMTestCase(
        input=row.get("input"),
        expected_output=row.get("expected_output"),
        actual_output=your_ai_function(row["input"])["answer"],
        retrieved_context=your_ai_function(row["input"])["retrieved_context"],
    )
    for row in DictDataset.fromcsv(dataset_path).load()
]
```

This data list is what you will pass into `evaluate()` when running evaluation.

{% hint style="info" %}
For all supported dataset types (Google Sheets, HuggingFace, Langfuse, JSONL, and more) see the [Dataset Reference](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/dataset).
{% endhint %}
{% endstep %}

{% step %}
## Step 3: Define Metrics and Success Criteria

This step answers: what does quality mean for your system, and how do you measure it? The answer lives in two SDK primitives, metrics and evaluators, that you configure before running any experiment.

### Metrics

A **metric** is a single, focused measurement of output quality. It takes an `LLMTestCase` object as input and returns a score, an explanation, and a pass/fail result.

Output format. Metrics return different result types depending on their implementation:

1. `MetricOutput`: the base type, returns any dict.
2. `MetricResult`: returns `score` and `explanation`.
3. `GEvalMetricResult`: the richest format, returns the full set of fields below. Recommended — prefer GEval metrics when available so you get structured, inspectable results.

<table><thead><tr><th width="161">Field</th><th width="123">Type</th><th>Description</th></tr></thead><tbody><tr><td>score</td><td>float</td><td>Normalized score in [0, 1]</td></tr><tr><td>rubric_score</td><td>int | float</td><td>Raw value from the LLM judge (e.g. 1–3 scale)</td></tr><tr><td>explanation</td><td>str | None</td><td>Human-readable reasoning from the judge</td></tr><tr><td>success</td><td>bool</td><td>True if score meets the threshold</td></tr><tr><td>threshold</td><td>float</td><td>The pass/fail cutoff you configure</td></tr><tr><td>higher_is_better</td><td>bool</td><td>False for metrics like redundancy or toxicity where lower is better</td></tr></tbody></table>

***

### How to Choose the Right Metrics

This is one of the most consequential decisions in the whole lifecycle. The wrong metric produces a number that looks meaningful but tells you nothing about the failure mode you actually care about.

Pick metrics that match the tasks your system performs. Each task type has distinct failure modes and corresponding metrics.

1. Generation catches hallucination, incomplete coverage, wrong refusal behavior, language drift, and verbose output. Use `GEvalGroundednessMetric`, `GEvalCompletenessMetric`, `GEvalRefusalAlignmentMetric`, or `DeepEvalAnswerRelevancyMetric` depending on which failure modes apply. Note that `GEvalCompletenessMetric` supports two modes: reference-based (needs `expected_output` as a gold answer) and criteria-based (needs `expected_output` as a coverage specification). Pick the mode that matches what you have in your dataset.
2. Retrieval catches context miss, irrelevant chunks retrieved, and insufficient context to answer the query. Use `GEvalContextSufficiencyMetric`, `DeepEvalContextualRecallMetric`, or `DeepEvalContextualRelevancyMetric`.
3. Safety catches bias, toxicity, PII leakage, prompt injection, role violation, and misuse. Use `DeepEvalBiasMetric`, `DeepEvalToxicityMetric`, `DeepEvalPIILeakageMetric`, or `DeepEvalPromptAlignmentMetric`.
4. Tool Use / Agentic catches wrong tool called, wrong order, and trajectory deviation. Use `DeepEvalToolCorrectnessMetric` and `LangChainAgentTrajectoryAccuracyMetric`.\
   For agentic systems, also consider an `EnvironmentMetric` to check if the environment reached the expected state after an agent action (e.g. file written, DB row updated). No generic metric exists for this, it is always a custom metric because "correct state" is system-specific.

***

### Metric Classification

Understanding how a metric works under the hood tells you when to trust its scores and what can go wrong.

By method:

<table><thead><tr><th width="158">Method</th><th>How it works</th><th>Trade-off</th></tr></thead><tbody><tr><td><strong>LLM-Judge</strong></td><td>A language model evaluates the output against a rubric</td><td>Flexible and handles nuance, but non-deterministic</td></tr><tr><td><strong>Deterministic</strong></td><td>Rule-based or classical algorithm (e.g. precision, recall)</td><td>Fast and fully reproducible, but cannot capture semantic quality</td></tr><tr><td><strong>Combined</strong></td><td>LLM produces intermediate judgments, then code-based post-processing computes the final score</td><td>Balances flexibility with consistency</td></tr><tr><td><strong>Human Evaluation</strong></td><td>A human grader scores the output directly</td><td>Highest reliability and nuance, but slow and expensive. Use to calibrate automated judges or resolve disagreements between them</td></tr></tbody></table>

By reference:

<table><thead><tr><th width="157">Type</th><th>What it compares against</th><th>Needs expected_output?</th></tr></thead><tbody><tr><td>Reference-based</td><td>Compares the output against a gold-standard answer</td><td>Yes, as a literal gold answer</td></tr><tr><td>Criteria-based</td><td>Checks the output against per-example requirements written in natural language</td><td>Yes, as a coverage specification</td></tr><tr><td>Referenceless</td><td>Scores from the query and/or retrieved context alone; any criteria are universal and baked into the metric definition</td><td>No</td></tr></tbody></table>

**Criteria-based evaluation** is the industry-standard recommendation when you do not have high-quality annotated gold answers. Instead of asking "does this match the expected output?", you define explicit requirements and the judge scores against those. It is generally more scalable because writing a specification is cheaper than annotating correct answers at scale. There are two ways to implement it:

1. **Per-example criteria in expected\_output** — the criteria vary per test case, so they live in the dataset as a natural language specification. `GEvalCompletenessMetric` supports this mode: instead of passing a literal gold answer, you pass something like `"Answer must cover 3 personas, nightly rates, and trip lengths"` and the judge checks coverage against that specification.
2. **Universal criteria baked into the metric** — the criteria are identical across all test cases, so they live in the metric's `rubric` and `evaluation_steps` rather than in `expected_output`. `GEvalContextSufficiencyMetric` is the example: sufficiency is always defined the same way, so the rubric is defined once in the metric class and no `expected_output` is needed. This makes the metric referenceless while still being criteria-driven.

This distinction matters practically: if you do not have high-quality `expected_output` annotations, reference-based metrics will give unreliable scores. Either invest in annotations, or lean on criteria-based evaluation — either by writing per-example specifications or by building a referenceless metric with a universal rubric.

### Set Thresholds

Each metric ships with a default threshold, but you should treat it as a starting point rather than a fixed rule. Adjust thresholds based on your system's risk tolerance and the failure modes that matter most for your use case. The right place to calibrate them systematically is the **Calibrate Evals** step, where you align thresholds against human labels and tighten or loosen them based on where your automated judge agrees or disagrees with human judgment.

### Custom Metrics

**Before building a custom metric, check the** [**available metrics list**](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/metric) **first**. `gllm-evals` wraps metrics from `DeepEval`, `RAGAS`, and `LangChain OpenEvals`. The built-in library is broad, and the quality dimension you need is likely already covered.

If none of the built-in metrics fits, follow this order:

1. **Extend `DeepEvalGEvalMetric` first.** This is the recommended approach. You define criteria or evaluation steps, a rubric, and the required fields, and you automatically get a `GEvalMetricResult` with structured, inspectable output including `rubric_score`, `threshold`, `success`, and `explanation`.

```python
from deepeval.metrics.g_eval import Rubric
from deepeval.test_case import LLMTestCaseParams
from gllm_evals.constant import ColumnNames
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric, MetricDefaults
from gllm_evals.types import LLMTestCase


class PolitenessMetric(DeepEvalGEvalMetric):
    """Custom metric evaluating politeness of responses."""
    description: str = "Politeness score. Normalized to [0, 1] range. Native rubric scale (1-3)."
    required_fields: set[str] = {ColumnNames.INPUT, ColumnNames.ACTUAL_OUTPUT}
    input_type: type = LLMTestCase
    higher_is_better: bool = True
    _defaults = MetricDefaults(
        name="geval_politeness",
        criteria="Politeness (1-3) - Assess how polite and professional the response is.",
        evaluation_steps=[
            "1. Check for polite language (greetings, 'please', 'thank you').",
            "2. Assess if the response avoids aggressive or rude language.",
            "3. Score 1 = rude, Score 2 = neutral, Score 3 = polite.",
        ],
        rubric=[
            Rubric(score_range=(1, 1), expected_outcome="Rude: uses aggressive language."),
            Rubric(score_range=(2, 2), expected_outcome="Neutral: standard tone."),
            Rubric(score_range=(3, 3), expected_outcome="Polite: respectful with courtesy."),
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    )


    def _to_rubric_score(self, raw: float) -> int:
        return int(1 + raw * 2)
```

2. Fall back to `BaseMetric` only when you need logic that `DeepEvalGEvalMetric` cannot express, whether that is a fully deterministic scoring method, a non-standard LLM scoring approach, or any custom evaluation logic that does not fit the GEval rubric pattern.

```python
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import MetricInput, MetricOutput


class ExactMatchMetric(BaseMetric):
    def __init__(self):
        self.name = "exact_match"

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        score = int(data["actual_output"] == data["expected_output"])
        return {"score": float(score), "explanation": None}
```

**Tips:**

1. Pick at most 5 metrics per test case.
2. Check the [available metrics list](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/metric#available-metrics) before building a custom metric.
3. Ensure your dataset has the columns required by your chosen metrics. If you add a metric that needs a column you do not have, go back to the Prepare Dataset step and add it.

{% hint style="info" %}
See [How to Create a Custom Metric](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/metric#how-to-create-a-custom-metric) for advanced patterns.
{% endhint %}

<table><thead><tr><th width="286">Metric</th><th>Required fields</th></tr></thead><tbody><tr><td><code>GEvalGroundednessMetric</code></td><td><code>input</code>, <code>actual_output</code>, <code>retrieved_context</code></td></tr><tr><td><code>GEvalCompletenessMetric</code></td><td><code>input</code>, <code>actual_output</code>, <code>expected_output</code></td></tr><tr><td><code>GEvalRefusalAlignmentMetric</code></td><td><code>input</code>, <code>actual_output</code>, <code>expected_output</code></td></tr><tr><td><code>DeepEvalToolCorrectnessMetric</code></td><td><code>input</code>, <code>actual_output</code>, <code>tools_called</code></td></tr><tr><td><code>LangChainCorrectnessMetric</code></td><td><code>input</code>, <code>actual_output</code>, <code>expected_output</code></td></tr><tr><td><code>DeepEvalContextualRecallMetric</code></td><td><code>input</code>, <code>actual_output</code>, <code>expected_output</code>, <code>retrieved_context</code></td></tr></tbody></table>

***

### Evaluators

An **evaluator** runs multiple metrics together and returns a unified report from a single `evaluate()` call.

The key aggregation field is `aggregate_success`: it is True only if **every** metric returns `success = True`. One failing metric fails the whole evaluation. This mirrors a strict quality gate where all dimensions must pass.

**Output format**. Every evaluator returns an `EvaluatorResult` with these top-level fields:

<table><thead><tr><th width="189">Field</th><th width="113">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>aggregate_success</code></td><td>bool</td><td>True only if every metric passed</td></tr><tr><td><code>aggregate_score</code></td><td>float</td><td>Average score across all metrics</td></tr><tr><td><code>aggregate_explanation</code></td><td>str</td><td>Human-readable summary of what failed and why</td></tr><tr><td><code>possible_issues</code></td><td>list[str]</td><td>High-level issue categories detected</td></tr><tr><td><code>is_refusal</code></td><td>bool</td><td>Whether the output was a refusal response</td></tr></tbody></table>

Each metric result is also nested under its own key (e.g. completeness, groundedness) with the same fields as `GEvalMetricResult`.

**Example — GEvalGenerationEvaluator:**

```python
import asyncio

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase

async def main():
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )

    evaluator = GEvalGenerationEvaluator(model="google/gemini-2.0-flash")
    result = await evaluator.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

**Example Output:**

```json
{
  "generation": {
    "aggregate_success": false,
    "aggregate_score": 0.33,
    "aggregate_explanation": "The following metrics failed:\n1. Completeness is 0 (should be >= 0.5)\n2. Groundedness is 0 (should be >= 0.5)",
    "possible_issues": ["Generation Issue", "Retrieval Issue"],
    "completeness": {
      "score": 0.0,
      "rubric_score": 1,
      "explanation": "'New York' contradicts the expected fact 'Paris'.",
      "success": false,
      "threshold": 0.5,
      "higher_is_better": true
    },
    "groundedness": {
      "score": 0.0,
      "rubric_score": 1,
      "explanation": "'New York' directly contradicts the retrieved context.",
      "success": false,
      "threshold": 0.5,
      "higher_is_better": true
    },
    "redundancy": {
      "score": 0.0,
      "rubric_score": 1,
      "explanation": "No repeated content detected.",
      "success": true,
      "threshold": 0.4,
      "higher_is_better": false
    },
    "is_refusal": false
  }
}
```

***

### Available Evaluators

Several built-in evaluators are available. Start with the one that fits your system type before building your own. Check the [full evaluator list](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluator-scorer) for details.

<table><thead><tr><th width="261">Evaluator</th><th>Metrics included</th></tr></thead><tbody><tr><td><code>GEvalGenerationEvaluator</code></td><td><code>GEvalCompletenessMetric</code>, <code>GEvalGroundednessMetric</code>, <code>GEvalRedundancyMetric</code></td></tr><tr><td><code>AgentEvaluator</code></td><td><code>DeepEvalToolCorrectnessMetric</code>, <code>GEvalCompletenessMetric</code>, <code>GEvalGroundednessMetric</code>, <code>GEvalRedundancyMetric</code></td></tr><tr><td><code>SummarizationEvaluator</code></td><td><code>GEvalSummarizationCoherenceMetric</code>, <code>GEvalSummarizationConsistencyMetric</code>, <code>GEvalSummarizationRelevanceMetric</code>, <code>GEvalSummarizationFluencyMetric</code></td></tr><tr><td><code>LMBasedRetrievalEvaluator</code></td><td><code>DeepEvalContextualPrecisionMetric</code>, <code>DeepEvalContextualRecallMetric</code></td></tr></tbody></table>

***

### Custom Evaluators

If the built-in evaluators do not exactly match your metric combination, use **`CompositeEvaluator`**. Pass it your chosen list of metrics and it handles aggregation automatically using the default `aggregate_success` logic, which is sufficient for the vast majority of use cases.

Only build a fully custom evaluator when you need non-standard aggregation logic that `CompositeEvaluator` cannot express.

{% hint style="info" %}
See [Create Custom Evaluator / Scorer](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluator-scorer) for the full guide.
{% endhint %}

***
{% endstep %}

{% step %}
## Step 4: Evaluate and Improve the Target System

With your metrics and criteria defined, run the evaluation on your full dataset using the default judge. The goal here is to find failures in the **target system** and fix them — calibration comes later if needed.

### Run evaluate()

```python
import asyncio
from gllm_evals import LLMTestCase, load_simple_qa_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from your_service import your_ai_func_result


async def main():
    """Main function."""
    data = [
        LLMTestCase(
            input=row["input"],
            actual_output=your_ai_func_result["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result["retrieved_context"],
        )
        for row in load_simple_qa_dataset().load()
    ]
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
        experiment_tracker=CSVExperimentTracker(project_name="evals"),
    )
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
To learn more about the evaluate() helper function, see the [Evaluate Helper Function reference](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluate-helper-function).
{% endhint %}

Every run is logged with its configuration (model, prompt, dataset, metrics) and results. Runs are comparable over time, which is the point of the experiment tracker.

### Read the results

`evaluate()` returns an `ExperimentResult` object. You can inspect it directly in code, or open the CSV files written by `CSVExperimentTracker` for easier row-by-row viewing.

\
**Experiment URI**

The tracker writes two files, both paths exposed under experiment\_uris:

1. `run_uri` — per-row, per-metric scores for this run.
2. `leaderboard_uri` — aggregated scores across runs, useful for comparing experiments over time.

```python
print(results.experiment_uris)
# {
#   "run_uri": "/path/to/experiments/experiment_results.csv",
#   "leaderboard_uri": "/path/to/experiments/leaderboard.csv",
# }
```

**Evaluator Result**

The `results.results` field contains the per-row, per-evaluator breakdown. Each row is a list of evaluator outputs. For `GEvalGenerationEvaluator`, each output includes `aggregate_success`, `aggregate_score`, and one entry per metric (completeness, redundancy, groundedness). Each metric entry includes `score`, `rubric_score`, `explanation`, `success`, `threshold`, and `higher_is_better`.

```python
# Example: single row result from GEvalGenerationEvaluator
{
    "generation": {
        "aggregate_explanation": "All metrics met the expected values.",
        "aggregate_success": True,
        "aggregate_score": 1.0,
        "completeness": {
            "score": 1.0,
            "rubric_score": 3,
            "explanation": "...",
            "success": True,
            "threshold": 0.5,
            "higher_is_better": True,
            "model_id": "google/gemini-3-flash-preview",
        },
        "redundancy": {
            "score": 0.0,
            "rubric_score": 1,
            "explanation": "...",
            "success": True,
            "threshold": 0.4,
            "higher_is_better": False,
            "model_id": "google/gemini-3-flash-preview",
        },
        "groundedness": {
            "score": 1.0,
            "rubric_score": 3,
            "explanation": "...",
            "success": True,
            "threshold": 0.5,
            "higher_is_better": True,
            "model_id": "google/gemini-3-flash-preview",
        },
        "is_refusal": False,
    }
}
```

Note that `redundancy` uses `higher_is_better: False`. A `score` of `0.0` with `success: True` means the output is not redundant, which is the desired outcome.

**Summary Evaluator**

`results.summary_result` contains batch-level statistics computed after all rows are evaluated. By default, `summary_accuracy` is always included and provides `accuracy`: the fraction of rows where every evaluator reported `aggregate_success: True`.

```python
"summary_result": {"accuracy": 0.67},
```

`accuracy` is rounded to 2 decimal places. A value of `0.67` means 2 out of 3 samples passed all evaluators.

Custom summary evaluators passed via `summary_evaluators` append their keys into the same dict.

### Inspect failures and improve

When the pass rate is below the target, follow these steps:

<figure><img src="../../../.gitbook/assets/Evals Impact Check.png" alt=""><figcaption></figcaption></figure>

1. **Evaluate the target system.** Run `evaluate()` on your dataset to generate scores and metric results across all test cases.
2. **Check if success criteria are met.** For example, accuracy > 90% across all test cases. If the threshold is reached, you're done. If not, proceed to the next steps.
3. **Find failed rows.** Filter rows where `aggregate_success = False`. The `aggregate_score` shows how close each row is to passing.
4. **Identify which metric(s) caused the failure.** Within each failed row, find the metric entries where `success = False`. A row fails if any single metric fails. The metric `score` shows how close each metric is to its threshold.
5. **Read the judge's reasoning.** For each failing metric, read the `explanation` field. This is the LLM judge's reasoning for the score it assigned and the most direct guide to what went wrong.
6. **Improve the target system.** Act on the explanation. Common fixes include prompt refinement, retriever tuning, output format constraints, or few-shot examples.
7. **Repeat.** Loop back to step 1 — re-run `evaluate()` and check whether the success criteria are now met. Continue iterating until all metrics pass their configured thresholds.

### When to proceed to Step 5: Calibrate the Evals

The default judge is unverified until calibrated. If you chose well-defined metrics and clear success criteria in Step 3, it may already be producing reliable verdicts — but you cannot confirm this without measuring it. Proceed to Step 5 when any of the following apply:

1. The judge's verdicts don't match your own reading of the outputs.
2. The pass rate is implausibly high or low given what you know about the system.
3. You are about to use scores to make a high-stakes decision (e.g. shipping to production).
{% endstep %}

{% step %}
## Step 5: Calibrate the Evals

After running `evaluate()`, the natural question is: can I trust these scores?

**Not automatically**. An LLM judge is itself a model — it can be wrong, misconfigured, or applied to the wrong question type. Calibration is the process of verifying your judge's trustworthiness and fixing it when it falls short.

### What Calibration Measures

Calibration is measured by **Human-LLM Agreement Rate** — how closely the LLM judge's verdicts match those of an SME (Subject Matter Expert). Use **TPR (True Positive Rate)** and **TNR (True Negative Rate)** rather than overall agreement rate, since an imbalanced dataset can make a lenient judge look accurate.

{% hint style="success" %}
**Stopping criterion: both TPR ≥ 90% AND TNR ≥ 90%.**
{% endhint %}

### When to Proceed to This Step

Proceed to calibration when any of the following apply:

1. The judge's verdicts don't match your own reading of the outputs.
2. The pass rate is implausibly high or low given what you know about the system.
3. You are about to use scores to make a high-stakes decision (e.g. shipping to production).

### Calibration at a Glance

Calibration runs in two phases: an Initial Calibration (done once, before any experiment result is trusted) and a **Per-Experiment Loop** (run each time the target system produces new outputs). In both phases, SME-labeled rows are compared against judge verdicts to compute TPR/TNR. When the judge drifts, you diagnose the root cause — wrong metric, human label error, ambiguous rubric, or unseen output patterns — and fix accordingly.

{% hint style="info" %}
For the full calibration workflow, SME sampling strategy, re-calibration stopping criterion, and diagnostic techniques, see the [Calibrate the Evals](calibrate-the-evals/) detailed guide
{% endhint %}
{% endstep %}

{% step %}
## Step 6: Ship to Production

Once success criteria are met in Step 4, the target system is ready to ship.

Shipping is not the end of the lifecycle. Production introduces real user behavior that your evaluation dataset may not have anticipated. When a new failure mode or edge case appears in production:

1. Add it to the dataset as a new test case.
2. Loop back to Step 2 to update the dataset.
3. Re-run evaluation in Step 4 to verify the system handles it correctly.
4. If the judge's scores on the new case look suspicious, re-enter Step 5 to check calibration on the new output pattern.

This keeps the evaluation dataset growing alongside the system — each production failure becomes a regression test that prevents the same failure from shipping again.
{% endstep %}
{% endstepper %}
