# CLI Web Search Commands

The GL Smart Search SDK provides powerful CLI commands for web searching, page fetching, and content extraction.

## Overview

Web search commands allow you to:

- **Search** the web for relevant documents and pages
- **Fetch** web page URLs matching your query
- **Extract** specific web page content
- **Get snippets** from web pages based on queries
- **Extract keypoints** from web pages

## Prerequisites

Before using web search commands, ensure you have:

- GL Smart Search SDK installed (`pip install smart-search-sdk`)
- `SMARTSEARCH_BASE_URL` environment variable set to `https://search.glair.ai/`
- Valid GL Smart Search Token (set via `SMARTSEARCH_TOKEN` environment variable)

## Available Commands

### Web Search

Search the web for documents or pages relevant to your query.

#### Usage

```bash
smart-search web search --query "<QUERY>" [OPTIONS]
```

#### Parameters

| Parameter       | Required | Type    | Default    | Description                                              |
| --------------- | -------- | ------- | ---------- | -------------------------------------------------------- |
| `--query`       | Yes      | String  | -          | Search query string                                      |
| `--site`        | No       | String  | -          | Comma-separated URLs to limit results to specific sites  |
| `--result-type` | No       | String  | `snippets` | Type of results: `snippets`, `keypoints`, `summary`, `description` |
| `--engine`      | No       | String  | `auto`     | Search engine: `auto`, `firecrawl`, or `perplexity`      |
| `--size`        | No       | Integer | `5`        | Maximum number of results (1-50)                         |
| `--stream`      | No       | Boolean | `false`    | Enable streaming response                                |
| `--view`        | No       | String  | `table`    | Output format: `table` or `json`                         |

#### Examples

**Basic search with snippets:**

```bash
smart-search web search --query "Python tutorials"
```

**Search with keypoints:**

```bash
smart-search web search \
  --query "machine learning best practices" \
  --result-type keypoints \
  --size 10
```

**Search with JSON output:**

```bash
smart-search web search \
  --query "climate change solutions" \
  --view json \
  --size 20
```

**Streaming search:**

```bash
smart-search web search \
  --query "latest AI developments" \
  --stream true
```

**Search with site filter:**

```bash
smart-search web search \
  --query "machine learning frameworks" \
  --site "https://github.com" \
  --result-type snippets \
  --size 10
```

**Search with multiple sites:**

```bash
smart-search web search \
  --query "python frameworks" \
  --site "https://realpython.com,https://stackoverflow.com" \
  --result-type snippets \
  --size 10
```

**Search with specific engine:**

```bash
smart-search web search \
  --query "latest research papers" \
  --engine perplexity \
  --result-type keypoints \
  --size 15
```

#### Response (Table View)

```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ No ┃ URL                ┃ Title                ┃ Content Preview      ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ python.org/tut...  │ Python Tutorial      │ Learn Python step... │
│ 2  │ realpython.com/... │ Real Python Guide    │ Comprehensive Pyt... │
└────┴────────────────────┴──────────────────────┴──────────────────────┘
✓ Found 2 results.
```

#### Response (JSON View)

```json
{
  "data": [
    {
      "content": "Learn Python step by step with examples...",
      "metadata": {
        "title": "Python Tutorial",
        "source": "https://docs.python.org/3/tutorial/"
      }
    }
  ]
}
```

---

### Web - Map Website

Map a website and discover its URL structure and hierarchy.

#### Usage

```bash
smart-search web map --base-url "<BASE_URL>" [OPTIONS]
```

#### Parameters

| Parameter              | Required | Type    | Default | Description                                                                                |
| ---------------------- | -------- | ------- | ------- | ------------------------------------------------------------------------------------------ |
| `--base-url`           | Yes      | String  | -       | Base URL of the website to map                                                             |
| `--page`               | No       | Integer | `1`     | Page number to return (default is 1). Can be skipped if `--return-all-map` is true.        |
| `--size`               | No       | Integer | `20`    | Maximum number of URLs to return (1-1000), default is 20. Can be skipped if `--return-all-map` is true. |
| `--return-all-map`     | No       | Boolean | `false` | Return all mapped links (default is false)                                                 |
| `--include-subdomains` | No       | Boolean | `false` | Include subdomains in the mapping                                                          |
| `--query`              | No       | String  | -       | Optional query to filter URLs by keywords                                                  |
| `--view`               | No       | String  | `table` | Output format: `table` or `json`                                                           |

