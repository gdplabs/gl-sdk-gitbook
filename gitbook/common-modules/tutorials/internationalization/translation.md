---
icon: language
---

# Translation

This guide explains translation and how to use `gllm-intl` to localize your applications with message catalogs and multiple locales.

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

## What is Translation?

**Translation** in the context of internationalization (i18n) is the process of adapting text, messages, and content from one language to another while preserving meaning and context. Unlike transliteration (which converts sounds between scripts), translation converts the _meaning_ and _intent_ of messages.

#### Key Concepts:

* **Message ID (msgid)**: A unique key identifying a translatable message (e.g., `"greeting"`)
* **Message String (msgstr)**: The translated text for a specific locale (e.g., `"Hello"` in English, `"Halo"` in Indonesian)
* **Locale**: A language and regional identifier (e.g., `en_US` for US English, `id_ID` for Indonesian)
* **Context**: Additional information to disambiguate identical keys with different meanings
* **Pluralization**: Different message forms based on quantity (e.g., "1 item" vs "2 items")

#### Examples:

| Message ID        | English (`en_US`) | Indonesian (`id_ID`)    | French (`fr_FR`)   |
| ----------------- | ----------------- | ----------------------- | ------------------ |
| `greeting`        | Hello             | Halo                    | Bonjour            |
| `welcome_user`    | Welcome, {name}!  | Selamat datang, {name}! | Bienvenue, {name}! |
| `item` (singular) | 1 item            | 1 item                  | 1 article          |
| `item` (plural)   | {count} items     | {count} item            | {count} articles   |

The `gllm-intl` library uses **GNU gettext** format via **Babel** for industry-standard translation catalog management.

***

### What is a Translation Catalog?

A **translation catalog** is a structured database of translated messages organized by locale. Catalogs use the gettext format, an industry standard for software localization.

#### Catalog File Types:

1.  **`.po` (Portable Object)** - Human-readable source file:

    ```po
    msgid "greeting"
    msgstr "Hello"

    msgid "welcome_user"
    msgstr "Welcome, {name}!"
    ```
2. **`.mo` (Machine Object)** - Compiled binary file used at runtime (generated from `.po`)

#### Catalog Structure:

```
locales/
├── en_US/                  # Locale identifier
│   └── LC_MESSAGES/        # Message category
│       ├── messages.po     # Source (optional)
│       └── messages.mo     # Compiled (required)
├── id_ID/
│   └── LC_MESSAGES/
│       ├── messages.po
│       └── messages.mo
└── fr_FR/
    └── LC_MESSAGES/
        ├── messages.po
        └── messages.mo
```

#### Catalog Features:

| Feature                    | Description                      | Example                                        |
| -------------------------- | -------------------------------- | ---------------------------------------------- |
| **Simple Messages**        | Basic key-value translations     | `msgid "greeting"` → `msgstr "Hello"`          |
| **Variable Interpolation** | Dynamic content injection        | `"Welcome, {name}!"` with `name="Alice"`       |
| **Plural Forms**           | Quantity-aware translations      | `msgid_plural "items"` with count rules        |
| **Contextual Messages**    | Disambiguate identical keys      | `msgctxt "file"` vs `msgctxt "person"`         |
| **Metadata**               | Language, encoding, plural rules | `"Plural-Forms: nplurals=2; plural=(n != 1);"` |

***

### Why Use Translation Catalogs?

#### 1. **Multi-Language Support**

Serve users in their preferred language:

```python
from gllm_intl.translation.shorthands import _

# User with English preference
set_locale("en_US")
print(_("greeting"))  # "Hello"

# User with Indonesian preference
set_locale("id_ID")
print(_("greeting"))  # "Halo"
```

#### 2. **Centralized Management**

Separate translatable content from code:

```python
# ❌ Bad: Hardcoded strings
def greet_user(name: str, lang: str) -> str:
    if lang == "en":
        return f"Welcome, {name}!"
    elif lang == "id":
        return f"Selamat datang, {name}!"
    # ... dozens more languages

# ✅ Good: Catalog-based
def greet_user(name: str) -> str:
    return _("welcome_user", name=name)
```

#### 3. **Professional Translation Workflow**

Enable translators to work independently:

