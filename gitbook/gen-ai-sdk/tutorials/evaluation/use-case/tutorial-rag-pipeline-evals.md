# Evaluate Your RAG Chatbot: A Practical Journey

This tutorial follows a small team that built a RAG chatbot for a researcher — and then had to answer the hard question: *"But how do you actually know it works?"* Each section maps to one step of the [Evals Lifecycle](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle). By the end, you will have run two evaluation scripts, seen a real failure, and made a calibrated, expert-backed decision to adjust the pass criterion.

{% hint style="info" %}
**New to GL SDK evaluation?** Read the [Evals Lifecycle](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle) page first. This tutorial is a worked example of that lifecycle applied to a real RAG pipeline.
{% endhint %}

***

## The Situation

> *Your team has just shipped a RAG chatbot for client, a researcher company who studies **Imaginary Animals**. It returns answers from a vector knowledge base. The demo went smoothly. Then your tech lead asks the question you were hoping to avoid: "But how do you know it actually works?" You have been manually testing with a few queries and eyeballing the results. It felt fine. But what if it quietly misses facts? What if it makes things up? What if the 3 queries you tested are the only 3 it handles correctly?*

This is the moment where the **Evals Lifecycle** begins. Instead of "it looks fine," you build a process that can answer: *does it meet defined criteria, across a defined dataset, measured by a consistent and explainable judge?*

### What Can Go Wrong in a RAG Pipeline

Before writing a single line of eval code, it helps to name the failure modes you are measuring. A RAG pipeline has three distinct ways to fail:

| Failure Mode | What Happens | Metric That Catches It |
| --- | --- | --- |
| **Retrieval miss** | The retriever never fetched the relevant chunks | `completeness` fails |
| **Generation hallucination** | The LLM invented facts not in the retrieved context | `groundedness` fails |
| **Generation drop** | The retriever fetched the right chunks but the LLM ignored them | `completeness` fails |

The third failure mode is the trickiest: a retrieval miss and a generation drop produce identical symptoms — `completeness` fails in both cases. The diagnostic guide in Step 4 explains how to tell them apart.

***

## 🚀 Getting Started

To follow along, use the code from the **Chatbot Using RAG Pipeline** cookbook.

{% stepper %}
{% step %}
**Clone the repository & open the directory**

