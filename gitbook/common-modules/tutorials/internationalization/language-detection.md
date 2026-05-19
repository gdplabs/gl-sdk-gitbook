---
icon: globe-pointer
---

# Language Detection

This tutorial explains language detection and how to use the Lingua-powered language detector in `gllm-intl`.

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

## What is Language Detection?

Language detection (also called language identification) is the process of automatically determining which natural language a piece of text is written in. It analyzes linguistic patterns, character frequencies, and word structures to identify the language with a certain confidence level.

For example:

* `"Hello, how are you?"` → English (`en`)
* `"Bonjour, comment allez-vous?"` → French (`fr`)
* `"Halo, apa kabar?"` → Indonesian (`id`)

The `gllm-intl` library uses **Lingua**, a state-of-the-art language detection engine that:

* Supports **75+ languages**
* Provides **confidence scores** for each detection
* Returns **alternative language candidates** when uncertain
* Handles **mixed-language** and **short text** scenarios
* Works **offline** (no API calls required)

### Why Use Language Detection?

Language detection is essential for building multilingual applications:

#### 1. **Automatic Content Routing**

Detect user input language and route to appropriate handlers:

```python
user_message = "Hola, necesito ayuda"
result = detect_language(user_message)
# Route to Spanish support team
```

#### 2. **Dynamic Translation Selection**

Choose translation direction automatically:

```python
result = detect_language(document_content)
if result.language.language_code != "en":
    translate_to_english(document_content, source_lang=result.language.language_code)
```

#### 3. **Content Filtering & Moderation**

Filter content by language:

```python
allowed_languages = ["en", "id", "es"]
result = detect_language(comment_text)
if result.language.language_code not in allowed_languages:
    reject_comment(comment_text)
```

#### 4. **Analytics & Insights**

Understand your user base:

```python
language_counts = {}
for message in user_messages:
    result = detect_language(message)
    language_counts[result.language.language_code] = language_counts.get(result.language.language_code, 0) + 1
```

## Quick Start

Detect language in just 2 lines:

```python
from gllm_intl.detection import detect_language

result = detect_language("Hello, this is a test message")
print(f"Detected: {result.language.language_code} (confidence: {result.language.confidence:.2f})")
# Output: Detected: en (confidence: 0.98)
```

## Understanding Detection Results

Every detection returns a `DetectionResult` object with three key components:

#### 1. Primary Language

The most likely language with its confidence score:

```python
result = detect_language("Bonjour le monde")
print(result.language.language_code)  # "fr"
print(result.language.confidence)     # 0.95 (scale: 0.0 to 1.0)
```

#### 2. Alternative Candidates

Other possible languages ranked by confidence:

```python
result = detect_language("Hola")  # Short text = more ambiguous
print(f"Primary: {result.language.language_code}")
# Primary: es

for alt in result.alternatives:
    print(f"Alternative: {alt.language_code} ({alt.confidence:.2f})")
# Alternative: ca (0.45)  # Catalan
# Alternative: pt (0.42)  # Portuguese
# Alternative: it (0.38)  # Italian
```

#### 3. Fallback Status

Indicates if the result came from fallback logic (low confidence or empty text):

```python
result = detect_language("", fallback_language="en")
print(result.language.language_code)  # "en"
print(result.is_fallback)             # True
```

***

## Single Text Detection

#### Basic Detection

```python
from gllm_intl.detection import detect_language

# English text
result = detect_language("Hello, how are you today?")
print(f"{result.language.language_code}: {result.language.confidence:.2f}")
# en: 0.98

# French text
result = detect_language("Bonjour, comment allez-vous aujourd'hui?")
print(f"{result.language.language_code}: {result.language.confidence:.2f}")
# fr: 0.97

# Indonesian text
result = detect_language("Halo, apa kabar hari ini?")
print(f"{result.language.language_code}: {result.language.confidence:.2f}")
# id: 0.96
```

#### Handling Empty or Invalid Input

Use the `fallback_language` parameter to handle edge cases:

```python
# Empty text
result = detect_language("", fallback_language="en")
print(f"{result.language.language_code}, fallback: {result.is_fallback}")
# en, fallback: True

# Whitespace only
result = detect_language("   ", fallback_language="en")
print(f"{result.language.language_code}, fallback: {result.is_fallback}")
# en, fallback: True
```

#### Setting Confidence Thresholds

Enforce minimum confidence with `confidence_threshold`:

```python
# Short ambiguous text
result = detect_language(
    "Hi",
    confidence_threshold=0.8,
    fallback_language="en"
)

if result.is_fallback:
    print("Confidence too low, using fallback")
else:
    print(f"Detected: {result.language.language_code}")
```