```bash
# 1. Developer extracts messages to .po
pybabel extract -o messages.pot .

# 2. Create locale-specific .po files
pybabel init -i messages.pot -d locales -l id_ID

# 3. Translator edits locales/id_ID/LC_MESSAGES/messages.po
# 4. Compile to .mo
pybabel compile -d locales
```

#### 4. **Plural Form Handling**

Handle language-specific pluralization rules automatically:

```python
from gllm_intl.translation.shorthands import _n

# English: 1 item, 2 items
set_locale("en_US")
print(_n("item", count=1))   # "1 item"
print(_n("item", count=5))   # "5 items"

# Indonesian: no plural distinction
set_locale("id_ID")
print(_n("item", count=1))   # "1 item"
print(_n("item", count=5))   # "5 item"
```

#### 5. **Context Disambiguation**

Differentiate identical words with different meanings:

```python
from gllm_intl.translation.shorthands import _p

# English
set_locale("en_US")
print(_p("name", context="file"))    # "Filename"
print(_p("name", context="person"))  # "Full Name"

# Indonesian
set_locale("id_ID")
print(_p("name", context="file"))    # "Nama Berkas"
print(_p("name", context="person"))  # "Nama Lengkap"
```

***

## Quick Start

Translate in 3 steps:

```python
from gllm_intl.translation.providers import FileSystemLocaleProvider
from gllm_intl.translation.context import configure_i18n, set_locale
from gllm_intl.translation.shorthands import _

# 1. Configure i18n (once at startup)
provider = FileSystemLocaleProvider(
    locales_dir="./locales",
    default_locale="en_US"
)
configure_i18n(provider)

# 2. Set locale for current thread
set_locale("id_ID")

# 3. Use translations
print(_("greeting"))  # "Halo"
```

***

## Setting Up Translation Directory Structure

The `gllm-intl` library uses Babel-style gettext catalogs for storing translations. Each locale requires a specific directory structure.

### Directory Structure

```
locales/
├── en_US/
│   └── LC_MESSAGES/
│       ├── messages.po  (optional, source file)
│       └── messages.mo  (required, compiled catalog)
└── id_ID/
    └── LC_MESSAGES/
        ├── messages.po  (optional, source file)
        └── messages.mo  (required, compiled catalog)
```

### Creating Translation Files

**Create the Directory Structure**

```bash
mkdir -p locales/en_US/LC_MESSAGES
mkdir -p locales/id_ID/LC_MESSAGES
```

**Create `.po` Files (Source Translation Files)**

**`locales/en_US/LC_MESSAGES/messages.po`:**

```po
# English (United States) translations
msgid ""
msgstr ""
"Language: en_US\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"

# Simple message
msgid "greeting"
msgstr "Hello"

# Message with variable interpolation
msgid "welcome_user"
msgstr "Welcome, {name}!"

# Plural forms
msgid "item"
msgid_plural "items"
msgstr[0] "{count} item"
msgstr[1] "{count} items"

# Contextual message (disambiguate same key in different contexts)
msgctxt "file"
msgid "name"
msgstr "Filename"

msgctxt "person"
msgid "name"
msgstr "Full Name"

# Contextual plural
msgctxt "file"
msgid "item"
msgid_plural "items"
msgstr[0] "{count} file"
msgstr[1] "{count} files"
```

**`locales/id_ID/LC_MESSAGES/messages.po`:**

```po
# Indonesian (Indonesia) translations
msgid ""
msgstr ""
"Language: id_ID\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"

# Simple message
msgid "greeting"
msgstr "Halo"

# Message with variable interpolation
msgid "welcome_user"
msgstr "Selamat datang, {name}!"

# Plural forms (Indonesian has no plural distinction, but we still define them)
msgid "item"
msgid_plural "items"
msgstr[0] "{count} item"
msgstr[1] "{count} item"

# Contextual message
msgctxt "file"
msgid "name"
msgstr "Nama Berkas"

msgctxt "person"
msgid "name"
msgstr "Nama Lengkap"

# Contextual plural
msgctxt "file"
msgid "item"
msgid_plural "items"
msgstr[0] "{count} berkas"
msgstr[1] "{count} berkas"
```

**Compile `.po` Files to `.mo` Files**

