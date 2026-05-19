---
icon: circle-info
---

# Prerequisites

Before you begin building, ensure your environment is ready with the following components.

{% stepper %}
{% step %}
**Python 3.11+**

Make sure you have [Python](https://www.python.org/downloads/) v3.11 or v3.12 installed along with [pip](https://pip.pypa.io/en/stable/installation/).
{% endstep %}

{% step %}
**Access to GDP Labs' Gen AI SDK repository**\
Access to the private repository is required to run this program. If you need access, kindly submit a ticket to our DevOps team.
{% endstep %}

{% step %}
**API Key for a Deep Researcher model provider**

Contact our DevOps team or the GL Open DeepResearch Team (for GL Open Deep Researcher) to obtain your API key. Afterwards, you can set it as an environment variable. In this example, an OpenAI API key is used.

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
export OPENAI_API_KEY="sk-..."
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
$env:OPENAI_API_KEY = "sk-..."
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
set OPENAI_API_KEY="sk-..."
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
**gcloud CLI**

Please refer to the [installation guide](https://cloud.google.com/sdk/docs/install). After installing, please run `gcloud auth login` to authorize gcloud to access the Cloud Platform with Google user credentials.
{% endstep %}

{% step %}
**Access to Gen AI Google Cloud Repository**

Request access to Gen AI Google Cloud repositories by submitting this [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) (alternatively, from your manager or team lead)
{% endstep %}
{% endstepper %}

## Next Steps

1. Get started with Deep Researcher components: [getting-started.md](getting-started.md "mention")
2. Explore more about deep researcher subclasses and features in [API reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/deep_researcher.html)
