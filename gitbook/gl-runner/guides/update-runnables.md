# Update a Runnable

Update an existing runnable with a new bundle. You can target by ID or key.
Since `.deploy()` auto-detects whether a deployment is already tracked,
the same method handles both first-time deploy and updates.

CLI:

```bash
python ./scripts/update.py --runnable-id <id> --bundle-path ./bundles/hello-world
```

```bash
python ./scripts/update.py --runnable-key hello-world --bundle-path ./bundles/hello-world
```

Python SDK:

```python
from gl_runner_sdk import Runnable

updated = (
    Runnable.from_key(
        "hello-world",
        base_url="http://localhost:4200",
        api_key="glr_...",
    )
    .set_bundle_path("./bundles/hello-world")
    .deploy(version="v2.0.0")
)
```

Advanced / direct ID lookup:

```python
from gl_runner_sdk import Runnable

updated = (
    Runnable.from_id(
        "<runnable-id>",
        base_url="http://localhost:4200",
        api_key="glr_...",
    )
    .set_bundle_path("./bundles/hello-world")
    .deploy(version="v2.0.0")
)
```

Tips:

- Use `--entrypoint` to override the entrypoint if it changed.
- Use `--version` to track bundle iterations.
- The SDK excludes `.env` by default. If an updated bundle needs a packaged
  runtime `.env`, include it explicitly with `--include-sensitive-file .env` or
  `include_sensitive_files=[".env"]`.
