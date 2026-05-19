# 🧭 Calibrate the Evals

## 🧭 Calibrate the Evals

After running evaluation (e.g. using evaluate()), a natural question is: can I trust these scores?

The answer is: **not automatically**. An LLM judge is itself a model — it can be wrong, misconfigured, or applied to the wrong type of question. Calibration is the process of verifying your judge's trustworthiness and fixing it when it falls short.

***

## Two Datasets, Two Purposes

Before anything else, clarify which dataset is which. Conflating them is the most common source of confusion in calibration.

<table><thead><tr><th width="202">Dataset</th><th>Purpose</th><th>Who labels it</th></tr></thead><tbody><tr><td><strong>Calibration Dataset</strong></td><td>Tune the judge. Accumulated across all experiments. Grows over time as new edge cases are found.</td><td>SME, once per case. Rows are added incrementally as new edge cases are discovered across evaluation runs.</td></tr><tr><td><strong>Calibration Validation Set</strong></td><td>The SME-labeled rows from the current experiment's new outputs. Used as the validation signal to check whether the judge is still calibrated. After the experiment, merged into the Calibration Dataset.</td><td>SME, after each evaluation run. Coverage depends on dataset size: all rows if ≤ 30; priority-stratified sample if > 30.</td></tr></tbody></table>

The Calibration Dataset is used to improve the judge. The Calibration Validation Set is used to check whether the current judge still works on new outputs. They are separate during each experiment, then merged afterward.

***

## What Calibration Measures

Calibration is measured by the Human-LLM Agreement Rate — how closely the LLM judge's verdicts match the verdicts of an SME (Subject Matter Expert). In this context, "human" refers specifically to an SME: a reviewer with sufficient domain expertise to reliably judge output quality for the task at hand.

Do not use **overall agreement rate** as your metric. On an imbalanced dataset — which is common, since a mostly-working system produces far more passes than fails — a judge that approves everything can still achieve 90% overall agreement while completely missing every real failure.

Use **TPR and TNR** instead, which measure each direction separately:

**TPR (True Positive Rate)** — of all outputs SME labeled PASS, what percentage did the judge also PASS?

```
TPR = TP / (TP + FN)
```

A low TPR means the judge is too strict — penalizing good outputs.

**TNR (True Negative Rate)** — of all outputs SME labeled FAIL, what percentage did the judge also FAIL?

```
TNR = TN / (TN + FP)
```

A low TNR means the judge is too lenient — missing real failures. This is the more dangerous failure mode.

**Stopping criterion: both TPR ≥ 90% AND TNR ≥ 90%.**

***

## Calibration Lifecycle

### Phase 1 — Initial Calibration (Done Once)

This phase runs before any experiment result is trusted.

**Determine SME coverage based on dataset size:**

```
Dataset size     SME coverage
─────────────────────────────────────────────────────
≤ 30 rows   →   Review ALL rows

> 30 rows   →   Run a naive/default judge first, then:
                  - SME labels ALL rows judge marked FAIL
                  - SME labels a random sample of rows judge marked PASS
                    (enough to get ~15–20 labeled PASSes minimum)
                Target: ~40–50 total labeled rows
```

Why label all FAILs when the dataset is large? Because TNR is computed over FAILs — if you under-sample them, your TNR estimate is unstable and you cannot tell whether the judge is truly catching failures.

**Tuning loop:**

```
1. Run judge on all rows in Calibration Dataset
2. Compare judge verdict vs SME label for every row
3. Compute TPR + TNR over all labeled rows
4. If TPR/TNR ≥ 90%: calibration confirmed ✓ → go to Phase 2
5. If TPR/TNR < 90%:
     → Find disagreement cases (judge ≠ SME)
     → SME reviews each disagreement:
         Is the judge wrong?     → fix judge (see Root Causes section)
         Is the SME label wrong? → correct the label
     → Fix judge (prompt, threshold, few-shots)
     → Return to step 1
```

