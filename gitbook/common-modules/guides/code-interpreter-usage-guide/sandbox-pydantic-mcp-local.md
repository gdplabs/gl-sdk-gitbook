---
icon: building-columns
---

# Sandbox: Pydantic MCP (Local)

`PydanticExecutorSandbox` runs code locally inside a WebAssembly sandbox powered by [Pyodide](https://pyodide.org). It communicates with a Pydantic MCP server over stdin/stdout using JSON-RPC.

#### Prerequisites

* [Deno](https://deno.land/manual/getting_started/installation) installed and available on `PATH`

```bash
# Install Deno
curl -fsSL https://deno.land/install.sh | sh
```

#### Setup

```python
from gllm_tools.code_interpreter.code_sandbox.pydantic_executor_sandbox import PydanticExecutorSandbox

# Uses 'deno' from PATH by default
sandbox = PydanticExecutorSandbox()

# Custom path to deno executable
sandbox = PydanticExecutorSandbox(mcp_server_path="/usr/local/bin/deno")
```

> **Note:** Unlike the other sandboxes, `PydanticExecutorSandbox` is synchronous in its constructor — the MCP server process is started immediately on instantiation.

#### Constructor Parameters

| Parameter         | Type          | Default    | Description                                                      |
| ----------------- | ------------- | ---------- | ---------------------------------------------------------------- |
| `mcp_server_path` | `str \| None` | `None`     | Path to the `deno` executable. Defaults to `"deno"` (from PATH). |
| `language`        | `str`         | `"python"` | Programming language (only Python supported)                     |

#### Execution Constraints

| Constraint        | Value                                     |
| ----------------- | ----------------------------------------- |
| Max timeout       | 300 seconds                               |
| Max output length | 10,000 characters                         |
| File download     | Not supported (returns `None`)            |
| Persistent state  | No — each `execute_code` call is isolated |

#### Full Example

```python
import asyncio
from gllm_tools.code_interpreter.code_sandbox.pydantic_executor_sandbox import PydanticExecutorSandbox

async def main():
    sandbox = PydanticExecutorSandbox()

    try:
        result = await sandbox.execute_code("""
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

for i in range(1, 8):
    print(f"{i}! = {factorial(i)}")
""", timeout=30)

        if result.status.value == "success":
            print(result.stdout)
        else:
            print(f"Error: {result.error}")

    finally:
        await sandbox.terminate()

asyncio.run(main())
```

#### With SandboxCodeInterpreter

```python
import asyncio
from gllm_tools.code_interpreter.code_sandbox.pydantic_executor_sandbox import PydanticExecutorSandbox
from gllm_tools.code_interpreter.code_interpreter.sandbox_code_interpreter import SandboxCodeInterpreter

async def main():
    sandbox = PydanticExecutorSandbox()
    interpreter = SandboxCodeInterpreter(sandbox=sandbox, lm_invoker=lm_invoker)

    result = await interpreter.execute("Write a function to check if a number is prime and test it on numbers 1–20")
    print(result.text)

    await sandbox.terminate()

asyncio.run(main())
```

#### Notes

* Each code execution is **fully isolated** — variables and imports do not persist between calls.
* File upload via `files=` is supported (content is base64-encoded and written to `/files/<filename>` inside the sandbox at execution time).
* File download is **not supported** — `download_file()` always returns `None`.
* Runs entirely locally — no cloud calls, no API keys required.