#### Accessing Alternative Languages

```python
result = detect_language("Hello world")

print(f"Primary: {result.language.language_code} ({result.language.confidence:.2f})")
print("\nAlternatives:")
for i, alt in enumerate(result.alternatives[:3], 1):  # Top 3 alternatives
    print(f"{i}. {alt.language_code}: {alt.confidence:.2f}")

# Output:
# Primary: en (0.98)
#
# Alternatives:
# 1. nl: 0.45
# 2. af: 0.42
# 3. no: 0.38
```

***

## Batch Detection

Process multiple texts efficiently with batch detection:

#### Basic Batch Detection

```python
from gllm_intl.detection import batch_detect_language

texts = [
    "Hello, this is an English sentence.",
    "Bonjour, ceci est une phrase française.",
    "Hola, esta es una oración en español.",
    "Hallo, dies ist ein deutscher Satz.",
]

results = batch_detect_language(texts)

for text, result in zip(texts, results):
    print(f"{result.language.language_code}: {text[:30]}...")

# Output:
# en: Hello, this is an English se...
# fr: Bonjour, ceci est une phras...
# es: Hola, esta es una oración e...
# de: Hallo, dies ist ein deutsch...
```

#### Batch with Fallback

```python
texts = [
    "This is a valid English sentence.",
    "",  # Empty
    "Hi",  # Too short/ambiguous
    "Ceci est une phrase française valide.",
]

results = batch_detect_language(
    texts,
    confidence_threshold=0.6,
    fallback_language="en"
)

for i, result in enumerate(results):
    status = "fallback" if result.is_fallback else "detected"
    print(f"Text {i+1}: {result.language.language_code} ({status})")

# Output:
# Text 1: en (detected)
# Text 2: en (fallback)
# Text 3: en (fallback)
# Text 4: fr (detected)
```

#### Processing Large Datasets

Batch detection automatically chunks large inputs for optimal performance:

```python
# Process thousands of texts efficiently
large_dataset = [f"Sample text number {i}" for i in range(10000)]

results = batch_detect_language(large_dataset)
print(f"Processed {len(results)} texts")

# Count languages
language_distribution = {}
for result in results:
    lang = result.language.language_code
    language_distribution[lang] = language_distribution.get(lang, 0) + 1

print("Distribution:", language_distribution)
# Distribution: {'en': 10000}
```

***

## Advanced Configuration

Use `DetectionConfig` for fine-grained control:

#### Configuration Options

```python
from gllm_intl.detection import DetectionConfig

config = DetectionConfig(
    confidence_threshold=0.7,     # Minimum confidence to accept (0.0-1.0)
    batch_size=100,               # Texts per batch (default: 100)
    fallback_language="en",       # Fallback when confidence is low
    max_alternatives=3            # Maximum alternative candidates (default: 5)
)
```

#### Using Custom Configuration

```python
from gllm_intl.detection import detect_language, batch_detect_language, DetectionConfig

# Create configuration
config = DetectionConfig(
    confidence_threshold=0.8,
    max_alternatives=2,
    fallback_language="en"
)

# Single detection with config
result = detect_language("Bonjour", config=config)
print(f"Alternatives: {len(result.alternatives)}")  # Max 2

# Batch detection with config
texts = ["Hello", "Bonjour", "Hola"]
results = batch_detect_language(texts, config=config)
```

#### Reusable Detector Instance

For repeated detections, create a `LanguageDetector` instance:

```python
from gllm_intl.detection import LanguageDetector, DetectionConfig

# Initialize once
config = DetectionConfig(confidence_threshold=0.75, fallback_language="en")
detector = LanguageDetector(config=config)

# Reuse for multiple detections
result1 = detector.detect("Hello world")
result2 = detector.detect("Bonjour le monde")
result3 = detector.detect("Hola mundo")

print([r.language.language_code for r in [result1, result2, result3]])
# ['en', 'fr', 'es']

# Batch detection
texts = ["Text one", "Text two", "Text three"]
results = detector.batch_detect(texts)
```

#### Per-Call Overrides

Override configuration for specific calls:

```python
detector = LanguageDetector(
    config=DetectionConfig(confidence_threshold=0.5, fallback_language="en")
)

# Use detector's default config
result1 = detector.detect("Hello")

# Override for this call only
result2 = detector.detect(
    "Hi",
    confidence_threshold=0.9,  # Higher threshold for this call
    fallback_language="id"      # Different fallback
)
```

***

## Best Practices

