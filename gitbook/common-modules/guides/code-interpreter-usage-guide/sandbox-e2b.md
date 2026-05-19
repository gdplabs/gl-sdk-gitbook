---
icon: building-columns
---

# Sandbox: E2B

E2B provides cloud-hosted, isolated sandboxes. Each sandbox is a fresh VM that persists across multiple `execute_code` calls within the same session.

#### Prerequisites

* An [E2B API key](https://e2b.dev/docs)

#### Setup

```python
from gllm_tools.code_interpreter.code_sandbox.e2b_sandbox import E2BSandbox

sandbox = await E2BSandbox.create(
    api_key="your-e2b-api-key",
    additional_packages=["pandas", "matplotlib"],  # installed via pip on creation
)
```

> **Note:** E2B uses an async factory method `E2BSandbox.create()`. Do not call `E2BSandbox()` directly.

#### Constructor Parameters

| Parameter             | Type                | Default    | Description                                                |
| --------------------- | ------------------- | ---------- | ---------------------------------------------------------- |
| `api_key`             | `str`               | required   | Your E2B API key                                           |
| `domain`              | `str \| None`       | `None`     | Custom E2B domain (for self-hosted). Defaults to E2B SaaS. |
| `template`            | `str \| None`       | `None`     | E2B sandbox template name                                  |
| `language`            | `str`               | `"python"` | Programming language (only Python supported)               |
| `additional_packages` | `list[str] \| None` | `None`     | pip packages to install on initialization                  |

#### Full Example

```python
import asyncio
from gllm_tools.code_interpreter.code_sandbox.e2b_sandbox import E2BSandbox

async def main():
    sandbox = await E2BSandbox.create(
        api_key="your-e2b-api-key",
        additional_packages=["numpy", "pandas"],
    )

    try:
        result = await sandbox.execute_code("""
import numpy as np
data = np.array([1, 2, 3, 4, 5])
print(f"Mean: {data.mean():.2f}")
print(f"Std: {data.std():.2f}")
""", timeout=30)

        print(result.stdout)

    finally:
        await sandbox.terminate()

asyncio.run(main())
```

#### With SandboxCodeInterpreter

```python
import asyncio
from gllm_tools.code_interpreter.code_sandbox.e2b_sandbox import E2BSandbox
from gllm_tools.code_interpreter.code_interpreter.sandbox_code_interpreter import SandboxCodeInterpreter

async def main():
    sandbox = await E2BSandbox.create(
        api_key="your-e2b-api-key",
        additional_packages=["pandas", "seaborn"],
    )

    interpreter = SandboxCodeInterpreter(sandbox=sandbox, lm_invoker=lm_invoker)

    result = await interpreter.execute("Plot a histogram of [10, 20, 20, 30, 40] and save it as hist.png")
    print(result.text)

    await sandbox.terminate()

asyncio.run(main())
```

#### Notes

* State **persists** across multiple `execute_code` calls within the same session (imports and variables are retained).
* Files uploaded via `files=` parameter land at `/files/<filename>`.
* Files downloaded via `download_file(path)` return raw `bytes`.
