---
icon: video
---

# Record Browser Sessions

This guide shows how to run GL Browser Use with hosted browser infrastructure and object storage so your application can return browser streaming and recording URLs.

<details>
<summary>Prerequisites</summary>

Complete the setup steps in [Prerequisites](../prerequisites.md "mention"). You need:

1. `gl-browser-use[steel]` for Steel browser infrastructure.
2. `gl-browser-use[minio]` for MinIO or S3-compatible object storage.
3. `STEEL_API_KEY` configured.
4. `OBJECT_STORAGE_*` variables configured when you want session recording uploads.
</details>

## 1. Install Optional Providers

Install only the providers your application uses:

```bash
pip install "gl-browser-use[steel]"
pip install "gl-browser-use[minio]"
```

Or install all currently available providers:

```bash
pip install "gl-browser-use[full]"
```

## 2. Configure Environment Variables

Configure Steel for hosted browser sessions:

```bash
export STEEL_API_KEY="your-steel-api-key"
```

Configure object storage for recording uploads:

```bash
export OBJECT_STORAGE_URL="localhost:9001"
export OBJECT_STORAGE_USERNAME="your-access-key"
export OBJECT_STORAGE_PASSWORD="your-secret-key"
export OBJECT_STORAGE_BUCKET_NAME="browser-recordings"
export OBJECT_STORAGE_DIRECTORY_PREFIX="production"
export OBJECT_STORAGE_SECURE="false"
```

`MinIOS3CompatibleStorage` creates the bucket if it does not already exist.

## 3. Create the Client

Attach both the infrastructure and storage provider to `BrowserUseClient`:

```python
from gl_browser_use import BrowserUseClient, BrowserUseClientConfig
from gl_browser_use.infrastructure import SteelBrowserInfrastructure
from gl_browser_use.storage import MinIOS3CompatibleStorage

client = BrowserUseClient(
    config=BrowserUseClientConfig(),
    infrastructure=SteelBrowserInfrastructure(),
    storage=MinIOS3CompatibleStorage.from_environment(),
)
```

`SteelBrowserInfrastructure()` reads `STEEL_API_KEY` when `api_key` is not passed. `MinIOS3CompatibleStorage.from_environment()` reads the `OBJECT_STORAGE_*` variables.

## 4. Run a Task

Use streaming mode when you want to surface the live browser view as soon as it is available:

```python
import asyncio

from gl_browser_use import BrowserUseClient, BrowserUseClientConfig
from gl_browser_use.infrastructure import SteelBrowserInfrastructure
from gl_browser_use.storage import MinIOS3CompatibleStorage


async def main() -> None:
    client = BrowserUseClient(
        config=BrowserUseClientConfig(),
        infrastructure=SteelBrowserInfrastructure(),
        storage=MinIOS3CompatibleStorage.from_environment(),
    )

    async for event in client.run("Open Hacker News and list five article titles"):
        print(event.content)


asyncio.run(main())
```

For a single aggregated result:

```python
result = client.run_sync("Open Hacker News and list five article titles")

print(result.session_id)
print(result.streaming_url)
print(result.recording_url)
print(result.metadata)
```

## 5. Understand Recording Metadata

Recording metadata is returned in `result.metadata`:

1. `disabled`: infrastructure, storage, or browser context is not available.
2. `unsupported`: the selected infrastructure does not support recording.
3. `unavailable`: storage is configured but not available.
4. `scheduled`: a background recording upload has been scheduled.
5. `unknown`: recording may have started, but the terminal error did not include enough context to determine the final state.

When recording is available, GL Browser Use resolves the expected object URL and schedules the Steel recording upload in the background during cleanup.

{% hint style="info" %}
Recording requires both an infrastructure provider that supports recordings and an available object storage provider. Local browser execution can still run tasks, but it does not produce Steel streaming or recording URLs.
{% endhint %}