#### Examples

**Basic website mapping:**

```bash
smart-search web map --base-url "https://docs.python.org"
```

**Map with keyword filtering:**

```bash
smart-search web map \
  --base-url "https://docs.python.org" \
  --query "tutorial" \
  --size 20 \
  --page 1
```

**Include subdomains:**

```bash
smart-search web map \
  --base-url "https://example.com" \
  --include-subdomains \
  --size 50
```

**Return all mapped links:**

```bash
smart-search web map \
  --base-url "https://docs.firecrawl.dev" \
  --return-all-map true
```

**Get JSON output:**

```bash
smart-search web map \
  --base-url "https://docs.firecrawl.dev" \
  --size 30 \
  --page 1 \
  --view json
```

#### Response (Table View)

```
🗺️  Mapping website...
Base URL: https://docs.python.org
Page: 1
Size: 20
Return All Map: False
Include Subdomains: False
Query: None
View: table

┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ #  ┃ URL                               ┃ Title                        ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ https://docs.python.org/3/        │ Python 3 Documentation       │
│ 2  │ https://docs.python.org/3/tuto... │ The Python Tutorial          │
│ 3  │ https://docs.python.org/3/lib...  │ The Python Standard Library  │
└────┴───────────────────────────────────┴──────────────────────────────┘
✓ Found 20 URLs.
```

#### Response (JSON View)

```json
{
  "data": [
    {
      "url": "https://docs.python.org/3/",
      "title": "Python 3 Documentation",
      "description": "Official Python documentation"
    },
    {
      "url": "https://docs.python.org/3/tutorial/",
      "title": "The Python Tutorial",
      "description": "Learn Python step by step"
    }
  ],
  "total_found_links": 42,
  "page": 1,
  "size": 20,
  "total_pages": 3
}
```

---

### Web - Search URLs

Search the web for pages and return their URLs (similar to Google search results).

#### Usage

```bash
smart-search web urls --query "<QUERY>" [OPTIONS]
```

#### Parameters

| Parameter  | Required | Type    | Default | Description                                           |
| ---------- | -------- | ------- | ------- | ----------------------------------------------------- |
| `--query`  | Yes      | String  | -       | Search query string                                   |
| `--site`   | No       | String  | -       | Comma-separated URLs to limit results to specific sites |
| `--engine` | No       | String  | `auto`  | Search engine: `auto`, `firecrawl`, or `perplexity`   |
| `--size`   | No       | Integer | `5`     | Maximum number of URLs (1-50)                         |
| `--stream` | No       | Boolean | `false` | Enable streaming response                             |
| `--view`   | No       | String  | `table` | Output format: `table` or `json`                      |

#### Examples

**Find URLs about Python documentation:**

```bash
smart-search web urls --query "Python documentation" --size 10
```

**Get URLs with JSON output:**

```bash
smart-search web urls \
  --query "react best practices" \
  --view json
```

**Search URLs with site filter:**

```bash
smart-search web urls \
  --query "python tutorials" \
  --site "https://realpython.com" \
  --size 10
```

**Search multiple sites for URLs:**

```bash
smart-search web urls \
  --query "ai tutorials" \
  --site "https://medium.com,https://dev.to" \
  --size 20
```

**Search with specific engine:**

```bash
smart-search web urls \
  --query "cloud computing guides" \
  --engine firecrawl \
  --size 10
```

#### Response (Table View)

```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No ┃ URL                                      ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ https://docs.python.org/3/              │
│ 2  │ https://www.python.org/doc/             │
│ 3  │ https://realpython.com/                 │
└────┴──────────────────────────────────────────┘
✓ Found 3 URLs.
```

---

### Web - Fetch Page

Fetch a single web page by URL and return its content and metadata.

#### Usage

```bash
smart-search web fetch --url "<URL>" [OPTIONS]
```

