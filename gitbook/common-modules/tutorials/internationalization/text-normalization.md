---
icon: align-right
---

# Text Normalization

This guide explains Unicode text normalization and how to use it with `gllm-intl` to ensure consistent text processing in multilingual applications.

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

## What is Text Normalization?

**Text normalization** is the process of converting text into a standard, canonical form. In Unicode, the same visual character can be represented in multiple ways using different byte sequences. Normalization ensures these equivalent representations are converted to a single consistent form.

#### Example: The Word "café"

The character "é" (e with acute accent) can be represented in two ways:

1. **Precomposed** (single character): `é` → `U+00E9`
2. **Decomposed** (base + combining mark): `e` + `´` → `U+0065` + `U+0301`

Both look identical to humans, but computers see them as different byte sequences:

```python
cafe_precomposed = "café"  # \u00e9
cafe_decomposed = "cafe\u0301"  # e + combining acute

print(cafe_precomposed == cafe_decomposed)  # False! 😱
```

Text normalization solves this problem by converting both representations to the same canonical form.

***

## Why Normalize Text?

#### 1. **String Comparison & Equality**

Without normalization, visually identical strings may not match:

```python
from gllm_intl.text import normalize_text

# Two representations of "café"
text1 = "café"           # Precomposed
text2 = "cafe\u0301"     # Decomposed

print(text1 == text2)    # False ❌

# After normalization
norm1 = normalize_text(text1, "NFC")
norm2 = normalize_text(text2, "NFC")
print(norm1 == norm2)    # True ✅
```

#### 2. **Database Storage & Retrieval**

Ensure consistent storage to prevent duplicate entries:

```python
# Without normalization: these might be stored as different records
users = ["José", "Jose\u0301"]  # Both mean "José"

# With normalization: stored consistently
normalized_users = [normalize_text(user, "NFC") for user in users]
# Both become "José" in the same representation
```

#### 3. **Search & Indexing**

Make search results predictable:

```python
search_query = "naïve"
document_text = "naive\u0308"  # Same word, different encoding

# Without normalization: no match
print(search_query in document_text)  # False ❌

# With normalization: matches correctly
from gllm_intl.text import normalize_text
normalized_query = normalize_text(search_query, "NFC")
normalized_doc = normalize_text(document_text, "NFC")
print(normalized_query in normalized_doc)  # True ✅
```

#### 4. **Text Processing Pipelines**

Ensure consistent input for downstream operations:

```python
from gllm_intl.text import normalize_text

def process_user_input(text: str) -> str:
    # Always normalize at the input boundary
    normalized = normalize_text(text, "NFC")
    # Now safe for tokenization, analysis, etc.
    return normalized.lower().strip()
```

***

## Understanding Unicode Normalization Forms

Unicode defines **four normalization forms**. The `gllm-intl` library supports all of them through the `NormalizationForm` enum.

#### NFC (Canonical Composition) - **Recommended Default**

Combines base characters with combining marks into precomposed forms when possible.

```python
from gllm_intl.text import normalize_text

text = "cafe\u0301"  # e + combining acute
result = normalize_text(text, "NFC")
print(result)  # "café" (single character U+00E9)
```

**Use when:**

* ✅ Storing text in databases
* ✅ Displaying text to users
* ✅ General-purpose text processing

#### NFD (Canonical Decomposition)

Decomposes precomposed characters into base + combining marks.

```python
from gllm_intl.text import normalize_text

text = "café"  # Single character é
result = normalize_text(text, "NFD")
print(result)  # "cafe\u0301" (e + combining acute)
print(repr(result))  # 'cafe\u0301'
```

**Use when:**

* ✅ Removing diacritics (decompose first, then strip combining marks)
* ✅ Linguistic analysis
* ✅ Sorting algorithms

#### NFKC (Compatibility Composition)

Like NFC, but also converts compatibility characters (ligatures, width variants) to standard forms.

```python
from gllm_intl.text import normalize_text

text = "ﬁle"  # fi ligature (U+FB01)
result = normalize_text(text, "NFKC")
print(result)  # "file" (separate f and i)

text2 = "Ｈｅｌｌｏ"  # Full-width characters
result2 = normalize_text(text2, "NFKC")
print(result2)  # "Hello" (standard width)
```

**Use when:**

* ✅ Search functionality (normalizes ligatures, width variants)
* ✅ Case-insensitive comparisons
* ⚠️ Be careful: loses distinction between variants (e.g., full-width vs. half-width)

#### NFKD (Compatibility Decomposition)

Like NFD, but also decomposes compatibility characters.

```python
from gllm_intl.text import normalize_text

text = "²"  # Superscript 2
result = normalize_text(text, "NFKD")
print(result)  # "2" (regular digit)
```

**Use when:**

* ✅ Text analysis requiring maximum decomposition
* ✅ Preparing text for ASCII conversion

#### Comparison Table

