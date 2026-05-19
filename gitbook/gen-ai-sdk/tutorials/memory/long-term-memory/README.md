---
icon: memory
---

# Long-Term Memory

## Introduction

GLLM Memory is a flexible and extensible memory system for AI Agents with [Mem0 Platform](https://docs.mem0.ai/introduction) integration. It's designed to provide a robust foundation for building AI applications that can remember and retrieve information.

## Installation

<details>

<summary>Prerequisites</summary>

Before installing, make sure you have:

1. [Python 3.11+](https://glair.gitbook.io/hello-world/prerequisites#python-v3.11-or-v3.12)
2. [Pip](https://pip.pypa.io/en/stable/installation/) or [Poetry](https://python-poetry.org/docs/)
3. Mem0 Platform Credentials
   1. [API Key](https://app.mem0.ai/dashboard/api-keys) — after logging in to the Mem0 console, you can create an API key from the menu on the left.
4. [gcloud CLI](https://cloud.google.com/sdk/docs/install) — required because `gllm-memory` is a private library hosted in a private Google Cloud repository.

After installing, please run

```bash
gcloud auth login
```

to authorize gcloud to access the Cloud Platform with Google user credentials.

{% hint style="info" %}
Our internal `gllm-memory` package is hosted in a secure Google Cloud Artifact Registry.\
You need to authenticate via `gcloud CLI` to access and download the package during installation.
{% endhint %}

</details>

{% tabs %}
{% tab title="Install with pip" %}
Run the following command to install

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-memory"
```
{% endtab %}

{% tab title="Install with poetry" %}
**Step 1**: Add the `gen-ai-internal` source to your `pyproject.toml`

```bash
poetry source add gen-ai-internal "https://asia-southeast2-python.pkg.dev/gdp-labs/gen-ai-internal/simple/" --priority supplemental
```

**Step 2**: Configure the authentication

```bash
poetry config http-basic.gen-ai-internal oauth2accesstoken "$(gcloud auth print-access-token)"
```

**Step 3**: Add to projects

```bash
poetry add "gllm-memory[mem0ai]"
```
{% endtab %}
{% endtabs %}

## Environment Setup

Set a Mem0 platform API key as an environment variable.

{% hint style="info" %}
**Get a Mem0 API key from** [**Mem0 console**](https://app.mem0.ai/dashboard/api-keys)**.**
{% endhint %}

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
export MEM0_API_KEY="m0-..."
```
{% endtab %}

{% tab title="Windows Powershell" %}
```bash
$env:MEM0_API_KEY = "m0-..."
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
set MEM0_API_KEY="m0-..."
```
{% endtab %}
{% endtabs %}

## Core Methods

[**Init Memory**](init-memory.md) — Start the memory client. Use this first.

[**Add Memory**](add-memory.md) — Save a new memory item for a user or agent.

[Search Memory](search-memory.md) — Find and return the most relevant memories for a query.

[List Memory](list-memories.md) — Get memories based on the provided parameters.

[Delete Memory](delete-memories.md) — Deletes multiple memories based on the provided parameters.

[**Delete Memory by User Query**](delete-memory-by-user-query.md) — Remove memories that match a query.
