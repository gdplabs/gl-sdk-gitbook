# Expected Output/Responses Design

Overview

Every evaluation test case requires an input. Most require an expected output -- the reference against which your AI system's actual output is measured.

Writing expected outputs well is one of the highest-leverage decisions in building reliable evals. A poorly written expected output produces false failures, misleads your metrics, and erodes trust in the entire evaluation pipeline.

This page covers:

1. The three types of expected outputs and when to use each
2. Best practices for writing expected outputs that produce reliable, calibrated results

***

## Types of Expected Outputs

Expected outputs in GL Evals fall into three categories: **constrained format**, **free text**, and **referenceless**. The type you choose determines which metrics are appropriate and how your judge interprets the result.

### Constrained Format

The expected output is a fixed string or schema. The actual output is scored by extracting a specific token, label, or structure and comparing it against the expected value using exact match, regex, or schema validation.

Constrained format is not a single type. Research identifies four commonly used constrained format categories: multiple-choice question-answer, wrapping, list, and mapping. These map to four practical subtypes.

#### Subtype 1: Multiple Choice (MCQ)

The model selects one option from a predefined set (A / B / C / D or labeled options). Scoring extracts the selected symbol and compares it to the correct option.

**Example:**

```
input:           "Which metric measures how much of the answer is grounded in the context?
                  A) Completeness  B) Groundedness  C) Relevancy  D) Fluency"
expected_output: "B"
actual_output:   "B"   # pass
actual_output:   "C"   # fail -- wrong option selected
```

**Used in:** MMLU, GPQA Diamond, classification benchmarks.

***

#### Subtype 2: Template / Wrapping

The model produces a free-text response but is instructed to wrap the final answer in a specific template. Scoring extracts the content inside the wrapper using regex.

Common wrappers: `\boxed{answer}`, `The answer is: X`, `<answer>X</answer>`, `Answer: X`

**Example:**

```
input:           "What is 17 times 8?"
expected_output: "136"
actual_output:   "Let me calculate. 17 × 8 = 136. \boxed{136}"  # pass -- value extracted from \boxed{}
actual_output:   "Let me calculate. 17 × 8 = 136."              # fail -- no wrapper present, extraction fails
```

The evaluator applies a regex pattern to extract `136` from the actual output, then compares it against `expected_output`. The surrounding reasoning text is ignored.

**Used in:** GSM8K, MATH benchmark, reasoning evaluation tasks.

***

#### Subtype 3: Structured Schema (JSON / XML / YAML)

The model is required to return output conforming to a predefined schema. Scoring validates schema compliance and extracts specific field values for comparison. This covers any structured shape: flat key-value objects, arrays, and nested structures.

**Example -- Object (NER extraction):**

```
input:           "Extract all people and organizations from: 'Elon Musk founded SpaceX in 2002.'"
expected_output: {"persons": ["Elon Musk"], "organizations": ["SpaceX"]}
actual_output:   {"persons": ["Elon Musk"], "organizations": ["SpaceX"]}          # pass
actual_output:   {"persons": ["Elon Musk"], "organizations": ["SpaceX", "2002"]}  # fail -- "2002" is not an organization
```

**Example -- Array (list output):**

```
input:           "List the RAG Triad metrics."
expected_output: ["Contextual Relevancy", "Faithfulness", "Answer Relevancy"]
actual_output:   ["Faithfulness", "Contextual Relevancy", "Answer Relevancy"]   # pass -- order does not matter
actual_output:   ["Faithfulness", "Answer Relevancy"]                           # fail -- Contextual Relevancy missing
```

**Example -- Flat key-value (classification):**

```
input:           "Classify this support ticket by urgency and category."
expected_output: {"urgency": "high", "category": "billing"}
actual_output:   {"urgency": "high", "category": "billing"}    # pass
actual_output:   {"urgency": "medium", "category": "billing"}  # fail -- urgency mismatch
```

**Used in:** NER tasks, information extraction, tool call validation, agent output parsing, multi-label classification.

**Note:** Constrained decoding (JSON-mode) can hinder reasoning abilities while enhancing classification task accuracy. Use structured schema format only when the task genuinely requires a structured output, not as a convenience for parsing.

***

**When to use constrained format (any subtype):**

1. Classification tasks where the correct output is one of a finite set of values
2. Factual recall where only one exact value is correct
3. Tasks where schema compliance is itself the requirement being tested
4. Benchmarking tasks that require exact reproducibility

**Limitations:**

