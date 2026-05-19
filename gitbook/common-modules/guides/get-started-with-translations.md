---
icon: language
---

# Get Started with Translations

This guide will walk you through the process of getting started with translations.

<details>

<summary>Prerequisites</summary>

1. Complete the [prerequisites.md](../../gen-ai-sdk/prerequisites.md "mention").
2. A compiled translation catalog. We are using the **Babel/gettext** format, which uses `.mo` files.
   1. If you don't have one, don't worry! We have already prepared one for you.

</details>

{% include "../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/GDP-ADMIN/gl-sdk-cookbook/tree/main/gen-ai/examples/i18n" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-intl
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-intl
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" python-dotenv gllm-intl
```
{% endtab %}
{% endtabs %}

## Quickstart

{% stepper %}
{% step %}
**Prepare your project**

Set up your project folder as follows.

You can use your own translation files, or use our pre-prepared translation files below.

{% file src="../../.gitbook/assets/locales.zip" %}

```
<project-name>/
├── locales/
│   ├── en_US/LC_MESSAGES/messages.mo   # English (US) locale
│   ├── id_ID/LC_MESSAGES/messages.mo   # Indonesian locale
│   ├── [other locales...]
└── main.py
```
{% endstep %}

{% step %}
**Implementation**

In your `main.py`, configure the provider to point at your locale folder, and set the locale. That's literally it! :tada:

```python
from gllm_intl import _, configure_i18n, set_locale
from gllm_intl.translation.providers import FileSystemLocaleProvider

configure_i18n(FileSystemLocaleProvider(locales_dir="./locales"))
set_locale("id_ID")
print(_("greeting"))  # "Halo"
```
{% endstep %}
{% endstepper %}

## What's next?

1.  **Need explicit locale control?** Use the provider directly:

    ```python
    provider.get_translation("greeting", locale="en_US")
    ```
2.  **Building a web app?** Set locale per request:

    ```python
    @app.before_request
    def setup_locale():
        set_locale(request.headers.get("Accept-Language", "en_US"))
    ```
3.  **Temporary locale switch?** Use a context manager:

    ```python
    with locale_context("id_ID"):
        print(_("greeting"))  # "Halo"
    ```

For more information, visit [internationalization](../tutorials/internationalization/ "mention").
