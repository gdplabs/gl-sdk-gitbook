# Phrase Matcher Engine

[**`gllm-guardrail`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-guardrail) | **Tutorial**: [.](./ "mention") | **Engine**: Phrase matcher | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_guardrail/index.html)

## What it does

`PhraseMatcherEngine` is a lightweight, rule-based engine that blocks content when it contains any configured **banned phrases**.

Key behavior:

1. **The same banned phrases list is used for both input and output checks.**
2. Matching uses **spaCy PhraseMatcher** if enabled and available, otherwise it falls back to a **regex-based matcher**.

## Cases it can handle

### 1) Banned phrases

Examples of phrases you might ban:

1. Disallowed instructions (e.g., `"make a bomb"`)
2. Sensitive terms or internal keywords (e.g., `"secret password"`)

### 2) Detecting simple patterns (prefix-style)

This engine is phrase-based, but you can still catch many “pattern-like” strings by banning a distinctive prefix.

Example: if you want to filter API keys that look like `sk-xxxxxxxx`, you can add **`"sk-"`** to `banned_phrases`.

{% hint style="warning" %}
This is not a full regex/pattern engine. It works best for **distinctive, stable markers** (prefixes, known tokens, exact phrases).
{% endhint %}

## Use default config

By default:

1. Engine mode is `GuardrailMode.INPUT_ONLY` (checks input only).
2. If spaCy is not installed, the engine uses regex matching automatically.

```python
from gllm_guardrail import PhraseMatcherEngine

engine = PhraseMatcherEngine()
```

## Use custom config

### Custom banned phrases

```python
from gllm_guardrail import PhraseMatcherEngine

engine = PhraseMatcherEngine(banned_phrases=["sk-", "internal-only", "do not share"])
```

### Check both input and output

```python
from gllm_guardrail import BaseGuardrailEngineConfig, GuardrailMode, PhraseMatcherEngine

config = BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.BOTH)
engine = PhraseMatcherEngine(config=config, banned_phrases=["sk-"])
```

## Using spaCy PhraseMatcher

### 1) Install the optional dependency

{% tabs %}
{% tab title="Internal Registry" %}
```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-guardrail[spacy]"
```
{% endtab %}

{% tab title="PyPI Binary" %}
```bash
pip install gllm-guardrail-binary spacy
```
{% endtab %}
{% endtabs %}

### 2) Download a spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 3) Enable spaCy mode in the engine

```python
from gllm_guardrail import PhraseMatcherEngine

engine = PhraseMatcherEngine(
    banned_phrases=["sk-", "secret password"],
    use_spacy=True,
    model_name="en_core_web_sm",
)
```

{% hint style="info" %}
If spaCy fails to initialize (missing model, incompatible environment, etc.), the engine automatically falls back to regex matching.
{% endhint %}
