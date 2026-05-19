# Modify Metrics

Use this when a built-in metric evaluates the right quality dimension, but the rubric, threshold, criteria, or few-shot examples do not match your domain.

Don't write a new metric class. Override the prompt components through the constructor. This is the most common customization path.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/metrics/modify_metrics" %}

{% hint style="info" %}
Before modifying metric behavior, review [Calibrate the Evals](../calibrate-the-evals/). Many metric issues come from miscalibrated prompts or wrong metric-type choices.
{% endhint %}

## Example: Recalibrating Context Sufficiency for RAG Pipelines

The default `GEvalContextSufficiencyMetric` checks whether context contains enough information to answer a query. A RAG-heavy evaluation might need different threshold boundaries, domain-specific few-shot examples, and refined rubric wording.

```python
from deepeval.metrics.g_eval import Rubric

from gllm_evals.metrics.generation.geval_context_sufficiency import GEvalContextSufficiencyMetric

CONTEXT_SUFFICIENCY_CRITERIA = """Context Sufficiency (1-3) - evaluate whether a chatbot
can answer a user's query using the information provided as context and chat history,
including reasonable calculations or inferences from that information. You are not concerned
with factual correctness or accuracy, but only whether the context contains enough information
to answer the query through direct statements, calculation, or logical inference."""

CONTEXT_SUFFICIENCY_EVALUATION_STEPS = [
    "Consider the user's query, context, and chat history.",
    "Determine if the query can be answered using the provided context through: (a) direct information, (b) calculation from provided data, or (c) reasonable inference from related information.",
    "If the chat history is not provided, consider only the context.",
    "Provide a brief explanation of why the context does or does not contain sufficient information, including what calculation or inference would be needed if applicable.",
]

CONTEXT_SUFFICIENCY_RUBRIC = [
    Rubric(
        score_range=(1, 1),
        expected_outcome="The context does not contain relevant information to answer the query, even through calculation or reasonable inference.",
    ),
    Rubric(
        score_range=(2, 2),
        expected_outcome="The context contains related information that allows partial answering through calculation or inference, but requires assumptions about missing variables or has multiple valid interpretations.",
    ),
    Rubric(
        score_range=(3, 3),
        expected_outcome="The context contains all necessary information to fully answer the query, either directly stated or through straightforward calculation from provided data.",
    ),
]

CONTEXT_SUFFICIENCY_FEW_SHOT = """FEW-SHOT EXAMPLES:

Example 1:
    Query: Who invented the linux os?
    Context: Bjarne Stroustrup invented C++
    Reason: No relevant information about Linux OS or its inventor.
    Score: 1.

Example 2:
    Query: What are the specific operational hours and ticket prices for the National Museum on weekends?
    Context: The National Museum is open every day of the week. On weekdays, the museum operates from 9:00 AM to 5:00 PM. Weekend hours are slightly shorter. Standard admission is $15 for adults, but weekend prices may vary.
    Reason: Context mentions hours and prices exist but doesn't specify exact weekend values. The phrase "may vary" indicates uncertainty.
    Score: 2.

Example 3:
    Query: Kapan bola lampu pijar praktis ditemukan?
    Context: Thomas Alva Edison mengembangkan banyak peralatan penting di abad ke-19. Salah satu penemuannya yang terpenting adalah bola lampu pijar praktis pertama. Penemuan bola lampu pijar tersebut didemonstrasikan pada tahun 1879.
    Reason: Context provides the exact year of discovery.
    Score: 3.

Example 4:
    Query: What is the average temperature in City X during summer?
    Context: City X recorded temperatures of 28°C, 32°C, 30°C, and 34°C in June, July, and August 2025.
    Reason: Specific temperature data points provided. Average can be calculated: (28+32+30+34)/4 = 31°C.
    Score: 3.
"""

metric = GEvalContextSufficiencyMetric(
    rubric=CONTEXT_SUFFICIENCY_RUBRIC,
    criteria=CONTEXT_SUFFICIENCY_CRITERIA,
    evaluation_steps=CONTEXT_SUFFICIENCY_EVALUATION_STEPS,
    additional_context=CONTEXT_SUFFICIENCY_FEW_SHOT,
    threshold=0.75,
)
```

## What Changed From the Default

| Attribute            | Change                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `rubric`             | Refined scoring boundaries for calculation-heavy evaluation                              |
| `additional_context` | Added few-shot examples that distinguish "calculable from data" vs "requires assumption" |
| `threshold`          | Increased from default `0.5` to `0.75` for stricter context sufficiency checks           |

The metric class itself is unchanged. No subclassing needed.

## Common Attributes to Override

| Attribute            | Purpose                                                       |
| -------------------- | ------------------------------------------------------------- |
| `criteria`           | Main instruction for what the judge evaluates                 |
| `evaluation_steps`   | Ordered reasoning steps the judge follows                     |
| `additional_context` | Extra prompt context, often few-shot examples                 |
| `rubric`             | Score ranges and expected outcomes                            |
| `threshold`          | Pass/fail cutoff                                              |
| `strict_mode`        | Force stricter binary-style pass/fail behavior when supported |

If modifying these attributes still cannot express your evaluation need, create a custom metric instead. See [Custom Metric](custom-metric.md).
