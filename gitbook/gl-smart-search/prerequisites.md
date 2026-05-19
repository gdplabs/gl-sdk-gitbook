---
icon: circle-exclamation
---

# Prerequisites

Before you begin using GL Smart Search SDK, ensure you have the following prerequisites in place.

{% stepper %}
{% step color="blue" %}
#### Python 3.11+

Make sure you have [Python](https://www.python.org/) version 3.11 or later installed. We recommend installing version 3.12 at the time of writing. Use this to verify you have the right version.

```bash
python --version

# Python 3.12.3
```

or

```bash
python3 --version

# Python 3.12.3
```
{% endstep %}

{% step color="blue" %}
#### Package Manager

Install the GL Smart Search SDK using pip:

```bash
pip install smart-search-sdk
```

Alternatively, you can use other package managers:
- [Poetry](https://python-poetry.org/) (recommended for Python projects)
- [uv](https://github.com/astral-sh/uv) (fast Python package installer)
{% endstep %}

{% step color="blue" %}
#### GL Smart Search Credentials

{% hint style="info" %}
Generate your GL Smart Search Token by following the instructions in [Authentication](guides/authentication.md "mention").
{% endhint %}

To use GL Smart Search SDK (be it the SDK, MCP Server, or CLI), you will need to obtain the GL Smart Search credentials first. Afterwards, you can use it as environment variables. In general, you will need the following:

* **GL Smart Search Base URL** – The API endpoint for GL Smart Search service (Production: `https://search.glair.ai/`)
* **GL Smart Search Token** – Your authentication token for accessing GL Smart Search API

Once obtained, store it securely and set it as an environment variable:

```bash
export SMARTSEARCH_BASE_URL="https://search.glair.ai/"
export SMARTSEARCH_TOKEN="your-access-token"
```
{% endstep %}
{% endstepper %}
