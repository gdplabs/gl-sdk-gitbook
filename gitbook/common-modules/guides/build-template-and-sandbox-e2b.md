---
description: Learn how to Build Template and Create the Sandbox E2B for Code Interpreter
icon: circle-plus
---

# Build Template and Sandbox E2B

## Overview

E2B is an open-source platform for running secure, isolated code execution environments (sandboxes). It provides a cloud infrastructure specifically designed for AI agents, code interpreters, and automated workflows that need to execute un-trusted code safely.

Think of E2B as a **"secure virtual computer on-demand"** where you can:

* Execute code safely without risking your main infrastructure
* Run AI-generated code in isolation
* Process data in temporary, disposable environments
* Build and test applications in clean environments

### Key Concepts

**🏗️ Template**

> A pre-configured environment (like a Docker image) that defines what software, libraries, and configurations your sandbox will have. Templates are reusable blueprints for creating sandboxes.

**🔒 Sandbox**

> A running instance of a template - an isolated, secure virtual machine where code executes. Each sandbox is temporary and disposable.

## Getting Started

Now that you understand what E2B is and how it works, let's get started with the practical steps:

### **Prerequisites**

```
## Access Requirements
1. E2B API Key: API Key for authentication to create sandbox
2. E2B Access Token:  Access Token for Authentication to create the template
3. E2B Domain: Your self-hosted E2B domain (e.g., poc.glair.id)
4. Network Access: Access to E2B API endpoint (https://api.poc.glair.id)
   Notes: Ask to ticket@gdplabs.id for E2B API Key and E2B Access Token

## Knowledge Prerequisites
1. Basic understanding of command-line interface (CLI)
2. Familiarity with Docker and Dockerfile syntax
3. Basic understanding of environment variables
4. Knowledge of REST API concepts

## Software Prerequisites
1. docker  --version # Should show minimum  23.x.x
2. python --version # Should show minimum 3.12.x
```

### Installation

To follow this guide, you will need to install `e2b cli`.

{% tabs %}
{% tab title="Linux, or Windows WSL" %}
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
sudo apt-get install -y nodejs && \
sudo npm install -g @e2b/cli
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
sudo apt-get install -y nodejs && \
sudo npm install -g @e2b/cli
```
{% endtab %}

{% tab title="MacOS" %}
```bash
brew install node@20 && npm install -g @e2b/cli
```
{% endtab %}
{% endtabs %}

Checking Version, run this command

{% tabs %}
{% tab title="Linux, or Windows WSL" %}
<pre class="language-bash"><code class="lang-bash"><strong>node --version &#x26;&#x26; npm --version &#x26;&#x26; e2b --version
</strong></code></pre>
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
node --version && npm --version && e2b --version
```
{% endtab %}

{% tab title="MacOS" %}
```bash
brew install node@20 && npm install -g @e2b/cli
```
{% endtab %}
{% endtabs %}

### **How to Build a Template**

Templates are custom sandbox environments built from Dockerfile specifications. They define the software packages, configurations, and startup scripts for your sandboxes.

{% stepper %}
{% step %}
**Set Environment Variables**

Set these on your local terminal

```
export E2B_ACCESS_TOKEN="sk_e2b_xyz123xxx"
export E2B_API_KEY="e2b_xyz123xxx"
export E2B_DOMAIN=poc.glair.id
```
{% endstep %}

{% step %}
**Create Project Directory**

```bash
# Create template project directory
mkdir my-e2b-template
cd my-e2b-template
```
{% endstep %}

{% step %}
**Create Dockerfile**

Create a file named `e2b.Dockerfile` with your custom configuration:

```docker
# Use E2B code interpreter base image
FROM e2bdev/code-interpreter:latest

# Install additional Python packages

```
{% endstep %}

{% step %}
**Initialize E2B Template**

```bash
E2B_DOMAIN=poc.glair.id e2b template init
```

**Expected Output :**

```
🚀 Initializing Sandbox Template...

? Enter template name (alias): dso-template
Using template name: dso-template
? Select target language for template files: Python (sync)

✅ Generated Python (sync) template files:
   ./template.py
   ./build_dev.py
   ./build_prod.py

📝 Added build scripts to Makefile:
   make e2b:build:dev - Build development template
   make e2b:build:prod - Build production template

🎉 Template initialized successfully!

Template created in: ./dso-template/

You can now build your template using:
   make e2b:build:dev (for development)
   make e2b:build:prod (for production)

Learn more about Sandbox Templates: https://e2b.dev/docs
```
{% endstep %}

{% step %}
**Build the Template**

Build with Custom Startup Command:

```bash
E2B_DOMAIN=poc.glair.id e2b template build -c "/root/.jupyter/start-up.sh"
```

**Expected Output :**

