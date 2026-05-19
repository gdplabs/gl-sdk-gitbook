---
icon: arrow-right-arrow-left
---

# Transliteration

This guide explains transliteration and how to use `gllm-intl` to convert text between writing systems for multilingual applications.

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

## What is Transliteration?

**Transliteration** is the process of converting text from one writing system (script) to another while preserving pronunciation. Unlike translation (which converts meaning), transliteration converts the _sounds_ or _characters_ of words.

#### Examples:

| Original | Script        | Transliterated | Target Script |
| -------- | ------------- | -------------- | ------------- |
| Москва   | Cyrillic      | Moskva         | Latin         |
| 北京       | Han (Chinese) | Beijing        | Latin         |
| Привет   | Cyrillic      | Privet         | Latin         |
| مرحبا    | Arabic        | mrḥbạ          | Latin         |
| こんにちは    | Hiragana      | Kon'nichiha    | Latin         |

The `gllm-intl` library uses **ICU (International Components for Unicode)** via PyICU for accurate, standards-based transliteration across multiple writing systems.

***

## Why Transliterate Text?

#### 1. **Search & Indexing**

Enable searches in Latin characters for non-Latin content:

```python
from gllm_intl.text import transliterate

# User searches for "moscow"
city_cyrillic = "Москва"
city_latin = transliterate(city_cyrillic, "Latin")
print(city_latin)  # "Moskva"

# Now searchable with latin keywords
if "moscow" in city_latin.lower():
    print("Match found!")
```

#### 2. **URL Slugs & Identifiers**

Create readable, ASCII-safe URLs from any script:

```python
from gllm_intl.text import to_ascii

title = "Путеводитель по Москве"
slug = to_ascii(title).lower().replace(" ", "-")
print(slug)  # "putevoditel-po-moskve"
```

#### 3. **Data Integration**

Convert names and addresses to a common script for processing:

```python
from gllm_intl.text import transliterate

names = ["José", "Иван", "محمد", "李明"]
# Convert all to Latin for consistent processing
latin_names = [transliterate(name, "Latin") for name in names]
print(latin_names)
# ["José", "Ivan", "mḥmd", "Lǐ Míng"]
```

#### 4. **Display Fallbacks**

Show transliterated text when original script fonts are unavailable:

```python
from gllm_intl.text import transliterate

original = "Здравствуйте"
fallback = transliterate(original, "Latin")
print(f"{original} ({fallback})")  # "Здравствуйте (Zdravstvujte)"
```

#### 5. **Cross-Script Communication**

Enable users to type in their preferred script:

```python
from gllm_intl.text import transliterate

# Japanese user types in Hiragana
user_input = "ひらがな"
# Convert to Katakana for display
katakana = transliterate(user_input, "Katakana", source_script="Hiragana")
print(katakana)  # "ヒラガナ"
```

***

## Quick Start

Transliterate in 2 lines:

```python
from gllm_intl.text import transliterate

result = transliterate("Привет мир", "Latin")
print(result)  # "Privet mir"
```

Convert to ASCII:

```python
from gllm_intl.text import to_ascii

result = to_ascii("Привет мир")
print(result)  # "Privet mir"
```

***

## Supported Scripts

The `gllm-intl` library supports transliteration between these scripts via the `SupportedScripts` enum:

```python
from gllm_intl.text import SupportedScripts

# Available scripts
print(list(SupportedScripts))
```

### Supported Scripts:

| Script       | Example    | Description                       |
| ------------ | ---------- | --------------------------------- |
| **Latin**    | `"Hello"`  | Latin/Roman alphabet (a-z)        |
| **Cyrillic** | `"Привет"` | Cyrillic alphabet (Russian, etc.) |
| **Arabic**   | `"مرحبا"`  | Arabic script                     |
| **Greek**    | `"Γειά"`   | Greek alphabet                    |
| **Han**      | `"你好"`     | Chinese characters (Hanzi)        |
| **Hebrew**   | `"שלום"`   | Hebrew script                     |
| **Hiragana** | `"こんにちは"`  | Japanese Hiragana                 |
| **Katakana** | `"コンニチハ"`  | Japanese Katakana                 |

### Common Script Pairs:

ICU provides optimized transliterators for these pairs:

