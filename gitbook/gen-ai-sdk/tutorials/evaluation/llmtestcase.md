# 🧾 LLMTestCase

## 🧾 LLMTestCase

**LLMTestCase** is the universal data structure used across all `gllm-evals` evaluations. It represents a single evaluation row and provides a standardized interface for passing data to metrics and evaluators.

## Overview

`LLMTestCase` is a Pydantic BaseModel that serves as the canonical input format for:

* All generation metrics (completeness, groundedness, redundancy, etc.)
* All retrieval metrics
* All agent evaluation metrics
* All evaluator/scorer components

Using `LLMTestCase` ensures consistency across different evaluation types and allows the library to handle various evaluation scenarios (QA, RAG, agents, tool use) with a single unified data model.

## Structure

All fields in `LLMTestCase` are optional, allowing a single row to represent different evaluation cases:

### Core Fields

* **input** (`str | None`): Input query or user prompt
* **actual\_output** (`str | None`): Model-generated response to be evaluated
* **expected\_output** (`str | None`): Reference or ground truth answer

### Context Fields

* **retrieved\_context** (`str | list[str] | None`): Retrieved context used to answer the query (for RAG evaluation)
* **expected\_context** (`str | list[str] | None`): Reference context expected to be retrieved (for retrieval evaluation)

### Agent Fields

* **agent\_trajectory** (`list[dict[str, Any]] | None`): Agent execution trace (for agent evaluation)
* **expected\_agent\_trajectory** (`list[dict[str, Any]] | None`): Reference agent execution trace
* **tools\_called** (`list[ToolCall] | None`): Tools invoked by the agent
* **expected\_tools** (`list[ToolCall] | None`): Tools expected to be invoked

### Special Fields

* **is\_refusal** (`bool | None`): Whether the sample is a refusal case (for refusal alignment evaluation)

### Extra Fields

`LLMTestCase` allows extra fields beyond those listed above. These are preserved throughout evaluation and can be accessed by attribute or via `model_dump()`:

```python
row = LLMTestCase(input="q", custom_score=0.9)
row.custom_score          # 0.9
row.model_dump()["custom_score"]  # 0.9
```

## ToolCall Type

`ToolCall` is a structured data type used to represent tool invocations in agent evaluation. It is used in the `tools_called` and `expected_tools` fields of `LLMTestCase`.

### Structure

* **name** (`str`): The name of the tool that was invoked
* **description** (`str | None`, optional): Tool description or metadata
* **reasoning** (`str | None`, optional): The model's reasoning for selecting the tool
* **output** (`Any | None`, optional): The output returned by the tool
* **input\_parameters** (`dict[str, Any] | None`, optional): The input parameters passed to the tool

### Creating ToolCall Objects

You can create `ToolCall` objects directly:

```python
from gllm_evals.types import LLMTestCase, ToolCall

data = LLMTestCase(
    input="Search for information about Python",
    actual_output="I found information about Python...",
    tools_called=[
        ToolCall(
            name="search",
            input_parameters={"query": "Python programming"},
            output="Python is a high-level programming language..."
        )
    ],
)
```

Or convert from dictionaries using the `from_dicts` class method:

```python
from gllm_evals.types import LLMTestCase, ToolCall

tool_calls_dicts = [
    {
        "name": "search",
        "input_parameters": {"query": "Python programming"},
        "output": "Python is a high-level programming language..."
    }
]

data = LLMTestCase(
    input="Search for information about Python",
    actual_output="I found information about Python...",
    tools_called=ToolCall.from_dicts(tool_calls_dicts),
)
```

## Examples

### QA Evaluation

For simple question-answering evaluation:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    actual_output="Paris",
    expected_output="Paris is the capital of France.",
)
```

### RAG Evaluation

For retrieval-augmented generation evaluation:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    actual_output="Paris is the capital of France.",
    retrieved_context="Paris is the capital city of France.",
    expected_output="Paris",
)
```

### Agent Evaluation

For agent-style evaluation with tool calls:

```python
from gllm_evals.types import LLMTestCase, ToolCall

data = LLMTestCase(
    input="Search for information about Python",
    actual_output="I found information about Python...",
    tools_called=[
        ToolCall(
            name="search",
            input_parameters={"query": "Python programming"},
            output="Python is a high-level programming language..."
        )
    ],
    expected_tools=[
        ToolCall(
            name="search",
            input_parameters={"query": "Python programming"},
        )
    ],
)
```

### Retrieval Evaluation

For retrieval system evaluation:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    retrieved_context=["Paris is the capital city of France.", "France is in Europe."],
    expected_context=["Paris is the capital city of France."],
)
```

## Usage with Metrics

`LLMTestCase` is the standard input type for all metrics:

```python
import asyncio
from gllm_evals.types import LLMTestCase
from gllm_evals.metrics import GEvalCompletenessMetric

async def main():
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris",
        expected_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage with Evaluators

`LLMTestCase` is also the standard input type for all evaluators:

```python
import asyncio
from gllm_evals.types import LLMTestCase
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator

async def main():
    evaluator = GEvalGenerationEvaluator()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris",
        expected_output="Paris is the capital of France.",
        retrieved_context="Paris is the capital city of France.",
    )
    result = await evaluator.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
