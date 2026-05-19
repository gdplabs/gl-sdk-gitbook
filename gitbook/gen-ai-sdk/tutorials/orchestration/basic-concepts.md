---
description: An introduction to the concepts in our orchestration component.
icon: flag
---

# Basic Concepts

<figure><img src="../../../.gitbook/assets/Copy of Diagram Color Guide (3).png" alt="A flow diagram of an orchestration pipeline, showing three sequential steps (Step 1, 2, and 3) processing data. Inputs include an Initial State and Runtime Context. Each step reads from and writes to a centralized &#x22;State&#x22; database and reads from a &#x22;Runtime Context&#x22; block, ultimately producing a Final State output."><figcaption><p>The core orchestration concepts: Pipeline, Steps, State, and Runtime Context.</p></figcaption></figure>

The diagram above illustrates how the core concepts work together: **Pipeline**, **Steps**, **State**, and **Runtime Context**. As you read through this guide, refer back to the visualization to see how data flows through your pipeline and how runtime context influences execution without cluttering your state.

If you are looking to go straight into implementing a Pipeline, refer to the following pages:

1. [#quickstart](pipeline.md#quickstart "mention")
2. [your-first-rag-pipeline.md](../../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md "mention")

{% hint style="info" %}
The Orchestration tutorials explain how to use the core orchestration library to **build custom pipelines**. If you are looking for instructions on how to integrate with or configure a pipeline in GLChat, please refer to the [GLChat GitBook](https://gdplabs.gitbook.io/glchat/developer-guide/custom-pipeline-development-guide).
{% endhint %}

## Pipeline

The **Pipeline** is the core orchestration component that sequences and manages the execution of steps in our SDK. It orchestrates sequential step execution where each **Step** explicitly declares its read/write operations on a shared **State** object and reads from an immutable **Runtime Context**. The **Pipeline** wraps the [LangGraph](https://langchain-ai.github.io/langgraph) library, which provides a powerful way to define and execute complex workflows.

Our **Pipeline**:

1. Orchestrates **Steps** to run in sequence, managing the flow of data through the shared **State**.
2. Can be empty (acts as a pass-through), contain a list of steps, or be composed from other Pipelines.
3. Supports chaining and nesting so you can build larger flows from smaller ones.
4. Validates and enforces the structure of the data that moves through.
5. Separates mutable application state from immutable execution context, providing transparency in data flow.

{% hint style="info" %}
For more information about LangGraph, refer to [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview).
{% endhint %}

## Steps

**Step**s represent a single action in the Pipeline that reads the current state, does some work, and returns what changed or was added. Each **Step** explicitly declares its read/write operations on the shared **State** object and reads from the immutable **Runtime Context**. A **Step** can wrap a component so that it can be executed within the pipeline framework, with automatic input/output handling through the pipeline's **State**.

Each **Step**:

1. Explicitly declares which fields it reads from and writes to in the **State**, making dependencies clear.
2. Reads from the immutable **Runtime Context** for execution metadata without modifying it.
3. Connects into the Pipeline flow with defined inputs and outputs.
4. Typically has one entry and one exit, but can also branch or merge data.
5. Can be chained easily with other steps.

## State

A **State** is the **mutable data container** that flows through your pipeline. It carries inputs, intermediate results, and outputs between steps. A **State** acts as the _shared context_ for the entire workflow, evolving as each step modifies fields based on its explicitly defined dependencies. This design provides transparency in data flow and makes it easy to reason about step dependencies.

The **State**:

1. Acts as the contract between Steps — each Step explicitly declares which fields it reads and writes.
2. Evolves through the pipeline as steps modify fields, with each modification clearly traceable.
3. Encourages predictable schemata so Steps remain reusable and composable.
4. Supports mapping when entering or leaving nested flows to keep keys aligned.
5. Remains separate from the immutable **Runtime Context**, keeping application data distinct from execution metadata.

## Runtime Context

**Runtime Context** is a separate channel for passing execution-time information to your pipeline without mixing it into your **State**. While **State** carries the data being processed (inputs, intermediate results, outputs), **Runtime Context** carries metadata about _how_ to process that data — things like user sessions, feature flags, or environment settings.

The **Runtime Context**:

1. Keeps execution metadata separate from business data, so your State schema stays clean and focused.
2. Is accessible to all Steps during execution but doesn't persist in the State between steps.
3. Is optional — you only define a `context_schema` when you need to pass runtime information.

#### When to use Runtime Context

You should use **Runtime Context** when:

1. You need to pass user-specific information (e.g., `session_id`, `user_id`) that affects execution but isn't part of the core data flow.
2. You want to control pipeline behavior with feature flags or configuration without hardcoding values.
3. You're converting a Pipeline to a tool and need to accept both input data and execution metadata.

You should NOT use **Runtime Context** when:

1. The information is part of the actual data being processed. That belongs in **State**.
2. The information needs to be persisted or transformed between steps. Use **State** instead.

## Putting It All Together: A Simple RAG Example

Let's see how these concepts work together in a typical RAG (Retrieval-Augmented Generation) pipeline:

<figure><img src="../../../.gitbook/assets/Copy of Diagram Color Guide (2).png" alt=""><figcaption><p>A simple RAG pipeline using the orchestration concepts.</p></figcaption></figure>

The **Pipeline** orchestrates two primary execution phases in sequence:

1. _Retrieval_: Fetches relevant information from the knowledge base.
2. _Generation_: Consolidates information into a coherent answer.

The **Steps** each perform a specific task by interacting with shared resources:

1. **Retrieval Step**: Reads the query from **State** and uses **runtime** parameters (like `index_name` and `top_k`) to find and write back relevant chunks.
2. **Generation Step**: Reads the retrieved chunks and the query from **State** to generate and write the final response.

The **State** acts as the mutable data container that evolves through the pipeline:

1. `query`: The initial user input that triggers the process.
2. `retrieved_chunks`: The context-specific data hunks added during the Retrieval phase.
3. `response`: The final generated output added during the Generation phase.

The **Runtime Context** provides static execution metadata required for the operation:

1. `model_name`: Specifies which LLM to use for generation.
2. `index_name`: Identifies the vector database or search index to query.
3. `top_k`: Determines the number of document chunks to retrieve.
4. `user_id`: Manages identity, permissions, or personalized configurations.

Notice how **State** carries the _data being processed_ (the "what") while **Runtime Context** carries _information about how to process it_ (the "how"). Each **Step** reads what it needs from both containers, executes its `execute()` method, and writes updates back to the **State** — all orchestrated seamlessly by the **Pipeline**.

***

## When to Use Pipeline

The orchestration components in this SDK are **optional**. You are not required to build a full Pipeline with custom States and Steps for every use case. The framework is designed to let you opt-in to features as your requirements grow.

| Orchestration Component | Use When...                                                                  | Don't Use When...                                                  |
| ----------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Pipeline**            | You need to orchestrate complex workflows or visualize execution flows.      | You have a simple linear script and don't need graph capabilities. |
| **Steps**               | You need **robustness** (retries, caching, error handling) or observability. | You are writing a quick prototype or simple function logic.        |
| **State**               | You want custom or stricter contracts for your data flow.                    | The built-in `RAGState` covers most standard RAG use cases.        |
| **Runtime Context**     | You need execution metadata (e.g. `session_id`) or static configuration.     | You don't need anything other than what is in the State.           |

## Pipelines and Agents

Many workflows require more than just a fixed sequence of steps. This is where **AI Agents** come in. Unlike a **Pipeline**, which executes a pre-defined sequence of steps (deterministic), an **AI Agent** uses an LLM to reason and decide its own actions at runtime (probabilistic).

1. **Use Pipelines** when you need predictable, auditable, and repeatable data processing (e.g., "Always search the database, then summarize").
2. **Use Agents** when the workflow depends on complex reasoning or dynamic decision-making (e.g., "Figure out if the user needs a search or a calculation, and do it").

You can combine these two primitives to get the reliability of a Pipeline with the flexibility of an Agent. We support two main patterns:

1. **Pipeline-as-a-Tool**: Exposing a robust Pipeline as a tool for an Agent to call.
2. **Agent-as-a-Step**: Embedding an Agent as a standardized step within a Pipeline.

For detailed integration guides, visit [pipelines-and-agents.md](pipelines-and-agents.md "mention").

## Advanced Composition

Once you understand how **Pipeline**, **Steps**, **State**, and **Runtime Context** work together, you can start composing more complex workflows using **Subgraphs**.

### Subgraph

A **Subgraph** is a reusable Pipeline that could be embedded inside another Pipeline.

A **Subgraph**:

1. Encapsulates a sequence of actions, so fomplex logic stays modular and easy to reuse.
2. Maps inputs from the parent flow into its flow.
3. Improves error context by hinting which inner action failed.

### When to use a Subgraph

You should consider using a **Subgraph** when:

1. The same _group of actions_ appear in more than one Pipeline.
2. A portion of your Pipeline is conceptually one functionality (e.g. "retrieve", "format").
3. You intend to evolve or swap implementations without changing the parent flow.

You should NOT use a **Subgraph** when:

1. The sequence is tiny, only used once, and shares the same State schema as the parent.
2. Nesting adds more mental overhead than it removes.