The library requires compiled `.mo` files. Use Babel's `msgfmt` or `pybabel` to compile:

{% hint style="warning" %}
You may need to prefix the command with `poetry run` or `uv run`.
{% endhint %}

```bash
# Using pybabel (recommended)
pybabel compile -d locales -l en_US -i locales/en_US/LC_MESSAGES/messages.po
pybabel compile -d locales -l id_ID -i locales/id_ID/LC_MESSAGES/messages.po

# Or using msgfmt
msgfmt locales/en_US/LC_MESSAGES/messages.po -o locales/en_US/LC_MESSAGES/messages.mo
msgfmt locales/id_ID/LC_MESSAGES/messages.po -o locales/id_ID/LC_MESSAGES/messages.mo
```

### Alternative: Programmatic Catalog Creation (Testing/Development)

For testing or development, you can create catalogs programmatically using Babel:

```python
from pathlib import Path
from babel.messages.catalog import Catalog
from babel.messages.mofile import write_mo

def create_catalog(locale_dir: Path, locale: str, messages: list[dict]):
    """Create a compiled .mo catalog programmatically."""
    catalog = Catalog(locale=locale, domain="messages")

    for msg in messages:
        catalog.add(
            msg["id"],
            msg["string"],
            context=msg.get("context"),
            flags=msg.get("flags", ())
        )

    lc_messages = locale_dir / locale / "LC_MESSAGES"
    lc_messages.mkdir(parents=True, exist_ok=True)

    mo_path = lc_messages / "messages.mo"
    with mo_path.open("wb") as mo_file:
        write_mo(mo_file, catalog)

# Example usage
locales_dir = Path("./locales")

# Create English catalog
create_catalog(locales_dir, "en_US", [
    {"id": "greeting", "string": "Hello"},
    {"id": "welcome_user", "string": "Welcome, {name}!"},
    {"id": ("item", "items"), "string": ("{count} item", "{count} items")},
])

# Create Indonesian catalog
create_catalog(locales_dir, "id_ID", [
    {"id": "greeting", "string": "Halo"},
    {"id": "welcome_user", "string": "Selamat datang, {name}!"},
    {"id": ("item", "items"), "string": ("{count} item", "{count} item")},
])
```

***

## Initializing a Translation Provider

The `FileSystemLocaleProvider` discovers and loads translation catalogs from your directory structure.

#### Basic Initialization

```python
from gllm_intl.translation.providers import FileSystemLocaleProvider

# Initialize the provider
provider = FileSystemLocaleProvider(
    locales_dir="./locales",           # Path to your locales directory
    backend="babel",                    # Translation backend (currently only "babel" is supported)
    default_locale="en_US",             # Default locale to use for fallbacks
    strict_mode=False,                  # If True, raises errors for missing translations
    backend_config={                    # Optional backend-specific configuration
        "domain": "messages"            # Gettext domain (default: "messages")
    }
)
```

#### Configuration Options

* **`locales_dir`** _(required)_: Absolute or relative path to the directory containing locale subdirectories.
* **`backend`** _(optional)_: Translation backend identifier. Default: `"babel"`.
* **`default_locale`** _(optional)_: Locale to use when requested locale is unavailable. Default: `"en"`.
* **`strict_mode`** _(optional)_:
  * `False` (default): Returns key or empty string for missing translations
  * `True`: Raises `LocaleNotFoundError` or `TranslationKeyError` for missing resources
* **`backend_config`** _(optional)_: Dictionary of backend-specific configuration:
  * `domain`: Gettext domain name (default: `"messages"`)

#### Checking Available Locales

```python
# Check if a specific locale is available
if provider.has_locale("id_ID"):
    print("Indonesian locale is available")

# Get all available locales
available = provider.get_available_locales()
print(f"Available locales: {available}")  # ['en_US', 'id_ID']
```

#### Direct Provider Usage (Without Manager)

You can use the provider directly with explicit locale parameters:

