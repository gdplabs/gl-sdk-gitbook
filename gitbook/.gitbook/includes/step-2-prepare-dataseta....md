---
title: '## Step 2: Prepare DatasetA...'
---

````
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

**QnA Chatbot** \-- input is a question, expected output is the reference answer.

| no | input | expected\_output |
| :---- | :---- | :---- |
| 1 | Kapan Strategi Nasional Kecerdasan Artifisial (Stranas KA) resmi diluncurkan? | Stranas KA resmi diluncurkan pada 10 Agustus 2020\. |

**Conversation Title Generator** \-- input is a full conversation transcript, expected output is the title the system should produce.

| no | input | expected\_output |
| :---- | :---- | :---- |
| 1 | | Entity | Owner | Event Message | Consumer | Reason for Use | Release Date (YYYY-MM-dd) | \<long table content\> Convert that table into html | Table Conversion into HTML |

The column names in your CSV do not need to match `input` and `expected_output` exactly. Map them explicitly when constructing `LLMTestCase` (see code below).

### Using gllm-evals

`gllm-evals` represents each row as an `LLMTestCase` object. The example below loads from CSV, but any dataset source works. Load your data, run your target system to generate `actual_output`, then construct the list:

```py
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

This `data` list is what you will pass into `evaluate()` when running evaluation.  
For all supported dataset types (Google Sheets, HuggingFace, Langfuse, JSONL, and more) see the [Dataset Reference](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/dataset).
````