Constrained format evaluation is not suitable for agents, RAG chatbots, summarizers, or any system that produces open-ended outputs in production. Regular Expression extraction fails in two primary scenarios: when the model does not produce a relevant response, and when the model's response does not conform to the expected format standards. Research demonstrates that regex-based extraction accuracy across leading evaluation frameworks is only 74.38% -- meaning more than 1 in 4 extractions fail before scoring even begins (xFinder, 2024). A model can also know the correct answer internally but produce a non-matching format and be penalized, introducing a gap of 30 to 43 percentage points between its true capability and its measured score (Let Me Speak Freely, 2024).

**GL Evals note:** GL Evals is designed primarily for free-text evaluation with LLM-as-judge metrics. Constrained format evaluation is supported via deterministic metrics and can be extended further through custom evaluators.

### Free Text (Unstructured)

The expected output is a reference answer, a criteria specification -- not a fixed string. Scoring is performed by an LLM judge using explicit evaluation criteria.

Free-text evaluation reflects actual production behavior. It is the appropriate methodology for any AI system that generates open-ended responses.

Free-text expected outputs divide further into three subtypes.

#### Reference-Based

The expected output is a gold-standard answer that the actual output is compared against. The judge checks whether the actual output contains the key facts or claims present in the reference.

**When to use:**

1. QA tasks with a known correct factual answer
2. Tasks where the correct answer is specific enough that paraphrases are acceptable but the underlying claim must be present

**Example:**

```
input:           "What is Aliikai's minimum charter price?"
expected_output: "USD 3,500/night"
actual_output:   "Aliikai's minimum charter starts at USD 3,500 per night."   # pass -- fact is present
actual_output:   "Aliikai offers competitive pricing for the region."          # fail -- no price stated
actual_output:   "Aliikai's minimum charter starts at USD 3,800 per night."   # fail -- wrong figure
```

The judge checks whether the actual output states the correct fact, not whether it matches word-for-word.

#### Criteria-Based

The expected output is a specification of what the actual output must satisfy -- a set of explicit, checkable requirements rather than a factual reference. The judge evaluates each criterion independently.

The key characteristic of criteria-based: **the criteria are input-specific**. They describe what this particular output must contain or avoid, and they can change from test case to test case.

**When to use:**

1. Tasks where multiple valid answers exist but input-specific requirements must be met. The requirements define what any acceptable answer must contain or avoid for this particular test case -- they change from test case to test case.
   1. Coverage requirements: "Must cover 3 personas. Must include a nightly rate for each."
   2. Format requirements: "Must not exceed 2 paragraphs. Must use bullet points."
   3. Behavioral requirements: "Must not recommend a specific booking date. Must redirect the user to a licensed advisor."
   4. Domain-specific prohibitions: "Must not recommend specific stocks. Must not include PII."

**Example:**

```
input:           "Which personas do different yachts appeal to, and how do nightly rates differ by persona?"
expected_output: "Must cover 3 personas: romantic couples, family groups, and dive seekers.
                  Include nightly rates and typical trip lengths for each."
actual_output:   "Romantic couples prefer Alexa ($6,500+/night, 7-night trips).
                  Family groups prefer Magia II ($4,950+/night, 5-7 night trips).
                  Dive seekers prefer Arenui ($3,800+/night, 7-10 night trips)."  # pass -- all 3 personas with rates and lengths
actual_output:   "Romantic couples prefer Alexa ($6,500+/night).
                  Family groups prefer Magia II ($4,950+/night)."                 # fail -- dive seekers missing, no trip lengths
```

### Referenceless

No expected output is provided. The judge evaluates the actual output using only the input and retrieved context.

The key characteristic of referenceless: **the criteria are generic and metric-level**. They apply the same way to any output regardless of what the input is. You do not write them -- they are built into the metric definition itself. Examples: conciseness, politeness, fluency, groundedness, toxicity.

This is the core distinction from criteria-based: if the criteria change per test case, use criteria-based. If the same criteria apply universally across all test cases, use referenceless.

**When to use:**

1. **Measuring generic output properties that apply to any response.** The criteria are baked into the metric definition -- you do not write an expected output per test case. Examples: conciseness, politeness, fluency, toxicity, hate speech.
   * Example: a customer support chatbot evaluated on whether every response is polite and free of toxic language. The same metric runs on every test case regardless of what the user asked.
2. **Early-stage or exploratory evals where golden answers are not yet available.** The task is defined but expected outputs have not yet been written or validated by an SME. Referenceless metrics catch obvious failures immediately while the golden answer set is being built in parallel.
   * Example: a new multilingual query transformer that rewrites user queries before retrieval. No expected outputs exist yet. Answer Relevancy checks whether the rewritten query still addresses the original user intent while the team collects real outputs for SME review.
