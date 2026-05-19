---
icon: arrows-to-circle
---

# Compressor

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/compressor) | **Tutorial**: [compressor.md](compressor.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/compressor.html)

## What's a Compressor?

In Retrieval-Augmented Generation (RAG), you often retrieve many passages, pack them into a single prompt context, and may exceed model context limits or pay extra latency/cost. A Compressor reduces the token count while trying to retain query-relevant content.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.
2. Compatibility PyTorch/CUDA setup for GPU usage.
3. Enough CPU or GPU memory to host the model used during compression.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-misc[llmlingua]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-misc[llmlingua]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment

FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-misc[llmlingua]"
```
{% endtab %}
{% endtabs %}

## Quickstart

Currently, we only support the LLMLingua compressor. This quickstart will allow you to use LLMLingua.

{% hint style="info" %}
If this is your first time using the Compressor using this model, Hugging Face will download the model for you. This process can take a while.
{% endhint %}

{% hint style="info" %}
It is recommended to use GPU, since inference using CPU could be slow.
{% endhint %}

```python
import asyncio

from gllm_generation.compressor import LLMLinguaCompressor

def main() -> None:
    # Choose device_map="cuda" for GPU, or "cpu" if no GPU
    compressor = LLMLinguaCompressor(
        model_name="microsoft/phi-2",
        device_map="cpu",
        rate=0.5,                      # default compression rate (keep ~50%)
        target_token=-1,               # -1 = no strict target; you can set e.g., 800
        use_sentence_level_filter=False,
        use_context_level_filter=True,
        use_token_level_filter=True,
        rank_method="longllmlingua",   # recommended
    )

    instruction = "Answer the question using the provided context."
    context = (
        "Document 1: ... long text ...\n"
        "Document 2: ... long text ...\n"
        "Document 3: ... long text ..."
    )
    query = "What are the main differences between approach A and B?"

    # Optionally override defaults at call time
    options = {
        "rate": 0.4,                   # compress further to ~40%
        # "target_token": 800,         # alternatively, target a specific token count
        # "use_sentence_level_filter": True,
        # "rank_method": "longllmlingua",
    }

    compressed = asyncio.run(compressor.run(
        context=context,
        query=query,
        instruction=instruction,
        options=options,
    ))

    print("Original length:", len(context))
    print("Compressed length:", len(compressed))
    print("Compressed preview:\n", compressed[:500])

if __name__ == "__main__":
    main()
```
