---
icon: list-timeline
---

# Sentry

Sentry is an application monitoring platform designed primarily for tracing and error tracking. It can help developers to find, diagnose, and fix issues in their software code. Sentry provides a comprehensive dashboard for data analysis, allowing teams to gain insights into application performance and error trends.

## Key Features in Sentry for Debugging

* **Real-Time Error Tracking**: Instant notifications about exceptions and errors with detailed contextual information.
* **Stack Trace**: Provides insights into the sequence of events leading up to an error to identify the root cause.
* **Breadcrumb Trails**: Captures and displays the sequence of events leading up to an error, offering a clear chronological context.

## Glossary

* **Trace**: Represents the full path of a single request, from start to finish, across all connected services in your system. It contains multiple spans.
* **Span**: A single unit of work within a trace, representing an operation like a function call or a database request.
* **Event**: Any notable occurrence in the application, like an error or a relevant transaction. Events are central to Sentry’s operations and help track application state changes.

## How to Setup

Check out the [quickstart.md](../../traces/quickstart.md "mention") page to learn how to setup python project to send traces data into Sentry.

## Sections

This guide will cover Sentry features that helpful in debugging code.

{% columns %}
{% column %}
{% content-ref url="issues.md" %}
[issues.md](issues.md)
{% endcontent-ref %}

{% content-ref url="discover.md" %}
[discover.md](discover.md)
{% endcontent-ref %}

{% content-ref url="data-scrubbing.md" %}
[data-scrubbing.md](data-scrubbing.md)
{% endcontent-ref %}


{% endcolumn %}

{% column %}
{% content-ref url="traces.md" %}
[traces.md](traces.md)
{% endcontent-ref %}

{% content-ref url="session-replays.md" %}
[session-replays.md](session-replays.md)
{% endcontent-ref %}


{% endcolumn %}
{% endcolumns %}