* **Cyrillic → Latin**: Russian, Ukrainian, etc. to Roman letters
* **Arabic → Latin**: Arabic script to Roman letters
* **Greek → Latin**: Greek alphabet to Roman letters
* **Han → Latin**: Chinese to Pinyin
* **Hebrew → Latin**: Hebrew script to Roman letters
* **Hiragana ↔ Katakana**: Japanese script conversion
* **Hiragana/Katakana → Latin**: Japanese to Romanization (Romaji)
* **Any → Latin**: Auto-detect source script, convert to Latin

***

## Basic Transliteration

#### `transliterate()` - Main Function

Convert text between any supported scripts:

```python
from gllm_intl.text import transliterate

# Cyrillic to Latin
result = transliterate("Привет мир", "Latin")
print(result)  # "Privet mir"

# Chinese to Latin (Pinyin)
result = transliterate("北京", "Latin")
print(result)  # "Běi Jīng"

# Greek to Latin
result = transliterate("Γειά σου", "Latin")
print(result)  # "Geia sou"
```

### Specifying Source Script

For better accuracy, specify the source script explicitly:

```python
from gllm_intl.text import transliterate, SupportedScripts

# With source script hint
result = transliterate(
    "مرحبا",
    target_script=SupportedScripts.LATIN,
    source_script=SupportedScripts.ARABIC
)
print(result)  # "mrḥbạ"

# Without hint (auto-detect)
result = transliterate("مرحبا", "Latin")
print(result)  # "mrḥbạ"
```

### Japanese Script Conversion

Convert between Hiragana, Katakana, and Latin:

```python
from gllm_intl.text import transliterate

# Hiragana to Katakana
result = transliterate("こんにちは", "Katakana", source_script="Hiragana")
print(result)  # "コンニチハ"

# Katakana to Hiragana
result = transliterate("カタカナ", "Hiragana", source_script="Katakana")
print(result)  # "かたかな"

# Hiragana to Latin (Romaji)
result = transliterate("ひらがな", "Latin", source_script="Hiragana")
print(result)  # "hiragana"

# Katakana to Latin (Romaji)
result = transliterate("カタカナ", "Latin", source_script="Katakana")
print(result)  # "katakana"
```

### Unicode Characters Preserved

Characters without transliteration mappings remain unchanged:

```python
from gllm_intl.text import transliterate

# Emoji preserved
result = transliterate("Привет 😀", "Latin")
print(result)  # "Privet 😀"

# Punctuation preserved
result = transliterate("Москва, Россия!", "Latin")
print(result)  # "Moskva, Rossiâ!"
```

***

## ASCII Conversion

### `to_ascii()` - Convert Any Script to ASCII

The `to_ascii()` function provides a fallback mechanism to convert any Unicode text to ASCII-safe characters, useful for systems that only support ASCII.

```python
from gllm_intl.text import to_ascii

# Cyrillic
result = to_ascii("Привет мир")
print(result)  # "Privet mir"

# Chinese
result = to_ascii("北京")
print(result)  # "Bei Jing"

# French
result = to_ascii("café")
print(result)  # "cafe"

# Mixed scripts
result = to_ascii("Café в Москве")
print(result)  # "Cafe v Moskve"
```

### Case Preservation

Control case handling with `preserve_case`:

```python
from gllm_intl.text import to_ascii

# Preserve original case (default)
result = to_ascii("CAFÉ", preserve_case=True)
print(result)  # "CAFE"

# Force lowercase
result = to_ascii("CAFÉ", preserve_case=False)
print(result)  # "cafe"

# Mixed case preserved
result = to_ascii("Café", preserve_case=True)
print(result)  # "Cafe"
```

### How Case Preservation Works

```python
from gllm_intl.text import to_ascii

# All uppercase → stays uppercase
print(to_ascii("МОСКВА", preserve_case=True))  # "MOSKVA"

# All lowercase → stays lowercase
print(to_ascii("москва", preserve_case=True))  # "moskva"

# Title case → stays title case
print(to_ascii("Москва", preserve_case=True))  # "Moskva"

# Mixed case → preserved as-is
print(to_ascii("МоСкВа", preserve_case=True))  # "MoSkVa"
```

***

## Advanced Features

### Reusable Transliterators

For repeated operations, create and cache transliterators:

```python
from gllm_intl.text import get_or_create_transliterator

# Create transliterator once
cyrillic_to_latin = get_or_create_transliterator(
    target_script="Latin",
    source_script="Cyrillic"
)

# Reuse for multiple texts
texts = ["Москва", "Санкт-Петербург", "Новосибирск"]
results = [cyrillic_to_latin.transliterate(text) for text in texts]
print(results)
# ["Moskva", "Sankt-Peterburg", "Novosibirsk"]
```

