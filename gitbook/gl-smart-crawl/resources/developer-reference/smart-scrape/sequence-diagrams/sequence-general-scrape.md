# Sequence Diagram: General Scrape

### Extraction Layer (`/scrape`): General Content Extraction Path (Fallback)

This subsection describes the general fallback execution path inside the Extraction Layer for URLs that do not match any domain-specific scraper.

For URLs without a dedicated domain scraper, the Orchestration Layer in GL Smart Crawl calls the Extraction Layer endpoint (`/scrape`), and `ScraperRouter` routes the request to `GeneralScraper`. `GeneralScraper` resolves extraction schema in priority order (`custom schema` -> `response_type` -> `default article schema`) before requesting structured extraction from GL Smart Search. It first attempts extraction using `SELF_HOST`; if that fails, it retries with `FIRECRAWL`; if both fail, it returns a fallback payload with a stable response shape. This preserves predictable downstream processing while improving resilience to provider-specific failures.

```mermaid
sequenceDiagram
    autonumber

    participant Orchestration as Orchestration Layer
    participant API as Extraction Layer API /scrape
    participant Router as ScraperRouter
    participant General as GeneralScraper
    participant Search as GL Smart Search

    Orchestration->>API: POST /scrape {url, source, response_type?, schema?}
    API->>Router: get_scraper(source, response_type, schema)
    Router-->>API: GeneralScraper instance (fallback path)

    API->>General: scrape(url)
    General->>General: Resolve schema (schema > response_type > default article)
    General->>Search: get_web_page(SELF_HOST, json_schema)

    alt SELF_HOST success
        Search-->>General: extracted structured data
        General-->>API: Normalized extracted payload
    else SELF_HOST failed
        General->>Search: get_web_page(FIRECRAWL, json_schema)
        alt FIRECRAWL success
            Search-->>General: extracted structured data
            General-->>API: Normalized extracted payload
        else FIRECRAWL failed
            General-->>API: Fallback payload with stable shape
        end
    end

    API-->>Orchestration: 200 Success {content, metadata}
    Orchestration->>Orchestration: Store result and update URL status
```
