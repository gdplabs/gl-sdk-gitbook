---
icon: tv
---

# Prometheus

In GDP Labs, we use the Grafana stack with Prometheus as our main monitoring platform. This open-source software allows us to query, visualize, set alerts, and analyze metrics like CPU, Memory, Network, and Disk usage efficiently.

## Glossary

1. **Prometheus**: Open source systems monitoring toolkit that collects and stores metrics as time series data, with a multi-dimensional data model.
2. **Metric**: Numerical measurements in layperson terms.
3. **Alert**: Conditions based on Prometheus expression language expressions and to send notifications about firing alerts to an external service.
4. **Kubernetes**: Portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.
5. **Kubernetes Cluster**: Group of nodes running containerized applications, managed by a control plane, and includes one or more nodes with running pods.
6. **Kubernetes Namespace**: Isolating groups of resources within a single cluster.
7. **Kubernetes Workload**: Application running on Kubernetes, run inside a set of pods.
8. **Kubernetes Deployment**: Manages Pods for an application, usually without state.
9. **Kubernetes Statefulset**: Manage stateful applications.
10. **Kubernetes Pod**: Smallest deployable units.
11. **Kubernetes Node**: Virtual or physical machines where containers run in Pods.
12. **Memory Leak**: Memory limits are enforced by the kernel with out of memory (OOM) kills.
13. **Persistent Volume**: Piece of storage in the cluster that has been provisioned.

## Prerequisites

