# GLLM Evals Migration Guide: v0.0.47 → Latest (v0.1.8)

This guide covers all **breaking changes** introduced in `gllm-evals` between `v0.0.47` and `v0.1.8`. Apply each section that is relevant to your usage.

{% hint style="warning" %}
If you previously pinned your dependency as `gllm-evals==0.0.47`, you will need to update it to the new version and apply **all** breaking changes below before your code will run.
{% endhint %}

---

## Part 1: Unified Data Model — `LLMTestCase` replaces `QAData`, `RAGData`, `AgentData`

The separate `QAData`, `RAGData`, and `AgentData` TypedDicts are **removed**. They are replaced by a single Pydantic model: `LLMTestCase`.

### Field renames

| Old field (TypedDict) | New field (`LLMTestCase`) |
|-----------------------|--------------------------|
| `query` | `input` |
| `generated_response` | `actual_output` |
| `expected_response` | `expected_output` |
| `expected_retrieved_context` | `expected_context` |

Fields unchanged: `retrieved_context`, `agent_trajectory`, `expected_agent_trajectory`, `is_refusal`.

New fields: `tools_called: list[ToolCall] | None`, `expected_tools: list[ToolCall] | None`.

### Before (v0.0.47)

```python
from gllm_evals import QAData, RAGData, AgentData

qa_row = QAData(
    query="What is AI?",
    expected_response="AI is ...",
    generated_response="AI stands for ...",
)

rag_row = RAGData(
    query="What is AI?",
    expected_response="AI is ...",
    generated_response="AI stands for ...",
    retrieved_context=["context 1", "context 2"],
    expected_retrieved_context=["context 1"],
)

agent_row = AgentData(
    agent_trajectory=[{"role": "tool", "content": "..."}],
    expected_agent_trajectory=[{"role": "tool", "content": "..."}],
)
```

### After (latest)

```python
from gllm_evals import LLMTestCase

qa_row = LLMTestCase(
    input="What is AI?",
    expected_output="AI is ...",
    actual_output="AI stands for ...",
)

rag_row = LLMTestCase(
    input="What is AI?",
    expected_output="AI is ...",
    actual_output="AI stands for ...",
    retrieved_context=["context 1", "context 2"],
    expected_context=["context 1"],
)

agent_row = LLMTestCase(
    agent_trajectory=[{"role": "tool", "content": "..."}],
    expected_agent_trajectory=[{"role": "tool", "content": "..."}],
)
```

{% hint style="info" %}
`LLMTestCase` allows extra fields. Custom columns are preserved through the pipeline and accessible via `row.my_field` or `row.model_dump()["my_field"]`.
{% endhint %}

### New `ToolCall` model

Agent data rows that include tool calls should use the `ToolCall` Pydantic model:

```python
from gllm_evals import ToolCall, LLMTestCase

row = LLMTestCase(
    input="Search for recent AI papers",
    actual_output="Here are the results ...",
    tools_called=[
        ToolCall(name="search", input_parameters={"query": "AI papers"}, output="..."),
    ],
    expected_tools=[
        ToolCall(name="search"),
    ],
)
```

---

## Part 2: `relevancy_rating` replaced by `aggregate_score` / `aggregate_success`

Evaluator output results previously included a categorical `relevancy_rating` string field (`"good"`, `"bad"`, `"incomplete"`). This is replaced by two numeric/boolean fields: `aggregate_score` (float mean of all metric scores) and `aggregate_success` (bool AND-gate across all metric pass/fail results).

### Before (v0.0.47)

```python
output = await evaluator.evaluate(data)
rating = output["relevancy_rating"]  # "good", "bad", or "incomplete"
```

### After (v0.1.8)

```python
output = await evaluator.evaluate(data)
passed = output["aggregate_success"]  # True / False
quality = output["aggregate_score"]   # 0.0 – 1.0 float
```

---

## Part 3: Per-metric output type changed — `dict` → `MetricScore` / `MetricResult`

Individual metric outputs were plain `dict` objects (`MetricOutput`) in v0.0.47. They are now typed Pydantic models.

| Type | Fields | When used |
|------|--------|-----------|
| `MetricScore` | `score`, `explanation` | Base result, returned by `build_metric_result()` |
| `MetricResult` | inherits `MetricScore` + `rubric_score`, `success`, `threshold`, `strict_mode`, `higher_is_better` | Full per-metric result inside `EvaluatorResult` |

