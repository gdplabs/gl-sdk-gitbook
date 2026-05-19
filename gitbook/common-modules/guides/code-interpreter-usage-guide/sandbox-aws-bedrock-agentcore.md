---
icon: building-columns
---

# Sandbox: AWS Bedrock AgentCore

AWS Bedrock AgentCore provides a managed code interpreter backed by AWS infrastructure.

#### Prerequisites

* AWS credentials with access to `bedrock-agentcore`
* Bedrock AgentCore available in your region (default: `us-east-1`)

AWS credentials are read from:

1. Parameters passed directly to the constructor (`aws_access_key_id`, `aws_secret_access_key`)
2. Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
3. Standard boto3 credential chain (IAM roles, `~/.aws/credentials`, etc.)

#### Setup

```python
from gllm_tools.code_interpreter.code_sandbox.bedrock_agentcore_sandbox import BedrockAgentCoreSandbox

# Using environment credentials
sandbox = BedrockAgentCoreSandbox(region="us-east-1")

# Using explicit credentials
sandbox = BedrockAgentCoreSandbox(
    region="us-east-1",
    aws_access_key_id="AKIA...",
    aws_secret_access_key="secret...",
)
```

> **Note:** The session is created lazily — no AWS connection is made until the first `execute_code` call.

#### Constructor Parameters

| Parameter                 | Type           | Default       | Description                                                      |
| ------------------------- | -------------- | ------------- | ---------------------------------------------------------------- |
| `region`                  | `str`          | `"us-east-1"` | AWS region for Bedrock service                                   |
| `aws_access_key_id`       | `str \| None`  | `None`        | AWS access key ID. Falls back to env vars / IAM role.            |
| `aws_secret_access_key`   | `str \| None`  | `None`        | AWS secret access key. Falls back to env vars / IAM role.        |
| `language`                | `str`          | `"python"`    | Programming language (only Python supported)                     |
| `session_timeout`         | `int`          | `60`          | Server-side session lifetime in seconds                          |
| `aioboto3_session_kwargs` | `dict \| None` | `None`        | Extra kwargs passed to `aioboto3.Session` (e.g., `profile_name`) |

#### Timeout Behaviour

There are two independent timeouts:

| Timeout          | Parameter                        | Scope       | Description                                      |
| ---------------- | -------------------------------- | ----------- | ------------------------------------------------ |
| Per-execution    | `timeout` in `execute_code()`    | Client-side | Max time for a single code run (default: 30s)    |
| Session lifetime | `session_timeout` in constructor | Server-side | Max total lifetime of the session (default: 60s) |

#### Full Example

```python
import asyncio
from gllm_tools.code_interpreter.code_sandbox.bedrock_agentcore_sandbox import BedrockAgentCoreSandbox

async def main():
    sandbox = BedrockAgentCoreSandbox(
        region="us-east-1",
        session_timeout=120,
    )

    try:
        result = await sandbox.execute_code("""
import math
print(f"Pi = {math.pi:.6f}")
print(f"e  = {math.e:.6f}")
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
from gllm_tools.code_interpreter.code_sandbox.bedrock_agentcore_sandbox import BedrockAgentCoreSandbox
from gllm_tools.code_interpreter.code_interpreter.sandbox_code_interpreter import SandboxCodeInterpreter

async def main():
    sandbox = BedrockAgentCoreSandbox(region="us-east-1", session_timeout=300)
    interpreter = SandboxCodeInterpreter(sandbox=sandbox, lm_invoker=lm_invoker)

    result = await interpreter.execute("Compute the first 10 Fibonacci numbers")
    print(result.text)

    await sandbox.terminate()

asyncio.run(main())
```

#### Notes

* State does **not** necessarily persist between separate `execute_code` calls (depends on AWS session state).
* File upload via the `files=` parameter is supported.
* `download_file(path)` returns `bytes` for both regular files and images.
* Using an AWS profile: pass `aioboto3_session_kwargs={"profile_name": "my-profile"}`.
