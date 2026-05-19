# General Scrape Implementation

This page explains how the GL Smart Crawl **Extraction Layer** (Smart Scrape module) implements fallback/general scraping through `POST /scrape` when a URL does not match any domain-specific scraper.

## 1. Scope and Intent

General scrape is the resilience path for unknown or unsupported domains.

Its responsibilities are:

- accept arbitrary URLs not covered by `URL_SCRAPER_MAP`,
- resolve extraction schema and prompt,
- request structured extraction from Smart Search,
- apply provider fallback (`SELF_HOST` -> `FIRECRAWL`),
- return predictable output shape even on failure.

## 2. Core Components in General Scrape Flow

Main implementation entry points:

- `applications/custom-scrapers/custom_scrapers/app.py` (`/scrape`)
- `custom_scrapers/scraper/helper/scraper_router.py` (`ScraperRouter`)
- `custom_scrapers/scraper/general/general_scraper.py` (`GeneralScraper`)
- `custom_scrapers/service/smart_search_service.py` (`SmartSearchService`)
- output schemas:
  - `custom_scrapers/api/schemas/article.py`
  - `custom_scrapers/api/schemas/property.py`
  - `custom_scrapers/api/schemas/regulation_government.py`

## 3. Router Entry Conditions

`ScraperRouter` behavior:

- if URL matches a known domain, domain scraper is returned,
- if no match, `GeneralScraper` is returned with request context:
  - `response_type`,
  - `schema`,
  - `prompt`.

This means general scrape only executes on non-mapped domains.

## 4. Request Contract

Input fields for general path:

- `source` (required),
- `response_type` (`article`, `property`, `regulation`; defaults to `article`),
- `schema` (optional custom JSON schema),
- `prompt` (optional extraction instruction).

Precedence rule:

- domain route has priority over general settings,
- for general route: `schema` overrides `response_type` schema.

## 5. Schema and Prompt Resolution

### 5.1 Schema resolution (`GeneralScraper._resolve_schema`)

Resolution order:

1. caller-provided `schema`,
2. schema generated from model mapped by `response_type`,
3. default article schema when neither is explicit.

### 5.2 Prompt resolution (`GeneralScraper._resolve_prompt`)

Resolution order:

1. caller-provided `prompt`,
2. response-type default prompt from config:
   - article default prompt,
   - property default prompt,
   - regulation default prompt.

## 6. Smart Search Call Chain and Fallback

General scraper calls Smart Search `/v2/web/page` using `json_schema` extraction.

Provider sequence:

1. primary: `search_mode=SELF_HOST`,
2. fallback: `search_mode=FIRECRAWL` if:
   - request raises exception, or
   - response fails extraction checks.

Extraction success criteria (`_is_extraction_success`):

- payload exists in `json` or `data`,
- payload is a dictionary,
- `metadata.status_code` is absent or equals `200`.

## 7. Fallback Payload Behavior

If both providers fail:

- with custom `schema`: returns `[{}]`,
- without custom `schema`: returns one empty object shaped like the target model:
  - list fields -> `[]`,
  - scalar/object fields -> `None`.

This gives stable downstream shape and avoids hard failures for orchestrators that expect deterministic keys.

## 8. Output Contract

General scrape always returns `list[dict]` (single-item list in current implementation):

- success: `[extracted_payload]`,
- full failure: `[fallback_payload]`.

API envelope remains:

- `message: "Success"`
- `content: [...]`

Errors are raised only for endpoint/router-level failures, not for extraction fallback conditions.

## 9. Reliability and Error Handling Mechanics

General scrape reliability characteristics:

- two-provider fallback improves extraction robustness,
- extraction validation filters false-success responses,
- fallback payload avoids schema-breaking null responses,
- schema generation from Pydantic models keeps extraction contract synchronized with code.

## 10. Practical Summary

Smart Scrape general scraping is a schema-driven fallback adapter:

- route unknown domains into a unified extraction pipeline,
- resolve schema/prompt deterministically,
- try self-hosted Smart Search first and Firecrawl second,
- guarantee predictable output shape for Smart Crawl and downstream processors.
