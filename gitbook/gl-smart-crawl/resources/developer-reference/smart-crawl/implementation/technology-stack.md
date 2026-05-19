# Technology Stack

This section lists the major technologies used by the current GL Smart Crawl **Orchestration Layer** implementation.

## Runtime and API Layer

- **Python**: `>=3.11,<3.13`
- **FastAPI**: `>=0.124`
- **Uvicorn**: `uvicorn[standard]>=0.38.0`
- **Pydantic**: v2 (used across request/response and domain models)

## Data and Persistence

- **PostgreSQL**: primary operational database
- **SQLAlchemy**: 2.x usage across repositories and models
- **Alembic**: `>=1.13.3` (database migration management)
- **psycopg2-binary**: `>=2.9.0` (PostgreSQL driver)

## Search and Indexing

- **Elasticsearch**: async client integration for article indexing/search
- **gllm-datastore**: `>=0.5.22` with `chroma, elasticsearch, kg` extras

## Scheduling and Background Processing

- **APScheduler**: `>=3.11.2` (listing/scraping scheduler orchestration)

## External Integrations and HTTP

- **httpx**: `>=0.27.0` (async HTTP client in engine adapters)
- **smart-search-sdk**: `>=0.0.10,<0.1.0` (Smart Search integration)
- **Custom Scrapers API**: integration (Extraction Layer service calls)

## GL Ecosystem Libraries

- **gllm-core**: `>=0.3.17`

## Notes

- The Orchestration Layer is stateful and DB-backed (PostgreSQL + crawl state/job tables).
- Elasticsearch features are optional at runtime and can be disabled by configuration.
