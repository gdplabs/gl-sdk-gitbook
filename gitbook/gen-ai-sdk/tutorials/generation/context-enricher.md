---
icon: brightness
---

# Context Enricher

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/context_enricher) | **Tutorial**: [context-enricher.md](context-enricher.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/context_enricher.html)

## What’s a Context Enricher?

A Context Enricher adds useful context (e.g., metadata) into your retrieved chunks before they’re passed to the LM. Enriching the context right after retrieval and before generation:

1. **Improves grounding**: include source/title/page so the model sees provenance.
2. **Reduces hallucination**: add constraints and traceability info.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-generation"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-generation"
```
{% endtab %}
{% endtabs %}

## Quickstart

In this example, we will create a metadata context enicher, which pulls metadata from the retrieved chunks and injects it to the chunk's content.

```python
import asyncio

from gllm_core.schema import Chunk
from gllm_generation.context_enricher import MetadataContextEnricher
from gllm_generation.context_enricher.metadata_context_enricher import (
    MetadataPosition,
)


def main() -> None:
    # Prepare retrieved chunks (each is a gllm_core.schema.Chunk)
    chunks = [
        Chunk(
            content="Neural networks learn by gradient descent.",
            metadata={"title": "Intro to DL", "source": "docs://ml101", "page": 3, "tags": ["ml", "basics"]},
        ),
        Chunk(
            content="Transformers use self-attention.",
            metadata={"title": "Transformers", "source": "docs://nlp", "page": 10},
        ),
    ]

    # Configure the enricher
    enricher = MetadataContextEnricher(
        metadata_fields=["title", "source", "page", "tags"],
        position=MetadataPosition.PREFIX,       # or MetadataPosition.SUFFIX
        separator="\n---\n",
        field_template="- {field}: {value}",
    )

    # Enrich in place; returns the same list for convenience
    enriched = asyncio.run(enricher.enrich(chunks))

    # Use enriched chunks downstream (e.g., to prompt an LLM)
    print(enriched[0].content)

if __name__ == "__main__":
    main()

```

**Example Output**

You should see an output similar to this:

```
- title: Intro to DL
- source: docs://ml101
- page: 3
- tags: ml, basics
---
Neural networks learn by gradient descent.
```
