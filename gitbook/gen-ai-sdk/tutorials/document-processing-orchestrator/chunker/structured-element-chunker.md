# Structured Element Chunker

**Structured Element Chunker** is designed to **segment elements based on their structural information**, while meticulously maintaining the hierarchical information within both the element metadata and the text of the element. This approach ensures that each chunked element retains its context and relationship to the overall document structure, facilitating a more nuanced and accurate analysis.

<details>

<summary>Prerequisites</summary>

If you want to try the snippet code in this page:

* Completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [input](https://assets.analytics.glair.ai/generative/pdf/pdfparser-tablecaptionparser-output.json).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json
from gllm_docproc.chunker.structured_element import StructuredElementChunker

# elements (input) that you want to Chunk
with open('./data/source/parsed_elements.json', 'r') as file:
    elements = json.load(file)

# initialize StructuredElementChunker
chunker = StructuredElementChunker()

# chunk elements
chunked_elements = chunker.chunk(elements)
print(chunked_elements)
```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pdf/structuredelementchunker-output.json).
{% endstep %}
{% endstepper %}

## Smart Bypass Feature

When enabled, the Smart Bypass Feature automatically adapts the Structured Element Chunker's strategy based on document character length to prevent over-fragmentation and optimize processing. Depending on the **document's total character count**:

1. **< `small_document_threshold_chars`** → Bypasses processing and returns a single chunk.
2. **`small_document_threshold_chars` - `medium_document_threshold_chars`** → Applies heading-level chunking.
3. **> `medium_document_threshold_chars`** → Applies standard chunking.

{% code lineNumbers="true" %}
```python
import json
from gllm_docproc.chunker.structured_element import StructuredElementChunker

# elements (input) that you want to Chunk
with open('./source/structuredelementchunker-with-smartbypass-input.json', 'r') as file:
    elements = json.load(file)

# initialize StructuredElementChunker with Smart Bypass feature
chunker = StructuredElementChunker(
    enable_smart_bypass=True,
    small_document_threshold_chars=500,
    medium_document_threshold_chars=25000
)

# chunk elements
chunked_elements = chunker.chunk(elements, excluded_structures=[])
print(chunked_elements)
```
{% endcode %}

In the example above, the [input JSON](https://assets.analytics.glair.ai/generative/pdf/structuredelementchunker-with-smartbypass-input.json) qualifies as a medium-sized file. As a result, the [output JSON](https://assets.analytics.glair.ai/generative/pdf/structuredelementchunker-with-smartbypass-output.json) shows that the elements are split at the heading level.

## Customize Structured Element Chunker

You can customize Structured Element Chunker like so:

{% code lineNumbers="true" %}
```python
import json
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from gllm_docproc.chunker.structured_element import StructuredElementChunker
from gllm_docproc.chunker.table import MARKDOWN, TableChunker
from gllm_docproc.model.element import AUDIO, FOOTER, FOOTNOTE, HEADER, IMAGE, VIDEO, Element

# elements (input) that you want to Chunk
with open("./data/source/parsed_elements.json", "r") as file:
    parsed_elements = json.load(file)

# initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n#", "\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""], chunk_size=1800, chunk_overlap=360
)

# initialize table chunker
table_chunker = TableChunker(chunk_size=4000, chunk_overlap=0, table_format=MARKDOWN)

# initialize StructuredElementChunker
chunker = StructuredElementChunker(
    text_splitter=text_splitter, table_chunker=table_chunker, is_parent_structure_info_included=True
)

# initialize excluded structures
excluded_structures = [HEADER, FOOTER, FOOTNOTE, IMAGE, VIDEO, AUDIO]


# initialize enrich chunk function
def enrich_chunk(chunk: Element, elements: list[Element]) -> Element:
    position: list[dict[str, Any]] = [
        {
            "coordinates": element.metadata.coordinates,
            "page_number": element.metadata.page_number,
        }
        for element in elements
        if hasattr(element.metadata, "coordinates") and hasattr(element.metadata, "page_number")
    ]
    if position:
        chunk.metadata.position = position
    return chunk


# chunk elements
chunked_elements = chunker.chunk(parsed_elements, excluded_structures=excluded_structures, enrich_chunk=enrich_chunk)

```
{% endcode %}

To get better understanding of how the above code works, here you can access the example [input](https://assets.analytics.glair.ai/generative/pdf/pdfparser-tablecaptionparser-output.json) and [output](https://assets.analytics.glair.ai/generative/pdf/structuredelementchunker-output.json).