```bash
git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/use-case/chatbot_using_rag_pipeline
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

Create a file called `.env` in the project root:

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
| **System type** | RAG chatbot |
| **Task** | Answer questions about imaginary animals from a vector knowledge base |
| **Inputs** | A user query sent to the chatbot |
| **Outputs** | A text answer that is **complete** (covers all key facts from `expected_output`), **grounded** (every claim is supported by `retrieved_context`), and **non-redundant** (no unnecessary repetition) |

Notice what is **not** in that table: no mention of accuracy percentages, no thresholds yet. This step is purely descriptive — you are drawing a boundary around the system you will evaluate.

{% hint style="info" %}
`gllm-evals` is a **judge**, not a pipeline runner. It evaluates outputs your system already produced — it does not call your pipeline during evaluation. This means by Step 2, each row in your dataset needs the `actual_output` your pipeline generated and the `retrieved_context` it used.
{% endhint %}

***

## Step 2: Prepare the Dataset

> *You ask client to write down three questions they regularly asks the chatbot, and for each question, write what they would consider a correct answer. "Think of it as writing the answer key," you say.*

A dataset is a collection of test cases that represent real usage. Even 3 well-chosen cases written by someone who knows the domain can expose meaningful failure modes. The key insight: the domain expert writes the expected outputs — not an engineer, not the LLM.

**What the CSV stores** — only what you know before running the pipeline:

| Column | Description |
| --- | --- |
| `query` | The user question (becomes `input` in `LLMTestCase`) |
| `expected_output` | The reference answer — the rubric the judge will use |

**What the pipeline generates at eval time** — never stored in the CSV, generated fresh each run:

| Field | Source |
| --- | --- |
| `actual_output` | The live response from the RAG pipeline for that query |
| `retrieved_context` | The chunks the retriever fetched — required to score `groundedness` |

Client's dataset lives at `data/eval_dataset.csv`. Here is what they wrote:

| # | `query` | `expected_output` |
| --- | --- | --- |
| 1 | Give me nocturnal creatures from the dataset | The nocturnal creatures in the dataset include the Luminafox and the Gloombat. |
| 2 | Where does the Dreamwhale live and what does it eat? | The Dreamwhale lives in the deepest oceans of the Reverie Sea. It feeds on plankton and small fish filtered through baleen-like structures. |
| 3 | What special ability does the Thunderbeetle have? | The Thunderbeetle can store electrical energy from lightning strikes in specialized organs and release it during mating season, creating spectacular lightning displays. |


***

## Step 3: Define Metrics and Success Criteria

> *question: "What makes an answer good?" they says three things: "It should cover the key facts. It shouldn't make things up. And please — no rambling." You write those down. Each one maps directly to a metric.*

For a RAG chatbot answering factual questions, three metrics cover all three failure modes identified earlier:

| Metric | What It Measures | `higher_is_better` | Default Threshold |
| --- | --- | --- | --- |
| `completeness` | All key facts from `expected_output` are present in `actual_output` | `true` | `1.0` |
| `groundedness` | Every claim in `actual_output` is supported by `retrieved_context` | `true` | `1.0` |
| `redundancy` | `actual_output` does not contain unnecessary repetition | `false` | `0.5` |

**Why these three together?** `completeness` catches retrieval misses and generation drops. `groundedness` catches hallucination. `redundancy` catches a chatty or looping response. Together they measure whether the system found the right information, used only that information, and presented it concisely.

**Why does `redundancy` work backwards?** A `redundancy` score of `0.0` means no repetition detected — that is the ideal outcome. Because lower is better, the metric uses `higher_is_better: false`, which means `success: true` when the score is **below** the threshold (`0.5`). Every other metric in this set works the normal way.

The `GEvalGenerationEvaluator` bundles all three metrics and runs them automatically when you pass it an `LLMTestCase`.

***

## Step 4: Evaluate and Improve

### Writing the Evaluation Script

> *With dataset and metrics defined, you open `eval.py` and write the evaluation. The goal: collect the outputs for every test case, then hand everything to the judge in one call.*

This example uses `MOCK_PIPELINE_OUTPUTS` to simulate pipeline responses without running a live RAG pipeline — it simplifies the setup so you can focus on the evaluation logic. When writing your own evals, replace `run_pipeline()` with your actual pipeline invocation.

{% code title="eval.py" lineNumbers="true" %}
```python
MOCK_PIPELINE_OUTPUTS: dict[str, tuple[str, str]] = {
    "Give me nocturnal creatures from the dataset": (
        "- Luminafox — a nocturnal creature in Nyxland's luminescent forests...\n"
        "- Dusk Panther — prowls the twilight forests of Shadowglade...",
        "Luminafox chunk 1\nLuminafox chunk 2\nDusk Panther chunk 1",
    ),
    # ... (Cases 2 and 3 follow the same structure)
}

def run_pipeline(query: str) -> tuple[str, str]:
    return MOCK_PIPELINE_OUTPUTS[query]


async def main():
    pipeline_results = [run_pipeline(row["query"]) for row in DATASET]

    # Build LLMTestCase list — CSV provides input/expected_output,
    # pipeline provides actual_output/retrieved_context
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=actual_output,
            expected_output=row["expected_output"],
            retrieved_context=retrieved_context,
        )
        for row, (actual_output, retrieved_context) in zip(DATASET, pipeline_results)
    ]

    judge_model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    tracker = CSVExperimentTracker(
        project_name="rag-chatbot-eval",
        output_dir=OUTPUT_DIR,
        include_eval_result=True,
    )
    experiment_result = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=judge_model)],
        experiment_tracker=tracker,
    )
    print(experiment_result)