| Form     | Canonical | Compatibility | Composed | Common Use                    |
| -------- | --------- | ------------- | -------- | ----------------------------- |
| **NFC**  | ✓         | ✗             | ✓        | **General storage & display** |
| **NFD**  | ✓         | ✗             | ✗        | Diacritic removal, analysis   |
| **NFKC** | ✓         | ✓             | ✓        | Search, case-insensitive ops  |
| **NFKD** | ✓         | ✓             | ✗        | Text analysis, ASCII prep     |

***

## Quick Start

Normalize text in 2 lines:

```python
from gllm_intl.text import normalize_text

normalized = normalize_text("café", "NFC")
print(normalized)  # "café" (consistent form)
```

***

## Normalization Functions

#### `normalize_text()` - Main Normalization Function

Normalize single strings or lists of strings:

```python
from gllm_intl.text import normalize_text, NormalizationForm

# Single string
result = normalize_text("café", NormalizationForm.NFC)
print(result)  # "café"

# Using string form name
result = normalize_text("café", "NFC")
print(result)  # "café"

# List of strings
texts = ["café", "naïve", "résumé"]
results = normalize_text(texts, "NFC")
print(results)  # ["café", "naïve", "résumé"]

# Handle None values (converted to empty string)
result = normalize_text(None, "NFC")
print(result)  # ""

# Mixed list with None
texts = ["café", None, "résumé"]
results = normalize_text(texts, "NFC")
print(results)  # ["café", "", "résumé"]
```

**Parameters:**

* `text`: Single string, list of strings, or None
* `form`: Normalization form (`"NFC"`, `"NFD"`, `"NFKC"`, `"NFKD"`)

**Returns:**

* Same type as input: `str` → `str`, `list` → `list`

***

## Removing Diacritics

Diacritics (accent marks) can be removed for accent-insensitive search and comparison.

#### `remove_diacritics()` - Strip Accent Marks

```python
from gllm_intl.text import remove_diacritics

# Single string
result = remove_diacritics("café")
print(result)  # "cafe"

result = remove_diacritics("naïve")
print(result)  # "naive"

# List of strings
texts = ["café", "résumé", "naïve"]
results = remove_diacritics(texts)
print(results)  # ["cafe", "resume", "naive"]

# Works with various languages
result = remove_diacritics("Ångström")
print(result)  # "Angstrom"
```

#### `normalize_and_strip()` - Normalize + Remove Diacritics

Convenience function that combines both operations:

```python
from gllm_intl.text import normalize_and_strip

# Normalize to NFC, then remove diacritics
result = normalize_and_strip("café")
print(result)  # "cafe"

# Specify normalization form
result = normalize_and_strip("café", "NFD")
print(result)  # "cafe"

# Works with lists
texts = ["café", "résumé", "Ångström"]
results = normalize_and_strip(texts, "NFC")
print(results)  # ["cafe", "resume", "Angstrom"]
```

**Why combine normalization + stripping?**

Diacritic removal works by:

1. Decomposing characters (NFD)
2. Filtering out combining marks
3. Recomposing to NFC

The `normalize_and_strip()` function does this efficiently in one call.

***

## Common Use Cases

#### Use Case 1: Case-Insensitive Search

```python
from gllm_intl.text import normalize_and_strip

def search_insensitive(query: str, documents: list[str]) -> list[str]:
    """Search documents with accent and case insensitivity."""
    # Normalize query
    normalized_query = normalize_and_strip(query, "NFC").lower()

    results = []
    for doc in documents:
        # Normalize each document
        normalized_doc = normalize_and_strip(doc, "NFC").lower()
        if normalized_query in normalized_doc:
            results.append(doc)

    return results

# Example usage
documents = [
    "The café is open",
    "I visited a cafe yesterday",
    "Café culture in Paris",
]

results = search_insensitive("cafe", documents)
print(results)
# ['The café is open', 'I visited a cafe yesterday', 'Café culture in Paris']
```

#### Use Case 2: Database Unique Constraints

```python
from gllm_intl.text import normalize_text

class User:
    def __init__(self, username: str):
        # Always store in normalized form
        self.username = normalize_text(username, "NFC")

    def __eq__(self, other):
        return self.username == other.username

# These will be treated as the same user
user1 = User("José")           # Precomposed
user2 = User("Jose\u0301")     # Decomposed

print(user1 == user2)  # True ✅
```

#### Use Case 3: Slug Generation

```python
from gllm_intl.text import normalize_and_strip

def generate_slug(title: str) -> str:
    """Generate URL-safe slug from title."""
    # Remove diacritics and normalize
    clean_title = normalize_and_strip(title, "NFKC")

    # Convert to lowercase and replace spaces
    slug = clean_title.lower().replace(" ", "-")

    # Remove non-alphanumeric characters (except hyphens)
    slug = "".join(c for c in slug if c.isalnum() or c == "-")

    return slug

# Examples
print(generate_slug("Café Culture"))      # "cafe-culture"
print(generate_slug("Résumé Tips"))       # "resume-tips"
print(generate_slug("Naïve Bayes"))       # "naive-bayes"
```

