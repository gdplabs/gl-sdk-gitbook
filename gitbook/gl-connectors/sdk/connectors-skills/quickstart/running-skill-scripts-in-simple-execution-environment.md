---
icon: bolt
---

# Running Skill Scripts in Simple Execution Environment

This guide works in conjunction with [implementing-with-agent.md](implementing-with-agent.md "mention"). We assume you have read that guide first before going here.

## DeepAgents Skill with Script Execution

### The Problem

You have a skill (`date-wizard`) that bundles a Python script (`datecalc.py`). The agent needs to:

1. **Discover** the skill (via `SKILL.md` frontmatter) ✅ — deepagents does this
2. **Read** the skill instructions (via `read_file` on `SKILL.md`) ✅ — deepagents does this
3. **Execute** the script (via shell: `python datecalc.py weekday 2026-05-02`) ❌ — **not automatic**

#### Why doesn't execution work out of the box?

DeepAgents has a built-in `execute` tool for shell commands, but it **only activates when the backend implements `SandboxBackendProtocol`**. The common backends:

| Backend             | File I/O | Shell (`execute`) | Use Case                         |
| ------------------- | -------- | ----------------- | -------------------------------- |
| `StateBackend`      | ✅ (RAM)  | ❌                 | Default. Virtual files in memory |
| `FilesystemBackend` | ✅ (disk) | ❌                 | Local disk access                |
| `StoreBackend`      | ✅ (DB)   | ❌                 | Persistent cross-thread storage  |
| Modal Sandbox       | ✅        | ✅                 | Remote sandboxed execution       |
| Runloop Sandbox     | ✅        | ✅                 | Remote sandboxed execution       |
| Daytona Sandbox     | ✅        | ✅                 | Remote sandboxed execution       |
| CLI ShellMiddleware | ✅        | ✅                 | Local shell (CLI package only)   |

So if you use `FilesystemBackend` (the natural choice for a server), the agent can read `SKILL.md` and discover `datecalc.py`, but it has no way to **run** it.

### Solutions

#### Approach A: Custom Tool (Recommended for your own server)

Add a simple `run_script` tool that wraps `subprocess`. This is 5 lines of code and gives you full control over what the agent can execute.

<pre class="language-python" data-line-numbers><code class="lang-python">import asyncio

from deepagents import create_deep_agent
from deepagents.graph import init_chat_model
from deepagents.backends.filesystem import FilesystemBackend
from pathlib import Path
import subprocess

PROJECT_DIR = Path(__file__).parent.resolve()

<strong>def run_script(command: str) -> str:
</strong><strong>    try:
</strong><strong>        result = subprocess.run(command,shell=True,capture_output=True,text=True,timeout=30,cwd=str(PROJECT_DIR))
</strong><strong>        if result.returncode != 0:
</strong><strong>            return f"Error (exit code {result.returncode}):\n{result.stderr.strip()}"
</strong><strong>        return result.stdout.strip()
</strong><strong>    except Exception as e:
</strong><strong>        return f"Error: {e}"
</strong>
async def main():
    agent = create_deep_agent(
        model=init_chat_model("openai:gpt-5-mini"),
        backend=FilesystemBackend(root_dir=str(PROJECT_DIR)),
<strong>        tools=[run_script],
</strong><strong>        skills=[".deepagents/skills/"],
</strong>    )

    result = agent.invoke({
        "messages":[{"role": "user", "content": "Tell me today's date and time, and what day it is in UTC+7."}],
    })
    print(result["messages"][-1].content)

asyncio.run(main())
</code></pre>

**Pros:** Simple, works everywhere, no extra dependencies.

**Cons:** No sandboxing — the agent runs commands on your server directly.

#### Approach B: Sandbox Backend (Recommended for production / multi-tenant)

Use Modal, Runloop, or Daytona for isolated execution:

```bash
pip install deepagents[modal]  # or deepagents[runloop] or deepagents[daytona]
```

With a sandbox backend, the built-in `execute` tool works automatically — no custom tool needed. The agent reads the SKILL.md, sees "run `python scripts/datecalc.py`", and calls `execute` directly.

#### Approach C: Virtual Files (No real filesystem needed)

For serverless or containerized deployments, load skills from a DB/S3/etc. as virtual files via `StateBackend`:

```python
from deepagents.middleware.filesystem import FileData
from langchain_core.messages import HumanMessage

agent = create_deep_agent(
    model="openai:gpt-4o-mini",
    skills=["/skills/"],
    tools=[run_script],  # still need this for execution
)

result = agent.invoke({
    "messages": [HumanMessage(content="What day is May 2, 2026?")],
    "files": {
        "/skills/date-wizard/SKILL.md": FileData(
            content=open("SKILL.md").read().split("\n"),
            created_at="2024-01-01T00:00:00Z",
            modified_at="2024-01-01T00:00:00Z",
        ),
    },
})
```

**Pros:** "Sandboxed" via virtual environment

**Cons:** Need to sync up all files and add it; can be problematic if there are many files and/or multiple file formats. Need to preserve structure as well.

### Directory Structure

```
project/
├── .deepagents/
│   └── skills/
│       └── date-wizard/
│           ├── SKILL.md              ← Agent reads this to learn the skill
│           └── scripts/
│               └── datecalc.py       ← Agent executes this via run_script tool
├── main.py                           ← Full example with all approaches
├── minimal.py                        ← Simplest working example
└── README.md                         ← This file
```

### How the Flow Works

<div data-with-frame="true"><figure><img src="../../../../.gitbook/assets/image (2).png" alt=""><figcaption><p><a href="https://docs.google.com/presentation/d/1DSqBvM3vfE7-QX5cIGm4aztnZgHVenq-bWo4_fTjNBw/edit?slide=id.g3d40ffae675_2_81#slide=id.g3d40ffae675_2_81">Diagram Link</a></p></figcaption></figure></div>

### Securing the Custom Tool

For production, you probably want to restrict what the agent can execute:

```python
import shlex

ALLOWED_SCRIPTS = {
    "datecalc": ".deepagents/skills/date-wizard/scripts/datecalc.py",
    # add more as needed
}

def run_skill_script(script_name: str, args: str) -> str:
    """Run an allowed skill script with the given arguments.

    Available scripts: datecalc
    Example: run_skill_script("datecalc", "weekday 2026-05-02")
    """
    if script_name not in ALLOWED_SCRIPTS:
        return f"Error: Unknown script '{script_name}'. Available: {list(ALLOWED_SCRIPTS.keys())}"

    script_path = PROJECT_DIR / ALLOWED_SCRIPTS[script_name]
    safe_args = shlex.split(args)
    result = subprocess.run(
        ["python", str(script_path)] + safe_args,
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
```

This avoids `shell=True` entirely and only allows pre-approved scripts.