{% hint style="info" %}
TPR/TNR ≥ 90% measured on the set you tuned against is somewhat optimistic. The real confirmation happens in Phase 2 when the judge is applied to new outputs it has never seen.
{% endhint %}

***

### Phase 2 — Per-Experiment Loop

Every time the target system changes and produces new outputs, run this loop.

**Step 1: Run calibrated judge on all new outputs (automated, no SME yet)**

**Step 2: Build the Calibration Validation Set — determine SME review scope**

The Calibration Validation Set is the SME-labeled subset of the new outputs used to check whether the judge is still calibrated. All four priorities below must be collected — Priority 4 (PASS sample) is not optional, because TPR cannot be computed without labeled PASSes.

```
IF new outputs ≤ 30 rows:
  SME reviews ALL rows → this is the full Calibration Validation Set

IF new outputs > 30 rows:
  Collect in priority order. All four priorities must be represented.

  Priority 1 → ALL rows judge marked FAIL (cap at 15 if very many)
               Needed for TNR. Non-negotiable.

  Priority 2 → All rows with near-threshold scores
               With categorical scores {0, 0.5, 1}: filter score == 0.5
               These are the most ambiguous verdicts, most likely to flip
               on distribution shift.

  Priority 3 → Structurally novel outputs (see detection below)
               Outputs the judge has no calibration examples for.
               Skip if none detected.

  Priority 4 → Random sample of clear PASSes (minimum 5–10 rows)
               Needed for TPR. Even if Priority 1 fills your budget,
               still collect these. Without PASSes, TPR cannot be computed.
```

**Step 3: Compute TPR/TNR on the Calibration Validation Set**

```
IF TPR/TNR ≥ 90%:
  → Judge is still calibrated ✓
  → Trust results, use for target system improvement
  → Merge Calibration Validation Set into Calibration Dataset
  → Go to next experiment

IF TPR/TNR < 90%:
  → Judge has drifted ✗
  → Go to Step 4 (re-calibration)
```

**Step 4: Re-calibration (when drift is detected)**

```
1. Find disagreement cases from the Calibration Validation Set
2. SME confirms each disagreement:
     Is the judge wrong?     → add to Calibration Dataset, fix judge
     Is the SME label wrong? → correct label, note the pattern
3. Add confirmed cases to Calibration Dataset
4. Fix judge (prompt, threshold, few-shots) on disagreement cases
5. Check stopping criterion (see below)
6. Repeat until stopping criterion is met
7. Merge Calibration Validation Set into Calibration Dataset
8. Return to Step 1 with re-calibrated judge
```

***

## Re-calibration Stopping Criterion

Do **not** measure TPR/TNR only on the full Calibration Dataset after adding new cases. This creates a masking problem.

**The masking problem:**

```
Calibration Dataset:        80 rows, judge gets 78 right → 97.5% agreement
Calibration Validation Set: 20 rows, judge gets 12 right → 60% agreement

Combined:                   100 rows, 90 right → 90% ← looks fine
                                                  but judge still fails
                                                  on 40% of new outputs
```

A high agreement rate on old cases inflates the combined number, hiding that the fix did not work on the new output type.

**The correct stopping criterion requires two conditions simultaneously:**

```
Condition 1 — TPR/TNR ≥ 90% on the CALIBRATION VALIDATION SET alone
              Proves the fix actually worked on the failing cases.
              This is the real validation signal.

Condition 2 — TPR/TNR ≥ 90% on the FULL CALIBRATION DATASET
              Proves the fix did not break previously working cases.
              This is the regression check.

Both must pass. Either alone is insufficient.
```

Interpretation when conditions partially pass:

```
Only Condition 2 passes → masking problem
                          keep tuning specifically on Calibration Validation Set cases

Only Condition 1 passes → regression on old cases
                          the fix broke something previously working
                          review what changed in the judge prompt or threshold

Neither passes          → keep tuning
```

***

## How the Calibration Dataset Grows

The Calibration Dataset is a living artifact. After each experiment, the Calibration Validation Set is merged into it.