```python
# Get a translation with explicit locale
translation = provider.get_translation("greeting", locale="id_ID")
print(translation)  # "Halo"

# Get plural translation
item_count = provider.get_plural_translation("item", locale="en_US", count=5)
print(item_count)  # "5 items"

# Get contextual translation
filename = provider.get_context_translation("name", locale="en_US", context="file")
print(filename)  # "Filename"

# Get contextual plural translation
file_count = provider.get_context_plural_translation(
    "item", locale="en_US", context="file", count=3
)
print(file_count)  # "3 files"
```

***

## Defining Translations in Code

There are three ways to use translations in your code: **direct provider usage**, **TranslationManager**, and **shorthand functions**.

### Method 1: Direct Provider Usage (Explicit Locale)

Best for: Applications that need explicit control over locale per operation.

```python
from gllm_intl.translation.providers import FileSystemLocaleProvider

provider = FileSystemLocaleProvider(
    locales_dir="./locales",
    default_locale="en_US"
)

# Simple translation with explicit locale
greeting = provider.get_translation("greeting", locale="id_ID")
print(greeting)  # "Halo"

# Translation with variable interpolation
welcome = provider.get_translation("welcome_user", locale="en_US", name="Alice")
print(welcome)  # "Welcome, Alice!"

# Plural translation
items = provider.get_plural_translation("item", locale="en_US", count=3)
print(items)  # "3 items"

# Contextual translation
person_name = provider.get_context_translation("name", locale="en_US", context="person")
file_name = provider.get_context_translation("name", locale="en_US", context="file")
print(person_name)  # "Full Name"
print(file_name)    # "Filename"
```

### Method 2: Translation Manager (Current Locale State)

Best for: Applications with a stable current locale that changes infrequently.

```python
from gllm_intl.translation.manager import TranslationManager
from gllm_intl.translation.providers import FileSystemLocaleProvider

provider = FileSystemLocaleProvider(
    locales_dir="./locales",
    default_locale="en_US"
)

# Create a manager instance
manager = TranslationManager(provider, default_locale="en_US")

# Set the current locale
manager.set_locale("id_ID")
print(f"Current locale: {manager.get_locale()}")  # "id_ID"

# Translations use the current locale automatically
greeting = manager.translate("greeting")
print(greeting)  # "Halo"

welcome = manager.translate("welcome_user", name="Budi")
print(welcome)  # "Selamat datang, Budi!"

# Change locale
manager.set_locale("en_US")

greeting = manager.translate("greeting")
print(greeting)  # "Hello"

# Plural translation
items = manager.translate_plural("item", count=5)
print(items)  # "5 items"

# Contextual translation
person_name = manager.translate_context("name", context="person")
print(person_name)  # "Full Name"

# Contextual plural translation
files = manager.translate_context_plural("item", context="file", count=2)
print(files)  # "2 files"

# Lazy translation (deferred evaluation)
lazy_greeting = manager.translate_lazy("greeting")
manager.set_locale("id_ID")
print(str(lazy_greeting))  # Evaluates to "Halo"
```

⚠️ **Thread Safety Note**: `TranslationManager` instances are not thread-safe. For multi-threaded applications:

* Create a manager instance per request/thread, OR
* Use the provider directly with explicit locale parameters, OR
* Use the global context API (Method 3)

### Method 3: Shorthand Functions (Global Context)

Best for: Web applications and multi-threaded environments with thread-local state.

```python
from gllm_intl.translation.providers import FileSystemLocaleProvider
from gllm_intl.translation.context import configure_i18n, set_locale, get_locale
from gllm_intl.translation.shorthands import _, _n, _p, _np, _l

# Step 1: Configure i18n globally (once at application startup)
provider = FileSystemLocaleProvider(
    locales_dir="./locales",
    default_locale="en_US"
)
configure_i18n(provider)

# Step 2: Set locale for the current thread
set_locale("id_ID")
print(f"Current locale: {get_locale()}")  # "id_ID"

# Step 3: Use shorthand functions (automatically use current thread's locale)

# Simple translation
greeting = _("greeting")
print(greeting)  # "Halo"

# Translation with variables
welcome = _("welcome_user", name="Budi")
print(welcome)  # "Selamat datang, Budi!"

# Plural translation
items = _n("item", count=3)
print(items)  # "3 item"

# Contextual translation
person_name = _p("name", context="person")
file_name = _p("name", context="file")
print(person_name)  # "Nama Lengkap"
print(file_name)    # "Nama Berkas"

# Contextual plural translation
files = _np("item", context="file", count=2)
print(files)  # "2 berkas"

# Lazy translation (re-evaluates on each string conversion)
lazy_greeting = _l("greeting")
set_locale("en_US")
print(str(lazy_greeting))  # "Hello" (evaluated with new locale)
```

