---
icon: rectangle-terminal
---

# ELK

{% hint style="info" %}
GDP Labs replaced logs storage from ELK to OpenSearch as of December 2025. OpenSearch guide can be found [here](opensearch.md). This section is maintained because CATAPA still uses ELK stack.
{% endhint %}

**ELK** stack (Elasticsearch, Logstash, and Kibana) within Elastic Cloud is used as our main observability platform for CATAPA. This cloud-based solution offers centralized log management and monitoring for our infrastructure.

## Glossary

1. **Data View**: A grouping or index of logs in Kibana.
2. **KQL/Lucene**: Query languages for flexible log searching.
3. **Logstash**: Middleware for log ingestion in the ELK stack.
4. **Bar Chart:** Visualizes log volume over time for easier analysis.

## Prerequisites

1. Ensure you have access to Elastic Cloud and the relevant Kibana data views.
2. Know the impacted application/service, environment (production/staging), and an approximate timeframe for the incident.

## Workflow: Investigating Application Log Incidents <a href="#docs-internal-guid-1468889e-7fff-3377-2f65-689fbc542bb4" id="docs-internal-guid-1468889e-7fff-3377-2f65-689fbc542bb4"></a>

1.  **Identify the Incident Scope**

    Determine the affected application/system, environment (production/staging), and time window.
2. **Select Data View**: Choose the Correct Source/Index
   1. In Elastic Cloud, select the appropriate data view to specify which data sources and indices you want to query.
   2.  Focus on the relevant environment—e.g., choose “GDP Labs EKS Production” for production issues.

       <figure><img src="../../../.gitbook/assets/unknown (69).png" alt=""><figcaption></figcaption></figure>
   3. Select the “GDP Labs EKS Production” data view from the dropdown to monitor the production environment. The “Data views” menu allows you to switch between environments like “GDP Labs EKS Production” and “GDP Labs EKS Staging.” Focus on key data by choosing “GDP Labs EKS Production” from the available data views.
3. **Set the Time Range**: Filter by Incident Period
   1. Use the time picker to narrow the query to the timeframe of the incident.
   2.  Choose between relative dates (e.g., Last 24 hours) or absolute values (specific start/end).

       <figure><img src="../../../.gitbook/assets/unknown (70).png" alt="" width="307"><figcaption></figcaption></figure>

       <figure><img src="../../../.gitbook/assets/unknown (71).png" alt="" width="298"><figcaption></figcaption></figure>
   3. The calendar icon and time settings make it easy to specify the precise timeframe when the incident occurred.
4. **Field-Based Filtering**: Customize the Log View
   1. Use the list of fields in the left sidebar to view all available log fields.
   2.  Select or deselect fields you want to display, such as `message`, `kubernetes.namespace`, `container.name`, etc.

       <figure><img src="../../../.gitbook/assets/unknown (74).png" alt=""><figcaption></figcaption></figure>
   3. The field selection panel separates popular fields from all available fields for easy navigation and discovery.
5. **Apply Filters**: Precise Log Selection
   1. Add filters to focus your search (e.g., by namespace, pod, or error type).
   2.  Use operators like `is`, `exists`, or `one of`.

       <figure><img src="../../../.gitbook/assets/unknown (34).png" alt=""><figcaption></figcaption></figure>
   3. The add filter interface allows you to set filter operators such as `is`, `is not`, `is one of`, `exists`, and `does not exist`.
6. **Advanced Querying**: Using KQL or Lucene
   1. For more complex searches, use Kibana Query Language (KQL) or Lucene syntax.
   2. Example KQL queries:
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
   3. Switch between KQL and Lucene as needed.
7. **Analyze Log Volume Trends (Bar Chart)**
   1. Use the vertical bar chart to see log activity over time.
   2.  Click bars to zoom in on peak times or anomalies for deeper analysis.

       <figure><img src="../../../.gitbook/assets/unknown (55).png" alt=""><figcaption></figcaption></figure>
8. **Review Log List**
   1. The Documents tab displays all log entries sorted by `@timestamp` .
   2.  Scan for errors, warnings, or notable events around the incident.

       <figure><img src="../../../.gitbook/assets/unknown (62).png" alt=""><figcaption></figcaption></figure>
9. **Inspect Log Details**
   1. Click any log entry to see a detailed breakdown in table or JSON view.
   2.  Check for context such as error codes, deployment info, container, pod, user agent, etc.

       <figure><img src="../../../.gitbook/assets/unknown (64).png" alt=""><figcaption></figcaption></figure>

       <figure><img src="../../../.gitbook/assets/unknown (54).png" alt=""><figcaption></figcaption></figure>
10. **Review Log and Field Statistics**
    1. Use the field statistics tool to quickly spot outliers, high cardinality fields, or trends.
    2.  Identify which fields are most relevant or show unusual values for this incident.

        <figure><img src="../../../.gitbook/assets/unknown (56).png" alt=""><figcaption></figcaption></figure>

## Troubleshooting: When Logs Don’t Appear

1. Double-check the time range, especially when switching between "Relative" and "Absolute" mode.
2. Confirm the correct data view/index is selected.
3. Loosen filters if too few logs appear; make them stricter if there are too many.
4. Check for typos or syntax errors in your KQL/Lucene queries.
5. Ensure you have permission to view the relevant logs/data views.

## Best Practices for Incident Log Analysis

1. Start with broad time and filter scopes, then refine as you spot patterns.
2. Combine field-based filters and search queries for the most accurate results.
3. Always expand individual log entries for full context.
4. Use export/share features to collaborate (if supported in your platform).
5. Correlate log findings with other observability tools (traces, metrics, APM) if available. Search by `otelTraceID` field to find logs from a specific OpenTelemetry trace, or search by `otelSpanID` to find logs from a specific span

## Quick-Reference Table: Common Log Fields <a href="#docs-internal-guid-e1a6faac-7fff-83a4-5589-3afd5e9aaaef" id="docs-internal-guid-e1a6faac-7fff-83a4-5589-3afd5e9aaaef"></a>

Below is a quick-reference table detailing the common log fields and their descriptions.

<table><thead><tr><th width="307">Field</th><th>Description</th></tr></thead><tbody><tr><td><code>@timestamp</code></td><td>The date and time the event occurred</td></tr><tr><td><code>message</code></td><td>The main log message</td></tr><tr><td><code>log.level</code></td><td>Log severity level (info, error, etc.)</td></tr><tr><td><code>container.name</code></td><td>Name of the Docker/Kubernetes container</td></tr><tr><td><code>kubernetes.namespace</code></td><td>Kubernetes namespace</td></tr><tr><td><code>kubernetes.pod.name</code></td><td>Kubernetes pod name</td></tr><tr><td><code>agent.type</code></td><td>Log collector agent type (e.g., filebeat)</td></tr><tr><td><code>otelTraceID</code></td><td>Trace ID associated with this log entry</td></tr><tr><td><code>otelSpanID</code></td><td>Span ID associated with this log entry</td></tr></tbody></table>

## Example Walkthrough

1. An incident occurs on a production service at 11:00.
2. Select “GDP Labs EKS Production” in Data Views.
3. Set the Absolute/Relative time range to cover around 11:00.
4. Filter logs with KQL: `log.level: "error"`
5. Click the spike in the bar chart around that time.
6. Review entries for error/warning patterns.
7. Expand specific entries for detailed context (trace ID, container, etc.).