3. **Multiple valid answers exist and enumerating them is impractical.** There is no single correct answer, and collecting all valid answers is not feasible.
   * Example: "How do I pay my annual home tax?" -- valid answers differ by region, payment channel, and time of year. Groundedness checks the response is supported by retrieved context. Answer Relevancy checks the response addresses the question.
4. **Time-sensitive answers with no fixed oracle.** The correct answer changes depending on when the query is asked and there is no database to retrieve the current ground truth from.
   * Example: "What is the number of cars bought last week?" via a web search agent. The search result becomes `retrieved_context` regardless of whether data exists. Groundedness catches fabricated numbers not present in the search result. Answer Relevancy accepts "no data found this week" as a valid response.
5. **Production monitoring at scale.** Live user queries cannot be labelled in advance. Referenceless metrics run on every query at runtime as continuous quality checks.
   * Example: a RAG chatbot in production. Every response is checked for Groundedness and Answer Relevancy automatically across thousands of daily queries with no human labelling required per query.

**When NOT to use Referenceless:**

1. The input has a specific correct answer that can be retrieved or written -- use reference-based instead
2. The output must satisfy input-specific requirements (must list 3 categories, must give a price in USD, must not recommend specific stocks) -- use criteria-based instead
3. You need to catch exact factual errors like wrong numbers or wrong names -- Groundedness covers hallucination but reference-based with oracle injection is stronger for exact factual verification

**GL Evals note:** Referenceless evaluation requires careful metric selection. Groundedness and ContextSufficiency work without an expected output. Completeness requires one.

**Example:**

```
input:             "What is the refund policy for charter cancellations?"
expected_output:   (none)
retrieved_context: "Cancellations made 30+ days before departure receive a full refund.
                    Cancellations within 30 days forfeit the deposit."
actual_output:     "You can cancel for a full refund if you do so at least 30 days before departure.
                    Cancellations within 30 days will forfeit your deposit."   # pass -- grounded in context, no hallucination
actual_output:     "You can cancel anytime for a full refund."                 # fail -- contradicts the 30-day rule in context
```

***

## Comparison Table

| Dimension                      | Constrained Format                                                                                                       | Free Text (Unstructured)                                                                        |                                                   | Referenceless                                       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------- |
|                                |                                                                                                                          | **Reference-Based**                                                                             | **Criteria-Based**                                |                                                     |
| Expected output required       | Yes -- fixed string or schema                                                                                            | Yes -- gold answer                                                                              | Yes -- criteria spec                              | No                                                  |
| Scoring mechanism              | Exact match / regex / schema validation                                                                                  | LLM judge vs reference                                                                          | LLM judge vs criteria                             | LLM judge vs input + context                        |
| Subtypes                       | MCQ, Template/Wrapping, Structured Schema                                                                                | --                                                                                              | --                                                | --                                                  |
| Criteria defined by            | N/A                                                                                                                      | Gold answer                                                                                     | You, per test case                                | Metric, applies universally                         |
| Suitable for                   | Classification, exact recall, schema compliance                                                                          | Factual QA                                                                                      | Open-ended synthesis, input-specific requirements | Generic property measurement, production monitoring |
| Detects hallucination          | No                                                                                                                       | Partially -- checks if gold fact is present, but misses extra false claims beyond the reference | Yes                                               | Yes                                                 |
| Multiple valid answers allowed | No                                                                                                                       | Partially -- paraphrases accepted, but anchored to one gold answer                              | Yes                                               | Yes                                                 |
| Reflects production behavior   | Depends on task -- yes for NER, classification, structured agent output; no when used as proxy for open-ended generation | Yes                                                                                             | Yes                                               | Yes                                                 |

***

## Best Practices for Writing Expected Outputs

### For Reference-Based Expected Outputs

**1. Write the facts, not a full sentence.**

The judge extracts and verifies claims. A sentence introduces paraphrase risk and may include claims you did not intend to test.

```
# Avoid
expected_output: "Aliikai's minimum charter is around USD 3,500 per night, which is competitive."

# Prefer
expected_output: "USD 3,500/night"
```

**2. Do not write the expected output as a paraphrase of the input.**

The expected output must contain information the model must retrieve or generate -- not a restatement of what was asked.

`input: "What is the cancellation policy?"`\
`expected_output: "The cancellation policy states the terms for cancelling." # paraphrase of input`\
`# any output will pass this`\
`# tells the judge nothing`