### Before (v0.0.47)

```python
# metric output was a plain dict
result: dict = {"score": 0.9, "explanation": "Good"}
score = result["score"]
```

### After (v0.1.8)

```python
from gllm_evals.types import MetricScore, MetricResult

# MetricScore — base result
score_obj: MetricScore = ...
score_obj.score          # float | int | str
score_obj.explanation    # str | None

# MetricResult — full per-metric result inside EvaluatorResult
result: MetricResult = ...
result.score             # float | int | str   (evaluation score)
result.explanation       # str | None          (detailed explanation)
result.rubric_score      # int | float         (raw rubric value, diagnostic only)
result.success           # bool                (pass/fail: polarity + threshold)
result.threshold         # float               (threshold used to compute success)
result.strict_mode       # bool                (if True, score binarized to 0.0 or 1.0)
result.higher_is_better  # bool                (polarity direction)
```

---

## Part 4: Renamed output types

Several TypedDicts used in outputs have been renamed for clarity.

| Old name | New name |
|----------|----------|
| `EvaluationOutput` | `EvaluatorResult` |
| `EvaluationResult` | `ExperimentResult` |
| `ExperimentUrls` | `ExperimentUris` |

The `ExperimentUris` fields also changed:

| Old field | New field |
|-----------|-----------|
| `run_url` | `run_uri` |
| `leaderboard_url` | `leaderboard_uri` |

The `ExperimentResult` (formerly `EvaluationResult`) also has these field changes:

- `experiment_urls` → `experiment_uris`
- `results` is now non-optional (`list[list[EvaluatorResult]]`, was `list[list[EvaluationOutput]] | None`)
- New `summary_result: NotRequired[dict[str, Any] | None]` field

### Before (v0.0.47)

```python
from gllm_evals import EvaluationOutput, EvaluationResult

result: EvaluationResult = await evaluate(...)
urls = result["experiment_urls"]
run_url = urls["run_url"]

if result["results"] is not None:
    for batch in result["results"]:
        row: EvaluationOutput = batch[0]
```

### After (latest)

```python
from gllm_evals import EvaluatorResult
from gllm_evals.types import ExperimentResult

result: ExperimentResult = await evaluate(...)
uris = result["experiment_uris"]
run_uri = uris["run_uri"]

for batch in result["results"]:   # results is always a list now
    row: EvaluatorResult = batch[0]
```

---

## Part 5: Evaluator output key renamed — `global_explanation` → `aggregate_explanation`

All evaluator output dictionaries previously included a `"global_explanation"` key. It is renamed to `"aggregate_explanation"`.

### Before (v0.0.47)

```python
output = await evaluator.evaluate(data)
explanation = output["global_explanation"]
```

### After (latest)

```python
output = await evaluator.evaluate(data)
explanation = output["aggregate_explanation"]
```

---

## Part 6: `evaluate()` — `inference_fn` is removed

The `evaluate()` function **no longer performs live model inference**. Pre-compute `actual_output` in your dataset before calling `evaluate()`.

Additional changes: returns `ExperimentResult`; accepts `list[LLMTestCase | dict]` directly. Note: `summary_evaluators` was already present in v0.0.47 as an optional parameter.

### Before (v0.0.47)

```python
from gllm_evals import evaluate

async def my_inference_fn(row):
    return my_model.generate(row["query"])

result = await evaluate(
    data=my_dataset,
    inference_fn=my_inference_fn,
    evaluators=my_evaluators,
)
```

### After (latest)

```python
from gllm_evals import evaluate, LLMTestCase

# Pre-compute outputs yourself before evaluating
rows = [
    LLMTestCase(
        input="What is AI?",
        actual_output=my_model.generate("What is AI?"),
        expected_output="AI is ...",
    )
]

result = await evaluate(
    data=rows,
    evaluators=my_evaluators,
    # summary_evaluators=[summary_accuracy],  # was also present in 0.0.47; summary_accuracy is new
)
```

---

## Part 7: `SimpleExperimentTracker` → `CSVExperimentTracker`

`SimpleExperimentTracker` is renamed to `CSVExperimentTracker`. The constructor gains new optional parameters.

### Before (v0.0.47)

```python
from gllm_evals.experiment_tracker import SimpleExperimentTracker

tracker = SimpleExperimentTracker(
    project_name="my_project",
    output_dir="./results",
    score_key="score",
)
```