```
After Experiment 1: Calibration Dataset = initial labeled rows (e.g. 20)
After Experiment 2: += Calibration Validation Set from Experiment 2
After Experiment 3: += Calibration Validation Set from Experiment 3
...
```

Add both disagreement cases and agreement cases from each Calibration Validation Set. Agreement cases are evidence that the judge handles those output patterns correctly — important context for future tuning and for the regression check.

As the Calibration Dataset grows and covers a wider range of output types, passing Condition 2 becomes an increasingly meaningful signal. Eventually, new experiments will consistently return TPR/TNR ≥ 90% on both conditions with no re-tuning needed. That is the signal that the judge is genuinely stable.

***

## When to Re-run SME Review

The goal is to automate as much as possible. A well-calibrated judge should be trusted to run without SME involvement on most evaluation runs. SME review should be the exception, not the default.

### Scheduled-Based Review

Re-run SME review on a fixed schedule, not on every target system change. How frequent depends on how actively the target system is being developed:

* Active development (frequent target system changes): SME review every 3-5 evaluation runs
* Stable / production (infrequent changes): SME review every 8-10 evaluation runs, or monthly

### Signal-Based Review

Outside of the fixed cadence, monitor one additional signal automatically after each evaluation run: **pass rate shift** vs **the previous evaluation run**.

If the shift exceeds 25%, trigger an unscheduled SME review.

All dataset sizes: flag if pass rate shift > 25%

Example:

| Run              | Rows | PASS | FAIL | Pass Rate |
| ---------------- | ---- | ---- | ---- | --------- |
| Evaluation run 3 | 20   | 15   | 5    | 75%       |
| Evaluation run 4 | 20   | 8    | 12   | 40%       |

Shift = 35%, exceeds 25% threshold, trigger SME review.

When a shift is flagged, there are two possible explanations and you cannot tell which without SME:

* **Legitimate**: the target system genuinely improved or regressed. The judge is correct; act on the results as-is.
* **Drift**: the judge is miscalibrated on the new output patterns. Re-calibrate the judge before acting on the results.

Acting on the wrong explanation wastes significant effort in the wrong direction.

{% hint style="info" %}
On small datasets (30 rows or fewer), a 25pp shift represents only 5-8 queries. Treat it as a signal to investigate, not a definitive conclusion. SME review will confirm whether the shift is real or noise.
{% endhint %}

***

## Why Your Evals Can Misalign

During calibration, you will sometimes find that your judge disagrees with human labels. Before reaching for a fix, understand that the judge is not always the problem. Disagreements have multiple possible sources — and applying the wrong fix wastes time.

The goal of this section is to help you **diagnose first, then fix**.

***

## Diagnose Before You Fix

When TPR or TNR falls below 90%, work through this table in order. Most disagreements are not caused by a bad judge prompt.

| Symptom                                                                              | Likely Cause                                                                                | Technique to Apply                                                                                                                                                                            |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| actual\_output is correct but marked FAIL for not matching expected\_output phrasing | Wrong metric usage — Completeness applied with a reference answer on an open-ended question | Either switch to Groundedness / Context Sufficiency, or rewrite expected\_output as a criteria spec (e.g. "Must cover X, Y, Z") so Completeness evaluates coverage rather than phrasing match |
| actual\_output marked FAIL for missing a fact that isn't in retrieved\_context       | expected\_output is wrong or outdated                                                       | Update expected\_output to reflect only what is derivable from retrieved\_context                                                                                                             |
| Judge explanation is specific and coherent, but human overrode it                    | Human mislabel — reviewer skimmed without reading the explanation                           | Re-read the judge explanation before overriding                                                                                                                                               |
| Judge fails consistently on a specific cluster of actual\_output patterns            | Judge hasn't seen this output pattern before                                                | Add few-shot examples drawn from real mispredictions                                                                                                                                          |
| Judge is inconsistent on the same actual\_output across runs                         | Single judge variance                                                                       | Run the same judge multiple times and aggregate verdicts to stabilize the score                                                                                                               |
| actual\_output with fabricated numbers passes because "most content is grounded"     | Threshold too lenient for the question type                                                 | Tighten the threshold or switch to a stricter metric                                                                                                                                          |
| Combined TPR/TNR looks fine but Calibration Validation Set still fails               | Masking problem — old cases inflate the combined number                                     | Measure Calibration Validation Set and Calibration Dataset separately                                                                                                                         |

