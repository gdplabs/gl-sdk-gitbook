---
icon: cubes
---

# Ingestion Pipeline: Index to Vector Database

{% include "../../../.gitbook/includes/coming-soon.md" %}

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[pdf]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[pdf]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[pdf]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [pdf-example.pdf](https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf).

## Ingestion Pipeline: Index to Vector Database

{% stepper %}
{% step %}
Continue the previous output in `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.pdf import PyMuPDFLoader

source = "pdf-example.pdf"


# load source
from gllm_docproc.loader.pdf import PDFPlumberLoader, PyMuPDFLoader
from gllm_docproc.loader.pipeline_loader import PipelineLoader

pipeline_loader = PipelineLoader()
pipeline_loader.add_loader(PyMuPDFLoader())
pipeline_loader.add_loader(PDFPlumberLoader())

loaded_elements = loader.load(source)

# parse
from gllm_docproc.parser.document import PDFParser
from gllm_docproc.parser.table import TableCaptionParser
from gllm_docproc.parser.pipeline_parser import PipelineParser

pipeline = PipelineParser()
pipeline.add_parser(PDFParser())
pipeline.add_parser(TableCaptionParser())

parsed_elements = parser.parse(loaded_elements)

# chunk
from gllm_docproc.chunker.structured_element import StructuredElementChunker
chunker = StructuredElementChunker()
chunked_elements = chunker.chunk(parsed_elements)

# index to vector database
from gllm_docproc.indexer.vector.vector_db_indexer import VectorDBIndexer
indexer = VectorDBIndexer()

result = indexer.index(
    elements=chunked_elements,
    file_id="file_001",
    vectorizer_kwargs={
        "model": "openai/text-embedding-3-small",  # Format: "provider/model_name"
        "api_key": "<OPENAI_API_KEY>",
    },
    db_engine="elasticsearch",  # Supported: "chroma", "elasticsearch", "opensearch"
    db_config={
        "url": "http://localhost:9200", # change to your Elasticsearch URL
        "index_name": "my_index", # change to your index name
    },
)
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
The pipeline load the PDF, parse, chunk, and finally index it into vector database (Elasticsearch). You can then perform retrieval into the Elasticsearch.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You have a full ingestion pipeline from reading PDF up to indexing it into a vector database!
{% endhint %}

Check out [gllm-docproc](../../tutorials/document-processing-orchestrator/) for more reusable building blocks for implementing ingestion pipeline.
