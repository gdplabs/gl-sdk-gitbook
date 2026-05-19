# 🔄 Evaluate Helper Function

We provide a convenience helper function called `evaluate`. This function provides a streamlined way to run AI evaluations with minimal setup. It orchestrates the entire evaluation process, from data loading to result tracking, in a single function call. This helper only supports structured evaluation rules, where each record receives the same evaluation treatment.

`evaluate` expects **precomputed model outputs** in your dataset (for example `actual_output`) and focuses only on evaluation and tracking.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluate_helper_function" %}

## Quick Start

{% stepper %}
{% step %}
Create a script called `evaluate_example.py`.

```python
import asyncio
import os

from gllm_evals import LLMTestCase, load_simple_qa_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.utils.demo_utils import your_ai_func_result
from gllm_evals.experiment_tracker import CSVExperimentTracker


async def main():
    """Main function."""
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in load_simple_qa_dataset().load()
    ]
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
        experiment_tracker=CSVExperimentTracker(project_name="evals_test"),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```
{% endstep %}

{% step %}
Run the script:

```
python evaluate_example.py
```
{% endstep %}

{% step %}
The evaluate function returns a structured run summary:

```python
x = {
  "experiment_uris": {
    "run_uri": "/path/to/experiments/experiment_results.csv",
    "leaderboard_uri": "/path/to/experiments/leaderboard.csv",
  },
  "run_id": "default_unnamed_dataset_0754853f",
  "dataset_name": "unnamed_dataset",
  "timestamp": "2026-04-20T15:47:07.742806",
  "num_samples": 3,
  "metadata": {
    "batch_size": 10,
    "evaluator_parameters": {
      "evaluator_0": {
        "name": "generation",
        "batch_status_check_interval": 30.0,
        "batch_max_iterations": 120,
        "run_parallel": True,
        "models": None,
        "metric_0": {
          "evaluation_steps": ["..."],
          "_runtime_params_applied": False,
          "strict_mode": False,
          "batch_status_check_interval": 30.0,
          "batch_max_iterations": 120,
          "threshold": 0.5,
          "name": "completeness",
          "_evaluation_lock": None,
        },
        "metric_1": {
          "evaluation_steps": ["..."],
          "_runtime_params_applied": False,
          "strict_mode": False,
          "batch_status_check_interval": 30.0,
          "batch_max_iterations": 120,
          "threshold": 0.4,
          "name": "redundancy",
          "_evaluation_lock": None,
        },
        "metric_2": {
          "evaluation_steps": ["..."],
          "_runtime_params_applied": False,
          "strict_mode": False,
          "batch_status_check_interval": 30.0,
          "batch_max_iterations": 120,
          "threshold": 0.5,
          "name": "groundedness",
          "_evaluation_lock": None,
        },
      }
    },
    "dataset_name": "unnamed_dataset",
  },
  "summary_result": {},
  "results": [
    [
      {
        "generation": {
          "aggregate_explanation": "All metrics met the expected values.",
          "aggregate_success": True,
          "aggregate_score": 1.0,
          "completeness": {
            "score": 1.0,
            "explanation": "...",
            "success": True,
            "rubric_score": 3,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": True,
          },
          "redundancy": {
            "score": 0.0,
            "explanation": "...",
            "rubric_score": 1,
            "success": True,
            "threshold": 0.4,
            "strict_mode": False,
            "higher_is_better": False,
          },
          "groundedness": {
            "score": 1.0,
            "explanation": "...",
            "success": True,
            "rubric_score": 3,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": True,
          },
          "is_refusal": False,
        }
      }
    ],
    ...
  ],
}



```
{% endstep %}

{% step %}
You will see the result of the run in the path written in `experiment_uris/run_uri` and additionally `experiment_uris/leaderboard_uri` for the leaderboard of each run you done.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You have successfully created your first evaluate convenience function!
{% endhint %}

***

## Function Signature

```python
async def evaluate(
    data: str | BaseDataset | list[EvalInput],
    evaluators: list[BaseEvaluator | BaseMetric],
    experiment_tracker: BaseExperimentTracker | None = None,
    batch_size: int = 10,
    allow_batch_evaluation: bool = False,
    summary_evaluators: list[SummaryEvaluatorCallable] | None = None,
    **kwargs: Any,
) -> ExperimentResult
```

### Parameters

* `data` (`str | BaseDataset | list[EvalInput]`): Dataset to be evaluated.
  * \[RECOMMENDED] Can be a `BaseDataset` object (see [Dataset](dataset.md) section).
  * Can be a list of rows (`list[EvalInput]`) when you already have normalized in-memory data.
  * For list input, use `LLMTestCase` as the canonical row model (`input`, `actual_output`, `expected_output`, etc.).
  * Can also be filled with a string:
    * `hf/[dataset_name]` -> load from HuggingFace Hub.
    * `gs/[worksheet_name]` -> load from Google Sheets spreadsheet.
    * `langfuse/[dataset_name]` -> load from Langfuse dataset.
    * `[dataset_name]` (no prefix) -> load from local path (`*.csv`, `*.jsonl`)
  * Input rows should already contain the model output fields required by your evaluator/metric (for example `actual_output`, plus `expected_output` when needed).
