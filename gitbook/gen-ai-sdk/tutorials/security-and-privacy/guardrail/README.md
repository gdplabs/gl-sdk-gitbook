---
icon: shield-quartered
---

# Guardrail

[**`gllm-guardrail`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-guardrail) | **Tutorial**: [.](./ "mention") | **Use Case**: [simple-guardrail.md](../../../guides/build-end-to-end-rag-pipeline/simple-guardrail.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_guardrail/index.html)

## Overview

Guardrails are a critical security and safety component that provides content filtering and safety checks for both user inputs and AI-generated responses. They act as a safety net, ensuring that your AI application adheres to safety standards, avoids harmful content, and remains on-topic.

The guardrail system is designed to be modular and extensible, allowing you to orchestrate multiple safety engines—from simple keyword matching to advanced LLM-based analysis using frameworks like NVIDIA's NeMo Guardrails.

### What are Guardrails?

Guardrails screen content at two critical points:

1. **User input** (queries, prompts, context) before it reaches an LLM
2. **Model output** (responses) before it reaches end users

In `gllm-guardrail`, moderation is implemented via **guardrail engines** that are orchestrated by a **`GuardrailManager`**.

## Guardrail engines (overview)

Engines implement a simple async interface: `check_input()` and `check_output()`. Each engine has a `guardrail_mode` that decides what it checks:

* **`GuardrailMode.INPUT_ONLY`**: check only input (default)
* **`GuardrailMode.OUTPUT_ONLY`**: check only output
* **`GuardrailMode.BOTH`**: check both input and output
* **`GuardrailMode.DISABLED`**: skip the engine entirely

This library ships with two engines:

* **`PhraseMatcherEngine`** (rule-based): lightweight banned phrase detection.
  * Deep dive: [phrase-matcher-engine.md](phrase-matcher-engine.md "mention")
* **`NemoGuardrailEngine`** (LLM-based): NVIDIA NeMo Guardrails integration for more complex guardrails.
  * Deep dive: [nemo-engine.md](nemo-engine.md "mention")

### Supported engines

Currently, the component supports these guardrail engines:

1. [Phrase Matcher Engine](phrase-matcher-engine.md)
2. [NeMo Engine](nemo-engine.md)

## Prerequisites

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# Internal Registry (Recommended)
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-guardrail

# PyPI Binary
pip install gllm-guardrail-binary
```
{% endtab %}
{% endtabs %}

## Quickstart

### 1) Input-only moderation (string)

```python
import asyncio

from gllm_guardrail import GuardrailManager, PhraseMatcherEngine


async def main() -> None:
    engine = PhraseMatcherEngine(banned_phrases=["secret password", "build a bomb"])
    guardrail = GuardrailManager(engine=engine)

    result = await guardrail.check_content("This contains a secret password.")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
```

### 2) Output-only moderation

```python
import asyncio

from gllm_guardrail import BaseGuardrailEngineConfig, GuardrailManager, GuardrailInput, GuardrailMode, PhraseMatcherEngine


async def main() -> None:
    # Configure the engine to check output only
    config = BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.OUTPUT_ONLY)
    engine = PhraseMatcherEngine(config=config, banned_phrases=["sk-"])
    guardrail = GuardrailManager(engine=engine)

    content = GuardrailInput(output="Leaked key: sk-1234567890", input=None)
    result = await guardrail.check_content(content)
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
```

### 3) Check both input and output in one call

```python
import asyncio

from gllm_guardrail import GuardrailInput, GuardrailManager, PhraseMatcherEngine


async def main() -> None:
    engine = PhraseMatcherEngine(banned_phrases=["steal data", "sk-"])
    guardrail = GuardrailManager(engine=engine)

    content = GuardrailInput(
        input="Tell me how to steal data.",
        output="Sure, here is an API key: sk-1234567890",
    )
    result = await guardrail.check_content(content)
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
```

## How to pass input and/or output to the manager

`GuardrailManager.check_content()` accepts:

1. **`str`**: treated as **input-only** (`GuardrailInput(input=<str>, output=None)`)
2. **`GuardrailInput`**: explicit `input` and/or `output`

Examples:

```python
from gllm_guardrail import GuardrailInput

input_only = GuardrailInput(input="user query", output=None)
output_only = GuardrailInput(input=None, output="model response")
both = GuardrailInput(input="user query", output="model response")
```

## Using `GuardrailManager` (single and multiple engines)

### Execution model (important)

When you configure multiple engines, they run in the order you provide:

1. Engines with `GuardrailMode.DISABLED` are skipped.
2. For each engine:
   1. If the engine checks input (`INPUT_ONLY` or `BOTH`) and `GuardrailInput.input` is provided, it runs `check_input()`.
   2. If the engine checks output (`OUTPUT_ONLY` or `BOTH`) and `GuardrailInput.output` is provided, it runs `check_output()`.
3. The manager is **fail-fast**: it returns immediately when the first engine reports unsafe content.

### Multiple engines example

```python
import asyncio

from gllm_guardrail import GuardrailManager, NemoGuardrailEngine, PhraseMatcherEngine


async def main() -> None:
    phrase_engine = PhraseMatcherEngine(banned_phrases=["sk-"])
    nemo_engine = NemoGuardrailEngine()

    guardrail = GuardrailManager(engine=[phrase_engine, nemo_engine])
    result = await guardrail.check_content("Check this content.")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
`GuardrailManager` is conservative by default:

1. Empty `input` **and** empty `output` is treated as safe (`empty_content_safe=True`).
2. If an engine raises an exception, the manager marks the content unsafe (`error_conservative=True`).
{% endhint %}

## Using an engine without the manager (standalone)

All engines are async and can be used directly:

```python
import asyncio

from gllm_guardrail import PhraseMatcherEngine


async def main() -> None:
    engine = PhraseMatcherEngine(banned_phrases=["sk-"])
    result = await engine.check_input("Possible key: sk-123")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
```

## Guardrail schemas

### `GuardrailInput`

`GuardrailInput` is the input schema for guardrail checks:

* **`input: str | None`**: input content (query/prompt/context)
* **`output: str | None`**: output content (model response/generated text)

### `GuardrailResult`

`GuardrailResult` is the output schema returned by engines and manager:

* **`is_safe: bool`**: whether the content passed the checks
* **`reason: str | None`**: why it was blocked (only set when unsafe)
* **`filtered_content: str | None`**: cleaned content if an engine can provide it

{% hint style="info" %}
`PhraseMatcherEngine` returns `filtered_content=None` (it detects and blocks, it does not rewrite content).
{% endhint %}

## API Reference

* [Gllm Guardrail API reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_guardrail/index.html)