### After (latest)

```python
from gllm_evals.experiment_tracker import CSVExperimentTracker

tracker = CSVExperimentTracker(
    project_name="my_project",
    output_dir="./results",
    score_key="score",
    # extra_score_keys=["aggregate_score"],
    # leaderboard_score_key="aggregate_success",  # new default — see warning below
    # summary_evaluators=[...],
)
```

{% hint style="warning" %}
`leaderboard_score_key` now defaults to `"aggregate_success"` (a boolean pass/fail column) instead of `"score"`. Set `leaderboard_score_key="score"` explicitly to preserve the old leaderboard behavior.
{% endhint %}

---

## Part 8: Evaluator model configuration — `model` / `model_credentials` replaced by `models`

This is the **most impactful** API change. The `model: str | ModelId | BaseLMInvoker`, `model_credentials: str | None`, `model_config: dict | None`, `rule_book`, `generation_rule_engine`, and `judge: MultipleLLMAsJudge | None` parameters are **removed** from all evaluators and GEval metrics. They are replaced by a single `models` parameter that accepts pre-built `BaseLMInvoker` instances.

**Affected classes:** `GEvalGenerationEvaluator`, `BaseGenerationEvaluator`, `AgentEvaluator`, `QTEvaluator`, `SummarizationEvaluator`, `LMBasedRetrievalEvaluator`, and all GEval metrics (`GEvalCompletenessMetric`, `GEvalGroundednessMetric`, `GEvalRedundancyMetric`, `GEvalLanguageConsistencyMetric`, `GEvalRefusalMetric`, `GEvalRefusalAlignmentMetric`, etc.).

### Before (v0.0.47)

```python
from gllm_evals.evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation import GEvalCompletenessMetric

# Single judge
evaluator = GEvalGenerationEvaluator(
    model="openai/gpt-4o-mini",
    model_credentials="OPENAI_API_KEY",
    model_config={"default_hyperparameters": {"temperature": 0.0}},
    rule_book=my_rule_book,         # removed in v0.1.6
    generation_rule_engine=my_engine,  # removed in v0.1.6
)

# Multiple judges (old multi-judge config)
from gllm_evals.judge import MultipleLLMAsJudge
evaluator = GEvalGenerationEvaluator(
    model="openai/gpt-4o-mini",
    model_credentials="OPENAI_API_KEY",
    judge=MultipleLLMAsJudge(...),
)

# Individual metric
metric = GEvalCompletenessMetric(
    model="openai/gpt-4o-mini",
    model_credentials="OPENAI_API_KEY",
)
```

### After (latest)

```python
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation import GEvalCompletenessMetric

# Build the invoker yourself (credentials loaded from env var or passed explicitly)
invoker = build_lm_invoker("openai/gpt-4o-mini", credentials="OPENAI_API_KEY")

# Single judge (models=None uses the default invoker from env)
evaluator = GEvalGenerationEvaluator(models=invoker)

# Multiple homogeneous judges (same model, N times)
evaluator = GEvalGenerationEvaluator(models=[invoker] * 3)

# Multiple heterogeneous judges (different models)
invoker_a = build_lm_invoker("openai/gpt-4o-mini", credentials="OPENAI_API_KEY")
invoker_b = build_lm_invoker("openai/gpt-4o", credentials="OPENAI_API_KEY")
evaluator = GEvalGenerationEvaluator(models=[invoker_a, invoker_b])

# Individual metric
metric = GEvalCompletenessMetric(models=invoker)
```

{% hint style="info" %}
Passing `models=None` (the default) uses the built-in default invoker. Credentials are still read from environment variables in that case.
{% endhint %}

{% hint style="warning" %}
The old `judge: MultipleLLMAsJudge` multi-judge config is removed. Multi-judge is now expressed purely through the `models` list (e.g. `[invoker] * N` for homogeneous, or `[invoker_a, invoker_b]` for heterogeneous).
{% endhint %}

---

## Part 9: `enabled_metrics` parameter removed from generation evaluators

`GEvalGenerationEvaluator` and `BaseGenerationEvaluator` no longer accept an `enabled_metrics` parameter. To customise which metrics run, pass pre-configured metric instances via the `metrics` list.

### Before (v0.0.47)

