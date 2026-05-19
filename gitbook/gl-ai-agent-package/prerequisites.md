---
icon: circle-exclamation
---

Comprehensive setup guide for the AIP SDK with advanced configuration options, security best practices, and troubleshooting tips.

{% hint style="info" %}
Need the fastest path to a working agent? Jump to the [**Quick Start**](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide) first, then return here when you need deeper configuration.
{% endhint %}

## Requirements

- **Python** 3.11 or 3.12 (3.10 and earlier are not supported)
  - Verify with: `python3 --version` or `python --version`
- **Operating System**: Windows, macOS, or Linux
- **Network**: Internet access for package installation

{% hint style="info" %}
**Corporate networks** may require outbound proxy variables (e.g. `HTTP_PROXY`/`HTTPS_PROXY`). Set those before installing or running the CLI if your organisation routes traffic through a proxy.
{% endhint %}

### Install SDK and CLI Together

Installing `glaip-sdk` provides both the Python SDK and the `aip` CLI. Pick the install command that matches how you manage dependencies.

{% hint style="info" %}
**Local Execution Mode:** To run agents locally using the `aip-agents` library, install the `[local]` extra:

```bash
pip install --upgrade "glaip-sdk[local]"
```

This includes `aip-agents` for local LLM execution. See [Local vs Remote Mode](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/local-vs-remote) for when to use each mode.
{% endhint %}

{% hint style="warning" %}
**Privacy Features:** If you plan to use PII masking and privacy features, install `glaip-sdk[privacy]`:

```bash
pip install --upgrade "glaip-sdk[privacy]"
```

**Note:** Privacy features work in both remote and local modes. For local execution with privacy, use `glaip-sdk[local,privacy]`. See the [Security and Privacy guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/security-and-privacy) for more details.
{% endhint %}

#### pip (Linux/macOS)

```bash
# Standard installation
pip install --upgrade glaip-sdk

# With local execution support
pip install --upgrade "glaip-sdk[local]"
```

Use when you manage environments with `venv` or system Python. Activate the environment before running the command.

#### pip (Windows PowerShell)

```powershell
# Standard installation
pip install --upgrade glaip-sdk

# With local execution support
pip install --upgrade "glaip-sdk[local]"
```

Run inside an elevated PowerShell session if your organisation restricts installs. Use `py -m pip install --upgrade glaip-sdk` when `pip` is not on `PATH`.

#### Poetry (project managed)

```bash
# Standard installation
poetry add glaip-sdk

# With local execution support
poetry add "glaip-sdk[local]"

poetry run aip --version
```

Ideal when the SDK ships with your application code. `poetry run` ensures the CLI uses the project virtual environment.

#### uv tool

```bash
uv tool install glaip-sdk
```

Great for users who prefer reproducible global installs while keeping Python projects isolated.

#### pipx (CLI only)

```bash
pipx install glaip-sdk
pipx ensurepath
```

Deploys the CLI in an isolated environment and keeps your global Python clean. Ideal for operations or QA stations. Recommended for data developers who only need the CLI.

- `--upgrade` (or the equivalent) ensures you pick up the latest release or refresh an existing installation.
- Using a virtual environment? Activate it first, then run the same command.
- Verify the CLI once installed:

```bash
aip --version
```

{% hint style="info" %}
If `pip` is not available as a command, fall back to `python3 -m pip` (Linux/ macOS) or `py -m pip` (Windows). After installing, ensure `~/.local/bin` (Linux/macOS) or `%APPDATA%\Python\Python311\Scripts` (Windows) is on your `PATH` so `aip` resolves.
{% endhint %}

### Configure Access Options

You only need these settings when pointing the SDK or CLI to the **AIP server**. Local runs (using `aip-agents` directly) use the built-in defaults. Choose the option that matches your workflow; each method sets the same API URL and API key, so pick one.

#### .env file (project scoped)

1. Create a `.env` file alongside your project code:

   ```bash
   AIP_API_URL=https://your-aip-instance.com
   AIP_API_KEY=your-api-key-here
   ```

