---
title: Set up your OPENAI_API_KEY
---

### Set up your `OPENAI_API_KEY`&#x20;

{% hint style="info" %}
# Get your OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
{% endhint %}

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