```python
from gllm_evals.evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation import GEvalCompletenessMetric

evaluator = GEvalGenerationEvaluator(
    model="openai/gpt-4o-mini",
    model_credentials="OPENAI_API_KEY",
    enabled_metrics=[GEvalCompletenessMetric],   # class references
)
```

### After (latest)

```python
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation import GEvalCompletenessMetric

invoker = build_lm_invoker("openai/gpt-4o-mini", credentials="OPENAI_API_KEY")

evaluator = GEvalGenerationEvaluator(
    models=invoker,
    metrics=[GEvalCompletenessMetric(models=invoker)],   # instances
)
```

---

## Part 10: `GenerationEvaluator` → `BaseGenerationEvaluator` (base class only)

`GenerationEvaluator` is now an internal base class named `BaseGenerationEvaluator` and should not be instantiated directly. Use `GEvalGenerationEvaluator` as the concrete implementation.

### Before (v0.0.47)

```python
from gllm_evals.evaluator import GenerationEvaluator
evaluator = GenerationEvaluator(model="openai/gpt-4o-mini", model_credentials="OPENAI_API_KEY")
```

### After (latest)

```python
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.evaluator import GEvalGenerationEvaluator

invoker = build_lm_invoker("openai/gpt-4o-mini", credentials="OPENAI_API_KEY")
evaluator = GEvalGenerationEvaluator(models=invoker)
```

---

## Part 11: `CustomEvaluator` → `CompositeEvaluator`

`CustomEvaluator` is removed. Replace it with `CompositeEvaluator` — the interface is the same.

### Before (v0.0.47)

```python
from gllm_evals.evaluator import CustomEvaluator
evaluator = CustomEvaluator(metrics=[metric_a, metric_b], name="my_eval")
```

### After (latest)

```python
from gllm_evals.evaluator import CompositeEvaluator
evaluator = CompositeEvaluator(metrics=[metric_a, metric_b], name="my_eval")
```

---

## Part 12: `RAGEvaluator` is removed

`RAGEvaluator` is **removed entirely**, along with `HybridRuleBook` and `HybridRuleEngine`. Run `LMBasedRetrievalEvaluator` and `GEvalGenerationEvaluator` as separate evaluators and pass both to `evaluate()`.

### Before (v0.0.47)

```python
from gllm_evals.evaluator import HybridRuleBook, HybridRuleEngine, RAGEvaluator

evaluator = RAGEvaluator(
    model="openai/gpt-4o-mini",
    model_credentials="OPENAI_API_KEY",
    rule_book=HybridRuleBook(...),
)
```

### After (latest)

```python
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals import evaluate
from gllm_evals.evaluator import LMBasedRetrievalEvaluator, GEvalGenerationEvaluator

invoker = build_lm_invoker("openai/gpt-4o-mini", credentials="OPENAI_API_KEY")

result = await evaluate(
    data=rows,
    evaluators=[
        LMBasedRetrievalEvaluator(models=invoker),
        GEvalGenerationEvaluator(models=invoker),
    ],
)
```

---

## Part 13: Non-GEval generation metrics removed

The following non-GEval metrics are removed. Use their `GEval*` counterparts:

| Removed | Replacement |
|---------|-------------|
| `CompletenessMetric` | `GEvalCompletenessMetric` |
| `GroundednessMetric` | `GEvalGroundednessMetric` |
| `RedundancyMetric` | `GEvalRedundancyMetric` |
| `LanguageConsistencyMetric` | `GEvalLanguageConsistencyMetric` |
| `RefusalMetric` | `GEvalRefusalMetric` |
| `RefusalAlignmentMetric` | `GEvalRefusalAlignmentMetric` |

### Before (v0.0.47)

```python
from gllm_evals.metrics.generation import (
    CompletenessMetric, GroundednessMetric, RedundancyMetric,
    LanguageConsistencyMetric, RefusalMetric, RefusalAlignmentMetric,
)
```

### After (latest)

```python
from gllm_evals.metrics.generation import (
    GEvalCompletenessMetric, GEvalGroundednessMetric, GEvalRedundancyMetric,
    GEvalLanguageConsistencyMetric, GEvalRefusalMetric, GEvalRefusalAlignmentMetric,
)
```

---

## Part 14: Safety metrics moved to `gllm_evals.metrics.safety`

### Before (v0.0.47)

