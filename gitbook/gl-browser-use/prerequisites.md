---
icon: circle-exclamation
---

# Prerequisites

Before you begin using GL Browser Use, make sure your environment and credentials are ready.

{% stepper %}
{% step %}
**Python 3.11 or 3.12**

GL Browser Use requires Python `>=3.11,<3.13`.

```bash
python --version

# Python 3.11.x or Python 3.12.x
```
{% endstep %}

{% step %}
**Install the SDK**

Install the core package when you only need local browser execution through `browser-use`:

```bash
pip install gl-browser-use
```

Install optional extras only when you use the matching provider:

```bash
pip install "gl-browser-use[steel]"
pip install "gl-browser-use[minio]"
pip install "gl-browser-use[full]"
```

{% hint style="info" %}
Use concrete extras such as `steel` and `minio` in application dependency files when you want to pin exactly which provider your application uses. The `infrastructure`, `storage`, and `full` extras are convenience aliases and may include more providers later.
{% endhint %}
{% endstep %}

{% step %}
**OpenAI API Key**

GL Browser Use uses OpenAI-compatible chat models through `browser-use`. Set `OPENAI_API_KEY`, or pass the keys directly through `BrowserUseClientConfig`.

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

If you do not pass `llm_openai_api_key` or `page_extraction_llm_openai_api_key`, both values default to `OPENAI_API_KEY`.
{% endstep %}

{% step %}
**Optional Steel Credentials**

Steel is only required when you want hosted browser sessions, streaming URLs, CDP URLs, or Steel-backed recordings.

```bash
export STEEL_API_KEY="your-steel-api-key"
```
{% endstep %}

{% step %}
**Optional Object Storage Credentials**

Object storage is only required when you want GL Browser Use to upload browser session recordings and return recording URLs.

```bash
export OBJECT_STORAGE_URL="localhost:9001"
export OBJECT_STORAGE_USERNAME="your-access-key"
export OBJECT_STORAGE_PASSWORD="your-secret-key"
export OBJECT_STORAGE_BUCKET_NAME="browser-recordings"
export OBJECT_STORAGE_DIRECTORY_PREFIX="optional-prefix"
export OBJECT_STORAGE_SECURE="false"
```

`OBJECT_STORAGE_URL` may include an `http://` or `https://` scheme. When no scheme is provided, `OBJECT_STORAGE_SECURE` controls whether the client uses HTTPS.
{% endstep %}
{% endstepper %}