1. Web Browser (e.g., Google Chrome, Microsoft Edge, Mozilla, etc)
2. GDP Labs Google Account (@[gdplabs.id](http://gdplabs.id))

## Simple Walkthrough

1. Open [https://grafana-kube-explore.obrol.id/](https://grafana-kube-explore.obrol.id/)
2. Click **Sign in with Google**
3. Choose your **@gdplabs.id** google account
4. Now, you are ready to explore visualization and dashboard:
   1. [Kubernetes / Compute Resources / Namespace (Workloads) - Dashboards - Staging](https://grafana-kube-explore.obrol.id/d/a87fb0d919ec0ea5f6543124e16c42a5/kubernetes-compute-resources-namespace-workloads?orgId=1\&from=now-1h\&to=now\&timezone=Asia%2FJakarta\&var-datasource=default\&var-cluster=eks-gl-staging\&var-namespace=ai-agent-platform-stag\&var-type=$__all\&refresh=10s)
   2. [Kubernetes / Compute Resources / Namespace (Workloads) - Dashboards - Production](https://grafana-kube-explore.obrol.id/d/a87fb0d919ec0ea5f6543124e16c42a5/kubernetes-compute-resources-namespace-workloads?orgId=1\&from=now-1h\&to=now\&timezone=Asia%2FJakarta\&var-datasource=default\&var-cluster=eks-gl-production\&var-namespace=ai-agent-platform-prod\&var-type=$__all\&refresh=10s)

## Workflow: Investigating Memory Leak Issue

1.  **Identify the Incident Scope**

    Determine the affected application/system, environment (production/staging), and time window.
2.  **Select Relevant Dashboard**

    Open [**Kubernetes / Compute Resources / Namespace (Workloads) - Dashboards**](https://grafana-kube-explore.obrol.id/d/a87fb0d919ec0ea5f6543124e16c42a5/kubernetes-compute-resources-namespace-workloads?orgId=1\&from=now-1h\&to=now\&timezone=Asia%2FJakarta\&var-datasource=default\&var-cluster=eks-gl-production\&var-namespace=ai-agent-platform-prod\&var-type=$__all\&refresh=10s)**.** Focus on relevant applications or projects – e.g, choose “cluster: eks-gl-production , namespace: ai-agent-platform-prod” for AIP production issues.

    <figure><img src="../../../.gitbook/assets/unknown (59).png" alt=""><figcaption></figcaption></figure>
3. **Set the Time Range**: Filter by Incident Period
   1. Use the time picker to narrow the query to the timeframe of the incident.
   2.  Choose between relative dates (e.g., "Last 24 hours") or absolute values (specific start/end).

       <figure><img src="../../../.gitbook/assets/unknown (60).png" alt=""><figcaption></figcaption></figure>
4.  **Narrow to specific widgets group**

    <figure><img src="../../../.gitbook/assets/unknown (61).png" alt=""><figcaption><p>Since the above is just an example; it shows that AIP usage does not seem to be high beyond the limit.</p></figcaption></figure>

## Dashboard Usage Scenarios

Below is a list of dashboards you can use to investigating your app and its usage.

1. [Kubernetes / Compute Resources / Namespace (Workloads) - Dashboards](https://grafana-kube-explore.obrol.id/d/a87fb0d919ec0ea5f6543124e16c42a5/kubernetes-compute-resources-namespace-workloads?orgId=1\&from=now-1h\&to=now\&timezone=Asia%2FJakarta\&var-datasource=default\&var-cluster=eks-gl-production\&var-namespace=ai-agent-platform-prod\&var-type=$__all\&refresh=10s)
   1. Investigate application resource (CPU, Memory, Network) usage
   2. Application specific usage
   3.  Relevant when these kind of alerts showed up:

       <pre data-overflow="wrap"><code>✅ Alert: KubePodMemoryHigh-SEV1-Prod
       Details: Pod gl-connectors-prod/gl-connectors-api-worker-865f74786c-chrp8 (gl-connectors-api-worker) has been using more than 90% of its memory limit for the last 5 minutes on cluster eks-gl-production.
       </code></pre>
2. [Kubernetes / Compute Resources / Node (Pods) - Dashboards - Grafana](https://grafana-kube-explore.obrol.id/d/200ac8fdbfbb74b39aff88118e4d1c2c/kubernetes-compute-resources-node-pods?orgId=1\&from=now-1h\&to=now\&timezone=Asia%2FJakarta\&var-datasource=default\&var-cluster=eks-cluster-datasaur\&var-node=ip-172-27-1-104.ec2.internal\&refresh=10s)
   1. Investigate node resource (CPU, Memory, Network) usage
   2. Node to application specific usage
   3.  Relevant when these kind of alerts showed up:

       <pre data-overflow="wrap"><code>🔥 Alert: NodeCPUHighUsage-SEV2-nonProdCluster
       Details: CPU usage at 10.10.14.193:9100 has been above 90% for the last 10 minutes, is currently at 96.13%.
       </code></pre>
3. [Kubernetes Container Images - Apps - Dashboards - Grafana](https://grafana-kube-explore.obrol.id/d/e1f01b79-dc3c-4849-976f-1c9d77852bc9/kubernetes-container-images-apps?orgId=1\&from=now-15m\&to=now\&timezone=browser\&var-namespace=gen-ai-template-stag)
   1. Investigate which application version are deployed now
4. [Kubernetes / Persistent Volume - Dashboards - Grafana](https://grafana-kube-explore.obrol.id/d/919b92a8e8041bd567af9edab12c840c/kubernetes-persistent-volumes?orgId=1\&from=now-1h\&to=now\&timezone=Asia%2FJakarta\&var-datasource=default\&var-cluster=eks-cluster-datasaur\&var-namespace=gen-ai-template-dtsr\&var-volume=data-add-ons-rbmq-rabbitmq-0\&refresh=10s)
   1. Investigate application persistent volume usage
   2.  Relevant when these kind of alerts showed up:

       <pre data-overflow="wrap"><code>✅ Based on recent sampling, the PersistentVolume claimed by prometheus-prometheus-stack-kube-prom-prometheus-db-prometheus-prometheus-stack-kube-prom-prometheus-0 in Namespace kube-addons on Cluster eks-gl-staging is expected to fill up within four days. Currently 5.045% is available.
       </code></pre>

## Best Practices from Grafana <a href="#docs-internal-guid-b2f74e69-7fff-35d3-07f0-82e69c68771d" id="docs-internal-guid-b2f74e69-7fff-35d3-07f0-82e69c68771d"></a>

Grafana documentation provide some tutorial best practice how to use their app. Here is the tutorial for Grafana [dashboard](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/) and [alert](https://grafana.com/docs/grafana/latest/alerting/best-practices/).

## Quick-Reference Dashboard Filter <a href="#docs-internal-guid-72e893cb-7fff-b468-447d-b4e1915c38c2" id="docs-internal-guid-72e893cb-7fff-b468-447d-b4e1915c38c2"></a>

The dashboard features a filter bar at the top, enabling you to refine the data shown across all panels. Utilize these controls to focus on specific clusters, namespaces, or workloads and set the desired time range for your analysis. Each filter's description is detailed in the table below.

<figure><img src="../../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

| Filter          | Description                                                                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@timestamp`    | The date and time the metric collected                                                                                                                                                       |
| `cluster`       | Kubernetes cluster to inspect (e.g., eks-gl-production)                                                                                                                                      |
| `namespace`     | Kubernetes namespace to inspect (e.g., ai-agent-platform-prod)                                                                                                                               |
| `workload_type` | Workload type ([statefulset](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) or [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)) |
| `workload`      | Specific workload on particular namespace (e.g., ai-agent-platform-runner-worker)                                                                                                            |