**Note:** Transliterators are automatically cached per thread, so calling `transliterate()` multiple times with the same scripts reuses the cached instance.

### Thread Safety

Transliterators use thread-local storage, making them safe for concurrent use:

```python
import threading
from gllm_intl.text import transliterate

def worker(text: str):
    # Each thread gets its own transliterator cache
    result = transliterate(text, "Latin")
    print(f"{threading.current_thread().name}: {result}")

texts = ["Москва", "Привет", "Санкт-Петербург"]
threads = [threading.Thread(target=worker, args=(text,)) for text in texts]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
```

***

## Common Use Cases

#### Use Case 1: URL Slug Generation

Generate SEO-friendly slugs from any script:

```python
from gllm_intl.text import to_ascii
import re

def generate_slug(title: str) -> str:
    """Generate URL-safe slug from title in any script."""
    # Convert to ASCII
    ascii_title = to_ascii(title, preserve_case=False)

    # Replace spaces with hyphens
    slug = ascii_title.replace(" ", "-")

    # Remove non-alphanumeric characters (except hyphens)
    slug = re.sub(r"[^a-z0-9-]", "", slug)

    # Remove consecutive hyphens
    slug = re.sub(r"-+", "-", slug)

    # Strip leading/trailing hyphens
    return slug.strip("-")

# Examples
print(generate_slug("Путеводитель по Москве"))
# "putevoditel-po-moskve"

print(generate_slug("北京旅游指南"))
# "bei-jing-lu-you-zhi-nan"

print(generate_slug("Café Culture in Paris"))
# "cafe-culture-in-paris"
```

#### Use Case 2: Search Index Creation

Build searchable indexes for non-Latin content:

```python
from gllm_intl.text import to_ascii

class SearchIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id: int, content: str):
        """Add document to search index."""
        # Store original
        original_tokens = content.lower().split()

        # Also index transliterated version
        ascii_content = to_ascii(content, preserve_case=False)
        ascii_tokens = ascii_content.split()

        # Index both versions
        for token in set(original_tokens + ascii_tokens):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def search(self, query: str) -> set[int]:
        """Search for documents."""
        # Search both original and transliterated
        query_lower = query.lower()
        query_ascii = to_ascii(query, preserve_case=False)

        results = set()
        results.update(self.index.get(query_lower, set()))
        results.update(self.index.get(query_ascii, set()))
        return results

# Example usage
index = SearchIndex()
index.add_document(1, "Москва столица России")
index.add_document(2, "Moscow is the capital")
index.add_document(3, "北京是中国的首都")

# Search with Latin characters finds Cyrillic content
print(index.search("moscow"))    # {1, 2}
print(index.search("Москва"))    # {1}
print(index.search("beijing"))   # {3}
```

#### Use Case 3: Name Normalization

Normalize names from various scripts for consistency:

```python
from gllm_intl.text import to_ascii

class Person:
    def __init__(self, name: str):
        self.name = name
        # Store ASCII version for sorting and comparison
        self.name_ascii = to_ascii(name, preserve_case=False)

    def __repr__(self):
        return f"Person(name={self.name!r}, ascii={self.name_ascii!r})"

# Create people with names in different scripts
people = [
    Person("Иван Петров"),
    Person("José García"),
    Person("李明"),
    Person("Ahmed Ali"),
]

# Sort by ASCII version
sorted_people = sorted(people, key=lambda p: p.name_ascii)
for person in sorted_people:
    print(person)

# Output:
# Person(name='Ahmed Ali', ascii='ahmed ali')
# Person(name='Иван Петров', ascii='ivan petrov')
# Person(name='José García', ascii='jose garcia')
# Person(name='李明', ascii='li ming')
```

#### Use Case 4: Multi-Script Form Validation

Validate input across different writing systems:

```python
from gllm_intl.text import to_ascii
import re

def validate_username(username: str) -> bool:
    """Validate username works in ASCII (for compatibility)."""
    # Convert to ASCII
    ascii_username = to_ascii(username, preserve_case=False)

    # Check if valid ASCII username format
    if not re.match(r"^[a-z0-9_-]{3,20}$", ascii_username):
        return False

    return True

# Test various scripts
usernames = [
    ("john_doe", True),
    ("josé123", True),
    ("иван_петров", True),
    ("李明", True),
    ("user@name", False),  # Contains @
]

for username, expected in usernames:
    result = validate_username(username)
    print(f"{username:20} → {result} (expected: {expected})")
```

