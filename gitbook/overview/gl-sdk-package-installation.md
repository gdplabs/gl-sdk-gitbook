---
icon: cubes
---

# GL SDK Package Installation

## What is the GL SDK Package?

The GL SDK package is a meta package for GenAI, GL Connectors, GL Observability and many more. It acts as a centralized installer for the entire GL SDK family.

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gl-sdk"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-sdk"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-sdk"
```
{% endtab %}
{% endtabs %}

<details>

<summary>Prerequisites</summary>

If you want to try the snippet code in this page:

* Completion of all setup steps listed on the [prerequisites.md](../gen-ai-sdk/prerequisites.md "mention") page.

</details>

## Using a Library in GL SDK

{% stepper %}
{% step %}
Create a script called `main.py`:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
response = asyncio.run(lm_invoker.invoke("What is the capital city of Indonesia?"))
print(f"Response: {response}")
```
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
The script will generate the following output (more or less):

```
[2025-09-17T15:12:36+0700.389 OpenAILMInvoker INFO] Invoking 'OpenAILMInvoker'
[2025-09-17T15:12:42+0700.907 httpx INFO] HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"
Response: Jakarta. (Note: Indonesia has been planning to move its administrative capital to Nusantara in East Kalimantan, but Jakarta remains the capital for now.)
```
{% endstep %}
{% endstepper %}

## Extras

By default, if you install GL SDK you will get `gllm-core` and `gllm-inference`.

To keep the installation lean, GL SDK provides several extras. So you don't have to install libraries you don't need:

1. `genai` = `gllm-privacy`, `gllm-datastore`, `gllm-misc`, `gllm-docproc`, `gllm-retrieval`, `gllm-generation`, `gllm-pipeline`, `gllm-rag`
2. `agent` = `gllm-agent`, `gllm-agents`
3. `gl-connectors` = `gl-connectors`
4. `gl-observability` = `gl-observability`
5. `eval` = `gllm-evals`

You can install the extras as follows:

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gl-sdk[genai, agent]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-sdk[genai, agent]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-sdk[genai, agent]"
```
{% endtab %}
{% endtabs %}
