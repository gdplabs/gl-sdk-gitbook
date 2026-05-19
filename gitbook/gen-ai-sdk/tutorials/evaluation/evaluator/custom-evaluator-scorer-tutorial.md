# Custom Evaluator Tutorial

In this guide, we'll walk through how to build a custom evaluator for a specific use case. You can adapt the tutorial to match your project's needs. In our example, the evaluator checks whether the summary of a customer's complaint is correct and accurate based on the detailed description provided.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/tutorials/custom_evaluator_tutorial" %}

## Step 0: Install the Required Libraries

To install `gllm-evals`, you can follow [this](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/getting-started#installation) section.

## Step 1: Prepare Your Dataset

Before running the evaluation, we need a dataset that contains all the information required for scoring.\
For this example, we’ll use the following data:

{% file src="../../../../.gitbook/assets/tsel_test_data.csv" %}

This data has 5 columns:

* `no`: The row number.
* `detailed_description`: The client’s full complaint description (this serves as the query).
* `detailed_case_gangguan`: The summarized complaint generated from the detailed description (this is the response we will evaluate).
* `gt_detail_case_gangguan`: The ground-truth summary, used to compare against `detailed_case_gangguan` to determine the true score. It is not used during evaluation itself, but it can be used afterward to measure the evaluator's accuracy.
* `score_detail_case_gangguan`: The ground-truth score representing how well `detailed_case_gangguan` matches `gt_detail_case_gangguan`. It is not used during the evaluation itself, but it will be used afterward to measure the evaluator’s accuracy as the alignment score.

## Step 2: Create a Custom Metric

Before we can evaluate our dataset, we need to decide which metric we will need to evaluate. Because this case is unique and specialized, we will create a custom metric using DeepEval's GEval with custom evaluation steps. Before proceeding, you can check the gllm-evals' [metrics](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-evals/gllm_evals/metrics) to decide whether to reuse the existing one or to create a custom one.

This is the example custom evaluation steps for the dataset above:

```python
CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS = [
    "You are provided with 'query', which contains a customer's complaint text "
    "serving as the original reference or source information.",
    "'actual_output' is the model-generated summary or copying with or without any reword from `query` that should"
    "condense the complaint into 1–5 short (or slightly more) easy-to-read and easy-to-understand sentences.",
    "Extract structured fields from both 'query' and 'actual_output': "
    "{actor (customer/system), action (verb), object (service/feature/app), "
    "channel/app (e.g., MyTelkomsel, GoPay), intent_type (request vs issue), "
    "polarity (can/cannot), key context}.",
    "Require at least ACTION + OBJECT in the summary. If OBJECT is missing or too general "
    "to be mapped to the taxonomy, mark score 0.",
    "Check that intent_type (request vs issue) and channel/app stay consistent. "
    "If 'query' targets a third-party account (e.g., GoPay) but the summary switches to a different app "
    "(e.g., MyTelkomsel), score 0.",
    "Copy of a long sentence from `query` with or without any reword use it as `actual_output` is allowed as long as "
    "the sentence is factual, not contradicted and not hallucinated by `query`."
    "So if it copy, it does not matter if the sentence is not summary still give reward by score 1.",
    "If the some word in 'actual_output' is in `AO Keyword: 'actual_output'` or `\nAO Keyword: 'actual_output'` (ignore case sensitivity) then give score 1"
    "For example: AO Keyword: AO_TELKOMSELPORTAL_RESEND_LINK_WEC_FMC, then the"
    "actual_output: ao_telkomselportal_resend_link_wec_fmc give score 1"
    "If the query has the value AO Keyword but actual_output does not contain AO Keyword, then first check whether"
    "actual_output contradicts or hallucinates the query. If it is a fact, then set the value to 1."
    "No need all word in actual_output is include in query, just some word is enough",
    "If the query is too short, but some words in actual_output is include in query (ignore case sensitivity), then give score 1"
    "For example: query: LOS, LOS and actual_output: los, then give score 1. No need all word in actual_output is include in query, just some word is enough",
    "To generate the summary, user used this prompt: 'ALWAYS provide a clear, concise summary "
    "of the main issue in the complaint note, focusing on the core problem without extraneous detail. "
    "If the note is too short or limited to technical jargon, treat the first line or labels like "
    "AO Keyword, Detail Request as the issue summary.'",
    "Check that all information in 'actual_output' is found in, or directly supported by, "
    "the content of 'query'. The summary may omit secondary or supporting details "
    "such as numbers, timestamps, or locations, as long as the main issue remains correct.",
    "Mark the summary as incorrect (score 0) only if it contradicts the 'query', introduces new facts, "
    "or hallucinates information not present in the source.",
    "If the summary changes the factual meaning of the complaint (for example reversing polarity like "
    "'cannot connect' becoming 'can connect'), set the score to 0. Simple rewording or paraphrasing "
    "that preserves the original meaning should still be considered correct.",
    "Some word like 'cannot connect' becoming 'can connect', 'unsubscribe' become 'subscribe', "
    "'unactivate' become 'activate' or similar word, of course it is not correct and give score 0",
    "The summary does not need to cover every single detail from the complaint. Focus on whether the "
    "information it includes is correct, relevant, and factually faithful to the source.",
    "Minor typos, short phrasing, or generalization of numeric or product values are acceptable "
    "if they do not distort the core issue. But take not type can change the meaning of the complaint.",
    "Even if the summary is short (1–2 sentences), as long as it accurately represents the customer's "
    "main problem and contains no hallucination or contradiction, it should still be considered correct.",
    "Assign a higher score if the summary is concise, accurate, faithful, non-contradictory, "
    "and captures the core meaning of the complaint clearly.",
]
```

After that, we can create our custom metric:

```python
from typing import Any

from deepeval.test_case import LLMTestCaseParams
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.schema import ModelId

from gllm_evals.constant import DefaultValues, ResultMetricKeys
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import MetricInput, MetricOutput


class CustomDetailCaseGangguanCorrectnessMetric(DeepEvalGEvalMetric):
    """Custom detail case gangguan correctness metric.

    Required Fields:
    - input (str): The customer's complaint description used as the source.
    - actual_output (str): The generated summary to evaluate.

    Attributes:
        name (str): The name of the metric.
        model (str | ModelId | BaseLMInvoker): The model to use for the metric.
        model_credentials (str | None): The model credentials to use for the metric.
        model_config (dict[str, Any] | None): The model config to use for the metric.
        criteria (str | None): The criteria to use for the metric.
        evaluation_steps (list[str] | None): The evaluation steps to use for the metric.
        threshold (float): The threshold to use for the metric.
    """

    def __init__(  # noqa: PLR0913
        self,
        model: str | ModelId | BaseLMInvoker = DefaultValues.MODEL,
        model_credentials: str | None = None,
        model_config: dict[str, Any] | None = None,
        criteria: str | None = None,
        evaluation_steps: list[str] | None = None,
        threshold: float = 0.5,
    ):
        """Initialize the custom detail case gangguan correctness metric.

        Args:
            model (str | ModelId | BaseLMInvoker, optional): The model to use for the metric.
                Defaults to DefaultValues.MODEL.
            model_credentials (str | None, optional): The model credentials to use for the metric.
                Defaults to None (falls back to GOOGLE_API_KEY env variable).
            model_config (dict[str, Any] | None, optional): The model config to use for the metric.
                Defaults to None.
            criteria (str | None, optional): The criteria to use for the metric. Defaults to None.
            evaluation_steps (list[str] | None, optional): The evaluation steps to use for the metric.
                Defaults to None.
            threshold (float, optional): The threshold to use for the metric. Defaults to 0.5.
        """
        super().__init__(
            name="detail_case_gangguan_correctness",
            model=model,
            model_credentials=model_credentials,
            model_config=model_config,
            criteria=criteria,
            evaluation_steps=evaluation_steps,
            threshold=threshold,
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        )

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        """Evaluate the metric.

        Args:
            data (MetricInput): The metric input.

        Returns:
            MetricOutput: The metric output with score binarized to integer.
        """
        output = await super()._evaluate(data)
        output[ResultMetricKeys.SCORE] = int(output[ResultMetricKeys.SCORE])
        return output

```

## Step 3: Create a Custom Evaluator

For the next step, we create our custom evaluator using the metric we have created:

```python
from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.types import EvaluatorResult, MetricInput


class CustomDetailCaseGangguanCorrectnessEvaluator(BaseEvaluator):
    """Custom detail case gangguan correctness evaluator."""

    def __init__(self, model_credentials: str, threshold: float = 0.5):
        """Initialize the CustomDetailCaseGangguanCorrectnessEvaluator.

        Args:
            model_credentials (str): The model credentials.
            threshold (float, optional): The threshold to use for the metric. Defaults to 0.5.
        """
        super().__init__(name="custom_detail_case_gangguan_correctness_evaluator")
        self.metric = CustomDetailCaseGangguanCorrectnessMetric(
            model_credentials=model_credentials,
            evaluation_steps=CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS,
            threshold=threshold,
        )

    async def _evaluate(self, data: MetricInput) -> EvaluatorResult:
        """Evaluate the custom metric.

        Args:
            data (MetricInput): The data to evaluate the metric on.

        Returns:
            EvaluatorResult: The evaluation output.
        """
        return await self.metric.evaluate(data)

```

{% hint style="info" %}
Alternatively, if you only need to orchestrate multiple metrics without custom logic, you can use Composite Evaluator directly instead of subclassing `BaseEvaluator`.
{% endhint %}

## Step 4: Perform Evaluation

To run the evaluation, we process our data, convert it into `LLMTestCase`, and pass it to the custom evaluator. You can adapt this step to fit your project’s specific requirements.

```python
import asyncio
import os

import pandas as pd

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset


async def main():
    """Main function."""

    # Initialize the custom evaluator we have just created above
    evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        threshold=0.75,
    )

    # Load the CSV dataset using DictDataset
    csv_path = "/path/to/tsel_test_data.csv"
    dataset = DictDataset.from_csv(csv_path).load()

    final_results = []
    alignment_scores = []
    for row in dataset:
        data = LLMTestCase(
            input=row["detailed_description"],
            actual_output=row["detail_case_gangguan"],
        )
        result = await evaluator.evaluate(data)
        final_results.append(
            {
                "no": row["no"],
                "query": row["detailed_description"],
                "generated_response": row["detail_case_gangguan"],
                "score": result[evaluator.name]["detail_case_gangguan_correctness"].get("score", 0),
                "explanation": result[evaluator.name]["detail_case_gangguan_correctness"].get("explanation", ""),
                "gt_score": row["score_detail_case_gangguan"],
                "is_aligned": row["score_detail_case_gangguan"]
                == result[evaluator.name]["detail_case_gangguan_correctness"].get("score", 0),
            }
        )
        alignment_scores.append(int(final_results[-1]["is_aligned"]))

    # Export the data with the evaluation results as CSV
    pd.DataFrame(final_results).to_csv("final_results_detail_case_gangguan_correctness.csv", index=False)

    # Optional Step - Calculate the alignment scores between LLM-as-a-judge and ground truth evaluation
    final_alignment_score = (sum(alignment_scores) / len(alignment_scores)) if len(alignment_scores) > 0 else 0.0
    print(f"Alignment score: {final_alignment_score * 100}%")


if __name__ == "__main__":
    asyncio.run(main())import asyncio
import os

import pandas as pd
from deepeval.test_case import LLMTestCaseParams
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.schema import ModelId

from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals import LLMTestCase
from gllm_evals.types import MetricInput, MetricOutput


async def main():
    """Main function."""

    # Initialize the custom evaluator we have just created above
    evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        threshold=0.75,
    )

    # Read our CSV data and convert it to list of dictionary
    csv_path = "/path/to/tsel_test_data.csv"
    df = pd.read_csv(csv_path)
    dataset = df.to_dict(orient="records")

    final_results = []
    alignment_scores = []
    for row in dataset:
        data = LLMTestCase(
            input=row["detailed_description"],
            actual_output=row["detail_case_gangguan"],
        )
        result = await evaluator.evaluate(data)
        final_results.append(
            {
                "no": row["no"],
                "query": row["detailed_description"],
                "generated_response": row["detail_case_gangguan"],
                "score": result[evaluator.name]["detail_case_gangguan_correctness"].get("score", 0),
                "explanation": result[evaluator.name]["detail_case_gangguan_correctness"].get("explanation", ""),
                "gt_score": row["score_detail_case_gangguan"],
                "is_aligned": row["score_detail_case_gangguan"]
                == result[evaluator.name]["detail_case_gangguan_correctness"].get("score", 0),
            }
        )
        alignment_scores.append(int(final_results[-1]["is_aligned"]))

    # Export the data with the evaluation results as CSV
    pd.DataFrame(final_results).to_csv("final_results_detail_case_gangguan_correctness.csv", index=False)

    # Optional Step - Calculate the alignment scores between LLM-as-a-judge and ground truth evaluation
    final_alignment_score = (sum(alignment_scores) / len(alignment_scores)) if len(alignment_scores) > 0 else 0.0
    print(f"Alignment score: {final_alignment_score * 100}%")


if __name__ == "__main__":
    asyncio.run(main())

```

In addition to saving the evaluation's score and explanation, we can also compute a final alignment score to check the evaluator’s accuracy by comparing its output with the ground-truth score.

Below is the CSV output based on the evaluation we have just done:

{% file src="../../../../.gitbook/assets/final_results_detail_case_gangguan_correctness.csv" %}

### Conclusion <a href="#conclusion" id="conclusion"></a>

This cookbook provides a simple guide to evaluating custom dataset using a custom metric and a custom evaluator. By following these steps, you can:

* Monitor your QA system's performance
* Automate the evaluation process if the alignment score is already high
* Ensure reliable and high-quality QA responses in production