***

## Techniques to Improve Calibration

### 1. Read the Judge Explanation Before Overriding

When the judge marks a case FAIL and you disagree, do not immediately change the label. Read the full explanation first.

Human reviewers mislabel more often than expected. Common patterns:

1. The metric or context was updated after labeling, and old labels were never revised
2. Reviewer skimmed the response without checking specific claims against the retrieved context

**Real examples from Nava project:**

A response analyzing seasonal demand patterns was initially marked as fail because the reviewer considered it too redundant. On closer review, the main insights were accurate and supported by data. The human label was too strict — the redundancy threshold was updated to reflect that a redundancy score of 2 is still above the passing threshold for complex analytical answers, so the case was corrected to pass.

The opposite can also happen. A response was marked pass by a reviewer, but the judge later flagged a factual contradiction. The question asked how trip length affects booking velocity across regions. The `actual_output` concluded that longer trips experience slower booking velocity — meaning they take more days to sell out. However, the `retrieved_context` contained data showing the opposite trend: as trip length increased from 8 to 12 days in one region, the time to sell out dropped from 280 days to under 3 days. The reviewer had skimmed the narrative conclusion without cross-checking it against the underlying data in context. Once identified, the score fell below threshold and the human label was revised to fail.

**Rule:** Only override a judge's verdict when you can articulate specifically why the judge is wrong — not just that you disagree. When the `expected_output` or `retrieved_context` changes, re-evaluate all affected labels.

***

### 2. Use the Right Metric for the Question Type

Do not apply the same metric set to every test case by default. The most common miscalibration source is not a bad judge prompt — it is the wrong metric applied to the wrong question type. For example:

**Test case: specific known answer**

> "What is Jakaré's minimum viable nightly charter price?"

If you use `GEvalGroundednessMetric` as the only evaluator, the judge checks whether claims are supported by `retrieved_context` — but it will not catch a response that gives a plausible-sounding but incorrect price. The response passes as grounded even if the number is wrong.

Use `GEvalCompletenessMetric` with a reference `expected_output` so the judge verifies the answer against the known correct value.

***

**Test case: open-ended or synthesis**

> "How do luxury operators like Aliikai and Amandira differentiate themselves from budget options like Ikan Kayu?"

If you use `GEvalCompletenessMetric` with a fixed reference `expected_output` string, the judge will penalize any response that covers the right points but phrases them differently. A correct, well-reasoned answer fails just because the wording doesn't match.

Rewrite `expected_output` as a criteria spec — "_Must cover: vessel size, crew count, amenities, pricing_" — so Completeness evaluates coverage rather than phrasing. Alternatively, use `GEvalGroundednessMetric` to check that all claims are supported by `retrieved_context`.

***

**Test case: calculation or reasoning from data, multiple valid answers**

> "Does Zada Nara's Master Bedroom generate more revenue as a private cabin or as two separate open-trip berths?"

If you use `GEvalCompletenessMetric` with a fixed `expected_output`, the judge compares the response against a single reference answer. But this question has multiple valid ground truths depending on which pricing data is retrieved — a correct derivation from different data points will be penalized.

Use `GEvalContextSufficiencyMetric` instead. It checks whether `retrieved_context` contains the fundamental data needed to derive the answer, regardless of how the answer is expressed.

***

### 3. Update the Judge Prompt or Threshold

Once you have ruled out the wrong metric and human label error, the problem may be in the judge configuration itself.

**Rubric is ambiguous**