#### Use Case 4: Email Address Normalization

```python
from gllm_intl.text import normalize_text

def normalize_email(email: str) -> str:
    """Normalize email address for storage and comparison."""
    # Split into local and domain parts
    local, domain = email.split("@")

    # Normalize both parts to NFC
    local = normalize_text(local, "NFC")
    domain = normalize_text(domain, "NFC")

    # Convert to lowercase
    return f"{local}@{domain}".lower()

# Example
email1 = "josé@example.com"
email2 = "jose\u0301@example.com"  # Decomposed é

norm1 = normalize_email(email1)
norm2 = normalize_email(email2)
print(norm1 == norm2)  # True ✅
```

#### Use Case 5: Text Deduplication

```python
from gllm_intl.text import normalize_and_strip

def deduplicate_texts(texts: list[str]) -> list[str]:
    """Remove duplicate texts considering normalization."""
    seen = set()
    unique = []

    for text in texts:
        # Normalize for comparison
        normalized = normalize_and_strip(text, "NFC").lower()

        if normalized not in seen:
            seen.add(normalized)
            unique.append(text)  # Keep original

    return unique

# Example
texts = [
    "café",
    "cafe",
    "café",  # Visually same as first, but might be different encoding
    "CAFÉ",
]

unique = deduplicate_texts(texts)
print(unique)  # ['café'] (only one kept)
```

#### Use Case 6: Batch Processing

```python
from gllm_intl.text import normalize_text

def process_csv_column(values: list[str | None]) -> list[str]:
    """Normalize a CSV column handling None values."""
    # Batch normalize (None becomes empty string)
    normalized = normalize_text(values, "NFC")

    # Further processing
    return [v.strip() for v in normalized]

# Example
csv_data = ["José", None, "María", "", "José"]
cleaned = process_csv_column(csv_data)
print(cleaned)  # ["José", "", "María", "", "José"]
```

***

## Best Practices

#### 1. **Always Use NFC for Storage**

NFC (Canonical Composition) is the recommended form for storing and displaying text:

```python
from gllm_intl.text import normalize_text

# ✅ Good: Normalize before storing
def save_user_name(name: str):
    normalized_name = normalize_text(name, "NFC")
    db.save(normalized_name)
```

#### 2. **Normalize at System Boundaries**

Normalize text as early as possible (at input):

```python
from flask import Flask, request
from gllm_intl.text import normalize_text

app = Flask(__name__)

@app.route("/api/users", methods=["POST"])
def create_user():
    # ✅ Normalize immediately upon receipt
    username = normalize_text(request.json["username"], "NFC")
    email = normalize_text(request.json["email"], "NFC")

    # Rest of logic works with normalized data
    user = User(username=username, email=email)
    db.save(user)
```

#### 3. **Use Batch Processing for Performance**

Process lists instead of individual strings:

```python
from gllm_intl.text import normalize_text

# ❌ Inefficient
results = [normalize_text(text, "NFC") for text in large_list]

# ✅ Efficient (single function call)
results = normalize_text(large_list, "NFC")
```

#### 4. **Combine Normalization with Diacritic Removal for Search**

```python
from gllm_intl.text import normalize_and_strip

# ✅ Best for search indexes
search_terms = ["café", "naïve", "résumé"]
indexed_terms = [
    normalize_and_strip(term, "NFC").lower()
    for term in search_terms
]
# ["cafe", "naive", "resume"]
```

#### 5. **Be Consistent Across Your Application**

Choose one normalization strategy and apply it everywhere:

```python
# config.py
NORMALIZATION_FORM = "NFC"

# utils.py
from gllm_intl.text import normalize_text
from config import NORMALIZATION_FORM

def normalize(text: str) -> str:
    """Application-wide normalization helper."""
    return normalize_text(text, NORMALIZATION_FORM)
```

#### 6. **Document Your Normalization Strategy**

Be explicit in your API documentation:

```python
def create_account(username: str, email: str) -> User:
    """Create a new user account.

    Args:
        username: User's display name (will be normalized to NFC)
        email: User's email address (will be normalized to NFC)

    Returns:
        User: Created user object with normalized fields
    """
    username = normalize_text(username, "NFC")
    email = normalize_text(email, "NFC")
    # ...
```

#### 7. **Test with Real Multilingual Data**

```python
import pytest
from gllm_intl.text import normalize_text

def test_normalization_preserves_meaning():
    """Ensure normalization doesn't corrupt non-Latin scripts."""
    test_cases = [
        ("café", "NFC", "café"),
        ("北京", "NFC", "北京"),  # Chinese
        ("Москва", "NFC", "Москва"),  # Russian
        ("القاهرة", "NFC", "القاهرة"),  # Arabic
    ]

    for text, form, expected in test_cases:
        result = normalize_text(text, form)
        assert result == expected
```