```python
from gllm_evals.metrics.generation import (
    DeepEvalBiasMetric, DeepEvalToxicityMetric, DeepEvalPIILeakageMetric,
    DeepEvalMisuseMetric, DeepEvalNonAdviceMetric,
    DeepEvalRoleViolationMetric, DeepEvalPromptAlignmentMetric,
)
```

### After (latest)

```python
from gllm_evals.metrics.safety import (
    DeepEvalBiasMetric, DeepEvalToxicityMetric, DeepEvalPIILeakageMetric,
    DeepEvalMisuseMetric, DeepEvalNonAdviceMetric,
    DeepEvalRoleViolationMetric, DeepEvalPromptAlignmentMetric,
)
```

---

## Part 15: Agent/tool metrics moved to `gllm_evals.metrics.tool_use`

Both `LangChainAgentTrajectoryAccuracyMetric` and `DeepEvalToolCorrectnessMetric` were in `gllm_evals.metrics.agent`. They are now in `gllm_evals.metrics.tool_use`.

### Before (v0.0.47)

```python
from gllm_evals.metrics.agent import (
    LangChainAgentTrajectoryAccuracyMetric,
    DeepEvalToolCorrectnessMetric,
)
```

### After (latest)

```python
from gllm_evals.metrics.tool_use import (
    LangChainAgentTrajectoryAccuracyMetric,
    DeepEvalToolCorrectnessMetric,
)
```

---

## Part 16: `validate_metric_result` → `build_metric_result`

The helper function for validating custom metric outputs is renamed and now returns a `MetricScore` object instead of a plain `dict`.

### Before (v0.0.47)

```python
from gllm_evals import validate_metric_result

result: dict = validate_metric_result({"score": 0.9, "explanation": "Good"})
```

### After (latest)

```python
from gllm_evals import build_metric_result
from gllm_evals.types import MetricScore

result: MetricScore = build_metric_result({"score": 0.9, "explanation": "Good"})
score = result.score
explanation = result.explanation
```

---

## Part 17: Default metric thresholds changed

If you relied on the previous default thresholds for pass/fail decisions, update your expectations or set them explicitly:

| Metric | Old default threshold | New default threshold |
|--------|-----------------------|-----------------------|
| `GEvalCompletenessMetric` | `0.5` | `1.0` |
| `GEvalGroundednessMetric` | `0.5` | `1.0` |

To restore old behavior:

```python
metric = GEvalCompletenessMetric(models=invoker, threshold=0.5)
metric = GEvalGroundednessMetric(models=invoker, threshold=0.5)
```

---

## Part 18: gllm-inference v0.6 dependency upgrade

`gllm-evals` now requires `gllm-inference>=0.6.0`. If your code imports directly from `gllm_inference`, also apply the **gllm-inference v0.5 → v0.6 migration guide**.

Key breaking changes from `gllm-inference` that affect evals usage:

1. **`LMInvoker.invoke()` always returns `LMOutput`** — no longer returns `str`.
2. **`Reasoning` renamed to `Thinking`** — update any schema imports.
3. **`prompt_kwargs` removed from LMRP** — pass prompt variables as keyword arguments.
4. **`OpenAICompatibleLMInvoker` removed** — use `OpenAIChatCompletionsLMInvoker(base_url=...)`.
5. **`build_lm_invoker` import path changed** — now use `from gllm_inference.lm_invoker import build_lm_invoker`.

---

## New Features (non-breaking)

These are additive features available after upgrade:

1. **`summary_accuracy` built-in summary evaluator** — compute batch-level accuracy rate automatically. The `summary_evaluators` param in `evaluate()` existed before, but this is the first built-in implementation.
   ```python
   from gllm_evals import summary_accuracy, evaluate

   result = await evaluate(
       data=rows,
       evaluators=my_evaluators,
       summary_evaluators=[summary_accuracy],
   )
   print(result["summary_result"])  # {"accuracy_rate": 0.85}
   ```

2. **`CompositeEvaluator`** — combine any `BaseMetric` instances into a single evaluator unit.

3. **`DictDataset` universal builder methods** — load datasets directly from external sources without manual preprocessing.
   ```python
   from gllm_evals.dataset.dict_dataset import DictDataset

   # From HuggingFace Hub
   dataset = DictDataset.from_huggingface_hub(path_or_name="my-org/my-dataset", split="test")

   # From Google Sheets (async)
   dataset = await DictDataset.from_gsheets(
       sheet_id="<SHEET_ID>",
       worksheet_name="Sheet1",
       client_email="svc@project.iam.gserviceaccount.com",
       private_key="<BASE64_KEY>",
   )

   # From Langfuse
   dataset = DictDataset.from_langfuse(langfuse_client=client, dataset_name="my-dataset")
   ```