A completeness prompt that says "score 3 if all key points are covered" without defining what counts as a key point will be applied inconsistently across runs. Rewrite the rubric with explicit score-level definitions — what does a 0, 0.5, and 1 actually look like for this specific question type.

**Threshold is mismatched to the question**

With categorical scores {0, 0.5, 1}, a threshold of >= 0.5 (partially correct = pass) may be appropriate for open synthesis questions but too lenient for questions with a specific correct answer. A response that scores 0.5 will pass when the threshold is 0.5, even if the answer is only partially correct — verify the threshold matches the strictness the question requires.

**Additional context for consistency**

For questions where a specific domain interpretation is needed, you can inject additional context directly into the judge prompt to anchor its behavior.

**Real example from Nava project:**

A pricing comparison test case had inconsistent groundedness scoring because reviewers disagreed on how strictly to penalize wrong price figures. The fix was adding explicit additional context to the judge:

> "When mentioning price or rate, it should be grounded to the context. If there are wrong rates given, it should penalize the score. If only some are wrong, not all, you can give score 2."

This anchored the score and threshold behavior consistently across runs without rewriting the entire rubric.

***

### 4. Add Few-Shot Examples from Real Mispredictions

When the judge fails consistently on a specific cluster of cases — a certain question type, response style, or edge case — add few-shot examples directly into the judge prompt.

**Do not use invented examples.** Invented examples teach general principles. Real mispredictions teach the specific failure modes your judge actually has.

The best source of few-shot examples is your disagreement cases from past calibration runs — cases where the judge scored below threshold and an SME confirmed the response should have passed.

**Real example from Nava project:**

A test case asking how luxury yacht operators differentiate themselves from budget options showed that the judge was penalizing responses for making market positioning classifications like "ultra-luxury segment" even when those classifications were logical interpretations of the retrieved data. The fix was adding a few-shot example to the groundedness judge:

> A response that classifies vessels into market segments based on factual differences in vessel size, crew count, and amenity breadth should score 3, even if those segment labels are not explicitly stated in the context. Interpretive classifications that logically follow from the data are not hallucinations.

This prevented the judge from scoring below threshold on reasonable analytical inference.

***

### 5. Use Multiple Judges (`models`)

Even with a well-tuned prompt, a single LLM judge can produce inconsistent scores on the same `actual_output` across runs. Running multiple judges and aggregating the results stabilizes the score.

Pass a list of `BaseLMInvoker` instances via the `models` parameter:

```python
from gllm_inference.lm_invoker import build_lm_invoker

model = build_lm_invoker("google/gemini-3-flash-preview", api_key)

# Homogeneous: same judge N times
evaluator = GEvalGenerationEvaluator(models=[model] * 3)

# Heterogeneous: different judges
judges = [
    build_lm_invoker("openai/gpt-4o", openai_key),
    build_lm_invoker("openai/gpt-4o-mini", openai_key),
]
evaluator = GEvalGenerationEvaluator(
    models=judges,
    aggregation_method=AggregationMethod.MAJORITY_VOTE,
)
```

**When all judges agree → high confidence, automate.**\
**When judges disagree → flag for human review.**

From internal experiments on the Nava project:

|                             | Single Judge Run | All 3 Runs Agree |
| --------------------------- | ---------------- | ---------------- |
| <p><br></p>                 |                  |                  |
| Human agreement             | Moderate         | High             |
| Coverage of dataset         | 100%             | \~66%            |
| Evaluation time (100 items) | 20 mins          | 7 mins           |

{% hint style="warning" %}
**The tradeoff:** multiple LLM calls cost more. Use this approach for cases where a single judge run has shown high score variance.
{% endhint %}

***

## Quick Reference

