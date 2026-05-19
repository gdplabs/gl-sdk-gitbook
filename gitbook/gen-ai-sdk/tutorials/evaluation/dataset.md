# 📂 Dataset

We provide a `BaseDataset` class as the foundation, and several ready-to-use dataset types. These make it simple to load data from different sources in a unified way. This dataset object also can be passed to the `evaluate` function that will be used for end-to-end evaluation.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/dataset" %}

***

## Available Datasets

1. [DictDataset](dataset.md#dictdataset)
2. [HuggingFaceDataset](dataset.md#huggingfacedataset)
3. [SpreadsheetDataset](dataset.md#spreadsheetdataset)
4. [LangfuseDataset](dataset.md#langfusedataset)

***

### 📖 DictDataset

**Use when:** You want to store your dataset directly in a **list of** **dictionary format**.

It can be created from JSONL or CSV.

Example usage:

```python
from gllm_evals.dataset.dict_dataset import DictDataset

csv_path = "path/to/csv/data"
data: DictDataset = DictDataset.from_csv(csv_path)
```

***

### 🤗 HuggingFaceDataset

**Use when:** You want to load datasets directly from the HuggingFace Hub or from a Python list.

Example usage:

```python
from datasets import load_dataset

from gllm_evals.dataset.hf_dataset import HuggingFaceDataset

hf_dataset_path = "path/to/hf/dataset"
data: HuggingFaceDataset = HuggingFaceDataset(
    dataset=load_dataset(path=path_or_name, split=split, **kwargs)
)
```

***

### 📝 SpreadsheetDataset

**Use when:** You want to load datasets from Google Sheets.

Example usage:

```python
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset

data: SpreadsheetDataset = await SpreadsheetDataset.from_gsheets(
    sheet_id="sheet-id",
    worksheet_name="worksheet-name",
    client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
    private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
)
```

***

### 📊 LangfuseDataset

**Use when:** You want to manage datasets in Langfuse or want to import from multiple formats (from Langfuse itself, dictionary, google sheets, CSV, JSONL).

Example usage:

```python
from langfuse import get_client

from gllm_evals.dataset.langfuse_dataset import LangfuseDataset

data: LangfuseDataset = LangfuseDataset.from_langfuse(
    langfuse_client=get_client(),
    dataset_name="dataset-name"
)
```

***

### Loading to LLMTestCase

All dataset types can be converted to `LLMTestCase` objects for use with metrics and evaluators. `LLMTestCase` is the universal data structure used across all `gllm-evals` evaluations.

#### Converting Datasets

After loading a dataset, you can convert it to a list of `LLMTestCase` objects:

```python
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.types import LLMTestCase

# Load dataset
dataset = DictDataset.from_csv("path/to/csv/data")

# Convert to LLMTestCase objects
data = [
    LLMTestCase(
        input=row_dict["input"],
        actual_output=row_dict["actual_output"],
        expected_output=row_dict.get("expected_output"),
    )
    for row_dict in dataset.load()
]
```

For detailed information about `LLMTestCase` structure and available fields, see [LLMTestCase](llmtestcase.md).

#### Using with Evaluators

Once converted to `LLMTestCase`, you can use the data directly with evaluators:

```python
import asyncio

from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase

async def main():
    # Load and convert dataset
    dataset = DictDataset.from_csv("path/to/csv/data")
    data = [
        LLMTestCase(
            input=row_dict["input"],
            actual_output=row_dict["actual_output"],
            expected_output=row_dict.get("expected_output"),
        )
        for row_dict in dataset.load()
    ]

    # Use with evaluator
    evaluator = GEvalGenerationEvaluator()
    results = await evaluator.evaluate_batch(data)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
For detailed information about `LLMTestCase` structure and fields, see [LLMTestCase](llmtestcase.md).
{% endhint %}

See [Expected Outputs/Responses Design](dataset/expected-output-responses-design.md) for a full guide on types of expected outputs and best practices for writing them.