#### Parameters

| Parameter       | Required | Type    | Default | Description                              |
| --------------- | -------- | ------- | ------- | ---------------------------------------- |
| `--url`         | Yes      | String  | -       | URL of the web page to fetch             |
| `--json-schema` | No       | String  | -       | Path to JSON schema file or JSON string  |
| `--return-html` | No       | Boolean | `false` | Return full HTML content                 |
| `--stream`      | No       | Boolean | `false` | Enable streaming response                |
| `--view`        | No       | String  | `json`  | Output format: `json` or `markdown`      |

#### Examples

**Fetch page content:**

```bash
smart-search web fetch --url "https://docs.python.org/3/tutorial/"
```

**Fetch with HTML:**

```bash
smart-search web fetch \
  --url "https://example.com/article" \
  --return-html \
  --view markdown
```

**Fetch with JSON schema:**

```bash
smart-search web fetch \
  --url "https://example.com/product-page" \
  --json-schema '{"type": "object", "properties": {"product_name": {"type": "string"}, "price": {"type": "number"}, "features": {"type": "array", "items": {"type": "string"}}}}' \
  --view json
```

**Fetch with schema from file:**

```bash
smart-search web fetch \
  --url "https://example.com/article" \
  --json-schema "@schema.json" \
  --view json
```

#### Response (Markdown View)

```
✓ Page fetched successfully
Title: Python Tutorial
Description: The Python Tutorial — Python 3.x documentation
Language: en
Status: 200

Page Content (Markdown):

# Python Tutorial

Python is an easy to learn, powerful programming language...
```

#### Response (JSON View)

```json
{
  "metadata": {
    "title": "Python Tutorial",
    "description": "The Python Tutorial",
    "language": "en",
    "status_code": 200
  },
  "markdown": "# Python Tutorial\n\nPython is...",
  "html": "<html>...</html>"
}
```

---

### Web - Get Web Page Snippets

Extract relevant text snippets from a web page for a given query.

#### Usage

```bash
smart-search web snippets --query "<QUERY>" --url "<URL>" [OPTIONS]
```

#### Parameters

| Parameter       | Required | Type    | Default     | Description                                 |
| --------------- | -------- | ------- | ----------- | ------------------------------------------- |
| `--query`       | Yes      | String  | -           | Query to search within the page             |
| `--url`         | Yes      | String  | -           | URL of the web page to extract from         |
| `--size`        | No       | Integer | `5`         | Maximum number of snippets (1-50)           |
| `--json-schema` | No       | String  | -           | Path to JSON schema file or JSON string     |
| `--style`       | No       | String  | `paragraph` | Snippet style: `paragraph` or `sentence`    |
| `--stream`      | No       | Boolean | `false`     | Enable streaming response                   |
| `--view`        | No       | String  | `table`     | Output format: `table` or `json`            |

#### Examples

**Extract snippets about list comprehension:**

```bash
smart-search web snippets \
  --query "list comprehension" \
  --url "https://docs.python.org/3/tutorial/" \
  --size 3
```

**Extract sentence-style snippets:**

```bash
smart-search web snippets \
  --query "async programming" \
  --url "https://docs.python.org/3/library/asyncio.html" \
  --style sentence \
  --size 5
```

**Extract with JSON schema:**

```bash
smart-search web snippets \
  --query "python examples" \
  --url "https://realpython.com/python-decorators/" \
  --json-schema '{"type": "object", "properties": {"code_examples": {"type": "array", "items": {"type": "object", "properties": {"language": {"type": "string"}, "code": {"type": "string"}}}}}}' \
  --size 5 \
  --view json
```

#### Response (Table View)

```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ No ┃ Content                         ┃ Score  ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1  │ List comprehensions provide...  │ 0.92   │
│ 2  │ A list comprehension consists...│ 0.88   │
└────┴─────────────────────────────────┴────────┘
✓ Found 2 snippets.
```

---

### Web - Get Web Page Keypoints

Extract concise key points from a web page.

#### Usage

```bash
smart-search web keypoints --query "<QUERY>" --url "<URL>" [OPTIONS]
```