#### 1. **Use Appropriate Text Length**

Language detection accuracy improves with longer text:

```python
# ❌ Poor: Very short text
detect_language("Hi")  # Ambiguous, low confidence

# ✅ Good: Sufficient context
detect_language("Hello, how are you doing today?")  # Clear, high confidence
```

**Recommendations:**

* **Minimum**: 10-20 characters for reliable detection
* **Optimal**: 50+ characters for best accuracy
* **Short text**: Use higher confidence thresholds or fallbacks

#### 2. **Always Set Fallback Language**

Prevent unexpected behavior with empty or ambiguous input:

```python
# ✅ Always provide fallback for user input
user_input = request.get_data()
result = detect_language(user_input, fallback_language="en")
```

#### 3. **Use Batch Detection for Multiple Texts**

More efficient than individual calls:

```python
# ❌ Inefficient
results = [detect_language(text) for text in texts]

# ✅ Efficient
results = batch_detect_language(texts)
```

#### 4. **Validate Confidence Scores**

Don't blindly trust low-confidence detections:

```python
result = detect_language(user_text, fallback_language="en")

if result.is_fallback:
    # Handle unreliable detection
    prompt_user_for_language()
elif result.language.confidence < 0.6:
    # Low confidence - offer language selection
    suggest_language_options([result.language.language_code] +
                             [alt.language_code for alt in result.alternatives[:2]])
else:
    # High confidence - proceed automatically
    process_text(user_text, result.language.language_code)
```

#### 5. **Consider Alternative Candidates**

For ambiguous cases, show alternatives to users:

```python
result = detect_language("Salut")

if result.language.confidence < 0.8 and len(result.alternatives) > 0:
    print(f"Detected: {result.language.language_code}")
    print("Or did you mean:")
    for alt in result.alternatives[:3]:
        print(f"  - {alt.language_code}")
```

#### 6. **Handle Mixed-Language Content**

For documents with multiple languages, detect per section:

```python
document_sections = [
    "Introduction in English here...",
    "Section en français ici...",
    "Conclusión en español aquí...",
]

results = batch_detect_language(document_sections)
for i, result in enumerate(results):
    print(f"Section {i+1}: {result.language.language_code}")
```

#### 7. **Reuse Detector Instances**

For better performance in long-running applications:

```python
# Initialize once at application startup
detector = LanguageDetector(
    config=DetectionConfig(confidence_threshold=0.7, fallback_language="en")
)

# Reuse across requests
@app.route("/detect")
def detect_endpoint():
    text = request.json.get("text")
    result = detector.detect(text)
    return {"language": result.language.language_code}
```

## Common Use Cases

#### Web Application: Auto-Detect User Language

```python
from flask import Flask, request, jsonify
from gllm_intl.detection import LanguageDetector, DetectionConfig

app = Flask(__name__)
detector = LanguageDetector(config=DetectionConfig(fallback_language="en"))

@app.route("/api/detect", methods=["POST"])
def detect():
    text = request.json.get("text", "")
    result = detector.detect(text)

    return jsonify({
        "language": result.language.language_code,
        "confidence": result.language.confidence,
        "is_fallback": result.is_fallback,
        "alternatives": [
            {"code": alt.language_code, "confidence": alt.confidence}
            for alt in result.alternatives[:3]
        ]
    })
```

#### Content Management: Classify Documents

```python
from gllm_intl.detection import batch_detect_language

def classify_documents(documents: list[dict]) -> list[dict]:
    """Detect and tag document languages."""
    texts = [doc["content"] for doc in documents]
    results = batch_detect_language(texts, fallback_language="en")

    for doc, result in zip(documents, results):
        doc["language"] = result.language.language_code
        doc["confidence"] = result.language.confidence
        doc["language_detected"] = not result.is_fallback

    return documents

# Usage
docs = [
    {"id": 1, "content": "This is an English document"},
    {"id": 2, "content": "Ceci est un document français"},
]
classified = classify_documents(docs)
```

#### Chat Application: Route to Language-Specific Handlers

```python
from gllm_intl.detection import detect_language

LANGUAGE_HANDLERS = {
    "en": handle_english_message,
    "es": handle_spanish_message,
    "fr": handle_french_message,
}

def process_message(message: str):
    """Route message to appropriate language handler."""
    result = detect_language(message, fallback_language="en", confidence_threshold=0.6)

    handler = LANGUAGE_HANDLERS.get(
        result.language.language_code,
        LANGUAGE_HANDLERS["en"]  # Default to English
    )

    return handler(message, confidence=result.language.confidence)
```