* `evaluators (list[BaseEvaluator | BaseMetric])`: List of evaluators or metrics to apply. Custom evaluator or metric also can be provided if there is currently no match evaluator / metric as long as either inherits from `BaseEvaluator` or `BaseMetric`.
* `experiment_tracker` (`BaseExperimentTracker | None, optional`): Optional tracker for logging results. Defaults to `SimpleExperimentTracker`. For experiment tracker object, see [Experiment Tracker](experiment-tracker.md) section.
* `batch_size` (`int, optional`): Number of samples to process in parallel. Defaults to 10.
* `allow_batch_evaluation` (`bool`): is a boolean parameter that enables **batch processing mode** for LLM API calls. When enabled, the runner passes entire batches to evaluators for optimized batch processing instead of processing items individually.
* `summary_evaluators` (`list[SummaryEvaluatorCallable] | None, optional` ): List of user-supplied callable functions that compute aggregate metrics across all evaluation results. They are called after each batch with cumulative data to produce batch-level statistics. Below are the input parameters and output expected for a summary evaluator.
  * **Input Parameters**:
    * `evaluation_results` (`list[EvaluatorResult]`): List of evaluation outputs from all processed batches (cumulative)
    * `data` (`list[MetricInput]`): List of input data rows from all processed batches (cumulative)
  * **Output (return)** :
    * should return a dictionary with any key value that will be appended into the `summary_result` in leaderboard and run result.
* `**kwargs` (`Any`): Additional configuration like `tags`, `metadata`, or `run_id`.

***

## Usage Example

### Using data from Google Sheets

```python
import asyncio
import os

from langfuse import get_client

from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.evaluate import evaluate
from gllm_evals.utils.demo_utils import your_ai_func_result


async def main():
    """Main function."""
    dataset = (await SpreadsheetDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )).to_standard_format()

    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in dataset
    ]

    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

### Using Langfuse Experiment Tracker with custom mapping

`mapping` tells the tracker **which of your dataset's columns** should be logged into **Langfuse’s canonical fields**. That’s useful when your dataset uses custom column names but you still want to import the dataset to Langfuse with consistent structure.

The tracker expects three top-level buckets:

* `input`: the input fields that are useful for the model (e.g., query, retrieved context).
* `expected_output`: the **target** you want to compare against (e.g., reference answer/label/ground truth).
* `metadata`: any extra attributes or information for each data row (e.g., topic, type).

Your `mapping` simply points each Langfuse field to **the column name in your dataset**.

#### Example Scenario

Your dataset has columns `question_id`, `user_question`, `answer`, `expected_response`, `topic`\
You want to map them to Langfuse’s fields as follows:

* `question_id` → `input.question_id`
* `user_question` → `input.query`
* `answer` → `input.generated_response`
* `expected_response` → `expected_output.expected_response`
* `topic` → `metadata.topic`

Then, your mapping should be:

```python
mapping = {
    "input": {
        "question_id": "question_id",
        "user_question": "query",
        "answer": "generated_response"
    },
    "expected_output": {
        "expected_response": "expected_response"
    },
    "metadata": {
        "topic": "topic"
    }
}
```

The tracker will log them based on your mapping.

***

Here is the full example of how to insert dataset from Google Sheets to Langfuse Dataset and to use Langfuse Experiment Tracker:

```python
import asyncio
import os

from langfuse import get_client

from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.evaluate import evaluate
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker


async def main():
    """Main function."""

    mapping = {
        "input": {
            "question_id": "question_id",
            "query": "query",
            "retrieved_context": "retrieved_context",
            "generated_response": "generated_response"
        },
        "expected_output": {
            "expected_response": "expected_response"
        },
        "metadata": {
            "topic": "topic"
        }
    }

    dataset = (await SpreadsheetDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )).to_standard_format()

    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in dataset
    ]

    results = await evaluate(
        data=dataset,
        evaluators=[GEvalGenerationEvaluator()],
        experiment_tracker=LangfuseExperimentTracker(
            langfuse_client=get_client(),
            mapping=mapping,
        ),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

### Summary Evaluator Example

```python
def accuracy_summary(
  evaluation_results: list[EvaluatorResult], data: list[MetricInput]
) -> dict[str, float]:
  """Compute average accuracy from evaluation results."""
  weighted_average_list = []
  for evaluation_result in evaluation_results:
    generation_result = evaluation_result["generation"]
    weighted_average = (
      generation_result["completeness"]["score"]
      + generation_result["redundancy"]["score"] * 3
    ) / 2
    weighted_average_list.append(weighted_average)

  return {"weighted_average": sum(weighted_average_list) / len(weighted_average_list)}


async def main():
  """Main function demonstrating summary evaluators."""
  result = await evaluate(
    data=load_simple_qa_dataset(),
    evaluators=[GEvalGenerationEvaluator()],
    summary_evaluators=[
        accuracy_summary,
    ]
  )
```
