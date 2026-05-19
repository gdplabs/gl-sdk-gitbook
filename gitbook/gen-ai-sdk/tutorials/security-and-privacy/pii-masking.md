---
icon: masks-theater
---

# PII Masking

## Overview

**PII Masking** is the process of obscuring Personally Identifiable Information (such as names, IDs, and phone numbers) within a text. In the context of Generative AI, this is critical for preventing sensitive user data from being exposed to third-party LLM providers or leaking into training data, ensuring compliance with data privacy regulations.

`gllm-privacy` is designed to robustly detect and anonymize sensitive data. It provides standard detection for global entities (Email, Phone, etc.) and specialized support for **Indonesian entities** (KTP, NPWP, BPJS, etc.). Additionally, it integrates **Named Entity Recognition (NER)** models to detect unstructured entities such as Names, Organizations, and Locations, allowing you to integrate comprehensive privacy protection seamlessly into your GenAI applications.


## Available Recognizers

GL SDK provides several recognizer types, each designed for specific entity detection needs:


### Indonesian Entity Recognizers

| Class | Entity | Description |
| ----- | ------ | ----------- |
| `BPJSNumberRecognizer` | `ID_BPJS` | BPJS healthcare membership number. |
| `CreditCardRecognizer` | `CREDIT_CARD` | Credit/debit card numbers (enhanced Indonesian patterns). |
| `KTPRecognizer` | `ID_KTP` | Indonesian National Identity Card (NIK) number. |

These recognizers are included by default when you initialize `TextAnalyzer()`.

### Remote NER Recognizers

| Class | Backend | Description |
| ----- | ------- | ----------- |
| `GDPLabsNerApiRemoteRecognizer` | GDPLabs NER API | Calls the GDPLabs NER API for entity detection. |
| `ProsaRemoteRecognizer` | Prosa.ai | Sends text to the Prosa NER API for entity detection. |
| `TransformersRecognizer` | HuggingFace | Uses any HF NER model for entity detection. See the NER section above. |


## Installation

{% tabs %}
{% tab title="Install with PIP" %}
```bash
pip install gllm-privacy-binary
```
{% endtab %}

{% tab title="Install with Poetry" %}
```bash
poetry add gllm-privacy-binary
```
{% endtab %}

{% tab title="Install with UV" %}
```bash
uv add gllm-privacy-binary
```
{% endtab %}
{% endtabs %}

## Running Your First Anonymization

In this tutorial, we will detect and anonymize sensitive data using the default recognizers (Regex-based).

{% stepper %}
{% step %}
Create a script called `privacy_quickstart.py`.

```python
import asyncio
from gllm_privacy.pii_detector import TextAnalyzer, TextAnonymizer
from gllm_privacy.pii_detector.constants import Entities
from gllm_privacy.pii_detector.anonymizer import Operation

async def main():
    # 1. Initialize the Analyzer & Anonymizer
    text_analyzer = TextAnalyzer()
    text_anonymizer = TextAnonymizer(text_analyzer)

    # 2. Define input text containing mixed PII
    text = "Halo, nama saya Budi. Nomor KTP saya 3525011212941001. Hubungi budi@example.com atau +628123456789"

    # 3. Define target entities
    entities = [Entities.KTP, Entities.EMAIL_ADDRESS, Entities.PHONE_NUMBER]

    # 4. Run Anonymization
    print("--- Anonymizing ---")
    anonymized_text = await text_anonymizer.run(
        text=text,
        entities=entities,
        operation=Operation.ANONYMIZE
    )
    print(anonymized_text)

    # 5. Run Deanonymization (Restore original values)
    print("\n--- Deanonymizing ---")
    deanonymized_text = await text_anonymizer.run(
        text=anonymized_text,
        operation=Operation.DEANONYMIZE
    )
    print(deanonymized_text)

if __name__ == "__main__":
    asyncio.run(main())
```
{% endstep %}

{% step %}
Run the script

```bash
python privacy_quickstart.py
```
{% endstep %}

{% step %}
The script will output the anonymized text with replaced values, and then restore the original values.

