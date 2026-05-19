---
icon: yin-yang
---

# OpenSearch

At GDP Labs, we leverage the OpenSearch for storing and visualizing logs data.

## Glossary

1. **DQL/Lucene**: Query languages for flexible log searching.
2. **Index Pattern**: String expression that defines which indices to be accessed and visualized

## Prerequisites

1. Ensure you have access to OpenSearch and the relevant index pattern.
2. Know the impacted application/service, environment (production/staging), and an approximate timeframe for the incident.

## Workflow: Investigating Application Log Incidents <a href="#docs-internal-guid-1468889e-7fff-3377-2f65-689fbc542bb4" id="docs-internal-guid-1468889e-7fff-3377-2f65-689fbc542bb4"></a>

1. **Identify the Incident Scope**\
   Determine the affected application/system, environment (production/staging), and time window.
2.  **Select Index Pattern**\
    Select the appropriate index pattern to specify which data sources and indices you want to query. Focus on the relevant environment—e.g., choose `gdplabs-eks-production-*` for production issues.

    <figure><img src="../../../.gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>
3. **Set the Time Range**: Filter by Incident Period
   1. Use the time picker to narrow the query to the timeframe of the incident.
   2.  Choose between relative dates (e.g., Last 24 hours) or absolute values (specific start/end).

       <figure><img src="../../../.gitbook/assets/image (32).png" alt="" width="365"><figcaption></figcaption></figure>

       <figure><img src="../../../.gitbook/assets/image (34).png" alt="" width="365"><figcaption></figcaption></figure>
   3. The calendar icon and time settings make it easy to specify the precise timeframe when the incident occurred.
4. **Field-Based Filtering**: Customize the Log View
   1. Use the list of fields in the left sidebar to view all available log fields.
   2.  Select or deselect fields you want to display, such as `message`, `kubernetes.namespace`, `kubernetes.container.name`, etc.<br>

       <figure><img src="../../../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>
   3. The field selection panel separates popular fields from all available fields for easy navigation and discovery.
5. **Apply Filters**: Precise Log Selection
   1. Add filters to focus your search (e.g., by namespace, pod, or error type).
   2.  Use operators like `is`, `exists`, or `one of`.

       <figure><img src="../../../.gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>
   3. The add filter interface allows you to set filter operators such as `is`, `is not`, `is one of`, `exists`, and `does not exist`.
6. **Advanced Querying**: Using DQL or Lucene
   1. For more complex searches, use Dashboard Query Language (DQL) or Lucene.
   2. Example DQL queries:
      1.  Error logs in production

          ```
          kubernetes.namespace: "production" and log.level: "error"
          ```
      2.  Logs by trace or pod

          ```
          trace.id: "abcd1234"
          ```
      3.  Search log messages for “timeout”

          ```
          message: "timeout"
          ```
   3.  Switch between DQL and Lucene as needed. This can be switched on search bar.

       <figure><img src="../../../.gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>
7. **Analyze Log Volume Trends (Bar Chart)**
   1. Use the vertical bar chart to see log activity over time.
   2.  Click bars to zoom in on peak times or anomalies for deeper analysis.

       <figure><img src="../../../.gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>
8. **Review Log List**
   1. The Documents tab displays all log entries sorted by `@timestamp` .
   2.  Scan for errors, warnings, or notable events around the incident.

       <figure><img src="../../../.gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>
9. **Inspect Log Details**
   1. Click any log entry to see a detailed breakdown in table or JSON view.
   2.  Check for context such as error codes, deployment info, container, pod, user agent, etc.

       <figure><img src="../../../.gitbook/assets/image (42).png" alt=""><figcaption></figcaption></figure>

       <figure><img src="../../../.gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>

## Share Discovery Search Query <a href="#troubleshooting-when-logs-dont-appear" id="troubleshooting-when-logs-dont-appear"></a>

Follow these steps to share a search query to other people:

1.  On the Discover page, create a new query by clicking the **New** button on the top right corner.

    <figure><img src="../../../.gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>
2. Write the query on the search bar.
3.  Save the query by clicking the **Save** button. Set a title for the saved query.

    <figure><img src="../../../.gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>
4.  Click the **Share** button, choose to generate the link as **Snapshot**, and click **Copy link**. Share the copied link.

    <figure><img src="../../../.gitbook/assets/image (48).png" alt=""><figcaption></figcaption></figure>
5.  Another option is to share the title and load the saved query by clicking the **Open** button.

    <figure><img src="../../../.gitbook/assets/image (47).png" alt="" width="563"><figcaption></figcaption></figure>

## Troubleshooting: When Logs Don’t Appear <a href="#troubleshooting-when-logs-dont-appear" id="troubleshooting-when-logs-dont-appear"></a>

1. Double-check the time range, especially when switching between "Relative" and "Absolute" mode.
2. Confirm the correct index pattern is selected.
3. Loosen filters if too few logs appear; make them stricter if there are too many.
4. Check for typos or syntax errors in your DQL/Lucene queries.
5. Ensure you have permission to view the relevant index pattern.

## Best Practices for Incident Log Analysis <a href="#best-practices-for-incident-log-analysis" id="best-practices-for-incident-log-analysis"></a>

1. Start with broad time and filter scopes, then refine as you spot patterns.
2. Combine field-based filters and search queries for the most accurate results.
3. Always expand individual log entries for full context.
4. Use export/share features to collaborate (if supported in your platform).
5. Correlate log findings with other observability tools (traces, metrics, APM) if available. Search by `otelTraceID` field to find logs from a specific OpenTelemetry trace, or search by `otelSpanID` to find logs from a specific span

## Quick-Reference Table: Common Log Fields <a href="#docs-internal-guid-e1a6faac-7fff-83a4-5589-3afd5e9aaaef" id="docs-internal-guid-e1a6faac-7fff-83a4-5589-3afd5e9aaaef"></a>

Below is a quick-reference table detailing the common log fields and their descriptions.

| Field                       | Description                               |
| --------------------------- | ----------------------------------------- |
| `@timestamp`                | The date and time the event occurred      |
| `message`                   | The main log message                      |
| `log.level`                 | Log severity level (info, error, etc.)    |
| `kubernetes.container.name` | Name of the Docker/Kubernetes container   |
| `kubernetes.namespace`      | Kubernetes namespace                      |
| `kubernetes.pod.name`       | Kubernetes pod name                       |
| `agent.type`                | Log collector agent type (e.g., filebeat) |
| `otelTraceID`               | Trace ID associated with this log entry   |
| `otelSpanID`                | Span ID associated with this log entry    |

## Example Walkthrough <a href="#example-walkthrough" id="example-walkthrough"></a>

1. An incident occurs on a production service at 11:00.
2. Select `gdplabs-eks-production-*` index pattern.
3. Set the Absolute/Relative time range to cover around 11:00.
4. Filter logs with DQL: `log.level: "error"`
5. Click the spike in the bar chart around that time.
6. Review entries for error/warning patterns.
7. Expand specific entries for detailed context (trace ID, container, etc.).
