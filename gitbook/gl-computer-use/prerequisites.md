---
icon: circle-exclamation
---

# Prerequisites

Before using GL Computer Use, ensure your environment and credentials are ready.

{% stepper %}
{% step %}
**Python 3.12 or 3.13**

GL Computer Use requires Python `>=3.12,<3.14`.

```bash
python --version
# Python 3.12.x or Python 3.13.x
```
{% endstep %}

{% step %}
**Install the SDK**

Install the core package:

```bash
pip install gl-computer-use
```

Install optional extras only when you need them:

| Extra | Installs | When to use |
|---|---|---|
| `recording` | Playwright + Pillow | WebM session recording |
| `agents` | Simular-AI Agent-S + pyautogui | Agent-S provider |
| `opensandbox` | Alibaba OpenSandbox client | OpenSandbox provider |
| `minio` | aiobotocore | MinIO / S3-compatible artifact store |
| `observability` | gl-observability, tenacity | OTLP tracing, Sentry, retries |
| `all` | All of the above | Full feature set |

```bash
pip install "gl-computer-use[recording]"
pip install "gl-computer-use[agents]"
pip install "gl-computer-use[opensandbox]"
pip install "gl-computer-use[minio]"
pip install "gl-computer-use[observability]"
pip install "gl-computer-use[all]"
```

{% hint style="info" %}
Use specific extras in production dependency files to pin exactly which providers your application uses.
{% endhint %}
{% endstep %}

{% step %}
**E2B API Key**

The default sandbox is E2B Desktop. Obtain an API key at [e2b.dev](https://e2b.dev) and set it in your environment:

```bash
export GLCU_E2B_API_KEY="sk-e2b-..."
```

This is required when `GLCU_SANDBOX=e2b` (the default).
{% endstep %}

{% step %}
**LLM API Key**

The default model is `anthropic/claude-sonnet-4-6`. Set whichever key matches your model provider:

```bash
# For Anthropic models (default)
export GLCU_ANTHROPIC_API_KEY="sk-ant-..."

# For OpenAI models
export GLCU_OPENAI_API_KEY="sk-..."
```
{% endstep %}

{% step %}
**Create a `.env` File (Recommended)**

Place a `.env` file in your working directory so the SDK loads credentials automatically:

```dotenv
# Required
GLCU_E2B_API_KEY=sk-e2b-...
GLCU_ANTHROPIC_API_KEY=sk-ant-...

# Optional overrides
GLCU_MODEL=anthropic/claude-sonnet-4-6
GLCU_TIMEOUT=600
GLCU_MAX_STEPS=100
GLCU_LOG_FORMAT=console
```

The SDK reads `GLCU_*` environment variables via `pydantic-settings` and `python-dotenv`.
{% endstep %}

{% step %}
**Session Recording Setup (Optional, One-Time)**

WebM recordings require Playwright's Chromium binaries (~130 MB). Run this once after installing the `recording` extra:

```bash
pip install "gl-computer-use[recording]"
gl-computer-use-setup
```

If you skip this step, the SDK automatically falls back to GIF recording via screenshot stitching.
{% endstep %}
{% endstepper %}
