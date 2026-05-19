# Technology Stack

This section lists the major technologies used by the current GL Smart Crawl **Extraction Layer** implementation.

## Runtime and API Layer

- **Python**: `>=3.11,<3.13`
- **FastAPI**: `>=0.122.0,<0.123.0`
- **Uvicorn**: `>=0.38.0,<0.39.0`
- **Pydantic**: v2 (structured request/response and extraction schemas)

## Scraping and Parsing Engine

- **Playwright**: `>=1.56.0,<2.0.0` (browser rendering for JS-heavy pages)
- **playwright-stealth**: `>=2.0.2,<3.0.0` (anti-bot hardening)
- **BeautifulSoup4**: `>=4.12.0,<5.0.0`
- **lxml**: `>=5.0.0,<6.0.0`
- **requests**: `>=2.32.5,<3.0.0` (HTTP/API access and Smart Search calls)
- **markdownify**: `>=1.2.2,<2.0.0` (HTML-to-markdown normalization)
- **quickjs**: `>=1.19.4,<2.0.0` (script metadata parsing for some sources, e.g., Lamudi)

## Document and Financial Report Processing

- **pdfplumber**: `>=0.11.0,<1.0.0` (PDF handling)
- **openpyxl**: (XLSX extraction for IDX report flows)

## External Integrations and AI/LLM

- **Smart Search API** (`/v2/web/page`, `/v2/web/page/keypoints`) for:
  - structured extraction fallback,
  - key-point summarization support.
- **gllm-core**: `>=0.3.15,<0.4.0`
- **gllm-inference[openai]**: `>=0.5.85,<0.6.0`
- **glaip-sdk**: `>=0.7.37,<0.8.0` (used in IDX report-related AI workflows)
- **httpx** (used in async integration clients such as LLM Labs adapters)

## Notes

- The Extraction Layer is designed as a stateless extraction service (no internal operational database in this service).
- Routing decides between domain scrapers and General Scraper, while Smart Search provides fallback extraction capability.