| If you see this...                                                             | Try this first                                                                                 |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `actual_output` is correct but scores below threshold due to phrasing mismatch | Switch metric or rewrite `expected_output` as a criteria spec before touching the judge prompt |
| `actual_output` fails for missing a fact not in retrieved\_context             | Update `expected_output` to reflect only what is derivable from `retrieved_context`            |
| Judge explanation is specific but human overrides it                           | Re-read the explanation — the human label may be wrong                                         |
| Judge consistently scores below threshold on one cluster of cases              | Add few-shot examples drawn from those mispredictions                                          |
| Same `actual_output` scores inconsistently across runs                         | Pass `models=[model] * N` to run multiple judges and aggregate                                 |
| `actual_output` with fabricated numbers scores above threshold                 | Tighten threshold or add additional context to anchor scoring                                  |
| Agent recommendations not in `retrieved_context` score below threshold         | Lower groundedness threshold to 2 for initiative-driven outputs                                |

***

## Summary: Unified Calibration Flow

***

### Phase 1: Initial Calibration (once)

**Build the Calibration Dataset:**

* Dataset ≤ 30 rows → SME labels ALL rows
* Dataset > 30 rows → SME labels ALL FAILs + sample of PASSes (\~40–50 total)

**Tuning loop:**

1. Run judge on Calibration Dataset
2. Compute TPR/TNR on all labeled rows
3. If ≥ 90% → calibrated ✓ → go to Phase 2
4. If < 90% → find disagreements → diagnose (wrong metric? human label error? prompt/threshold? few-shots needed?) → fix → return to step 1

***

### Phase 2: Per-Experiment Loop

Run new target system → new outputs (N rows)

**`Step 1:`** Run calibrated judge on ALL N rows (automated)

**Step 2:** Build Calibration Validation Set (SME review scope)

* N ≤ 30 rows → SME reviews ALL rows
* N > 30 rows → collect all four priorities:
  * Priority 1 → ALL FAIL verdicts (cap at 15) — needed for TNR
  * Priority 2 → All score == 0.5 (near-threshold) — most ambiguous
  * Priority 3 → Structurally novel outputs — skip if none found
  * Priority 4 → Random sample of clear PASSes (minimum 5–10) — needed for TPR

**Step 3:** Compute TPR/TNR on Calibration Validation Set

* If ≥ 90% → still calibrated ✓ → merge into Calibration Dataset → next experiment
* If < 90% → drift detected ✗ → go to Step 4

**Step 4:** Re-calibration

1. Find disagreements from Calibration Validation Set
2. SME confirms each: judge wrong? → fix judge / label wrong? → correct label
3. Add confirmed cases to Calibration Dataset
4. Fix judge (wrong metric? prompt/threshold? few-shots? num\_judge?)
5. Check stopping criterion — both must pass:
   1. TPR/TNR ≥ 90% on Calibration Validation Set → fix actually worked
   2. TPR/TNR ≥ 90% on Calibration Dataset → no regression on old cases
6. Interpret partial results:
   1. Only Calibration Dataset passes → masking problem, keep tuning on new cases
   2. Only Calibration Validation Set passes → regression on old cases, review what changed
   3. Both pass → re-calibrated ✓
7. Merge Calibration Validation Set into Calibration Dataset → return to Step 1

**Triggers for unscheduled SME review:**

* Pass rate shifts > 25pp vs previous evaluation run
* Priority 3 detection flags structurally novel outputs

***

## Improving Your Judge

Once you've identified the root cause of miscalibration, the following guides walk through concrete techniques and sample code for fixing it:

* [Adjust Metric Configuration](../metric/custom-metric.md#modify-existing-metrics-prompts-and-attributes) — Update the rubric, prompt, or threshold to tighten or loosen judge behavior.
* [Add Temporary Few-Shot Examples](temporary-fewshot-per-test-case.md) — Inject real mispredictions as few-shot examples per test case to handle specific failure clusters.
* [Run Multiple Judges](multiple-llm-as-a-judge.md) — Use multiple same-model or cross-model judge runs and aggregate verdicts to reduce variance.
* [Create a Custom Metric](../metric/custom-metric.md) — Build a metric from scratch when no built-in metric fits your quality dimension.
* [Create a Custom Evaluator](../evaluator/create-custom-evaluator-scorer.md) — Compose your own evaluator when you need a non-standard metric combination or aggregation logic.
