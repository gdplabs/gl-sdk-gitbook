---
icon: lightbulb-on
cover: https://gitbookio.github.io/onboarding-template-images/header.png
coverY: 0
---

# Introduction to GL Smart Crawl

**GL Smart Crawl** is a unified web crawling platform that automates the discovery, extraction, and storage of structured content from the web. It uses a two-layer architecture that separates orchestration from extraction execution, enabling reliable, scalable, and fault-tolerant crawling pipelines for news articles, real estate listings, and financial reports.

***

## System Layers

GL Smart Crawl consists of two complementary internal layers:

**Orchestration Layer** (`applications/smart-crawl`) — manages the full crawl lifecycle:

* Schedules and triggers listing jobs per source on configurable cron schedules
* Coordinates the two-phase pipeline: URL discovery (listing) then content extraction (scraping)
* Stores crawled data in PostgreSQL and Elasticsearch
* Exposes a Data API for downstream consumers with pagination, filtering, and source integrity metadata
* Implements bi-directional scraping pointers for reliable chronological data coverage

**Extraction Layer** (`applications/custom-scrapers`) — executes URL and content extraction:

* Provides domain-specific scrapers for news portals, property listing sites, and IDX financial reports
* Extracts structured metadata, article content, and property details from HTML pages
* Discovers paginated URLs from listing pages for the Orchestration Layer to process
* Falls back to GL Smart Search (Firecrawl-powered) for anti-bot protected sites
* Uses Playwright for JavaScript-heavy dynamic pages

***

## Key Features

**Automated Scheduling** – Per-source cron jobs handle listing and scraping automatically. Failed runs retry on the next scheduled tick without manual intervention.

**Two-Phase Pipeline** – Listing (URL discovery) and scraping (content extraction) run as separate phases, giving operational visibility into each stage independently.

**Data Integrity** – FIFO scraping with bi-directional pointers ensures oldest-first chronological ordering. Source integrity metadata in every API response shows coverage, freshness, and backlog per source.

**Multi-Source Support** – Supports 8 article sources (CNN Indonesia, CNBC Indonesia, Bloomberg Technoz, Bisnis, Kontan, MetroTV, Google News, Forex Factory) and 4 property sources (Rumah123, OLX, Lamudi, 99.co).

**Fault Tolerant** – Incremental URL saving preserves partial progress on listing failures. Failed scrapes are isolated per URL and do not halt the batch.

**Elasticsearch Integration** – Crawled articles are migrated to Elasticsearch for full-text search with keyword queries across sources and date ranges.

***

## Get Started

1. [**Prerequisites**](prerequisites.md) – Set up your environment and dependencies
2. [**Getting Started**](getting-started.md) – Run your first crawl and retrieve data
3. [**Guides**](guides/) – Explore the Data API and scheduler operations
