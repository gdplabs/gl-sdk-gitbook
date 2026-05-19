---
icon: circle-exclamation
---

# Prerequisites

Before you begin using GL Observability on your python project, ensure you have the following handy.

{% stepper %}
{% step %}
#### Python 3.11 - 3.13

Make sure you have [Python](https://www.python.org/) version 3.11 or later installed. We recommend installing version 3.12 at the time of writing. Use this to verify you have the right version.

```bash
python --version

# Python 3.12.3
```
{% endstep %}

{% step %}
#### UV Package Manager

While PIP works as a global installer, it's harder to manage the versions, lock versions, etc. We recommend using [UV](https://docs.astral.sh/uv/) as the package manager. All the guides will utilize UV.

```bash
uv --version

# uv 0.7.6
```
{% endstep %}

{% step %}
#### Access to Observability Backend

Observability backend is a server or service that receives, stores, and analyzes telemetry data, e.g. Sentry, Jaeger, Signoz, etc.
{% endstep %}

{% step %}
#### Next Step?

Check out the [getting-started-1.md](getting-started-1.md "mention") page.
{% endstep %}
{% endstepper %}