1. Load it with `python-dotenv`, your framework of choice, or a task runner.

1. Ideal when you check environment files into a secure secrets store per project.

#### Shell profile (persistent)

Use when you want the **Python SDK** (scripts/notebooks/CI) available in every terminal.

The `aip` CLI uses account profiles stored in `~/.aip/config.yaml` and does **not** read `AIP_API_URL` / `AIP_API_KEY` from the environment.

- **Linux / macOS:**

  ```bash
  export AIP_API_URL="https://your-aip-instance.com"
  export AIP_API_KEY="your-api-key-here"
  ```

  Add the lines to `~/.bashrc`, `~/.zshrc`, or your shell profile to persist them.

- **Windows PowerShell:**

  ```powershell
  setx AIP_API_URL "https://your-aip-instance.com"
  setx AIP_API_KEY "your-api-key-here"
  ```

  Restart the terminal after running `setx` so the variables are picked up.

#### Interactive CLI (per machine)

Add a profile to store credentials in the CLI config file:

```bash
aip accounts add dev
aip accounts use dev
```

You will be prompted for:

- API URL
- API Key

This is convenient on developer laptops or CI agents that already store the values securely.

{% hint style="info" %}
Configuration precedence:

- CLI: account profiles (`aip accounts ...`) > (deprecated) `--api-url/--api-key` flags.
- Python SDK: `AIP_API_URL`/`AIP_API_KEY` env vars (or `.env`) > library defaults.
{% endhint %}

{% hint style="info" %}
CLI configuration is stored in `~/.aip/config.yaml` (Linux/macOS) or `%USERPROFILE%\\.aip\\config.yaml` (Windows).
{% endhint %}

### Verify Installation

Confirm both the CLI and SDK can reach your AIP instance.

#### CLI

```bash
aip status
```

Expected output includes `✅ Connected to AIP server`.

{% hint style="warning" %}
`aip status` may also report:
{% endhint %}

| Indicator               | Meaning                                                                | Common fix                                                                                                                     |
| ----------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `⚠️ Partial Connection` | DNS/SSL failure or blocked outbound request after the client connects. | Check VPN/proxy settings, verify the API URL in your active account profile (`aip accounts show <name>`), and retry.           |
| `❌ Connection failed`  | Credentials missing or rejected before any data flows.                 | Re-run `aip accounts add <name>` and `aip accounts use <name>`, then rerun the command.                                        |
| `Timed out`             | CLI could not reach the API within the configured timeout.             | Confirm the service is up and adjust `--timeout` if your environment requires longer waits.                                    |

{% hint style="warning" %}
If the error mentions `Temporary failure in name resolution`, your DNS cannot resolve the host—double-check the URL or try again once network connectivity is restored.
{% endhint %}

#### Python SDK

Preferred validation is the Agent-first quick start (`Agent(...)` + `agent.run(...)`).
Use the `Client().ping()` check below for low-level connectivity diagnostics.

```python
from glaip_sdk import Client

client = Client()  # Reads AIP_API_URL and AIP_API_KEY from environment

if client.ping():
    print("✅ Connected to AIP server")
else:
    print("❌ Connection failed")
```

### Security Best Practices

These apply to anyone handling API keys for the platform—whether you are a developer, DevOps engineer, or administrator.

- Use different API keys per environment (development, staging, production).
- Never commit keys to source control—prefer secret managers or CI variables.
- Rotate keys regularly and revoke unused ones promptly.

### Optional CLI Configuration Helpers

Use these after installation when you need to inspect or adjust saved values.

```bash
# List saved accounts
aip accounts list

# Show a specific account
aip accounts show dev

# Add or update accounts interactively
aip accounts add dev
aip accounts use dev

# Update a specific account non-interactively
aip accounts edit dev --url "https://your-aip-instance.com" --key "$AIP_API_KEY"

# Remove an account
aip accounts remove dev
```

### Continue

Ready to run your first agent? Head to the [Quick Start](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide) and follow the Python or CLI track.
