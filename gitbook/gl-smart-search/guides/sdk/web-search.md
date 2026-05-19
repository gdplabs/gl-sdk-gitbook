# Web Search

The **Web Search** module enables you to perform searches across the web, retrieve URLs, fetch page content, and extract structured insights such as snippets or keypoints.\
It provides a unified interface for integrating external search and content retrieval into your application.

---

### Setup

Before using the Web Search SDK, ensure the following environment variables are configured:

```bash
export SMARTSEARCH_BASE_URL="https://search.glair.ai/"
export SMARTSEARCH_TOKEN="your-access-token"
```

Install the SDK and dependencies:

```bash
pip install smart-search-sdk
```

Initialize the client:

```python
import asyncio
import json
import os
from dotenv import load_dotenv

from smart_search_sdk.web.client import WebSearchClient
from smart_search_sdk.web.models import (
    GetWebSearchResultsRequest,
    GetWebSearchUrlsRequest,
    GetWebPageRequest,
    GetWebPageSnippetsRequest,
    GetWebPageKeypointsRequest,
    GetWebSearchMapRequest,
)

load_dotenv()

client = WebSearchClient(base_url=os.getenv("SMARTSEARCH_BASE_URL"))
await client.authenticate(token=os.getenv("SMARTSEARCH_TOKEN"))
```

---

### 1. Perform a Basic Web Search

Retrieve search results containing snippets, keypoints, or summaries from the web.

```python
request = GetWebSearchResultsRequest(
    query="What is cloud computing?",
    result_type="snippets",
    size=5
)
result = await client.search_web(request)
print(json.dumps(result, indent=4))
```

#### Parameters

| Parameter     | Type               | Description                                                                                                                                                                                                   |
| ------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `query`       | `str`              | The text query to search for.                                                                                                                                                                                 |
| `result_type` | `str`              | Type of output format. Supported values: • `"snippets"` – short excerpts from web pages.• `"keypoints"` – summarized highlights from results.• `"summary"` – condensed summary across sources.• `"description"` – descriptions of results. |
| `size`        | `int`              | Number of results to return.                                                                                                                                                                                  |
| `site`        | `list[str]` / `str` | (Optional) URL or list of URLs to limit search results to specific sites or domains.                                                                                                                          |
| `engine`      | `str`              | (Optional) Search engine to use: `"auto"`, `"firecrawl"`, or `"perplexity"`. Defaults to `"auto"`.                                                                                                          |

#### Search Results with Site Filter

To limit search results to a specific site or domain, use the `site` parameter in `GetWebSearchResultsRequest`:

```python
request = GetWebSearchResultsRequest(
    query="machine learning frameworks",
    site="https://github.com",
    result_type="snippets",
    size=5
)
result = await client.search_web(request)
print(json.dumps(result, indent=4))
```

#### Search with Multiple Sites

You can search across multiple sites simultaneously by providing a list of URLs:

```python
request = GetWebSearchResultsRequest(
    query="machine learning tutorials",
    site=["https://realpython.com", "https://medium.com", "https://towardsdatascience.com"],
    result_type="snippets",
    size=10
)
result = await client.search_web(request)
print(json.dumps(result, indent=4))
```

#### Search with Specific Engine

Choose a specific search engine for your query:

```python
from smart_search_sdk.web.models.model import WebSearchEngine

request = GetWebSearchResultsRequest(
    query="latest AI research",
    engine=WebSearchEngine.PERPLEXITY,
    result_type="keypoints",
    size=5
)
result = await client.search_web(request)
print(json.dumps(result, indent=4))
```

---

### 2. Retrieve Web Search Keypoints

Extract summarized keypoints directly from top web search results.

```python
request = GetWebSearchResultsRequest(
    query="Python programming best practices",
    result_type="keypoints",
    size=3
)
result = await client.search_web(request)
print(json.dumps(result, indent=4))
```

#### Parameters

Same as above — `result_type` can be set to `"keypoints"` to focus on summarized insights instead of raw snippets.

---

### 3. Get Web Search URLs

Return a list of URLs that match the given query.

```python
request = GetWebSearchUrlsRequest(
    query="Python programming tutorials",
    size=5
)
result = await client.search_web_urls(request)
print(json.dumps(result, indent=4))
```

#### Parameters

| Parameter | Type               | Description                                                          |
| --------- | ------------------ | -------------------------------------------------------------------- |
| `query`   | `str`              | The text query to search for.                                        |
| `size`    | `int`              | Number of URLs to return.                                            |
| `site`    | `list[str]` / `str` | (Optional) URL or list of URLs to limit search results to specific sites or domains. |
| `engine`  | `str`              | (Optional) Search engine to use: `"auto"`, `"firecrawl"`, or `"perplexity"`. |

