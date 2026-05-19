---
hidden: true
icon: compass-drafting
---

# backup-design-pattern

This section outlines the design pattern useful for integration solutions. The design and implementation pattern acts as a blueprint, providing a structured approach that ensures consistency, reliability, and efficiency in integration processes.

## Overview

Deep Research consists of multi-stage information synthesis capability that transforms complex queries into comprehensive, evidence-based reports. Implementation strategies vary based on:

1. **Data sources**:
   1. External internet data,
   2. internal intranet data, or
   3. Both
2. **Service provider**:
   1. Proprietary external service, or
   2. self-managed orchestration
3. **Customization level**:
   1. Pre-built components, or
   2. Fully customized pipeline.

The SDK provides modular components and patterns to support all combinations. Selection depends on data isolation requirements, control needs, and operational complexity tolerance.

## Core Design Pattern

### Structure

<figure><img src="../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>

Generally, at its core, a deep researcher utilizes a modular approach, consisting of several agents/components each serving a distinct role in the **research process**:

1. **Planner**: Decompose query into research tasks; generate tasks.
2. **Researcher**: Execute tasks via connectors and internet APIs.
3. **Evaluator**: Assess evidence quality, filter sources, rank by credibility.
4. **Synthesizer**: Aggregate evidence, resolve conflicts, generate narrative.
5. **Reporter**: Format output, apply templates, generate citations.
6. **Orchestrator:**
   1. Controls pipeline execution flow.
   2. Manages state and data passing between stages.
   3. Routes data to appropriate agents.

This is useful when modifying an existing deep researcher service or building one from scratch.

### Capabilities

In the outlined process, each research process typically incorporates the following capabilities:

1. **MCP Servers**: These handle private and enterprise data securely, ensuring efficient data management.
2. **Function / Tool Calling**: This involves utilizing various functions or tools to perform specific tasks within the process.
3. **External APIs**: Accessing internet-based APIs to gather additional data or services that are not internally available.
4. **Internal APIs**: Utilizing intranet-based APIs for accessing internal resources and services.
5. **Document Fetchers & Data Tools**: Implementing tools for retrieving documents and processing data effectively.

{% hint style="info" %}
[Broken link](/broken/pages/ficVWztvNF56kw3j5qDG "mention") provides a unified integration platform for implementing these capabilities.
{% endhint %}

## Implementation Patterns

Five distinct implementation patterns address different requirements as described below, sorted by customization level:

### 1. Proprietary Service + External Data Only

**Goal**: Rapid deployment with minimal operational overhead for internet-only research\
**Data sources**: Internet only\
**Service provider**: External proprietary service\
**Research process customization**: Not available

**Research process composition**:

The external **proprietary service orchestrates the entire research process** internally. The researcher agent executes tasks and compiles sources from the internet.

**Implementation references:**

1. [deep-research-in-a-pipeline-with-routing.md](guides/compose-a-deep-research-flow/deep-research-in-a-pipeline-with-routing.md "mention")

***

### 2. Proprietary Service + External & Internal Data

**Goal**: Leverage proprietary reasoning while integrating internal data sources for comprehensive research\
**Data sources**: Internet + intranet (internal data via connectors)\
**Service provider**: External proprietary service\
**Research process customization**: Not available

**Research process composition**:

1. **Orchestrator**: The external **proprietary service orchestrates the entire research process** internally.
2. **Researcher**: The access for intranet data can be provided to the service by (but not limited to):
   1. Using a provider supported connectors.
   2. Compiling the internal data via RAG outside the orchestrator via a customized pipeline.

**Implementation references**:

1. For provider supported connectors:
   1. [deep-research-pipeline-with-google-drive-connector.md](guides/compose-a-deep-research-flow/deep-research-pipeline-with-google-drive-connector.md "mention")
   2. [agentic-tools-and-model-context-protocol-mcp](../gl-connectors/sdk/agentic-tools-and-model-context-protocol-mcp/ "mention")
   3. [lm-invoker](../gen-ai-sdk/tutorials/inference/lm-invoker/ "mention") > [mcp-connector.md](../gen-ai-sdk/tutorials/inference/lm-invoker/mcp-connector.md "mention")
