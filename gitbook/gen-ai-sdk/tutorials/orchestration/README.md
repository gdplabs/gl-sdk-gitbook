---
description: >-
  The Pipeline is our orchestrator: an execution framework that coordinates
  steps, tool usage, and state—enabling everything from simple sequential
  workflows to sophisticated multi-step agents.
icon: arrow-progress
---

# Orchestration

Orchestration is what turns an LLM from a one-shot chatbot into a **multi-step system** that can deliver real outcomes in [**GLChat**](https://app.gitbook.com/o/l7iZNPfPGNFLFlscNeoe/s/DY50EL4OmcrPvtoecg4h/)**,** [**AI Agents**](https://app.gitbook.com/s/LqsWGI0JUnaas9v07yZ5/gl-aip)**,** [**Deep Research**](https://gdplabs.gitbook.io/gl-deepresearch)**,** and [**Digital Employees**](https://gdplabs.gitbook.io/catapa/digital-employee/overview/digital-employee-overview).

An LLM on its own can reason and respond, but it cannot coordinate actions, tools, or manage state across multiple operations. Orchestration provides the framework that lets the system **sequence steps, pass context between them, and manage execution flow** until a task is completed.

{% hint style="info" %}
The Orchestration tutorials explain how to use the core orchestration library to **build custom pipelines**. If you are looking for instructions on how to integrate with or configure a pipeline in GLChat, please refer to the [GLChat GitBook](https://gdplabs.gitbook.io/glchat/developer-guide/custom-pipeline-development-guide).
{% endhint %}

## Pipeline as the Orchestrator

In our system, the **Pipeline** is the core orchestration component. It manages workflow execution through a series of coordinated actions:

1. Determining which step should run next.
2. Executing the selected step or tool.
3. Collecting results (data, outputs, errors).
4. Updating the shared state.
5. Providing the updated context to subsequent steps.

The Pipeline continues this process until the workflow reaches completion or a terminal condition. This makes the Pipeline the central **orchestrator** that governs how your system executes.

## How Orchestration Works in Practice

<figure><img src="../../../.gitbook/assets/Copy of Diagram Color Guide (5).png" alt=""><figcaption><p>Orchestration flow pattern.<br>Steps sequentially (1) read current state, (2) execute logic and tools, (3) write results back to state, and (4) pass updated context forward. This continues until the workflow completes.</p></figcaption></figure>

When a Pipeline runs, it coordinates the flow between reasoning and action through a repeating cycle:

1. **A step processes the current state and goal**. Based on the current context, the step determines what action to take next (this could involve LLM reasoning, conditional logic, user settings, or other decision mechanisms).
2. **The Pipeline executes the step's logic or tool calls**. The chosen action is performed, whether that's calling an API, querying a database, or running a computation.
3. **Results are added to the shared state**. Outputs, errors, and any other data produced by the step are captured.
4. **The updated state becomes the input for the next step**. The enriched context flows forward to inform subsequent decisions.

This pattern of state updates and step execution enables sophisticated behaviors: **planning**, **tool usage**, **error handling**, **conditional branching**, and **adaptive decision**-making all emerge from this fundamental coordination mechanism.

## Reusable Blocks

If you want prebuilt orchestration patterns instead of assembling every step manually, see [Reusable Blocks](blocks/README.md).

That section covers the reusable pieces exposed by `gllm-rag`, including simple query helpers, retrieval blocks, routing blocks, and higher-level RAG strategies.

### A Simple Analogy

To understand how orchestration coordinates an AI system:

1. **LLM** 🧠 is the brain (decides what to do).
2. **Tools** 🛠️ are the hands (e.g. search, read, calculate, act).
3. **Pipeline / Orchestrator** ⚡ is the nervous system (coordinates everything).

Thinking alone is not enough. Coordination is what turns decisions into actions and enables feedback. The Pipeline plays this role in an AI application.

## Why Orchestration Matters

The difference between a system with and without orchestration fundamentally shapes what that system can accomplish. Orchestration transforms the scope of what's possible with LLMs.

| Without Orchestration                                                                     | With Orchestration                                                                                                                                      |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Single-response**. The LLM responds once and stops.                                     | **Multi-step execution**. Tasks can span multiple steps with continued reasoning.                                                                       |
| **No state management**. Progress and context are not tracked between operations.         | **Persistent state**. Context is maintained from start to finish across all steps.                                                                      |
| **Isolated tool usage**. Tools cannot be reliably chained or used in sequence.            | **Coordinated tool usage**. Tools can be used in sequence, conditionally, or in combination.                                                            |
| **Implicit workflow**. All logic and control flow happens within a single LLM invocation. | **Explicit workflow control**. Enables sophisticated multi-stage workflows, agentic systems that reason and adapt, and programmable execution patterns. |