`# vs`

`expected_output: "Full refund if cancelled 30+ days before departure.`\
`Deposit forfeited if cancelled within 30 days." # actual content the model must retrieve`

***

### For Criteria-Based Expected Outputs

**1. Replace vague adjectives with specific requirements.**

Words like "accurate," "complete," "relevant," and "comprehensive" are not checkable criteria. Replace them with the specific properties the output must have.

| Vague              | Specific                                                              |
| ------------------ | --------------------------------------------------------------------- |
| "Must be complete" | "Must cover all 3 product tiers"                                      |
| "Must be accurate" | "Must state the correct charter price in USD"                         |
| "Must be relevant" | "Must answer the question asked without introducing unrelated topics" |

**2. Specify what must NOT be present, not only what must be present.**

Negative criteria catch hallucination, refusal failures, and behavioral violations that positive criteria miss.

```
expected_output: "Must state the refusal reason. Must not provide the requested financial advice.
                  Must offer to connect the user with a licensed advisor."
```

***

### For Constrained Format Expected Outputs

**1. Use the least restrictive format that still allows reliable scoring.**

Template/wrapping is less harmful to reasoning than full JSON-mode constrained decoding. Only use JSON-mode or schema constraints when the output is genuinely structured data.

**2. For array outputs inside a structured schema, specify whether ordering matters.**

If order does not matter, use set equality for scoring. Requiring exact ordering on unordered arrays produces false failures.

***

### General Rules for All Types

**1. Review expected outputs before each major eval run.**

Outdated expected outputs are one of the leading causes of false failures. If your system's behavior changes -- due to a prompt update, a model upgrade, or new context -- your expected outputs must be reviewed to remain valid.

**2. When a judge's verdict surprises you, check the expected output before overriding.**

Humans mislabel more than expected. Before concluding that the judge is wrong, re-read the expected output carefully. A common finding is that the expected output was ambiguous or incorrect, not the judge's verdict. Only override when you can articulate specifically why the judge is wrong -- not just that you disagree.

***

## Choosing the Right Type

Use this decision tree when writing a new test case.

```
Does the task require a fixed string, label, or schema as output?
|
+-- Yes --> Constrained Format
|           |
|           +-- A/B/C/D selection?                      --> MCQ
|           +-- Final answer wrapped inside a template? --> Template/Wrapping
|           +-- Structured data (JSON/XML/YAML)?        --> Structured Schema
|                 (covers flat objects, arrays, nested structures)
|
+-- No --> Does a specific gold answer exist that the output must match?
            |
            +-- Yes --> Reference-Based Free Text
            |
            +-- No --> Are there input-specific requirements the output must satisfy?
                        |
                        +-- Yes --> Criteria-Based Free Text
                        |
                        +-- No --> Referenceless
```

***

## Academic References

1. "Can Multiple-Choice Questions Really Be Useful in Detecting the Abilities of LLMs?" ACL 2024. [https://arxiv.org/html/2403.17752v3](https://arxiv.org/html/2403.17752v3)
2. "Beyond Probabilities: Unveiling the Misalignment in Evaluating Large Language Models." arXiv 2024. [https://arxiv.org/html/2402.13887](https://arxiv.org/html/2402.13887)
3. "Bridging the Knowledge-Potential Gap in LLMs on Multiple-Choice Questions." arXiv 2026. [https://arxiv.org/html/2509.23782](https://arxiv.org/html/2509.23782)
4. "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models." arXiv 2024. [https://arxiv.org/html/2408.02442v1](https://arxiv.org/html/2408.02442v1)
5. "xFinder: Large Language Models as Automated Evaluators for Reliable Evaluation." arXiv 2024. [https://arxiv.org/html/2405.11874](https://arxiv.org/html/2405.11874)
6. "AdaRubric: Task-Adaptive Rubrics for LLM Agent Evaluation." arXiv 2025. [https://arxiv.org/pdf/2603.21362](https://arxiv.org/pdf/2603.21362)
7. "RubricRAG: Towards Interpretable and Reliable LLM Evaluation via Domain Knowledge Retrieval for Rubric Generation." arXiv 2025. [https://arxiv.org/pdf/2603.20882](https://arxiv.org/pdf/2603.20882)
8. "LLMs Are Biased Towards Output Formats! Systematically Evaluating and Mitigating Output Format Bias of LLMs." arXiv 2024. [https://arxiv.org/pdf/2408.08656](https://arxiv.org/pdf/2408.08656)
