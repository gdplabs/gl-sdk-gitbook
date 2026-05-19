---
icon: user-robot
---

# Observability Agent

The GL Observability team has developed an agent to assist in the debugging process. This agent can retrieve information from observability tools such as Sentry, ELK/OpenSearch, and Prometheus. It processes the data to provide suggestions for fixing bugs.

## Observability Tools Support

This agent support debugging analysis from the following observability tools:

1. Sentry.
2. ELK/OpenSearch.
3. Prometheus.

On default, the agent will try to get all information from all tools for complete analysis. You can ask the agent to only do analysis on some tools only. To do that, you had to explicitly state that to the agent.

## Current Limitation

* Only connected to Sentry on-premise ([https://sentry.obrol.id](https://sentry.obrol.id)) but can be changed on the configuration.
* Must provide complete information for each observability tools. Some of the value can be found on the project's environment documentation.
  * **Sentry**
    * Project name/ID
    * An Issue ID, a Trace ID, or a Span attribute name and its value
  * **OpenSearch**
    * Index pattern
    * Specify one of the following fields and its value to filter the search: `kubernetes.namespace`, `kubernetes.deployment.name`, or `kubernetes.container.name`.
  * **ELK**
    * Data views name or index pattern.
    * Specify one of the following fields and its value to filter the search: `kubernetes.namespace`, `kubernetes.deployment.name`, or `kubernetes.container.name`.
  * **Prometheus**
    * Cluster
    * Namespace

## How to Use

This section will explain to you how to use the agent for debugging.

1. Go to [**Claudia**](https://claudia.catapa.com/).
2.  Change the application to **General Purpose**

    <figure><img src="../../../.gitbook/assets/Screenshot 2026-01-19 at 20.05.54.png" alt=""><figcaption></figcaption></figure>
3.  Open **More Agents** menu and search for **Observability Agent**.

    <figure><img src="../../../.gitbook/assets/Screenshot 2026-01-19 at 20.07.08.png" alt=""><figcaption></figcaption></figure>
4.  Provide details about the error to the agent. This information can come from a Sentry error event email notification or the Sentry Issues page.

    <figure><img src="../../../.gitbook/assets/Screenshot 2026-01-19 at 20.34.36.png" alt=""><figcaption></figcaption></figure>
5.  If the information is not complete, the agent might ask for more information. Provide all necessary information required by the agent so it can continue the process.

    <figure><img src="../../../.gitbook/assets/Screenshot 2026-01-19 at 20.50.59.png" alt=""><figcaption></figcaption></figure>
6.  The agent will analyze the received information and suggest a fix for the error. The full conversation example can be found [here](https://claudia.catapa.com/c/shared/069eacc7-e921-4900-825b-83b26d8395c5). The screenshot below shows a section of the response.

    <figure><img src="../../../.gitbook/assets/Screenshot 2026-01-19 at 21.03.14.png" alt="" width="563"><figcaption></figcaption></figure>

## Example Prompt

This is an example prompt containing all the required information for debugging on all observability tools.

```
Help me fix an error in my project. Here is the information about the error on Sentry:
- Project: <PROJECT_NAME>
- Event ID: <ISSUE_EVENT_ID>

OpenSearch:
- Index pattern: <OPENSEARCH_INDEX_PATTERN>
- kubernetes namespace: <OPENSEARCH_KUBERNETES_NAMESPACE_FIELD_VALUE>

ELK:
- Data View: <ELK_DATA_VIEWS>
- kubernetes namespace: <ELK_KUBERNETES_NAMESPACE_FIELD_VALUE>

Prometheus:
- Cluster: <PROMETHEUS_CLUSTER>
- Namespace: <PROMETHEUS_NAMESPACE>
```

This is an example prompt instructing the agent to only analyze Sentry data.

```
Help me fix an error in my project. Here is the information about the error on Sentry:
- Project: <PROJECT_NAME>
- Event ID: <ISSUE_EVENT_ID>
Only do analysis on Sentry.
```

## Tips

1. Please provide all relevant information at the start of the conversation to ensure you receive the most accurate response.
2. Limit the analysis time range to a narrow window to reduce agent hallucination. Maybe maximum one minute around the incident.

## Have Questions?

For further questions, please contact the [GL Observability Team](mailto:bosa-eng@gdplabs.id).
