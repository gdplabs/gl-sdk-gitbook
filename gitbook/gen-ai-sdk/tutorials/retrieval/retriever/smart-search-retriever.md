# Smart Search Web Retriever

## What's a Smart Search Web Retriever?

**Smart Search Web Retriever** retrieves information from the web using the SmartSearch SDK. It performs web searches, extracts content from web pages, and returns structured results. This enables real-time internet search capabilities integrated directly into your RAG pipeline.

**Best For**:

* Real-time web search integration
* Current events and recent information retrieval
* Web page content extraction and summarization
* Multi-source web search
* Live data retrieval beyond static knowledge bases

**Key Features**:

* Web search query execution
* URL-based retrieval
* Web page content fetching
* Snippet and keypoint extraction
* Search map generation
* Structured result formatting as Chunks

**Use Cases**:

* Real-time question answering with current web data
* News and event monitoring
* Competitive intelligence and market research
* Fact-checking with live sources
* Augmenting internal knowledge bases with web results

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Retriever](./README.md) concepts
2. SmartSearch SDK setup and authentication
3. Web search query formulation

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-retrieval"
```
{% endtab %}
{% endtabs %}

## What it does

The Smart Search Web Retriever connects to the SmartSearch SDK to perform web searches, fetch page content, and extract relevant information. Results are returned as standardized Chunk objects for integration with your RAG pipeline.

## Basic Usage

Set up the retriever with SmartSearch credentials:

```python
from gllm_retrieval.retriever import SmartSearchWebRetriever

# Initialize with SmartSearch endpoint and credentials
retriever = SmartSearchWebRetriever(
    base_url="https://your-smartsearch-endpoint",
    token="your-access-token"
)

# Perform a web search
results = await retriever.retrieve(
    "What is the latest news about AI?",
    top_k=5
)
```

## Search Modes and Options

Different search modes for various use cases:

```python
from gllm_retrieval.constants import SmartSearchResultType, SmartSearchSnippetStyle

retriever = SmartSearchWebRetriever(
    base_url="https://your-smartsearch-endpoint",
    token="your-access-token"
)

# Web search results with snippets
results = await retriever.retrieve(
    "machine learning trends",
    top_k=10,
    result_type=SmartSearchResultType.WEB_SEARCH
)

# URL-based retrieval
results = await retriever.retrieve(
    urls=["https://example.com/article"],
    top_k=5
)

# Page content fetching with keypoincts
results = await retriever.retrieve(
    query="extract key information",
    top_k=5,
    snippet_style=SmartSearchSnippetStyle.KEYPOINT
)
```

{% hint style="info" %}
**Implementation Notes**:
- SmartSearch provides multiple result modes: web search, URL retrieval, page fetching, and content extraction
- Snippet styles control result format (summary, keypoints, full page)
- Results are automatically converted to Chunk format for downstream processing
- API token and base URL must be configured before use
- Web search results include relevance scores and source metadata
{% endhint %}