#### Use Case 5: Display with Romanization

Show original text with romanized version for clarity:

```python
from gllm_intl.text import transliterate

def display_with_romanization(text: str, source_script: str | None = None) -> str:
    """Display text with romanized version in parentheses."""
    romanized = transliterate(text, "Latin", source_script=source_script)

    # Only show romanization if different from original
    if romanized != text:
        return f"{text} ({romanized})"
    return text

# Examples
print(display_with_romanization("Москва"))
# "Москва (Moskva)"

print(display_with_romanization("北京"))
# "北京 (Běi Jīng)"

print(display_with_romanization("Hello"))
# "Hello" (no romanization needed)
```

#### Use Case 6: File Name Sanitization

Create safe file names from any Unicode input:

```python
from gllm_intl.text import to_ascii
import re

def sanitize_filename(filename: str) -> str:
    """Convert filename to ASCII-safe version."""
    # Split into name and extension
    parts = filename.rsplit(".", 1)
    name = parts[0]
    extension = parts[1] if len(parts) > 1 else ""

    # Convert to ASCII
    safe_name = to_ascii(name, preserve_case=False)

    # Replace spaces with underscores
    safe_name = safe_name.replace(" ", "_")

    # Remove invalid characters
    safe_name = re.sub(r"[^a-z0-9_-]", "", safe_name)

    # Reconstruct with extension
    if extension:
        return f"{safe_name}.{extension}"
    return safe_name

# Examples
print(sanitize_filename("Фотография Москвы.jpg"))
# "fotografiia_moskvy.jpg"

print(sanitize_filename("北京旅游.pdf"))
# "bei_jing_lu_you.pdf"

print(sanitize_filename("Café Menu 2024.docx"))
# "cafe_menu_2024.docx"
```

***

## Best Practices

#### 1. **Specify Source Script for Accuracy**

When you know the source script, specify it explicitly:

```python
from gllm_intl.text import transliterate

# ✅ Better: Explicit source script
result = transliterate("مرحبا", "Latin", source_script="Arabic")

# ⚠️ Works but less accurate: Auto-detect
result = transliterate("مرحبا", "Latin")
```

#### 2. **Use `to_ascii()` for System Compatibility**

When dealing with legacy systems that only support ASCII:

```python
from gllm_intl.text import to_ascii

# ✅ Safe for ASCII-only systems
filename = to_ascii("文档.txt", preserve_case=False)
# "wen_dang.txt"
```

#### 3. **Cache Transliterators for Performance**

For bulk operations, reuse transliterator instances:

```python
from gllm_intl.text import get_or_create_transliterator

# ✅ Create once, reuse many times
trans = get_or_create_transliterator("Latin", "Cyrillic")
results = [trans.transliterate(text) for text in large_list]
```

#### 4. **Combine with Normalization**

Normalize before transliterating for consistency:

```python
from gllm_intl.text import normalize_text, transliterate

# ✅ Best practice: normalize first
text = normalize_text("café", "NFC")
result = transliterate(text, "Latin")
```

#### 5. **Handle Mixed Scripts Gracefully**

Not all characters can be transliterated - handle them appropriately:

```python
from gllm_intl.text import to_ascii

def safe_transliterate(text: str) -> str:
    """Transliterate with fallback for untransliterable characters."""
    result = to_ascii(text, preserve_case=True)

    # Remove any remaining non-ASCII characters
    result = "".join(c if ord(c) < 128 else "?" for c in result)

    return result
```

#### 6. **Test with Real Data**

Test transliteration with actual text in target languages:

```python
import pytest
from gllm_intl.text import transliterate

def test_cyrillic_transliteration():
    """Test real Russian words."""
    test_cases = [
        ("Москва", "Moskva"),
        ("Привет", "Privet"),
        ("Здравствуйте", "Zdravstvujte"),
    ]

    for original, expected in test_cases:
        result = transliterate(original, "Latin")
        assert result == expected
```

#### 7. **Document Transliteration Scheme**

Be clear about which transliteration standard you're using:

```python
def romanize_russian(text: str) -> str:
    """Romanize Russian text using ICU Latin transliteration.

    Uses the ICU Cyrillic-Latin transliterator which follows
    ISO 9 / GOST standards for Russian romanization.

    Args:
        text: Russian text in Cyrillic script

    Returns:
        Romanized text in Latin script

    Example:
        >>> romanize_russian("Москва")
        'Moskva'
    """
    return transliterate(text, "Latin", source_script="Cyrillic")
```
