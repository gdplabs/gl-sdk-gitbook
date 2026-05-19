# Bundle Format

A runnable bundle is a directory packaged into a ZIP with a `runnables.yaml`
and an entrypoint module. See the example bundles under
`examples/bundles/` for working layouts.

Typical bundle layout:

```
hello-world/
├── runnables.yaml
├── entrypoint.py
└── __init__.py
```

The server requires `__init__.py` to validate the bundle, so it is part of the
bare minimum structure. It can be empty, but best practice is to include a
package docstring with author and references.

The SDK packages the directory for you when you pass `bundle_path`.

## Bundles and .env Files

Some bundles load environment variables at runtime using `python-dotenv`.
For example, `simple-de` calls `load_dotenv()` in its entrypoint, which means
it reads a `.env` file packaged alongside the code.

Guidance:

- Use `.env.example` to document required variables.
- The SDK excludes `.env`, `.env.*`, caches, virtualenvs, build outputs, and
  VCS metadata from generated bundle ZIPs by default.
- `.env.example` remains included by default so bundles can document required
  variables without uploading real secrets.
- If your runnable depends on `.env` at runtime and the runner environment does
  not provide those variables, include it explicitly:

```python
from gl_runner_sdk import Runnable

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

- Do not commit real secrets; use your environment or a secret manager.
- Including `.env` uploads it inside the runnable bundle artifact. Use this only
  for local development or trusted private runner environments until GL Runner
  has first-class runnable secret storage.
