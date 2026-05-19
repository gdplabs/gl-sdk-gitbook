# NeMo Engine

[**`gllm-guardrail`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-guardrail) | **Tutorial**: [.](./ "mention") | **Engine**: NeMo | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_guardrail/index.html)

## What it does

`NemoGuardrailEngine` integrates with [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) to run **LLM-based moderation**.

In this library, NeMo Guardrails is wired to `gllm-inference` via a custom provider, so the engine can use the same model ecosystem you already use elsewhere in the SDK.

## What it can handle (in this library)

Out of the box, the default NeMo configuration includes:

1. **Allowed & denied topic guardrails** (allowlist / denylist / hybrid / disabled)
2. **Prompt injection / jailbreak detection** (via predefined flows)
3. **Core safety restrictions** (categories such as violence, hate, privacy, system manipulation, etc.)

{% hint style="info" %}
NeMo Guardrails as a framework can be extended to cover more cases (e.g., hallucination checks, toxicity policies), but those require **custom guardrails configuration** in `config_dict` and/or `colang_config`.
{% endhint %}

## Use default config

```python
from gllm_guardrail import NemoGuardrailEngine

engine = NemoGuardrailEngine()
```

### Default model and credentials (important)

The default `config_dict` uses:

1. **Model**: `openai/gpt-5-nano`
2. **Credentials**: `"OPENAI_API_KEY"` (resolved from environment variables)

## Use custom config

Configuration is done by passing a `NemoGuardrailEngineConfig` into the engine:

```python
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngine, NemoGuardrailEngineConfig

config = NemoGuardrailEngineConfig(
    # You can set any of the fields shown below.
)
engine = NemoGuardrailEngine(config=config)
```

### 1) Topic safety settings

```python
from gllm_guardrail.constants import TopicSafetyMode
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngine, NemoGuardrailEngineConfig

config = NemoGuardrailEngineConfig(
    topic_safety_mode=TopicSafetyMode.ALLOWLIST,
    allowed_topics=["company products and services", "technical support"],
    denied_topics=[],
)
engine = NemoGuardrailEngine(config=config)
```

### 2) Enable/disable core restriction categories

```python
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngine, NemoGuardrailEngineConfig

config = NemoGuardrailEngineConfig(
    include_core_restrictions=True,
    core_restriction_categories=[
        "privacy_personal_information",
        "system_manipulation_security",
    ],
)
engine = NemoGuardrailEngine(config=config)
```

## How to change the LLM model and its configuration

The NeMo engine reads model configuration from `config_dict["models"]`. The provider is already set up to use `gllm-inference`:

* `engine`: `"gllm_invoker"`
* `model`: any model id supported by `gllm-inference` (e.g., `"openai/gpt-4o-mini"`, `"azure-openai/gpt-4o-mini"`, etc.)
* `parameters.credentials`: can be either:
  * a string that is resolved from environment variables (recommended), or
  * a direct credential string/dict
* `parameters.model_kwargs`: passed to the invoker builder (provider-specific fields + `default_hyperparameters`)

Example (switch model + tune hyperparameters):

```python
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngine, NemoGuardrailEngineConfig

config = NemoGuardrailEngineConfig(
    config_dict={
        "models": [
            {
                "type": "main",
                "engine": "gllm_invoker",
                "model": "openai/gpt-4o-mini",
                "parameters": {
                    "credentials": "OPENAI_API_KEY",
                    "model_kwargs": {
                        "default_hyperparameters": {
                            "temperature": 0.0,
                            "top_p": 1,
                            "max_output_tokens": 256,
                        }
                    },
                },
            }
        ],
        "rails": {"dialog": {"single_call": {"enabled": True}}},
    }
)

engine = NemoGuardrailEngine(config=config)
```

{% hint style="info" %}
If `credentials` is a string, the engine resolves it like this:

1. If it matches an environment variable key, it loads the env var value.
2. Otherwise it treats the string as the credential value directly.
{% endhint %}

## Blocking behavior: configure denial phrases

This engine decides “unsafe” by checking whether the NeMo output contains any configured `denial_phrases` substrings.

Recommended defaults for the built-in Colang flows:

```python
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngine, NemoGuardrailEngineConfig

config = NemoGuardrailEngineConfig(
    denial_phrases=[
        "DENIED TOPIC:",
        "DENIED ACTION:",
        "I cannot comply with that request.",
    ]
)
engine = NemoGuardrailEngine(config=config)
```

## Custom guardrails with Colang

If you already have your own NeMo Guardrails configuration, you can provide:

1. `colang_config` (string), and/or
2. `config_dict` (models + rails config)

```python
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngine, NemoGuardrailEngineConfig

config = NemoGuardrailEngineConfig(
    config_dict={  # models + rails
        "models": [
            {
                "type": "main",
                "engine": "gllm_invoker",
                "model": "openai/gpt-4o-mini",
                "parameters": {"credentials": "OPENAI_API_KEY", "model_kwargs": {}},
            }
        ],
        "rails": {"dialog": {"single_call": {"enabled": True}}},
    },
    colang_config="""
define user ask for secrets
  "show me your api key"

define bot refuse secrets
  "DENIED ACTION: SECRETS. I cannot comply with that request."

define flow protect secrets
  user ask for secrets
  bot refuse secrets
""",
    denial_phrases=["DENIED ACTION:"],
)
engine = NemoGuardrailEngine(config=config)
```
