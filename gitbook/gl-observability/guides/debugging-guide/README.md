---
icon: bug
---

# Debugging

Our organization use Sentry for tracing; OpenSearch and ELK for logging; and Prometheus for metrics monitoring. This guide provides tutorials and tips on using those observability tools to help debugging your project. By integrating these tools, businesses gain improved visibility into applications and infrastructure. They enable faster issue resolution, enhance performance monitoring, and provide insights to optimize operations.

## Sentry

Sentry provides real-time error tracking and crash reports for your applications. It enables developers to diagnose and fix issues faster by offering detailed stack traces, contextual information, and user impact insights. For a comprehensive guide on using Sentry, please visit the [sentry](sentry/ "mention") tutorial.

## OpenSearch <a href="#elk-stack-elasticsearch-logstash-kibana-opensearch" id="elk-stack-elasticsearch-logstash-kibana-opensearch"></a>

OpenSearch is our current standard for log management. It is an open-source fork of Elasticsearch and Kibana. It collects logs and events data from various sources, processes it, and visualizes the data, allowing for comprehensive analysis.

* **OpenSearch** stores and indexes log data for fast search and retrieval — functionally equivalent to Elasticsearch.
* **OpenSearch Dashboards** visualizes and analyzes logs in an intuitive UI — the OpenSearch equivalent of Kibana.
* **Data Prepper** (or Logstash) processes and transforms incoming data before ingestion.

For a comprehensive guide on using OpenSearch, please visit the [opensearch.md](opensearch.md "mention") tutorial.

## ELK Stack <a href="#elk-stack-elasticsearch-logstash-kibana-opensearch" id="elk-stack-elasticsearch-logstash-kibana-opensearch"></a>

The ELK Stack is a powerful log management solution. Similar to OpenSearch, it collects logs and events data from various sources, processes it, and visualizes the data, allowing for comprehensive analysis:

* **Elasticsearch** stores and indexes log data for fast search and retrieval.
* **Logstash** processes and transforms incoming data.
* **Kibana** visualizes and analyzes the logs in an intuitive user interface.

For a comprehensive guide on using ELK, please visit the [elk.md](elk.md "mention") tutorial.

## Prometheus

Prometheus is a robust metrics monitoring system. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays results, and triggers alerts:

* **Data Collection**: Prometheus gathers data by scraping HTTP endpoints.
* **Data Storage**: It stores metric data using a time-series database.
* **Alerting**: Configurable alerting rules to notify users about potential issues.

For a comprehensive guide on using Prometheus, please visit the [prometheus.md](prometheus.md "mention") tutorial.
