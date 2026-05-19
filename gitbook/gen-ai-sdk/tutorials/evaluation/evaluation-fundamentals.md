# 🧠 Evaluation Fundamentals

This page explains what **Evaluation (Evals)** is, what it is not, and the core components used in **gllm-evals** so teams can align on reuse and avoid common misunderstandings.

## **What is Evaluation**

**Evaluation** is a structured and repeatable way to **measure the quality of an AI system’s outputs** against **explicit criteria**, producing **machine-readable results** (scores/verdicts, plus optional explanations/evidence).

Evaluation answers questions like:

* Is the output **correct** (when ground truth exists)?
* Is it **complete**, **grounded**, and not hallucinating?
* Is retrieval **good enough** for a given query?
* Does the system behavior satisfy a rubric (e.g., clarity, coherence, bias)?

The key point: **evaluation measures** outputs; it does not create those outputs.

## **What Evaluation is Not**

Evaluation is commonly confused with the system being evaluated, or with the criteria being checked. The following are **not** “evals”:

### **1) The thing we want to evaluate is not the evaluator**

Example misconception:

* “We evaluate 5W1H and one-sidedness, therefore the whole pipeline is evals.”

Correct framing:

* 5W1H and one-sidedness are **evaluation criteria** (what we care about).
* The **evaluator** is the component that produces structured scores/verdicts for those criteria.
* Other parts of the system (crawler, ingestion, storage, orchestration, UI) are not evaluation.

### **2) Evaluation is not the AI system itself (it does not replace the Target System)**

In gllm-evals, the system being evaluated is called the **Target System**: any AI component or system that produces outputs, such as:

* QnA agents
* RAG pipelines
* summarizers
* classifiers
* retrievers
* reporting/analysis systems

**Evaluation does not replace the Target System.** The Target System generates outputs; evaluation measures their quality.

### **3) Evaluation is not ad-hoc “LLM analysis”**

If a workflow calls an LLM to “analyze something” but has no explicit criteria, no stable scoring format, and is not repeatable across versions/runs, that is closer to **ad-hoc analysis** than evaluation.

Evaluation requires:

* explicit criteria/rubric,
* a stable scoring format (scores/verdicts),
* repeatability (so results can be compared across versions).

## **Components of Evaluation**

Evaluation typically includes these components:

### **1) Dataset (what you test on)**

A **dataset** defines evaluation cases (inputs) and optionally ground truth (expected outputs, labels, references). It enables repeatable comparison across changes.

Typical fields depend on the Target System, for example:

* QnA: question, expected answer, reference docs
* Retrieval: query, relevant documents/chunks
* Summarization: source text, expected summary or rubric criteria

### **2) Target System (the system under test)**

The **Target System** is the component being measured. It is responsible for producing the output that will be evaluated (answer, summary, retrieved context, classification label, etc.).

Important: **evaluation measures the Target System’s outputs; it does not implement the Target System.**

### **3) Evaluator / Scorer (how you score)**

An **evaluator/scorer** consumes:

* dataset fields (inputs and optional ground truth), and
* the Target System outputs,\
  then produces structured results such as:
* overall score,
* per-dimension scores (e.g., completeness, groundedness),
* pass/fail verdict,
* optional explanations/evidence.

### **4) Metric and Evaluator (the scoring signals)**

A **metric** is an individual scoring signal used by an evaluator (e.g., exact match, groundedness score, contextual precision/recall, rubric scores). **Evaluator** often combine multiple metrics into a final verdict.

### **5) Experiment Tracker (how you compare runs)**

An **experiment tracker** records evaluation results so you can compare performance across:

* model versions,
* prompts,
* retrieval configuration,
* logic changes,
* dataset revisions.

This makes evaluation useful as an engineering tool: you can detect regressions and quantify improvements.

## **Reference-based vs Reference-less Evaluation**

Evaluation can be performed with or without ground truth.

### **Reference-based evaluation (with ground truth)**

Use this when you have an expected output or labeled reference.\
Examples:

* QnA accuracy with expected answer
* Retrieval evaluation with known relevant documents/chunks
* Classification with gold labels

Typical outcomes:

* correctness score,
* precision/recall,
* pass/fail vs expected output.

### **Reference-less evaluation (without ground truth)**

Use this when ground truth is unavailable or too expensive to label.

Reference-less evaluation typically uses **rubric-based criteria** and can act as an **in-system critic** component:

* The evaluator judges the output against criteria like coherence, consistency, groundedness, safety, or bias.
* This can be used:
  * offline (to measure quality), and/or
  * inside a system loop (to critique an output and trigger revision or escalation).

Example reference-less criteria:

* “Does this summary contain contradictions?”
* “Is this answer grounded in the provided context?”
* “Is this article analysis one-sided? Provide evidence spans.”

## **Summary**

* **Evaluation** is a reusable measurement layer for output quality against explicit criteria.
* **The Target System** is the system being evaluated (any AI component that generates outputs).
* Evaluation **does not replace** the Target System; it measures the Target System outputs and behavior.
* Core components: **Dataset, Target System, Evaluator/Scorer, Metrics, Experiment Tracker**.
* Evaluation can be **reference-based** (with ground truth) or **reference-less**, where it can also serve as an **in-system critic**.
