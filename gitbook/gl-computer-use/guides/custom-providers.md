---
icon: wrench
---

# Custom Providers

GL Computer Use supports plugging in alternative sandbox, agent, or artifact store implementations without modifying the SDK. Register your provider once and reference it by name in config.

## Custom Sandbox

Subclass `BaseSandbox`, implement all abstract methods, then register it:

```python
from gl_computer_use import register_sandbox, GLComputerUseClient, GLComputerUseConfig
from gl_computer_use.sandbox.base import BaseSandbox


class MyCustomSandbox(BaseSandbox):
    async def provision(self) -> None:
        """Allocate the sandbox."""
        ...

    async def destroy(self) -> None:
        """Release the sandbox."""
        ...

    @property
    def stream_url(self) -> str | None:
        """Return the live desktop URL, or None if unavailable."""
        ...

    async def execute(self, action) -> None:
        """Apply a desktop action to the running sandbox."""
        ...

    async def screenshot(self) -> bytes:
        """Capture a PNG screenshot of the current desktop state."""
        ...


register_sandbox("my-sandbox", MyCustomSandbox)

client = GLComputerUseClient(config=GLComputerUseConfig(sandbox="my-sandbox"))
```

**BaseSandbox abstract methods:**

| Method | Signature | Purpose |
|---|---|---|
| `provision` | `async () → None` | Allocate and start the sandbox |
| `destroy` | `async () → None` | Shut down and release the sandbox |
| `stream_url` | `property → str \| None` | Return live desktop URL |
| `execute` | `async (action) → None` | Apply a desktop action |
| `screenshot` | `async () → bytes` | Capture a PNG screenshot |

## Custom Agent

Subclass `BaseAgent` and implement its abstract interface:

```python
from gl_computer_use import register_agent, GLComputerUseClient, GLComputerUseConfig
from gl_computer_use.agent.base import BaseAgent


class MyCustomAgent(BaseAgent):
    async def run(self, prompt: str, sandbox, on_step) -> str:
        """Run the agent loop and return the final output."""
        ...


register_agent("my-agent", MyCustomAgent)

client = GLComputerUseClient(config=GLComputerUseConfig(agent="my-agent"))
```

## Custom Artifact Store

Subclass `BaseArtifact` and implement the storage interface:

```python
from gl_computer_use import register_artifact, GLComputerUseClient, GLComputerUseConfig
from gl_computer_use.artifact.base import BaseArtifact


class MyCustomArtifact(BaseArtifact):
    async def save_screenshot(self, data: bytes, task_id: str, step: int) -> str | None:
        """Persist a screenshot and return its URL or path."""
        ...

    async def save_recording(self, path: str, task_id: str) -> str | None:
        """Persist a session recording and return its URL or path."""
        ...

    async def save_file(self, data: bytes, remote_path: str, task_id: str) -> str | None:
        """Persist a retrieved file and return its URL or path."""
        ...


register_artifact("my-artifact", MyCustomArtifact)

client = GLComputerUseClient(config=GLComputerUseConfig(artifact="my-artifact"))
```

## Registration Summary

| Function | Base class to extend | Config key |
|---|---|---|
| `register_sandbox(name, cls)` | `BaseSandbox` | `GLComputerUseConfig(sandbox=name)` |
| `register_agent(name, cls)` | `BaseAgent` | `GLComputerUseConfig(agent=name)` |
| `register_artifact(name, cls)` | `BaseArtifact` | `GLComputerUseConfig(artifact=name)` |

{% hint style="info" %}
Registration is process-global. Call `register_*` once at application startup before creating any client instances.
{% endhint %}
