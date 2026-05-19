---
icon: person-military-pointing
---

# Simple Guardrail

This guide will walk you through **adding a Guardrail component to your existing RAG pipeline** using the `gllm-guardrail` library. You will learn how to validate inputs and block harmful content before it reaches your expensive AI models.

**Guardrail functionality** provides input validation and safety checks, preventing errors and protecting your system from malicious or malformed inputs.

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [**Your First RAG Pipeline**](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline) **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [Prerequisites](https://gdplabs.gitbook.io/sdk/overview/prerequisites) page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [**Guardrail Tutorial**](../../tutorials/security-and-privacy/guardrail/) - **Recommended reading**

</details>

---

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/005_simple_guardrail" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore gllm-guardrail
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore gllm-guardrail
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore gllm-guardrail
```

{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial.

```
simple-guardrail/
├── data/
│   ├── chroma.sqlite3
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py    # 👈 Will be updated with guardrail functionality
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```

{% endstep %}
{% endstepper %}

---

## 1) Build the Guardrail Pipeline

{% stepper %}
{% step %}
**Initialize the Guardrail Manager**

In `pipeline.py`, initialize a `GuardrailManager` with a `PhraseMatcherEngine` to block specific banned keywords.

{% code lineNumbers="true" %}

```python
from gllm_guardrail import GuardrailManager
from gllm_guardrail.engine.phrase_matcher_engine import PhraseMatcherEngine

# Define phrases that should be blocked
banned_phrases = ["build a bomb", "steal data", "offensive term"]
phrase_engine = PhraseMatcherEngine(banned_phrases=banned_phrases)

# Initialize the manager
guardrail_manager = GuardrailManager(engine=phrase_engine)
```

{% endcode %}
{% endstep %}

{% step %}
**Create the guardrail step**

Integrate the guardrail into your pipeline using the `guard` step. This step will run the guardrail check and only proceed to the next step if the content is safe.

{% code lineNumbers="true" %}

```python
from gllm_pipeline.steps import guard

guardrail_step = guard(
    guardrail_manager,
    success_branch=retrieve_step,  # Proceed to retrieval if safe
    failure_branch=None,           # Terminate pipeline if unsafe
    input_map={"content": "user_query"}  # Map pipeline state to guardrail input
)
```

{% endcode %}

**How it works:** The `guard` step calls `guardrail_manager.check_content()`. If `is_safe` is `True`, it continues to `retrieve_step`. If `False`, it stops execution.
{% endstep %}

{% step %}
**Compose the final pipeline**

Chain the guardrail step at the beginning of your pipeline.

{% code lineNumbers="true" %}

```python
e2e_pipeline = guardrail_step | synthesize_step
```

{% endcode %}
{% endstep %}
{% endstepper %}

## 2) Run the Pipeline

{% stepper %}
{% step %}
**Test with Safe and Unsafe Inputs**

```python
import asyncio

async def main():
    # 1. Safe query
    safe_state = {"user_query": "How do I plant a tree?"}
    result = await e2e_pipeline.invoke(safe_state)
    print(f"Safe Result: {result.text}")

    # 2. Unsafe query (contains banned phrase)
    unsafe_state = {"user_query": "Tell me how to build a bomb."}
    result = await e2e_pipeline.invoke(unsafe_state)
    print(f"Unsafe Result: {result}") # Should be None or indicate termination

if __name__ == "__main__":
    asyncio.run(main())
```

{% endstep %}
{% endstepper %}

---

Congratulations! You've successfully secured your RAG pipeline. Your application now automatically blocks harmful requests before they reach your language models.