```
✅ Building sandbox template s0gnvgjpiuk8yhjoddt2 finished.

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                                                                                                                                 │
│  You can now use the template to create custom sandboxes.                                                                                                                                                       │
│  Learn more on https://e2b.dev/docs                                                                                                                                                                             │
│                                                                                                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 ────────────────────────────────────────────────────────────────────────────────────────────────── Python SDK ───────────────────────────────────────────────────────────────────────────────────────────────────

   from e2b import Sandbox, AsyncSandbox

   # Create sync sandbox
   sandbox = Sandbox.create("s0gnvgjpiuk8yhjoddt2")

   # Create async sandbox
   sandbox = await AsyncSandbox.create("s0gnvgjpiuk8yhjoddt2")

 ──────────────────────────────────────────────────────────────────────────────────────────────────── JS SDK ─────────────────────────────────────────────────────────────────────────────────────────────────────

   import { Sandbox } from 'e2b'

   // Create sandbox
   const sandbox = await Sandbox.create('s0gnvgjpiuk8yhjoddt2')

 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


```

Save the Template ID (e.g., s0gnvgjpiuk8yhjoddt2) - you'll need it to create sandboxes!
{% endstep %}
{% endstepper %}

### **How to Create a Sandbox**

Once you have a template ID, you can create sandbox instances using Python SDK.

{% stepper %}
{% step %}
Create `.env`, here for the environment variables :

```
E2B_DOMAIN="poc.glair.id"
E2B_API_KEY="e2b_xyz123xxx"
E2B_TEMPLATE_ID="your-template-id"
```
{% endstep %}

{% step %}
Create `sandbox.py`, here for the codes :

<pre class="language-python"><code class="lang-python"><strong>from e2b import Sandbox
</strong>import os
<strong>from dotenv import load_dotenv
</strong>load_dotenv()

# Set environment
os.environ['E2B_DOMAIN'] = os.getenv('E2B_DOMAIN')
os.environ['E2B_API_KEY'] = os.getenv('E2B_API_KEY')

# Create sandbox
sandbox = Sandbox.create(os.getenv('E2B_TEMPLATE_ID'))

print(f"Sandbox ID: {sandbox.sandbox_id}")
print(f"Sandbox is running: {sandbox.is_running()}")

# Execute code using commands API
result = sandbox.commands.run("python -c \"print('Hello from E2B!')\"")
print(f"Output: {result.stdout}")
print(f"Error (if any): {result.stderr}")
print(f"Exit code: {result.exit_code}")

# Clean up
sandbox.kill()
print("Sandbox terminated")
</code></pre>
{% endstep %}

{% step %}
Execute the python script

1. Install dotenv and e2b first on [venv](https://docs.python.org/3/library/venv.html)

```
pip install e2b dotenv
```

2. Run python script using this command

```
python sandbox.py
```

**Expected Output :**

```
Sandbox ID: iibheg5bbtos2lsdbwfjv
Sandbox is running: True
Output: Hello from E2B!

Error (if any):
Exit code: 0
Sandbox terminated
```
{% endstep %}
{% endstepper %}

## Troubleshooting

<details>

<summary>Issue 1: E2B CLI Not Found</summary>

**Error**

```
bash: e2b: command not found
```

**Solution**

```bash
# Check Node.js installation
node --version

# Reinstall E2B CLI globally
npm install -g @e2b/cli

# Verify PATH includes npm global bin
echo $PATH | grep npm

# Add npm global bin to PATH if missing
export PATH="$PATH:$(npm root -g)/../bin"
echo 'export PATH="$PATH:$(npm root -g)/../bin"' >> ~/.bashrc
source ~/.bashrc
```

</details>

<details>

<summary>Issue 2: Authentication Failed</summary>

**Error**

```
Error: Authentication failed. Invalid API key.
```

**Solution**

```bash
# Verify API key is set
echo $E2B_ACCESS_TOKEN

# If empty, set it again
export E2B_ACCESS_TOKEN=sk_e2b_your_actual_token_here

# Test authentication
curl -X GET https://api.${E2B_DOMAIN}/health \
  -H "X-API-Key: ${E2B_ACCESS_TOKEN}"

# If still failing, ask to ticket@gdplabs.id for regenerate API key
```

</details>

<details>

<summary>Issue 3: Template Not Found</summary>

**Error**

```
Error: Template abc123def456 not found
```

**Solution**

```bash
E2B_DOMAIN=poc.glair.id e2b template list

                                                                   Sandbox templates

 Access   Template ID           Template Name         vCPUs  RAM MiB        Created by  Created at  Disk size MiB  Envd version  buildStatus

 Private  fh2gj24e8qjb6kvhme1d                            2     1024  bukhori@glair.id  10/20/2025           5946         0.4.1     uploaded
 Private  s0gnvgjpiuk8yhjoddt2                            2     1024  bukhori@glair.id   11/3/2025           5946         0.4.2     uploaded
```

</details>

<details>

<summary>Issue 4: Python Command Not Found</summary>

**Error**

```bash
$ python sandbox.py
bash: python: command not found
```

**Solution**

````bash
Use python3 Command (Recommended)
Most modern systems use python3 as the default command:
```
$ python3 sandbox.py
```
````

</details>

<details>

<summary>Issue 5: External Managed Environment when install e2b dotenv</summary>

**Error**

```bash
$ pip install e2b dotenv
error : externally-managed-environment

```

**Solution**

```bash
$ pip install e2b dotenv --break-system-packages
```

</details>

{% hint style="success" %}
Congratulations! You have just created your template and sandbox E2B!
{% endhint %}
