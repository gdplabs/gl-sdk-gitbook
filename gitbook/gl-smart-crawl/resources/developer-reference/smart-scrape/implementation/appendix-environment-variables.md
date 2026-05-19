# Appendix: Environment Variables (Smart Scrape)

This appendix lists environment variables used by the GL Smart Crawl Extraction Layer (Smart Scrape module), grouped by purpose.

## 1. Smart Search Integration (Core)


| Variable                       | Description                                         | Example / Notes                         |
| ------------------------------ | --------------------------------------------------- | --------------------------------------- |
| `SMART_SEARCH_BASE_URL`        | Smart Search base URL used by `SmartSearchService`. | `https://stag-be-smart-search.obrol.id` |
| `SMART_SEARCH_TOKEN`           | Bearer token for Smart Search API calls.            | `your-smart-search-token`               |
| `SMART_SEARCH_TIMEOUT_SECONDS` | Request timeout (seconds) for Smart Search calls.   | `15`                                    |


## 2. LLM Labs Integration (IDX Workflow)


| Variable                    | Description                                       | Example / Notes                       |
| --------------------------- | ------------------------------------------------- | ------------------------------------- |
| `LLMLABS_CLIENT_ID`         | OAuth client ID for LLM Labs.                     | `your-client-id`                      |
| `LLMLABS_CLIENT_SECRET`     | OAuth client secret for LLM Labs.                 | `your-client-secret`                  |
| `LLMLABS_TOKEN_URL`         | OAuth token endpoint.                             | `https://datasaur.ai/api/oauth/token` |
| `LLMLABS_API_BASE`          | LLM Labs REST base URL.                           | `https://datasaur.ai/api`             |
| `LLMLABS_UPLOAD_URL`        | Upload endpoint base for document upload.         | `https://upload.datasaur.ai/api`      |
| `LLMLABS_GRAPHQL_URL`       | GraphQL endpoint for KB attachment workflows.     | `https://app.datasaur.ai/graphql`     |
| `LLMLABS_KNOWLEDGE_BASE_ID` | Target knowledge base ID for document attachment. | `4488`                                |
| `LLMLABS_CLIENT_TIMEOUT`    | HTTP timeout for LLM Labs client (seconds).       | `60.0`                                |


## 3. OLX Scraper Tuning


| Variable                           | Description                             | Example / Notes                      |
| ---------------------------------- | --------------------------------------- | ------------------------------------ |
| `OLX_BASE_URL`                     | Base URL for OLX site links.            | Default: `https://www.olx.co.id`     |
| `OLX_BASE_SEARCH_URL`              | Base URL for OLX relevance API.         | `https://api.olx.co.id/relevance/v4` |
| `OLX_TIMEOUT_CONNECT_SECONDS`      | OLX connect timeout (seconds).          | `10`                                 |
| `OLX_TIMEOUT_READ_SECONDS`         | OLX read timeout (seconds).             | `60`                                 |
| `OLX_TIMEOUT_CONNECT_READ_SECONDS` | Combined `(connect,read)` timeout pair. | `10,60`                              |
| `OLX_MAX_RETRIES`                  | Retry attempts for OLX requests.        | `3`                                  |
| `OLX_BACKOFF_FACTOR`               | Retry backoff multiplier.               | `0.1`                                |
| `OLX_RETRY_STATUS_CODES`           | Retry HTTP status codes.                | `500,502,503,504`                    |


## 4. Kontan Data Extractor Tuning


| Variable                                      | Description                                          | Example / Notes                              |
| --------------------------------------------- | ---------------------------------------------------- | -------------------------------------------- |
| `KONTAN_PUSAT_DATA_TIMEOUT_SECONDS`           | Global timeout for Kontan Data load-more extraction. | `90` (internally converted to milliseconds). |
| `KONTAN_PUSAT_DATA_TIMEOUT_READ_SECONDS`      | Initial page-read timeout.                           | `60` (converted to milliseconds).            |
| `KONTAN_PUSAT_DATA_TIMEOUT_LOAD_NEXT_SECONDS` | Wait timeout after each load-more click.             | `10` (converted to milliseconds).            |
| `KONTAN_PUSAT_DATA_MAX_CLICK_ITERATION`       | Maximum load-more click iterations.                  | `30`                                         |


## 5. IDX Scraper Endpoints


| Variable         | Description                                 | Example / Notes                                                             |
| ---------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
| `IDX_BASE_URL`   | Base URL for IDX site and file downloads.   | `https://www.idx.co.id`                                                     |
| `IDX_PAGE_URL`   | IDX listing page URL for financial reports. | `https://www.idx.co.id/id/perusahaan-tercatat/laporan-keuangan-dan-tahunan` |
| `IDX_VALID_PATH` | Required path segment for URL validation.   | `/id/perusahaan-tercatat/laporan-keuangan-dan-tahunan`                      |
| `IDX_API_URL`    | IDX API endpoint for report search.         | `https://www.idx.co.id/primary/ListedCompany/GetFinancialReport`            |


## 6. Extraction Prompt Defaults


| Variable        | Description                                                      | Example / Notes                         |
| --------------- | ---------------------------------------------------------------- | --------------------------------------- |
| `SUMMARY_QUERY` | Query used when requesting keypoint summaries from Smart Search. | `Kesimpulan dalam **Bahasa Indonesia**` |


## 7. Quick Notes

- The Extraction Layer reads environment values at startup via `load_dotenv()`.
- Several timeout variables are parsed as integers/floats; invalid values will fall back to code defaults.
- Keep credentials (`*_TOKEN`, `*_SECRET`) in secret manager for production deployments.