4. **`CSVExperimentTracker` per-metric `success` columns** — the tracker now writes a `*.success` boolean column for every metric alongside its score column, making pass/fail filtering easy in the output CSV.

5. **Lazy optional imports** — `deepeval`, `ragas`, and `langchain` extras now degrade gracefully if not installed; their imports no longer fail at package import time.

---

## Quick Reference: All Changed Import Paths

| Old import | New import |
|-----------|------------|
| `from gllm_evals import QAData` | `from gllm_evals import LLMTestCase` |
| `from gllm_evals import RAGData` | `from gllm_evals import LLMTestCase` |
| `from gllm_evals import AgentData` | `from gllm_evals import LLMTestCase` |
| `from gllm_evals import EvaluationOutput` | `from gllm_evals import EvaluatorResult` |
| `from gllm_evals import validate_metric_result` | `from gllm_evals import build_metric_result` |
| `from gllm_evals.experiment_tracker import SimpleExperimentTracker` | `from gllm_evals.experiment_tracker import CSVExperimentTracker` |
| `from gllm_evals.evaluator import GenerationEvaluator` | `from gllm_evals.evaluator import GEvalGenerationEvaluator` |
| `from gllm_evals.evaluator import CustomEvaluator` | `from gllm_evals.evaluator import CompositeEvaluator` |
| `from gllm_evals.evaluator import RAGEvaluator` | *(removed — see Part 10)* |
| `from gllm_evals.evaluator import HybridRuleBook, HybridRuleEngine` | *(removed — no replacement)* |
| `from gllm_evals.metrics.generation import CompletenessMetric` | `from gllm_evals.metrics.generation import GEvalCompletenessMetric` |
| `from gllm_evals.metrics.generation import GroundednessMetric` | `from gllm_evals.metrics.generation import GEvalGroundednessMetric` |
| `from gllm_evals.metrics.generation import RedundancyMetric` | `from gllm_evals.metrics.generation import GEvalRedundancyMetric` |
| `from gllm_evals.metrics.generation import LanguageConsistencyMetric` | `from gllm_evals.metrics.generation import GEvalLanguageConsistencyMetric` |
| `from gllm_evals.metrics.generation import RefusalMetric` | `from gllm_evals.metrics.generation import GEvalRefusalMetric` |
| `from gllm_evals.metrics.generation import RefusalAlignmentMetric` | `from gllm_evals.metrics.generation import GEvalRefusalAlignmentMetric` |
| `from gllm_evals.metrics.generation import DeepEvalBiasMetric` | `from gllm_evals.metrics.safety import DeepEvalBiasMetric` |
| `from gllm_evals.metrics.generation import DeepEvalToxicityMetric` | `from gllm_evals.metrics.safety import DeepEvalToxicityMetric` |
| `from gllm_evals.metrics.generation import DeepEvalPIILeakageMetric` | `from gllm_evals.metrics.safety import DeepEvalPIILeakageMetric` |
| `from gllm_evals.metrics.generation import DeepEvalMisuseMetric` | `from gllm_evals.metrics.safety import DeepEvalMisuseMetric` |
| `from gllm_evals.metrics.generation import DeepEvalNonAdviceMetric` | `from gllm_evals.metrics.safety import DeepEvalNonAdviceMetric` |
| `from gllm_evals.metrics.generation import DeepEvalRoleViolationMetric` | `from gllm_evals.metrics.safety import DeepEvalRoleViolationMetric` |
| `from gllm_evals.metrics.generation import DeepEvalPromptAlignmentMetric` | `from gllm_evals.metrics.safety import DeepEvalPromptAlignmentMetric` |
| `from gllm_evals.metrics.agent import LangChainAgentTrajectoryAccuracyMetric` | `from gllm_evals.metrics.tool_use import LangChainAgentTrajectoryAccuracyMetric` |
| `from gllm_evals.metrics.agent import DeepEvalToolCorrectnessMetric` | `from gllm_evals.metrics.tool_use import DeepEvalToolCorrectnessMetric` |

