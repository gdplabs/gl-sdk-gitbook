---
icon: box-archive
---

# Artifact Storage

GL Computer Use saves screenshots and session recordings as artifacts. By default they are written to local disk. Switch to MinIO or any S3-compatible object store to get presigned URLs accessible from anywhere.

## Local vs MinIO Comparison

| | Local (default) | MinIO / S3 |
|---|---|---|
| **Extra required** | — | `minio` |
| **Config value** | `artifact="local"` | `artifact="minio"` |
| **Screenshot access** | Local file paths | Presigned HTTPS URLs |
| **Recording access** | Local file path | Presigned HTTPS URL |
| **Retrieved files** | Local file paths | Presigned HTTPS URLs |
| **URL expiry** | Never | `presigned_url_expiry_seconds` (default 3600 s) |

## Local Storage (Default)

Artifacts are saved to the directory set by `GLCU_LOCAL_ARTIFACT_DIR` (default `./artifacts`):

```python
from gl_computer_use import GLComputerUseClient, GLComputerUseConfig

config = GLComputerUseConfig(
    local_artifact_dir="./my-artifacts",
)
result = GLComputerUseClient(config=config).run_sync("Open a terminal")

# With local storage, URL fields are empty or local paths
print(result.screenshot_urls)   # []
print(result.recording_url)     # None or local path
```

## MinIO / S3 Storage

Install the extra and configure the object store:

```bash
pip install "gl-computer-use[minio]"
```

Start a local MinIO server for development:

```bash
docker run -p 9000:9000 -p 9001:9001 \
    -e MINIO_ROOT_USER=minioadmin \
    -e MINIO_ROOT_PASSWORD=minioadmin \
    minio/minio server /data --console-address ':9001'
```

Configure via environment variables:

```dotenv
GLCU_ARTIFACT=minio
GLCU_OBJECT_STORE_ENDPOINT=localhost:9000
GLCU_OBJECT_STORE_ACCESS_KEY=minioadmin
GLCU_OBJECT_STORE_SECRET_KEY=minioadmin
GLCU_OBJECT_STORE_BUCKET=gl-computer-use
GLCU_PRESIGNED_URL_EXPIRY_SECONDS=3600
```

Or via explicit config:

```python
import asyncio
from gl_computer_use import GLComputerUseClient, GLComputerUseConfig, File


async def main() -> None:
    config = GLComputerUseConfig(
        artifact="minio",
        object_store_endpoint="localhost:9000",
        object_store_access_key="minioadmin",
        object_store_secret_key="minioadmin",
        object_store_bucket="gl-computer-use",
        presigned_url_expiry_seconds=3600,
    )
    client = GLComputerUseClient(config=config)

    input_file = File(path="/home/user/input.txt", data=b"Hello, World!\n")

    result = await client.run_once(
        "Read /home/user/input.txt and display its contents",
        files=[input_file],
        retrieve_files=["/home/user/input.txt"],
    )

    print(f"Screenshots ({len(result.screenshot_urls)}):")
    for url in result.screenshot_urls[:3]:
        print(f"  {url}")

    print(f"\nRetrieved files:")
    for path, url in result.file_urls.items():
        print(f"  {path}: {url or '(failed)'}")

    print(f"\nRecording: {result.recording_url or '(none)'}")
    print(f"Recording status: {result.recording_status}")


asyncio.run(main())
```

## Session Recording

GL Computer Use records each session as either a WebM video or a GIF fallback.

### Recording Formats

| Format | Extra | Quality | Notes |
|---|---|---|---|
| **WebM** | `recording` + one-time `gl-computer-use-setup` | High — full-motion video | Requires Playwright Chromium (~130 MB) |
| **GIF** | None (automatic fallback) | Medium — screenshot stitching | No extra install needed |

Install and set up WebM recording:

```bash
pip install "gl-computer-use[recording]"
gl-computer-use-setup   # installs Playwright Chromium (~130 MB, one-time)
```

If the setup step is skipped, the SDK falls back to GIF automatically.

### Recording Status Values

`result.recording_status` reflects the upload outcome when MinIO is configured:

| Status | Meaning |
|---|---|
| `UPLOADED` | Recording was uploaded successfully; `recording_url` is valid |
| `PARTIAL` | Recording started but may be incomplete |
| `FAILED` | Recording upload failed; `recording_url` may be `None` |

```python
result = await client.run_once("do something")
if result.recording_url:
    print(f"Recording: {result.recording_url}")
    print(f"Status: {result.recording_status}")
```

{% hint style="info" %}
With local artifact storage the recording URL will be a local file path or `None`. Use MinIO storage to get a shareable presigned URL.
{% endhint %}