```
--- Anonymizing ---
Halo, nama saya Budi. Nomor KTP saya <ID_KTP_1>. Hubungi <EMAIL_ADDRESS_1> atau <PHONE_NUMBER_1>.

--- Deanonymizing ---
Halo, nama saya Budi. Nomor KTP saya 3525011212941001. Hubungi budi@example.com atau +628123456789.
```
{% endstep %}
{% endstepper %}

{% hint style="info" %}
**Default Behavior:** gllm-privacy uses **reversible placeholders** (e.g., \<ID\_KTP\_1>) by default. This ensures that the same entity is always replaced by the same placeholder, allowing for accurate deanonymization later.\
\
To use **Fake Data** (e.g., generating a fake KTP number instead of a placeholder), initialize the anonymizer with: `TextAnonymizer(text_analyzer, add_default_faker_operators=True)`\\
{% endhint %}

### Enhanced Anonymization with NER

While Regex patterns are highly efficient for structured data like IDs or phone numbers, they struggle with unstructured entities such as Names, Organizations, and Locations which rely on context. To solve this, `gllm-privacy` supports Hugging Face models to provide deep-learning-based PII detection.

{% stepper %}
{% step %}
Installation

To enable NER capabilities, install `gllm-privacy` with the `transformers` extra:

```bash
pip install gllm-privacy-binary[transformers]
```
{% endstep %}

{% step %}
Configure the Transformer Recognizer

We use the `TransformersRecognizer` class to bridge Hugging Face models with our privacy pipeline. In this example, we utilize `cahya/NusaBert-ner`

```python
from gllm_privacy.pii_detector.recognizer import TransformersRecognizer
from gllm_privacy.pii_detector import TextAnalyzer, TextAnonymizer
from gllm_privacy.pii_detector.constants import Entities

# Initialize the recognizer with the specific HF model
model_path = "cahya/NusaBert-ner"
recognizer = TransformersRecognizer(model_path)

# Configure the mapping between Model Labels and Presidio Entities
recognizer.load_transformer(
    **{
        "PRESIDIO_SUPPORTED_ENTITIES": ["LOCATION", "PERSON", "ORGANIZATION"],
        "MODEL_TO_PRESIDIO_MAPPING": {
            "PER": "PERSON",
            "LOC": "LOCATION",
            "GPE": "LOCATION",
            "ORG": "ORGANIZATION",
        },
        "DEFAULT_EXPLANATION": f"Identified by the {model_path} NER model",
    }
)
```
{% endstep %}

{% step %}
Execute Entity Analysis

Next, we inject the transformer recognizer into the `TextAnalyzer`.

```python
# Initialize analyzer with our custom NER recognizer
text_analyzer = TextAnalyzer(additional_recognizers=[recognizer])

text = "Budi Santoso adalah Lead Engineer di PT Samudra Raya di Bandung"

# Run the analysis
results = text_analyzer.analyze(text=text)

print("--- Detected Entities ---")
for res in results:
    detected_word = text[res.start : res.end]
    print(f"[{res.entity_type}] {detected_word} (Score: {res.score:.2f})")

```

**Example Output**:

```
--- Detected Entities ---
[PERSON] Budi Santoso (Score: 1.0)
[LOCATION] Bandung (Score: 0.9900000095367432)
[ORGANIZATION] PT Samudra Raya (Score: 0.9700000286102295)
```
{% endstep %}

{% step %}
Run Anonymization

Once the entities are accurately identified, use the `TextAnonymizer` to mask the sensitive values. This replaces the detected text with secure placeholders.

```python
# Initialize the Anonymizer
text_anonymizer = TextAnonymizer(text_analyzer)

# Run Anonymization
anonymized_text = text_anonymizer.anonymize(text=text)

print("\n--- Anonymized Text ---")
print(anonymized_text)
```

**Example Output:**

```
--- Anonymized Text ---
<PERSON_1> adalah Lead Engineer di <ORGANIZATION_1> di <LOCATION_1>
```
{% endstep %}
{% endstepper %}