#### Parameters

| Parameter       | Required | Type    | Default | Description                               |
| --------------- | -------- | ------- | ------- | ----------------------------------------- |
| `--query`       | Yes      | String  | -       | Query to search for                       |
| `--url`         | Yes      | String  | -       | URL of the web page to extract from       |
| `--size`        | No       | Integer | `5`     | Maximum number of keypoints (1-50)        |
| `--json-schema` | No       | String  | -       | Path to JSON schema file or JSON string   |
| `--stream`      | No       | Boolean | `false` | Enable streaming response                 |
| `--view`        | No       | String  | `table` | Output format: `table` or `json`          |

#### Examples

**Extract Python features:**

```bash
smart-search web keypoints \
  --query "Python features" \
  --url "https://www.python.org/about/" \
  --size 5
```

**Get keypoints with JSON output:**

```bash
smart-search web keypoints \
  --query "benefits of TypeScript" \
  --url "https://www.typescriptlang.org/" \
  --view json
```

**Extract keypoints with JSON schema:**

```bash
smart-search web keypoints \
  --query "product information" \
  --url "https://example.com/product" \
  --json-schema '{"type": "object", "properties": {"features": {"type": "array", "items": {"type": "string"}}, "benefits": {"type": "array", "items": {"type": "string"}}}}' \
  --size 5 \
  --view json
```

#### Response (Table View)

```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ No ┃ Key Point                       ┃ Score  ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1  │ Python is easy to learn         │ 0.95   │
│ 2  │ Extensive standard library      │ 0.91   │
│ 3  │ Dynamic typing system           │ 0.87   │
└────┴─────────────────────────────────┴────────┘
✓ Found 3 key points.
```

## Output Formats

### Table View

- Human-readable format
- Best for interactive CLI usage
- Automatically formats columns and rows

### JSON View

- Machine-readable format
- Best for scripting and automation
- Complete data structure with all fields

## Streaming Responses

Enable streaming for better performance with large result sets:

```bash
smart-search web search --query "AI news" --stream true
```

Benefits:

- Real-time results as they arrive
- Reduced memory usage
- Better user experience for long-running queries

## Best Practices

1. **Choose appropriate result types**:

   - Use `snippets` for detailed text excerpts
   - Use `keypoints` for concise summaries
   - Use `summary` for high-level overviews

2. **Optimize size parameter**:

   - Start with default (5) for quick results
   - Increase for comprehensive searches
   - Maximum is 50 results per query

3. **Use streaming for performance**:

   - Enable `--stream true` for queries returning many results
   - Reduces waiting time and memory usage

4. **Select appropriate snippet style**:

   - `paragraph`: For contextual information
   - `sentence`: For precise, concise answers

5. **JSON for automation**:
   - Use `--view json` when integrating with scripts
   - Easier to parse and process programmatically

## Common Use Cases

### Research and Documentation

```bash
# Find comprehensive guides
smart-search web search \
  --query "TypeScript advanced patterns" \
  --result-type snippets \
  --size 10

# Extract specific information
smart-search web snippets \
  --query "dependency injection" \
  --url "https://angular.io/guide/dependency-injection"
```

### Quick Information Lookup

```bash
# Get concise answers
smart-search web keypoints \
  --query "React hooks useEffect" \
  --url "https://react.dev/reference/react/useEffect"
```

### Content Aggregation

```bash
# Collect URLs for further processing
smart-search web urls \
  --query "climate change research papers 2024" \
  --size 50 \
  --view json > urls.json
```

### Page Analysis

```bash
# Analyze webpage content
smart-search web fetch \
  --url "https://example.com/article" \
  --view markdown > article.md
```

## Error Handling

All commands provide clear error messages:

```bash
❌ Error occurred during web search
Details: Invalid URL format - please provide a valid HTTP/HTTPS URL
```

Common errors:

- **Invalid URL**: Ensure URLs start with `http://` or `https://`
- **Connection timeout**: Check network connectivity and `SMARTSEARCH_BASE_URL`
- **Authentication failed**: Verify credentials and environment variables
- **Size out of range**: Use values between 1 and 50
