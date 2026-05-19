# Sequence Diagram: Listing Process

### Orchestration Layer: Listing Orchestration Flow (URL Discovery Lifecycle)

This subsection describes orchestration behavior (job lifecycle, checkpointing, and status transitions), not extraction implementation details.

When a scheduled listing task is triggered for a source and date range, the Orchestration Layer in GL Smart Crawl starts URL discovery by creating or resuming listing jobs per target date. For each job, it processes listing pages sequentially and calls the Extraction Layer via `/extract-urls` to retrieve discovered URLs and pagination metadata (`page`, `max_page`). After each page, the Orchestration Layer stores discovered URLs incrementally and updates checkpoint/progress fields (for example `current_page`, `total_pages`, `urls_found`, and `urls_stored`) so interrupted runs can resume from the last processed state. At the end of each listing job, status is finalized as `COMPLETED` when coverage is sufficient, or `FAILED` when the run is partial and requires retry/resume.

```mermaid
sequenceDiagram
    autonumber

    participant Scheduler as Scheduler
    participant Orchestration as Orchestration Layer
    participant Extraction as Extraction Layer
    participant Search as GL Smart Search

    Scheduler->>Orchestration: Trigger scheduled listing task {source, start_date, end_date}
    Orchestration->>Orchestration: Create or resume listing jobs per target date

    loop For each listing job (date)
        Orchestration->>Orchestration: Mark job IN_PROGRESS and load checkpoint

        loop For each listing page
            Orchestration->>Extraction: Extract URLs from listing page
            Extraction->>Search: Execute URL extraction request
            Search-->>Extraction: {urls, page, max_page}
            Extraction-->>Orchestration: {urls, page, max_page}
            Orchestration->>Orchestration: Store discovered URLs incrementally
            Orchestration->>Orchestration: Update progress {current_page, total_pages, urls_found, urls_stored}
        end

        alt Coverage sufficient
            Orchestration->>Orchestration: Mark job COMPLETED
        else Partial or interrupted run
            Orchestration->>Orchestration: Mark job FAILED (retry/resume)
        end
    end

    Orchestration-->>Scheduler: Return listing summary {pages_crawled, urls_found, urls_stored, status}
```
