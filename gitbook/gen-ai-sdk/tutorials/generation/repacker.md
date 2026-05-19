---
icon: box-open
---

# Repacker

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/repacker) | **Tutorial**: [repacker.md](repacker.md "mention") | **Use Case:** [#create-the-repacker](../../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#create-the-repacker "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/repacker.html)

## What is a Repacker

A repacker **rearranges a list of content chunks** into an order that’s more effective for downstream model consumption. It can return the reordered chunks as a list or merge them into a single context string. This helps with long inputs where models often over-focus on the beginning or the end (“lost-in-the-middle”).

* **Benefit**: Mitigates lost-in-the-middle by reordering information.
* **Outputs**: List of chunks (chunk mode) or a single string (context mode).
* **Key features**: Pluggable strategies, two output modes, optional size limits, configurable delimiter, custom size metric.
* **Outcomes**: Either a reordered list of chunks (chunk mode) or one prompt-ready string (context mode).
* **When to use**: Anytime you have multiple chunks and want better model recall across the whole input.
* **Purpose**: Improve how long inputs are read by models by reordering chunks.

## What a Repacker Can Do

A repacker lets you choose a repacking strategy and an output mode, optionally enforce a size limit, and control how the final context is joined with a delimiter.

* **Strategies**: `forward`, `reverse`, `sides`.
* **Modes**: `chunk` returns a list; `context` returns a string.
* **Size limit**: Trims from the end before reordering; delimiter size is not counted.
* **Delimiter**: Customizable in context mode (e.g., `\n\n`, `|`).
* **Size function**: Default is character length; can be customized to approximate tokens.

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
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-generation"
```
{% endtab %}
{% endtabs %}

## Quickstart

This quickstart shows a basic pass-through (forward order) and how to produce a single context string.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

async def main():
    chunks = [Chunk(content="Intro"), Chunk(content="Middle"), Chunk(content="Conclusion")]
    repacker = Repacker()
    result = await repacker.repack(chunks)
    print([c.content for c in result])  # ['Intro', 'Middle', 'Conclusion']

if __name__ == "__main__":
    asyncio.run(main())
```

## Repacker Method

Repacker provides three repacking method so you can tune the order to your needs.

### Forward Method (default)

This method preserves the original order. Use when chronology matters or your source sequence is already ideal.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

async def main():
    chunks = [Chunk(content="Oldest"), Chunk(content="Middle"), Chunk(content="Newest")]
    repacker = Repacker(method="forward")
    result = await repacker.repack(chunks)
    print([c.content for c in result])  # ['Oldest', 'Middle', 'Newest']

if __name__ == "__main__":
    asyncio.run(main())
```

### Reverse Method

This method flips the order so the most recent or concluding information appears first.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

async def main():
    chunks = [Chunk(content="Older"), Chunk(content="Newer")]
    repacker = Repacker(method="reverse")
    result = await repacker.repack(chunks)
    print([c.content for c in result])  # ['Newer', 'Older']

if __name__ == "__main__":
    asyncio.run(main())
```

### Sides Method

This method works by alternating the chunks from the end and start, emphasizing both beginning and end to reduce “lost-in-the-middle”.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

async def main():
    # With three items, Sides typically yields ['A', 'C', 'B']
    chunks = [Chunk(content="A"), Chunk(content="B"), Chunk(content="C")]
    repacker = Repacker(method="sides", mode="chunk")
    result = await repacker.repack(chunks)
    print([c.content for c in result])  # ['A', 'C', 'B']

if __name__ == "__main__":
    asyncio.run(main())
```

## Repacker Mode

Repacker provides two repacking mode so you can tune the format of the output.

### Chunk Mode (default)

This mode returns a reordered list of `Chunk` objects. Best when you need per-chunk operations (filtering, windowing, budgeting, scoring) downstream.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

async def main():
    chunks = [Chunk(content="X"), Chunk(content="Y")]
    repacker = Repacker(method="forward", mode="chunk")
    result = await repacker.repack(chunks) # a list of Chunk
    for chunk in result:
        print(chunk.content)

if __name__ == "__main__":
    asyncio.run(main())
```

### Context Mode

This mode returns a single string joined by your delimiter. Best when you want a prompt-ready context immediately.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

async def main():
    chunks = [Chunk(content="Part 1"), Chunk(content="Part 2")]
    repacker = Repacker(method="forward", mode="context", delimiter="\n---\n")
    context = await repacker.repack(chunks) # a string
    print(context) # Part 1 \n---\n Part 2

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced: size limits and custom size functions

Repacker also has several keyword arguments you can use to customize the repacker even further.

* **Limit behavior**: Trims from the end until total size (by `size_func`) fits the budget.
* **Default metric**: Character length of `chunk.content`.
* Custom metric: Provide your own `size_func` (e.g., a rough token estimator).
* Delimiter not counted: In context mode, delimiter length is excluded from the limit.

```python
import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

def rough_token_count(chunk: Chunk) -> int:
    # Extremely rough token estimate: words * 1.3
    return int(len(str(chunk.content).split()) * 1.3)

async def main():
    chunks = [
        Chunk(content="Short intro."),
        Chunk(content="Detailed middle section with more words."),
        Chunk(content="Final notes.")
    ]
    repacker = Repacker(
        method="sides",
        mode="context",
        delimiter="\n\n",
        size_func=rough_token_count,
        size_limit=10,
    )
    context = await repacker.repack(chunks)
    print(context)

if __name__ == "__main__":
    asyncio.run(main())
```