```
{% endcode %}

**`MOCK_PIPELINE_OUTPUTS`** — a dict that maps each query to `(actual_output, retrieved_context)`. These are the exact outputs produced by the real RAG pipeline, captured once and frozen here so the eval can run without pipeline dependencies.

**`run_pipeline`** — returns the pre-captured mock output for a query. In a live system, this would invoke your actual RAG pipeline.

**`zip(DATASET, pipeline_results)`** — pairs each dataset row with its corresponding pipeline output. Since both are iterated in the same order, the pairing is always correct.

**`LLMTestCase`** — a container the judge reads. It bundles:
- `input` — what the user asked
- `actual_output` — what the pipeline said
- `expected_output` — what client said it should say (the expected answer)
- `retrieved_context` — what the retriever fetched (required for `groundedness`)

**`CSVExperimentTracker`** — automatically writes two files after each run:
- `results/experiment_results.csv` — one row per test case with per-metric scores and full judge explanations
- `results/leaderboard.csv` — one row per run with an average score, useful for tracking improvement over time

Run the evaluation:

```bash
uv run eval.py
```

### First Run: Two Cases Pass, One Fails

> *The results come in. You scan through them. Cases 2 and 3 pass with perfect scores. Then you see Case 1: `aggregate_success: False`. You read the judge explanation.*

```python
{
  'run_id': 'rag-chatbot-eval_...',
  'num_samples': 3,
  'results': [
    [{'generation': {'aggregate_success': False, 'aggregate_score': 0.83,
        'completeness': {'score': 0.5, 'success': False, 'threshold': 1.0, ...},
        'groundedness': {'score': 1.0, 'success': True, ...},
        'redundancy':   {'score': 0.0, 'success': True, ...}}}],
    [{'generation': {'aggregate_success': True, 'aggregate_score': 1.0, ...}}],
    [{'generation': {'aggregate_success': True, 'aggregate_score': 1.0, ...}}],
  ],
  'experiment_uris': {
    'run_uri': 'results/experiment_results.csv',
    'leaderboard_uri': 'results/leaderboard.csv'
  },
}
```

Case 1 judge explanation: *"The minimum key facts are: [Luminafox] and [Gloombat]. The Generated Response Matched 'Luminafox' and provided additional descriptive details. However, the 'Gloombat' is Missing from the response. The inclusion of the 'Dusk Panther' is treated as extra information which carries no penalty, but it does not fulfill the requirement for the missing key fact. Per Step 5C Coverage Rule, because some minimum key facts are matched but at least one is missing, the response is categorized as partial coverage."* Completeness score: `0.5`. Threshold: `1.0`. Result: `success: False`.

Here is what each result field means:

| Field | Meaning |
| --- | --- |
| `aggregate_success` | `false` if **any** single metric fails its threshold |
| `aggregate_score` | Average score across all metrics |
| `score` | Normalized 0–1 score for this metric |
| `success` | `true` if the score meets the threshold |
| `explanation` | The judge's reasoning — **the most useful field for diagnosing failures** |
| `higher_is_better` | `true` for most metrics; `false` for `redundancy` |

### Diagnosing the Case 1 Failure

> *You open `results/experiment_results.csv` and read the full explanation. The judge says: "Gloombat was not present in the pipeline response." You check `retrieved_context` for Case 1 — Gloombat's chunk was never returned by the retriever. The pipeline only fetched Luminafox chunks (with some duplicates) and Dusk Panther.*

This is the core of Step 4: **evaluate → inspect → fix → repeat**.

***

## Step 5: Calibrate the Evals

> *Before you close the laptop, your tech lead asks the second uncomfortable question: "How do you know the judge is right?" You realize you have been trusting the LLM judge without ever checking whether its verdicts match what a human would say.*

Calibration answers one question: **can I trust these scores?** A judge model is itself an LLM — it can be too strict, too lenient, or inconsistent. Its verdicts need to be cross-checked against human ground truth before you rely on them for decisions.

Proceed to calibration when any of the following apply:
- The judge's verdicts don't match your own reading of the outputs.
- The pass rate feels implausibly high or low for what you know about the system.
- You are about to make a production deployment decision based on scores.

### The Conversation That Triggers It

> *You bring the Case 1 result to the client. They read the pipeline output — it mentioned Luminafox clearly, and included Dusk Panther, which is also nocturnal. Gloombat was absent. They look at the completeness score of 0.5 and the `success: false` verdict, then say: "Wait — the score says only 1 of 2 required facts were covered. But Dusk Panther is nocturnal too. The system actually gave me two nocturnal creatures. Why does it need to score 1.0 to pass? For a browse query, a representative sample is enough — I'll ask follow-ups for the rest. Isn't a 50% threshold enough?"*

This is the calibration trigger. The judge scored correctly — `0.5` accurately reflects 1/2 required facts covered. But the **threshold** of `1.0` may be too strict for this specific query type. The client's domain expert, just told you that.

### What the Results Show

| Case | Query | Completeness | Groundedness | Redundancy | Pass |
| --- | --- | --- | --- | --- | --- |
| 1 | Give me nocturnal creatures… | 0.5 | 1.0 | 0.0 | ✗ |
| 2 | Where does the Dreamwhale live… | 1.0 | 1.0 | 0.0 | ✓ |
| 3 | What special ability does the Thunderbeetle… | 1.0 | 1.0 | 0.0 | ✓ |

**Human review of Case 1:** score of `0.5` is accurate — Luminafox matched, Gloombat missed. The judge is not wrong. The question is whether the threshold of `1.0` is the right policy for a browse query.

### Why Lowering the Threshold Is Justified

This is the most important calibration judgment call. Lowering a threshold can either be a **legitimate calibration** or a **way to hide a real failure** — the difference lies entirely in whether a domain expert endorses it.

Here is the reasoning that makes it legitimate in this case:

**1. The query type matters.** "Give me nocturnal creatures" is a browse query, not a targeted lookup. Browse queries are designed for exploration — the user expects a sample to orient from, not an exhaustive list. Client explicitly confirmed this usage pattern: *"I ask follow-ups for the rest."*

**2. A threshold is a policy, not a fact.** `threshold=1.0` says: *"the system must cover every expected fact to pass."* That is the right policy for precise queries like "What does the Dreamwhale eat?" — where an incomplete answer is genuinely misleading. For a browse query, it is a bar that any `top_k=5` retriever will frequently miss — not because the system is broken, but because the retrieval paradigm is sampling, not exhaustive search.

**3. The alternative is worse.** If you keep `threshold=1.0` for browse queries, you face a permanently failing eval with no path to green. That trains your team to ignore the metric. A calibrated threshold that reflects real user expectations gives you a signal you can actually act on.

**4. Expert sign-off is the safeguard.** Calibration without domain expert review is just moving goalposts. With Client explicit endorsement — *"50% coverage is sufficient for browse queries"* — you have a documented, defensible reason that can be traced back to a real user need.

### The Calibrated Script: `eval_calibrated.py`

You copy `eval.py` to `eval_calibrated.py` and make one targeted change — override the `completeness` threshold using a custom metric instance:

{% code title="eval_calibrated.py" %}
```python
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric

# Calibrated evaluator.
# completeness threshold lowered from 1.0 → 0.5 after SME review:
# Client confirmed that for browse queries, representative coverage is sufficient.
experiment_result = await evaluate(
    data=data,
    evaluators=[
        GEvalGenerationEvaluator(
            models=judge_model,
            metrics=[
                GEvalCompletenessMetric(threshold=0.5),  # was 1.0
                GEvalGroundednessMetric(),
                GEvalRedundancyMetric(),
            ],
        )
    ],
    experiment_tracker=tracker,
)
```
{% endcode %}

**Why pass individual metric instances instead of just `GEvalGenerationEvaluator(models=judge_model)`?** The default constructor uses each metric's built-in default threshold — `1.0` for `completeness` and `groundedness`, `0.5` for `redundancy`. Passing explicit metric instances lets you override individual thresholds without affecting the others.

Run the calibrated evaluation:

```bash
uv run eval_calibrated.py
```

**Effect:** Case 1 completeness score is `0.5`, threshold is now `0.5` → `success: True` → `aggregate_success: True`. All three cases pass.

### What Calibration Is Not

Calibration is not about making failing cases pass by lowering the bar until everything is green. The test is: **would a domain expert reviewing the pipeline output agree with the verdict?**

- If the expert says *"yes, 0.5 is a fair score and a pass is reasonable"* → calibration is legitimate.
- If the expert says *"no, the system really should have found all the animals"* → keep the threshold at `1.0` and fix the retriever instead.

In our case, client said the first. The calibration is documented, traceable, and grounded in a real user conversation.


See the [Calibrate the Evals](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/calibrate-the-evals) guide for the full calibration workflow, including systematic human agreement scoring across multiple annotators.

***

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation Evals Lifecycle page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle).