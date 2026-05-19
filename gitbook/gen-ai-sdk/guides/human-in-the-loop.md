---
icon: people-roof
---

# Human-in-the-loop Orchestration

Human-in-the-loop (HITL) orchestration allows you to pause a pipeline's execution to request manual approval, decision-making, or human edits before proceeding. This is crucial for production environments where AI agents or pipelines perform sensitive or high-risk actions (e.g., sending emails, deleting records, or committing code).

This guide walks you through building a reliable HITL flow using `gllm_pipeline`'s core primitives.

<details>
<summary>Prerequisites</summary>

This example specifically requires you to complete all setup steps listed on the [prerequisites.md](../../gen-ai-sdk/prerequisites.md "mention").

You should be familiar with these concepts and components:

1. [Pipeline Orchestration](../tutorials/orchestration/pipeline.md)
2. [Interrupt Step](../tutorials/orchestration/steps/README.md#interrupt)
</details>

## 1. Designing for Approval

To implement a manual approval checkpoint, use the unconditionally halting `interrupt` step right before your sensitive operation.

You can configure what data the pipeline exposes to the frontend operator (`message`) and exactly how the human's response should map back into the pipeline state (`resume_value_map`).

{% stepper %}
{% step %}
**Define the pipeline with an interrupt checkpoint**

{% code lineNumbers="true" expandable="true" %}
```python
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import if_else, interrupt, step


class PipelineState(TypedDict, total=False):
    topic: str
    email_draft: str
    hitl_decision: bool
    email_status: str


# Simple executable components
class GenerateDraftComponent(Component):
    @main
    async def run(self, topic: str) -> str:
        return f"Draft about: {topic}"


class SendEmailComponent(Component):
    @main
    async def run(self, body: str) -> str:
        return f"Sent: {body}"


class DiscardDraftComponent(Component):
    @main
    async def run(self) -> str:
        return "Draft discarded"


draft_email = step(GenerateDraftComponent(), output_state="email_draft", input_map={"topic": "topic"}, name="draft_email")
send_email = step(SendEmailComponent(), output_state="email_status", input_map={"body": "email_draft"}, name="send_email")
discard_draft = step(DiscardDraftComponent(), output_state="email_status", name="discard_draft")

# Branching based on human decision
conditional_send = if_else(
    condition=lambda state: state.get("hitl_decision", False),
    if_branch=send_email,
    else_branch=discard_draft,
    name="handle_decision",
)

memory = MemorySaver()

pipeline = Pipeline(
    steps=[
        draft_email,
        # Pauses execution and asks for human intervention
        interrupt(
            name="wait_for_human",
            message={"alert": "Please review the email draft", "priority": "high"},
            resume_value_map="hitl_decision",
        ),
        conditional_send,
    ],
    state_type=PipelineState,
    checkpointer=memory,
)
```
{% endcode %}
{% endstep %}
{% endstepper %}

## 2. Running with Session Persistence

For HITL to work across stateless web boundaries (e.g., a user closing their browser and returning later), you must track the pipeline's memory. The SDK inherently provisions a checkpointer when an interrupt is detected, but you must consistently provide a `thread_id`.

{% stepper %}
{% step %}
**Initialize the execution**

The pipeline will execute until it reaches the `wait_for_human` step. It will then yield the state.

{% code lineNumbers="true" expandable="true" %}
```python
print("Starting pipeline...")
state = await pipeline.invoke(
    initial_state={"topic": "Quarterly earnings report"},
    config={"thread_id": "email-session-123"},
)

print(f"Pipeline paused! Current Draft: {state.get('email_draft')}")
# This state is now persisted. The server can safely sleep.
```
{% endcode %}
{% endstep %}
{% endstepper %}

## 3. Injecting the Human Decision

When the operator is ready, they provide a decision through your application's UI. You inject this decision back into the exact same pipeline graph using LangGraph's `Command` interface.

{% stepper %}
{% step %}
**Resume execution with the payload**

The value assigned to `resume` will be mapped directly to your state via the `resume_value_map` defined earlier (in this case, into the `"hitl_decision"` key).

{% code lineNumbers="true" expandable="true" %}
```python
from langgraph.types import Command

# The human operator reviews the draft and approves it
operator_input = True

print("Resuming pipeline with human decision...")
final_result = await pipeline.invoke(
    Command(resume=operator_input),
    config={"thread_id": "email-session-123"},  # Must match the exact thread_id!
)

print(f"Final output status: {final_result.get('email_status')}")
```
{% endcode %}
{% endstep %}
{% endstepper %}



## Best Practices

### Structured Resume Payloads
If your approval process requires multiple inputs (e.g., a boolean decision AND a text feedback reason), define your `resume_value_map` as a list of strings: `["is_approved", "feedback"]`.

When resuming, you **must** match the expected dict signature:
```python
await pipeline.invoke(
    Command(resume={"is_approved": False, "feedback": "Too informal"}),
    config={"thread_id": "email-session-123"},
)
```

### Production Checkpointers
By default, the pipeline uses an `InMemorySaver` when it detects an interrupt. While perfect for local scripts and Jupyter notebooks, all data is lost when the Python process dies.

For production, provide a database-backed checkpointer explicitly during initialization:
```python
from langgraph.checkpoint.postgres import PostgresSaver

pipeline = Pipeline(
    steps=[...],
    checkpointer=PostgresSaver(...) # Persistent memory!
)
```

## See Also

- [Human-in-the-Loop Approvals](../../gl-ai-agent-package/guides/human-in-the-loop-approvals.md) — fully managed out-of-the-box HITL handler for Client SDK remote applications.
- [Interrupting Flow for Debugging](pausing-flow-for-debugging.md) — use `PauseStep` with `interrupt_before`/`interrupt_after` for static debugging breakpoints.