#### Search URLs with Site Filter

To limit URL search results to a specific site or domain, use the `site` parameter in `GetWebSearchUrlsRequest`:

```python
request = GetWebSearchUrlsRequest(
    query="python tutorials",
    site="https://realpython.com",
    size=5
)
result = await client.search_web_urls(request)
print(json.dumps(result, indent=4))
```

#### Search URLs Across Multiple Sites

```python
request = GetWebSearchUrlsRequest(
    query="python tutorials",
    site=["https://realpython.com", "https://docs.python.org"],
    size=10
)
result = await client.search_web_urls(request)
print(json.dumps(result, indent=4))
```

---

### 4. Map a Website

Discover and map the URL structure of a website.

```python
request = GetWebSearchMapRequest(
    base_url="https://docs.python.org",
    page=1,
    size=20,
    include_subdomains=False
)
result = await client.search_web_map(request)
print(json.dumps(result, indent=4))
```

#### Parameters

| Parameter            | Type   | Description                                                    |
| -------------------- | ------ | -------------------------------------------------------------- |
| `base_url`           | `str`  | The base URL of the website to map.                            |
| `size`               | `int`  | Maximum number of URLs to return (1-1000).                     |
| `include_subdomains` | `bool` | Whether to include subdomains in the mapping (default: False). |

#### 4.1 Map a Website with Query Filter

To filter mapped URLs by a search query, use the `query` parameter in `GetWebSearchMapRequest`:

```python
request = GetWebSearchMapRequest(
    base_url="https://docs.python.org",
    size=20,
    return_all_map=False,
    include_subdomains=False,
    query="tutorial"
)
result = await client.search_web_map(request)
print(json.dumps(result, indent=4))
```

#### Parameters for Query Filter

| Parameter            | Type   | Description                                                       |
| -------------------- | ------ | ----------------------------------------------------------------- |
| `base_url`           | `str`  | The base URL of the website to map.                               |
| `page`               | `int`  | Page number to return (default: 1).                               |
| `size`               | `int`  | Maximum number of URLs to return (1-1000), default is 20.         |
| `return_all_map`     | `bool` | Whether to return all mapped links (default: False).              |
| `include_subdomains` | `bool` | Whether to include subdomains in the mapping (default: False).    |
| `query`              | `str`  | Search query to filter URLs by keywords.                         |

---

### 5. Fetch a Web Page

Retrieve the content of a specific web page, either as raw HTML or structured text.

```python
request = GetWebPageRequest(
    source="https://docs.python.org/3/tutorial/",
    return_html=False
)
result = await client.fetch_web_page(request)
print(json.dumps(result, indent=4))
```

#### Parameters

| Parameter     | Type   | Description                                                                |
| ------------- | ------ | -------------------------------------------------------------------------- |
| `source`      | `str`  | The URL of the web page to fetch.                                          |
| `json_schema` | `dict` | (Optional) JSON schema for custom structured data extraction.              |
| `return_html` | `bool` | Whether to return the page as raw HTML (`True`) or cleaned text (`False`). |

---

### 5.1 Fetch Page with JSON Schema Extraction

Extract structured data from a web page using a custom JSON schema:

```python
schema = {
    "type": "object",
    "properties": {
        "article_title": {
            "type": "string",
            "description": "Main title of the article"
        },
        "author": {
            "type": "string",
            "description": "Author name"
        },
        "publish_date": {
            "type": "string",
            "description": "Publication date"
        },
        "key_points": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Main points from the article"
        }
    },
    "required": ["article_title", "key_points"]
}

request = GetWebPageRequest(
    source="https://example.com/blog/article",
    json_schema=schema
)
result = await client.fetch_web_page(request)

# Access structured data
print(result["json"]["article_title"])
print(result["json"]["key_points"])
```

**Using Pydantic Models (Recommended):**

Instead of manually writing JSON schemas, you can define Pydantic models and convert them automatically:

```python
from pydantic import BaseModel

class ArticleInfo(BaseModel):
    article_title: str
    author: str
    publish_date: str
    key_points: list[str]

request = GetWebPageRequest(
    source="https://example.com/blog/article",
    json_schema=ArticleInfo.model_json_schema()
)
result = await client.fetch_web_page(request)

# Access structured data
print(result["json"]["article_title"])
print(result["json"]["key_points"])
```

---

### 6. Extract Snippets from a Web Page

Extract relevant text snippets from a single web page based on a query.

