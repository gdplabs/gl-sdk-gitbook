---
icon: globe-pointer
---

# Introduction to GL Browser Use

**GL Browser Use** is a typed Python SDK for running browser automation tasks through [`browser-use`](https://github.com/browser-use/browser-use). It gives application code a stable client facade, structured stream events, explicit run results, bounded retries for recoverable browser-session failures, and optional integrations for hosted browser infrastructure and session recordings.

Use GL Browser Use when you want an LLM-powered agent to operate a browser for tasks such as opening websites, gathering information from pages, filling forms, checking web workflows, or producing an auditable trace of a browser run.

## Key Features

**Typed client API**: Run browser tasks with `BrowserUseClient` using streaming, async one-shot, or synchronous methods.

**Structured events**: Consume progress, thinking/activity updates, tool-call summaries, streaming URLs, recording URLs, and terminal errors through `BrowserUseStreamEvent`.

**Explicit results**: Inspect status, final output, session IDs, browser streaming links, recording links, step counts, errors, and metadata through `BrowserUseRunResult`.

**Optional hosted browser sessions**: Use `SteelBrowserInfrastructure` when you want a remote browser session with CDP and streaming URLs.

**Optional recording storage**: Use `MinIOS3CompatibleStorage` to upload Steel session recordings to MinIO or an S3-compatible object store and return presigned URLs.

**Recoverable session retries**: Retry only classified browser-session failures, such as browser closure or websocket disconnects, with a bounded retry count.

## Get Started

1. [**Prerequisites**](prerequisites.md): Prepare Python, model credentials, and optional provider credentials.
2. [**Getting Started**](getting-started.md): Run your first browser automation task.
3. [**Guides**](guides/): Learn streaming, recordings, and production usage patterns.
4. [**Resources**](resources/): Review the SDK reference and runtime contracts.
