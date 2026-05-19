# Deploy Runnables

Deploy from a bundle directory.

```python
from gl_runner_sdk import Runnable

runnable = Runnable(
    base_url="http://localhost:4200",
    api_key="glr_...",
    key="hello-world",
    bundle_path="./examples/bundles/hello-world",
)
deployment = runnable.deploy()
```

Note: If the runnable key already exists on the server, `deploy()` automatically
updates the existing deployment instead of creating a new one. See the
[Update a Runnable](./update-runnables.md) guide for details.

CLI:

```bash
python ./scripts/deploy.py --key hello-world --bundle-path ./examples/bundles/hello-world
```

Note on `.env` files:

- Some bundles (like `simple-de`) load `.env` at runtime using `dotenv`.
- The SDK excludes `.env` and `.env.*` files by default. `.env.example` remains
  included for documentation.
- If your runnable needs `.env` and the runner environment cannot provide those
  variables, opt in explicitly:

```python
runnable = Runnable(
    base_url="http://localhost:4200",
    api_key="glr_...",
    key="simple-de",
    bundle_path="./examples/bundles/simple-de",
)
deployment = runnable.deploy(include_sensitive_files=[".env"])
```

```bash
python ./scripts/deploy.py \
  --key simple-de \
  --bundle-path ./examples/bundles/simple-de \
  --include-sensitive-file .env
```

- Use `.env.example` as a template and keep secrets out of your repo.
- Explicit `.env` inclusion uploads the file inside the runnable bundle
  artifact. Use it only for local development or trusted private runner
  environments until GL Runner has first-class runnable secret storage.