```python
request = GetWebPageSnippetsRequest(
    query="Python tutorial",
    source="https://docs.python.org/3/tutorial/",
    size=3,
    snippet_style="paragraph"
)
result = await client.get_web_page_snippets(request)
print(json.dumps(result, indent=4))
```

#### Parameters

| Parameter       | Type  | Description                                                                                                                                                                                         |
| --------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `query`         | `str` | The text to match against the web page content.                                                                                                                                                     |
| `source`        | `str` | The URL of the web page.                                                                                                                                                                            |
| `size`          | `int` | Number of snippets to extract.                                                                                                                                                                      |
| `json_schema`   | `dict` | (Optional) JSON schema for custom extraction. Uses Firecrawl extract API.                                                                                                                          |
| `snippet_style` | `str` | Style of snippet extraction. Supported values: • `"paragraph"` – extracts full paragraphs containing the match.• `"sentence"` – extracts individual sentences related to the query. |

---

### 6.1 Extract Snippets with JSON Schema

Extract structured information from a web page:

```python
schema = {
    "type": "object",
    "properties": {
        "code_examples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "language": {"type": "string"},
                    "code": {"type": "string"},
                    "description": {"type": "string"}
                }
            },
            "description": "Code examples from the page"
        },
        "main_concepts": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Key concepts explained"
        }
    },
    "required": ["main_concepts"]
}

request = GetWebPageSnippetsRequest(
    query="python decorators",
    source="https://realpython.com/primer-on-python-decorators/",
    size=5,
    json_schema=schema
)
result = await client.get_web_page_snippets(request)

# Access structured data
print(result["raw_data"]["main_concepts"])
for  example in result["raw_data"].get("code_examples", []):
    print(f"Language: {example['language']}")
    print(f"Code: {example['code']}")
```

**Using Pydantic Models (Recommended):**

```python
from pydantic import BaseModel

class CodeExample(BaseModel):
    language: str
    code: str
    description: str

class BlogPostInfo(BaseModel):
    code_examples: list[CodeExample]
    main_concepts: list[str]

request = GetWebPageSnippetsRequest(
    query="python decorators",
    source="https://realpython.com/primer-on-python-decorators/",
    size=5,
    json_schema=BlogPostInfo.model_json_schema()
)
result = await client.get_web_page_snippets(request)

# Access structured data
print(result["raw_data"]["main_concepts"])
for example in result["raw_data"].get("code_examples", []):
    print(f"Language: {example['language']}")
    print(f"Code: {example['code']}")
```

---

### 7. Extract Keypoints from a Web Page

Generate key points summarizing the content of a given web page.

```python
request = GetWebPageKeypointsRequest(
    query="Python programming concepts",
    source="https://docs.python.org/3/tutorial/",
    size=3
)
result = await client.get_web_page_keypoints(request)
print(json.dumps(result, indent=4))
```

#### Parameters

| Parameter | Type  | Description                                           |
| --------- | ----- | ----------------------------------------------------- |
| `query`   | `str` | The focus topic for extracting keypoints.             |
| `source`  | `str` | The web page URL to analyze.                          |
| `size`    | `int` | Number of keypoints to return.                        |
| `json_schema` | `dict` | (Optional) JSON schema for custom extraction.     |

---

### 7.1 Extract Keypoints with JSON Schema

Extract structured keypoint information:

```python
schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "features": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Product features"
        },
        "benefits": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Product benefits"
        },
        "pricing": {
            "type": "object",
            "properties": {
                "currency": {"type": "string"},
                "amount": {"type": "number"}
            }
        }
    },
    "required": ["product_name", "features"]
}

request = GetWebPageKeypointsRequest(
    query="product features",
    source="https://example.com/product",
    size=5,
    json_schema=schema
)
result = await client.get_web_page_keypoints(request)

# Access structured data
print(result["raw_data"]["product_name"])
print(result["raw_data"]["features"])
```

**Using Pydantic Models (Recommended):**

```python
from pydantic import BaseModel

class Pricing(BaseModel):
    currency: str
    amount: float

class ProductInfo(BaseModel):
    product_name: str
    features: list[str]
    benefits: list[str]
    pricing: Pricing | None = None

request = GetWebPageKeypointsRequest(
    query="product features",
    source="https://example.com/product",
    size=5,
    json_schema=ProductInfo.model_json_schema()
)
result = await client.get_web_page_keypoints(request)

# Access structured data
print(result["raw_data"]["product_name"])
print(result["raw_data"]["features"])
```

---

### Summary

