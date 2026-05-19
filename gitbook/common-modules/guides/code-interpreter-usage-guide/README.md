---
icon: trowel
---

# Code Interpreter — Usage Guide

The `gllm_tools` code interpreter lets a language model execute Python code inside a secure sandbox. It supports three sandbox backends:

* **E2B** — Cloud-based sandbox via [E2B](https://e2b.dev)
* **AWS Bedrock AgentCore** — Managed sandbox via AWS Bedrock
* **Pydantic MCP** — Local WebAssembly sandbox via Pydantic's MCP server (Pyodide)

***

### Architecture Overview

```
SandboxCodeInterpreter
├── BaseLMInvoker          ← language model (generates code)
└── BaseSandbox            ← executes code
    ├── E2BSandbox
    ├── BedrockAgentCoreSandbox
    └── PydanticExecutorSandbox
```

The `SandboxCodeInterpreter` orchestrates a multi-turn conversation where the LM generates Python code, the sandbox executes it, and results are fed back to the LM until it produces a final answer.

***

### Installation

Install `gllm-tools` with the extras matching the sandbox(es) you want to use:

```bash
# E2B sandbox
pip install "gllm-tools[e2b]"

# AWS Bedrock sandbox
pip install "gllm-tools[bedrock]"

# Pydantic MCP sandbox (requires deno in PATH)
pip install "gllm-tools[pydantic-mcp]"
```

***

### Common Imports

```python
from gllm_tools.code_interpreter.code_interpreter.sandbox_code_interpreter import SandboxCodeInterpreter
from gllm_tools.code_interpreter.code_sandbox.models import ExecutionResult, ExecutionStatus
```

***

### Using SandboxCodeInterpreter (High-Level)

`SandboxCodeInterpreter` is the main entry point. It pairs a sandbox with a language model invoker and handles the full tool-calling loop automatically.

```python
import asyncio
from gllm_tools.code_interpreter.code_interpreter.sandbox_code_interpreter import SandboxCodeInterpreter

async def main():
    # 1. Create a sandbox (see sandbox-specific sections below)
    sandbox = ...

    # 2. Create an LM invoker (BaseLMInvoker from gllm_inference)
    lm_invoker = ...

    # 3. Build the interpreter
    interpreter = SandboxCodeInterpreter(sandbox=sandbox, lm_invoker=lm_invoker)

    # 4. Execute a natural language request
    result = await interpreter.execute("Calculate the mean and standard deviation of [1, 2, 3, 4, 5]")

    print(result.text)                  # LM's final response text
    print(result.code_exec_results)     # list of CodeExecResult objects

    # 5. Always terminate the sandbox when done
    await sandbox.terminate()

asyncio.run(main())
```

#### Passing Files

You can pass files as `Attachment` objects. They are uploaded to the sandbox at `/files/<filename>` before execution.

```python
from gllm_inference.schema import Attachment

with open("data.csv", "rb") as f:
    attachment = Attachment.from_bytes(bytes=f.read(), filename="data.csv")

result = await interpreter.execute(
    "Load /files/data.csv and print the first 5 rows",
    files=[attachment]
)
```

#### Downloading Output Files

If the LM creates files during execution, it will include download links in its response using the format:

```
[Download output.csv](sandbox:/files/output.csv)
```

These files are automatically downloaded and returned as `Attachment` objects inside `result.code_exec_results[-1].output`.

***

### Using Sandboxes Directly (Low-Level)

You can also use the sandboxes directly without `SandboxCodeInterpreter` for raw code execution.

```python
result = await sandbox.execute_code("print('hello world')", timeout=30)

print(result.status)      # ExecutionStatus.SUCCESS / ERROR / TIMEOUT
print(result.stdout)      # standard output
print(result.stderr)      # standard error
print(result.error)       # error message (on failure)
print(result.duration_ms) # execution time in milliseconds
```

For each implementation guide, you can check:

1. [Sandbox: E2B](sandbox-e2b.md)
2. [Sandbox: Aws Bedrock](sandbox-aws-bedrock-agentcore.md)
3. [Sandbox: Pydantic](sandbox-pydantic-mcp-local.md)

***

### ExecutionResult Reference

All sandboxes return an `ExecutionResult` object from `execute_code()`.

```python
from gllm_tools.code_interpreter.code_sandbox.models import ExecutionResult, ExecutionStatus
```

| Field         | Type              | Description                                 |
| ------------- | ----------------- | ------------------------------------------- |
| `status`      | `ExecutionStatus` | `SUCCESS`, `ERROR`, or `TIMEOUT`            |
| `code`        | `str`             | The code that was executed                  |
| `stdout`      | `str`             | Standard output                             |
| `stderr`      | `str`             | Standard error                              |
| `text`        | `str`             | Combined output/error, suitable for display |
| `error`       | `str`             | Error message (populated on failure)        |
| `exit_code`   | `int`             | `0` on success, `1` on error                |
| `duration_ms` | `int \| None`     | Execution time in milliseconds              |

#### Checking Results

```python
result = await sandbox.execute_code("print(1 + 1)")

if result.status == ExecutionStatus.SUCCESS:
    print(result.stdout)
elif result.status == ExecutionStatus.TIMEOUT:
    print("Execution timed out")
else:
    print(f"Error: {result.error}")
    print(f"Stderr: {result.stderr}")
```

***

### Sandbox Comparison

| Feature                      | E2B                            | Bedrock AgentCore              | Pydantic MCP                |
| ---------------------------- | ------------------------------ | ------------------------------ | --------------------------- |
| Execution environment        | Cloud VM                       | AWS managed                    | Local WASM (Pyodide)        |
| API key required             | Yes (E2B)                      | AWS credentials                | No                          |
| State persists between calls | Yes                            | Partial                        | No                          |
| File upload                  | Yes (`/files/`)                | Yes                            | Yes (`/files/`)             |
| File download                | Yes                            | Yes                            | No                          |
| Custom packages              | `additional_packages`          | Not configurable               | Not supported               |
| Requires network             | Yes                            | Yes                            | No                          |
| Deno required                | No                             | No                             | Yes                         |
| Initialization style         | `await E2BSandbox.create(...)` | `BedrockAgentCoreSandbox(...)` | `PydanticExecutorSandbox()` |

***

### Error Handling

All sandboxes return structured `ExecutionResult` objects instead of raising exceptions on code errors. Unexpected infrastructure failures (network, credentials, process crashes) do raise exceptions.

```python
try:
    result = await sandbox.execute_code("1 / 0")

    if result.status == ExecutionStatus.ERROR:
        # Code raised an exception — safe to handle
        print(f"Code error: {result.error}")
    elif result.status == ExecutionStatus.TIMEOUT:
        print("Code timed out")
    else:
        print(result.stdout)

except RuntimeError as e:
    # Infrastructure error (session not started, network failure, etc.)
    print(f"Sandbox error: {e}")
```

#### Always Terminate

Always call `await sandbox.terminate()` when done, ideally inside a `finally` block:

```python
sandbox = await E2BSandbox.create(api_key="...")
try:
    result = await sandbox.execute_code("print('hello')")
finally:
    await sandbox.terminate()
```