***

## Setting Locale Globally and in Context

### Global Configuration (Application Startup)

Configure the i18n system once at application startup:

```python
from gllm_intl.translation.providers import FileSystemLocaleProvider
from gllm_intl.translation.context import configure_i18n, is_i18n_configured

provider = FileSystemLocaleProvider(
    locales_dir="./locales",
    default_locale="en_US"
)

# Configure once at application startup
configure_i18n(provider)

# Check if configured
if is_i18n_configured():
    print("i18n is ready!")
```

⚠️ **Important**: By default, `configure_i18n()` can only be called once. To reconfigure (e.g., in tests):

```python
configure_i18n(new_provider, force=True)  # Allows reconfiguration
```

### Setting Locale for Current Thread

Each thread maintains its own locale context:

```python
from gllm_intl.translation.context import set_locale, get_locale, is_locale_set, clear

# Set locale for current thread
set_locale("id_ID")

# Check if locale is set
if is_locale_set():
    current = get_locale()
    print(f"Current thread locale: {current}")  # "id_ID"

# Clear locale for current thread
clear()
```

### Temporary Locale Context (Context Manager)

Use `locale_context()` to temporarily switch locales:

```python
from gllm_intl.translation.context import set_locale, locale_context
from gllm_intl.translation.shorthands import _

# Set base locale
set_locale("en_US")
print(_("greeting"))  # "Hello"

# Temporarily switch to Indonesian
with locale_context("id_ID"):
    print(_("greeting"))  # "Halo"

    # Nested context
    with locale_context("en_US"):
        print(_("greeting"))  # "Hello"

    print(_("greeting"))  # "Halo" (back to id_ID)

# Back to original locale
print(_("greeting"))  # "Hello"
```

### Multi-Threaded Usage

Each thread has independent locale context:

```python
import threading
from gllm_intl.translation.context import configure_i18n, set_locale
from gllm_intl.translation.shorthands import _
from gllm_intl.translation.providers import FileSystemLocaleProvider

# Configure globally once
provider = FileSystemLocaleProvider(locales_dir="./locales", default_locale="en_US")
configure_i18n(provider)

def worker(locale: str, worker_id: int):
    """Each thread sets its own locale and uses translations independently."""
    set_locale(locale)
    greeting = _("greeting")
    print(f"Worker {worker_id} [{locale}]: {greeting}")

# Create threads with different locales
threads = [
    threading.Thread(target=worker, args=("en_US", 1)),
    threading.Thread(target=worker, args=("id_ID", 2)),
    threading.Thread(target=worker, args=("en_US", 3)),
    threading.Thread(target=worker, args=("id_ID", 4)),
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# Output (order may vary):
# Worker 1 [en_US]: Hello
# Worker 2 [id_ID]: Halo
# Worker 3 [en_US]: Hello
# Worker 4 [id_ID]: Halo
```

### Web Application Example (Flask)

```python
from flask import Flask, request, g
from gllm_intl.translation.context import configure_i18n, set_locale
from gllm_intl.translation.shorthands import _
from gllm_intl.translation.providers import FileSystemLocaleProvider

app = Flask(__name__)

# Configure i18n at application startup
provider = FileSystemLocaleProvider(locales_dir="./locales", default_locale="en_US")
configure_i18n(provider)

@app.before_request
def set_request_locale():
    """Set locale based on request header or user preference."""
    locale = request.headers.get("Accept-Language", "en_US")
    # Parse locale from header (simplified example)
    locale = locale.split(",")[0].replace("-", "_")
    set_locale(locale)
    g.locale = locale

@app.route("/greeting")
def greeting():
    """Return localized greeting."""
    message = _("greeting")
    return {"message": message, "locale": g.locale}

# Example requests:
# GET /greeting with Accept-Language: en-US
# -> {"message": "Hello", "locale": "en_US"}
#
# GET /greeting with Accept-Language: id-ID
# -> {"message": "Halo", "locale": "id_ID"}
```