| Capability               | Method                            | Description                                                          |
| ------------------------ | --------------------------------- | -------------------------------------------------------------------- |
| `get_web_search_results` | `client.search_web()`             | Perform a web search and retrieve snippets, keypoints, or summaries. |
| `get_web_search_urls`    | `client.search_web_urls()`        | Retrieve a list of relevant web URLs.                                |
| `get_web_search_map`     | `client.search_web_map()`         | Map a website and discover its URL structure.                        |
| `get_web_page`           | `client.fetch_web_page()`         | Fetch the full content of a web page.                                |
| `get_web_page_snippets`  | `client.get_web_page_snippets()`  | Extract snippets from a specific web page.                           |
| `get_web_page_keypoints` | `client.get_web_page_keypoints()` | Generate keypoints summarizing a web page.                           |

---

### Full Code Snippet

<details>

<summary>Search</summary>

```python
import asyncio
import json
import os
from dotenv import load_dotenv

from smart_search_sdk.web.client import WebSearchClient
from smart_search_sdk.web.models import (
    GetWebSearchResultsRequest,
    GetWebSearchUrlsRequest,
    GetWebPageRequest,
    GetWebPageSnippetsRequest,
    GetWebPageKeypointsRequest,
    GetWebSearchMapRequest,
)

load_dotenv()

async def main():
    client = WebSearchClient(base_url=os.getenv("SMARTSEARCH_BASE_URL"))
    await client.authenticate(token=os.getenv("SMARTSEARCH_TOKEN"))

    # 1. Web Search (Snippets)
    request = GetWebSearchResultsRequest(
        query="What is cloud computing?",
        result_type="snippets",
        size=5
    )
    result = await client.search_web(request)
    print("=== Web Search (Snippets) ===")
    print(json.dumps(result, indent=4))

    # 1.5 Web Search (Snippets) with Site Filter
    request = GetWebSearchResultsRequest(
        query="machine learning frameworks",
        site="https://github.com",
        result_type="snippets",
        size=5
    )
    result = await client.search_web(request)
    print("\n=== Web Search (Snippets) with Site Filter ===")
    print(json.dumps(result, indent=4))

    # 2. Web Search (Keypoints)
    request = GetWebSearchResultsRequest(
        query="Python programming best practices",
        result_type="keypoints",
        size=3
    )
    result = await client.search_web(request)
    print("\n=== Web Search (Keypoints) ===")
    print(json.dumps(result, indent=4))

    # 3. Web Search URLs
    request = GetWebSearchUrlsRequest(
        query="Python programming tutorials",
        size=5
    )
    result = await client.search_web_urls(request)
    print("\n=== Web Search URLs ===")
    print(json.dumps(result, indent=4))

    # 3.2 Web Search URLs with Site Filter
    request = GetWebSearchUrlsRequest(
        query="python tutorials",
        site="https://realpython.com",
        size=5
    )
    result = await client.search_web_urls(request)
    print("\n=== Web Search URLs with Site Filter ===")
    print(json.dumps(result, indent=4))

    # 3.5 Web Search Map
    request = GetWebSearchMapRequest(
        base_url="https://docs.python.org",
        page=1,
        size=20,
        return_all_map=False,
        include_subdomains=False
    )
    result = await client.search_web_map(request)
    print("\n=== Web Search Map ===")
    print(json.dumps(result, indent=4))

    # 3.6 Web Search Map with Query Filter
    request = GetWebSearchMapRequest(
        base_url="https://docs.python.org",
        size=20,
        include_subdomains=False,
        query="tutorial"
    )
    result = await client.search_web_map(request)
    print("\n=== Web Search Map with Query Filter ===")
    print(json.dumps(result, indent=4))

    # 4. Fetch Web Page
    request = GetWebPageRequest(
        source="https://docs.python.org/3/tutorial/",
        return_html=False
    )
    result = await client.fetch_web_page(request)
    print("\n=== Fetch Web Page ===")
    print(json.dumps(result, indent=4))

    # 5. Web Page Snippets
    request = GetWebPageSnippetsRequest(
        query="Python tutorial",
        source="https://docs.python.org/3/tutorial/",
        size=3,
        snippet_style="paragraph"
    )
    result = await client.get_web_page_snippets(request)
    print("\n=== Web Page Snippets ===")
    print(json.dumps(result, indent=4))

    # 6. Web Page Keypoints
    request = GetWebPageKeypointsRequest(
        query="Python programming concepts",
        source="https://docs.python.org/3/tutorial/",
        size=3
    )
    result = await client.get_web_page_keypoints(request)
    print("\n=== Web Page Keypoints ===")
    print(json.dumps(result, indent=4))

asyncio.run(main())
```

</details>
