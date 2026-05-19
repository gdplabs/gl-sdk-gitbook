---
icon: wand-magic-sparkles
---

# General Scrape

This guide shows how to run **ad-hoc scraping for a single URL** using GL Smart Crawl API.

Use this when you want quick extraction outside scheduler-based listing/scraping batches.

Endpoint used in this guide:

```bash
POST /api/v1/scrape
```

***

## When to Use General Scrape

- You want to scrape one URL immediately.
- The URL is not part of scheduled crawl yet.
- You need custom extraction shape (`schema`) or extraction hint (`prompt`).

***

## 1) Known Domain URL (Domain-Specific Scraper Path)

For supported domains, GL Smart Crawl uses domain-specific extraction automatically.

```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.cnnindonesia.com/ekonomi/20260422091500-92-123456/example-article"
  }'
```

***

## 2) Unknown Domain URL (General Article Extraction)

For unknown domains, set `response_type` so GL Smart Crawl routes to general extraction.

```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Indonesia",
    "response_type": "article"
  }'
```

***

## 3) Unknown Domain URL (General Property Extraction)

Use `response_type: "property"` for property-shaped output.

```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example-property-site.com/listing/123",
    "response_type": "property"
  }'
```

***

## 4) Custom Schema + Prompt (Advanced General Extraction)

When you need custom output fields, provide both:
- `response_type` (required by API when using `schema`/`prompt`)
- `schema` (JSON schema)
- `prompt` (extraction instruction)

```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Indonesia",
    "response_type": "article",
    "schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "key_facts": {
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["title"]
    },
    "prompt": "Focus on concise summary and key facts only."
  }'
```

***

## Common Notes

- `response_type` values in GL Smart Crawl API: `article`, `property`.
- If `schema` or `prompt` is provided without `response_type`, API returns `400`.
- Result is persisted by GL Smart Crawl as crawled data (`SUCCESS`/`FAILED` status handling).
- For unknown domains, general extraction depends on Smart Scrape integration with GL Smart Search.

***

## Related Guides

- [**Article Crawl**](article-crawl.md)
- [**Property Crawl**](property-crawl.md)
- [**Auto Crawl Scheduler**](auto-crawl-scheduler.md)