2. Customize a pipeline:
   1. [your-first-rag-pipeline.md](../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md "mention")
   2. [orchestration](../gen-ai-sdk/tutorials/orchestration/ "mention")

***

### 3. Self-Managed Service

**Goal**: Data control & compliance, possible orchestration customization, predictable cost\
**Data sources**: Internet and intranet (optional)\
**Service provider**: Self-managed (e.g. Tongyi and other self-managed profile in [GLOpenDeepResearcher](https://gdplabs.gitbook.io/gl-open-deepresearch))\
**Research process customization**: Available (subject to the capabilities and limitations of the underlying open-source framework)

**Research process composition:**

1. **Orchestrator**: The **self-managed service orchestrates the entire research process internally**.
2. **Researcher**: Intranet data may be provided to the researcher as a result of open source component modification in [GLOpenDeepResearcher](https://gdplabs.gitbook.io/gl-open-deepresearch).

{% hint style="info" %}
Other customization in research process can be implemented as needed through modification of open-source components.
{% endhint %}

**Implementation references**:

1. [GL Open DeepResearch Profile customization](https://gdplabs.gitbook.io/gl-open-deepresearch/api-contract/api-profiles)
2. [Integrate deep research to internal document in GL Open DeepResearch](https://gdplabs.gitbook.io/gl-open-deepresearch/developers-guide/examples/deep-research-to-internal-documents#consume-use-the-sdk-with-the-internal-profile)

***

### 4. Hybrid Orchestration (Proprietary + Self-Managed)

**Goal**: Combine proprietary service reasoning with self-managed orchestration for advanced scenarios requiring both speed and transparency\
**Data sources**: Internet + intranet (optional)\
**Service provider**: Proprietary + self-managed\
**Research process customization**: Available for self-managed service (see [#id-3.-self-managed-service](backup-design-pattern.md#id-3.-self-managed-service "mention"))

**Research process composition**:

1. **Orchestrator**: May consist of two orchestrators, proprietary builtin orchestrator and self managed service, which orchestrates the entire research process internally.
2. **Reporter**: Externally merge results from both orchestrators; generate unified report.

**Implementation References**:

1. [#id-1.-proprietary-service--external-data-only](backup-design-pattern.md#id-1.-proprietary-service--external-data-only "mention")
2. [#id-2.-proprietary-service--external-and-internal-data](backup-design-pattern.md#id-2.-proprietary-service--external-and-internal-data "mention")
3. [#id-3.-self-managed-service](backup-design-pattern.md#id-3.-self-managed-service "mention")

***

### 5. Fully Custom Deep Research Pipeline

**Goal**: Build specialized Deep Research pipeline from scratch for domain-specific requirements with complete control and customization\
**Data sources**: Custom-defined (internet/intranet)\
**Service provider**: Custom-defined

Build custom deep reserach pipeline from scratch for specialized requirements with full control over orchestration and execution. When customizing, refer to the [#core-design-pattern](backup-design-pattern.md#core-design-pattern "mention") for the research process composition.

**Research process composition:**

1. **Orchestrator**: Custom agent-based orchestration (no pre-built components).
2. **Planner**: Define custom logic to decompose query into research tasks.
3. **Researcher**: Implement custom execution via arbitrary data sources (APIs, databases, knowledge graphs, connectors).
4. **Evaluator**: Implement specialized evidence quality assessment and source ranking.
5. **Synthesizer**: Implement custom aggregation, conflict resolution, and narrative generation strategies.
6. **Reporter**: Implement custom output formatting and citation generation.

**Implementation references**:

1. Pipeline building
   1. [build-end-to-end-rag-pipeline](../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/ "mention")
   2. [orchestration](../gen-ai-sdk/tutorials/orchestration/ "mention")
2. Agent building
   1. [Creating custom agents](https://gdplabs.gitbook.io/sdk/gl-aip/guides/agents-guide)
3. Deep research related capabilities and integration options
   1. [Broken link](/broken/pages/ficVWztvNF56kw3j5qDG "mention")

## Next Steps

1. Install prerequisites in [prerequisites.md](prerequisites.md "mention")
2. Get started with Deep Researcher components: [getting-started.md](getting-started.md "mention")