***

## Best Practices

#### 1. **Use Message IDs, Not English Text**

Use descriptive keys instead of full English text:

```python
# ✅ Good: Semantic message IDs
_("user.greeting")
_("form.submit_button")
_("error.invalid_email")

# ⚠️ Less maintainable: English text as keys
_("Hello")
_("Submit")
_("Invalid email address")
```

#### 2. **Keep Variable Names Consistent**

Use the same variable names across all locales:

```po
# ✅ Good: Consistent variable names
msgid "welcome_user"
msgstr "Welcome, {name}!"  # English

msgid "welcome_user"
msgstr "Selamat datang, {name}!"  # Indonesian

# ❌ Bad: Different variable names
msgstr "Welcome, {username}!"  # English
msgstr "Selamat datang, {nama}!"  # Indonesian
```

#### 3. **Provide Context for Ambiguous Words**

Use `msgctxt` to disambiguate:

```python
# ✅ Good: Context prevents confusion
_p("close", context="button")    # "Close" (verb)
_p("close", context="adjective")  # "Close" (near)

# ❌ Ambiguous without context
_("close")  # Which meaning?
```

#### 4. **Handle Pluralization Properly**

Always use plural-aware functions for counts:

```python
# ✅ Good: Handles all plural forms correctly
_n("item", count=count)

# ❌ Bad: Broken for many languages
f"{count} " + _("item") if count == 1 else _("items")
```

#### 5. **Configure Once, Set Locale Per Request**

In web applications, configure globally and set locale per request:

```python
# ✅ Good: Global config, per-request locale
# app.py
configure_i18n(provider)  # Once at startup

# middleware.py
@app.before_request
def set_request_locale():
    locale = get_user_preferred_locale(request)
    set_locale(locale)

# ❌ Bad: Reconfiguring on every request
@app.before_request
def setup():
    configure_i18n(provider)  # Wasteful
```

#### 6. **Use Lazy Translations for Module-Level Strings**

For strings defined at module level that need runtime evaluation:

```python
from gllm_intl.translation.shorthands import _l

# ✅ Good: Lazy evaluation
ERROR_MESSAGES = {
    "not_found": _l("error.not_found"),
    "unauthorized": _l("error.unauthorized"),
}

# Later, when locale is set
print(str(ERROR_MESSAGES["not_found"]))

# ❌ Bad: Evaluated at import time
ERROR_MESSAGES = {
    "not_found": _("error.not_found"),  # Uses import-time locale
}
```

#### 7. **Test with Multiple Locales**

Include locale switching in your tests:

```python
import pytest
from gllm_intl.translation.context import set_locale
from gllm_intl.translation.shorthands import _

def test_greeting_localization():
    """Test greeting in multiple locales."""
    set_locale("en_US")
    assert _("greeting") == "Hello"

    set_locale("id_ID")
    assert _("greeting") == "Halo"

    set_locale("fr_FR")
    assert _("greeting") == "Bonjour"
```

#### 8. **Document Your Message IDs**

Keep a reference document of message IDs and their purpose:

```python
"""
Message ID Reference
====================

User Interface:
- greeting: Main welcome greeting
- welcome_user: Personalized welcome with name parameter
- logout: Logout button text

Forms:
- form.submit: Submit button
- form.cancel: Cancel button
- form.required: Required field indicator

Errors:
- error.invalid_email: Email validation error
- error.server: Generic server error
"""
```

#### 9. **Handle Missing Translations Gracefully**

Set up appropriate fallbacks:

```python
# ✅ Good: Graceful fallback to default locale
provider = FileSystemLocaleProvider(
    locales_dir="./locales",
    default_locale="en_US",
    strict_mode=False  # Returns key if missing
)

# For production logging
translation = _("some.key")
if translation == "some.key":
    logger.warning(f"Missing translation: {translation}")
```

#### 10. **Extract and Update Catalogs Regularly**

Maintain up-to-date translation files:

```bash
# Extract new messages from code
pybabel extract -F babel.cfg -o messages.pot .

# Update existing catalogs with new messages
pybabel update -i messages.pot -d locales

# Compile after translation
pybabel compile -d locales
```
