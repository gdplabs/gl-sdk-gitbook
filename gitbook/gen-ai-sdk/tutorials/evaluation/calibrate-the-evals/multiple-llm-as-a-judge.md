# Multiple LLM-as-a-Judge

Multiple LLM-as-a-Judge is an advanced evaluation approach that uses multiple language models as judges to evaluate tasks in parallel and aggregate their results using ensemble methods. This approach provides higher alignment with human judgment and can significantly accelerate human annotation workflows.

## Key Benefits

1. **Higher Alignment**: Multiple judges provide more reliable and consistent evaluations compared to single-judge approaches.
2. **Faster Human Annotation**: Humans can focus on scoring only cases where agreement score < 100%, reducing annotation workload.
3. **Human Alignment**: When agreement score reaches 100%, the alignment with human judgment is high.

The current module supports both categorical and numeric evaluations, with flexible ensemble methods for result aggregation.

**When to use:** Use multiple LLM-as-a-Judge when judge results are inconsistent or when you find disagreement between different LLM judge models.

## Example Usage

```python
import asyncio
import os

from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.constant import AggregationMethod
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase

# Homogeneous: same judge 3 times
model = build_lm_invoker(
    "google/gemini-3-flash-preview",
    os.getenv("GOOGLE_API_KEY"),
)
evaluator = GEvalGenerationEvaluator(
    models=[model] * 3,
    aggregation_method=AggregationMethod.MAJORITY_VOTE,
)

# Or heterogeneous: different judges
# judges = [
#     build_lm_invoker("openai/gpt-4o", os.getenv("OPENAI_API_KEY")),
#     build_lm_invoker("openai/gpt-4o-mini", os.getenv("OPENAI_API_KEY")),
# ]
# evaluator = GEvalGenerationEvaluator(
#     models=judges,
#     aggregation_method=AggregationMethod.MAJORITY_VOTE,
# )

data = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris",
    actual_output="Paris",
    retrieved_context="Paris is the capital of France.",
)

result = await evaluator.evaluate(data)
print(result)
```

### Example Output

```json
{
  "generation": {
    "aggregate_explanation": "All metrics met the expected values.",
    "aggregate_success": true,
    "aggregate_score": 1.0,
    "completeness": {
      "score": 1.0,
      "explanation": "The minimum key facts are: [A] Paris. The generated response correctly matches the key fact by identifying Paris as the capital.",
      "rubric_score": 3,
      "success": true,
      "threshold": 1.0,
      "strict_mode": false,
      "higher_is_better": true,
      "model_id": "google/gemini-3-flash-preview",
      "judge_id": 0,
      "num_judges": 3,
      "ensemble_method": "majority_vote",
      "agreement_score": 1.0,
      "individual_judge_results": [
        {
          "score": 1.0,
          "explanation": "...",
          "rubric_score": 3,
          "success": true,
          "threshold": 1.0,
          "strict_mode": false,
          "higher_is_better": true,
          "model_id": "google/gemini-3-flash-preview",
          "judge_id": 0
        },
        {
          "score": 1.0,
          "explanation": "...",
          "rubric_score": 3,
          "success": true,
          "threshold": 1.0,
          "strict_mode": false,
          "higher_is_better": true,
          "model_id": "google/gemini-3-flash-preview",
          "judge_id": 1
        },
        {
          "score": 1.0,
          "explanation": "...",
          "rubric_score": 3,
          "success": true,
          "threshold": 1.0,
          "strict_mode": false,
          "higher_is_better": true,
          "model_id": "google/gemini-3-flash-preview",
          "judge_id": 2
        }
      ],
      "representative_judge_index": 0,
      "explanation_aggregation_method": "representative_result",
      "score_distribution": { "1": 3 }
    },
    "redundancy": {
      "score": 0.0,
      "explanation": "The response is direct and concise, providing the key information in a single sentence.",
      "rubric_score": 1,
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": false,
      "model_id": "google/gemini-3-flash-preview",
      "judge_id": 0,
      "num_judges": 3,
      "ensemble_method": "majority_vote",
      "agreement_score": 1.0,
      "individual_judge_results": [
        {
          "score": 0.0,
          "explanation": "...",
          "rubric_score": 1,
          "success": true,
          "threshold": 0.5,
          "strict_mode": false,
          "higher_is_better": false,
          "model_id": "google/gemini-3-flash-preview",
          "judge_id": 0
        },
        {
          "score": 0.0,
          "explanation": "...",
          "rubric_score": 1,
          "success": true,
          "threshold": 0.5,
          "strict_mode": false,
          "higher_is_better": false,
          "model_id": "google/gemini-3-flash-preview",
          "judge_id": 1
        },
        {
          "score": 0.0,
          "explanation": "...",
          "rubric_score": 1,
          "success": true,
          "threshold": 0.5,
          "strict_mode": false,
          "higher_is_better": false,
          "model_id": "google/gemini-3-flash-preview",
          "judge_id": 2
        }
      ],
      "representative_judge_index": 0,
      "explanation_aggregation_method": "representative_result",
      "score_distribution": { "0": 3 }
    },
    "is_refusal": false
  }
}
```

***

## Output Shape

When only one model is set in `models`, each metric returns a normal single-judge result without ensemble metadata.

When multiple judges are set in `models`, metric-level results include ensemble metadata:

| Field | Meaning |
| :---- | :---- |
| `score` | Aggregated metric score |
| `agreement_score` | Judge agreement in `[0.0, 1.0]` |
| `individual_judge_results` | Raw result from each judge, including judge error payloads if a judge fails |
| `ensemble_method` | Aggregation method actually used |
| `num_judges` | Total judges used |
| `representative_judge_index` | Judge result selected as representative for explanation fields |
| `explanation_aggregation_method` | Strategy used for combining or selecting explanations |
| `score_distribution` | Count of each score value |

Each item in `individual_judge_results` can include:

* `judge_id`
* `model_id`
* `score`
* `explanation`
* `rubric_score`
* `success`
* `threshold`
* `strict_mode`
* `higher_is_better`

If a judge fails, its item can contain `error`, `judge_id`, and `model_id` instead of score fields.

At evaluator aggregate level, ensemble output uses aggregate fields:

| Field | Meaning |
| :---- | :---- |
| `aggregate_score` | Aggregated evaluator score |
| `aggregate_success` | Majority pass/fail result across valid judges |
| `aggregate_explanation` | Combined judge aggregate explanations, labeled by judge model |
| `agreement_score` | Agreement score across valid aggregate scores |
| `ensemble_method` | Aggregation method actually used |
| `weights` | Judge weights used by the aggregation method |
| `individual_judge_results` | Valid judge aggregate results with `aggregate_explanation` removed |

***

## How Scoring Works <a href="#how-scoring-works" id="how-scoring-works"></a>

1. Collect judge results from multiple LLM judges
2. Apply ensemble method:
   * **Majority Vote**: Uses mode of scores (default)
   * **Median**: Uses weighted median of scores
   * **Average**: Uses weighted average of scores
3. **Calculate agreement score** to measure consensus among judges:
   1. For categorical ensemble: the percentage of judges with the same categorical rating.
   2. For numerical ensemble: `max(0.0, 1.0 - coefficient_of_variation)` (lower variation = higher agreement)
4. **Score distribution** shows how many judges assigned each score value.
