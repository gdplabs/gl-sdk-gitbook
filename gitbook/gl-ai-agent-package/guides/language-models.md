---
icon: messages-question
---

# Language Models

AIP language models are catalog entries stored in `language_models`. They can be seeded (`account_id = null`) or owned by a tenant.
This page reflects the current BYOK contract from PR 983 and the current SDK behavior.

{% hint style="info" %}
At a glance:
- Catalog CRUD is REST-based.
- `client.list_language_models()` and `aip models list` are read-only.
- `language_model_id` is the canonical agent reference for shared catalog entries.
- Legacy aliases (`provider`, `lm_name`, `lm_display_name`, and `agent_config.lm_provider/lm_name`) still work.
- API responses intentionally omit `base_url` and `credentials`.
- See the platform capability matrix for interface coverage and feature support.
{% endhint %}

## SDK vs API Vocabulary

The page uses two related but different surfaces:

- **SDK local execution** uses `Agent(model=...)` and `Model(...)` for direct runtime config.
- **AIP API / server execution** uses `language_model_id` or `provider` + `model_name` to resolve a shared catalog entry.
- **Catalog records** use `lm_invoker_type`, `name`, and display/provider labels.

## Discover Language Models

Use this when you want to inspect what the current API key can see.

```python
from glaip_sdk import Client

client = Client()
for model in client.list_language_models(force_refresh=True):
    print(model["id"], model["provider_name"], model["display_name"])
```

```bash
aip models list
```

{% hint style="info" %}
Visibility depends on the API key:
- master key: seeded models by default, or any account with `account_id=<uuid>`
- tenant key: seeded models plus models owned by that tenant
{% endhint %}

The list response includes the model UUID, provider labels, model name, display name, and hyperparameters. It does not include `base_url` or `credentials`.

`force_refresh=True` bypasses the SDK's short-lived list cache, which is useful immediately after you create or update a language model.

## Language Model Record Shape

### Canonical fields

| Field | Meaning |
| --- | --- |
| `lm_invoker_type` | Canonical runtime invoker. Examples: `openai`, `azure-openai`, `openai-compatible`. |
| `name` | Canonical model slug used by the invoker. Example: `gpt-4.1`, `Qwen/Qwen3-30B-A3B`. |
| `provider_name` | Tenant-scoped unique key. Defaults to `<lm_invoker_type>-<name>`. |
| `provider_display_name` | Provider label shown in UI. Defaults to `provider_name`. |
| `display_name` | Model label shown in UI. Defaults to `provider_name`. |
| `hyperparameters` | Default model parameters like `temperature`, `top_p`, or reasoning config. |
| `base_url` | Optional provider endpoint. |
| `credentials` | API key or other secret material. Hidden from API responses. |

### Accepted aliases

| Canonical field | Accepted alias |
| --- | --- |
| `lm_invoker_type` | `provider` |
| `name` | `lm_name` |
| `display_name` | `lm_display_name` |

{% hint style="warning" %}
For `openai-compatible`, slash-qualified names are accepted as-is. For other invokers, slash-qualified names must match the invoker prefix.
{% endhint %}

### Defaulting behavior

The service fills in values when they are omitted:

| Missing field | Default |
| --- | --- |
| `provider_name` | `<lm_invoker_type>-<name>` |
| `provider_display_name` | `provider_name` |
| `display_name` | `provider_name` |
| `hyperparameters` | `{}` |

## Create, Update, Delete

Use the REST API for catalog writes. The auth key decides whether the record is seeded or tenant-owned.

{% hint style="warning" %}
The examples below use placeholders only. Never place real credentials in docs, scripts, or shell history. Load them from environment variables or a secret store.
{% endhint %}

### Create

```bash
curl --location "$AIP_API_URL/language-models/" \
  --header "Content-Type: application/json" \
  --header "X-API-Key: $AIP_API_KEY" \
  --data '{
    "lm_invoker_type": "openai-compatible",
    "name": "google/gemma-4-31B-it",
    "display_name": "Gemma 4 31B IT",
    "base_url": "https://api.deepinfra.com/v1/openai",
    "credentials": "your-api-key-here",
    "hyperparameters": {
      "temperature": 0.5,
      "top_p": 0.95
    }
  }'
```

### Update

Use `PUT /language-models/{lm_id}`. The payload is optional-by-field, so omitted fields are preserved.

```bash
curl --location --request PUT "$AIP_API_URL/language-models/$LM_ID" \
  --header "Content-Type: application/json" \
  --header "X-API-Key: $AIP_API_KEY" \
  --data '{
    "display_name": "Gemma 4 31B IT (AIP)",
    "hyperparameters": {
      "temperature": 0.2
    }
  }'
```

### Delete

```bash
curl --location --request DELETE "$AIP_API_URL/language-models/$LM_ID" \
  --header "X-API-Key: $AIP_API_KEY"
```

{% hint style="info" %}
Creation is scoped by the API key used:
- tenant key creates a tenant-owned model
- master key creates a seeded model

Updates and deletes are limited to the caller's scope.
{% endhint %}

### Response example

```json
{
  "id": "8cfc2f58-1f1e-4f38-b7d8-4a4e8df8ad5d",
  "account_id": null,
  "lm_invoker_type": "openai-compatible",
  "provider": "openai-compatible",
  "provider_name": "openai-compatible-google-gemma-4-31B-it",
  "provider_display_name": "openai-compatible-google-gemma-4-31B-it",
  "name": "google/gemma-4-31B-it",
  "lm_name": "google/gemma-4-31B-it",
  "display_name": "Gemma 4 31B IT",
  "lm_display_name": "Gemma 4 31B IT",
  "hyperparameters": {
    "temperature": 0.5,
    "top_p": 0.95
  }
}
```

## Scope Rules

| Action | Master key | Tenant key |
| --- | --- | --- |
| List | Seeded only by default, or any account with `account_id` | Seeded + own models |
| Get by ID | Any model | Seeded + own models |
| Create | Seeded model | Tenant-owned model |
| Update/Delete | Seeded models only | Own models only |

The list endpoint also supports `account_id`, `offset`, `limit`, and deprecated `skip`.

## Validation Rules

The current backend validates these rules on create/update:

1. `lm_invoker_type` or legacy `provider` must be present on create.
2. `name` or legacy `lm_name` must be present on create.
3. If both canonical and legacy aliases are provided, they must match.
4. `provider_name`, `provider_display_name`, and `display_name` must be unique within the current account scope.
5. Seeded models (`account_id = null`) also enforce unique `(lm_invoker_type, name)` pairs.
6. `openai-compatible` allows slash-qualified model names without matching the invoker prefix rule.
7. Other invokers require slash-qualified names to start with the invoker prefix.

### Common validation examples

```json
{
  "lm_invoker_type": "openai",
  "name": "gpt-4o",
  "provider_name": "my-openai-model",
  "display_name": "My OpenAI Model"
}
```

```json
{
  "lm_invoker_type": "anthropic",
  "provider": "anthropic",
  "name": "claude-sonnet-4-5"
}
```

```json
{
  "lm_invoker_type": "openai",
  "provider": "anthropic",
  "name": "claude-sonnet-4-5"
}
```

## Attach Models to Agents

For config agents, the API accepts exactly one language-model mechanism:

1. `language_model_id`
2. `provider` + `model_name`
3. legacy `agent_config.lm_provider` + `agent_config.lm_name`

`language_model_id` is the canonical choice for shared catalog entries.

```json
{
  "name": "support-agent",
  "type": "config",
  "framework": "langchain",
  "language_model_id": "<uuid>"
}
```

```json
{
  "name": "support-agent",
  "type": "config",
  "framework": "langchain",
  "provider": "openai",
  "model_name": "gpt-4.1"
}
```

```json
{
  "name": "support-agent",
  "type": "config",
  "framework": "langchain",
  "agent_config": {
    "lm_provider": "openai",
    "lm_name": "gpt-4.1"
  }
}
```

{% hint style="info" %}
`a2a` and `langflow` agents may omit language-model fields. `config` agents must specify one mechanism only.
{% endhint %}

## Agent Workflows

### Direct ID

Use this when the catalog entry already exists.

```json
{
  "name": "analysis-agent",
  "type": "config",
  "framework": "langchain",
  "language_model_id": "fc945f0a-595e-471f-807c-47334c0eba9f"
}
```

### Provider and model name

Use this when the server-side catalog has a seeded master entry.

```json
{
  "name": "analysis-agent",
  "type": "config",
  "framework": "langchain",
  "provider": "openai",
  "model_name": "gpt-4.1"
}
```

### Legacy agent_config

Use this only if you are still migrating old payloads.

```json
{
  "name": "analysis-agent",
  "type": "config",
  "framework": "langchain",
  "agent_config": {
    "lm_provider": "openai",
    "lm_name": "gpt-4.1"
  }
}
```

## Model Constants in the SDK

Use typed constants when you want IDE support and stable names.

{% hint style="info" %}
These are plain Python classes with class attributes, not enums. The SDK currently ships constants through `GPT_5_2`; newer platform seed names may appear in the backend before SDK constants are added.
{% endhint %}

```python
from glaip_sdk import Agent
from glaip_sdk.models import OpenAI, DeepInfra, Anthropic, Google, AzureOpenAI, Bedrock

agent = Agent(
    name="analysis",
    instruction="You are a precise analyst.",
    model=OpenAI.GPT_5_NANO,  # resolves to "openai/gpt-5-nano"
)

agent = Agent(
    name="research",
    instruction="You are a research assistant.",
    model=DeepInfra.KIMI_K2_INSTRUCT,  # resolves to "deepinfra/moonshotai/Kimi-K2-Instruct"
)

agent = Agent(
    name="creative",
    instruction="You are a creative writer.",
    model=Anthropic.CLAUDE_SONNET_4_5,  # resolves to "anthropic/claude-sonnet-4-5"
)
```

**Available constants:**

| Provider | Import | Examples |
| --- | --- | --- |
| OpenAI | `from glaip_sdk.models import OpenAI` | `GPT_5_NANO`, `GPT_5_2`, `GPT_4O`, `O4_MINI` |
| Anthropic | `from glaip_sdk.models import Anthropic` | `CLAUDE_3_7_SONNET_LATEST`, `CLAUDE_SONNET_4_5`, `CLAUDE_OPUS_4_1` |
| Google | `from glaip_sdk.models import Google` | `GEMINI_2_5_FLASH`, `GEMINI_3_FLASH_PREVIEW`, `GEMINI_2_5_PRO` |
| Azure OpenAI | `from glaip_sdk.models import AzureOpenAI` | `GPT_4O`, `GPT_4O_MINI`, `GPT_4_1` |
| DeepInfra | `from glaip_sdk.models import DeepInfra` | `KIMI_K2_INSTRUCT`, `QWEN3_30B_A3B`, `GLM_4_5` |
| DeepSeek | `from glaip_sdk.models import DeepSeek` | `DEEPSEEK_CHAT`, `DEEPSEEK_V3_1` |
| AWS Bedrock | `from glaip_sdk.models import Bedrock` | `CLAUDE_SONNET_4_20250514_V1_0`, `CLAUDE_SONNET_4_5_20250929_V1_0` |

The current default model is `OpenAI.GPT_5_NANO`.

## String Format

Use the standardized `provider/model` format when you do not want to rely on constants.
Bare model names like `gpt-4o` still work, but they emit a deprecation warning.

```python
from glaip_sdk import Agent

agent = Agent(
    name="analysis",
    instruction="You are a precise analyst.",
    model="openai/gpt-5.2",
)

agent = Agent(
    name="research",
    instruction="You are a research assistant.",
    model="deepinfra/moonshotai/Kimi-K2-Instruct",
)

agent = Agent(
    name="creative",
    instruction="You are a creative writer.",
    model="anthropic/claude-sonnet-4-5",
)
```

```bash
aip agents create \
  --name analysis \
  --instruction "You are a precise analyst." \
  --model openai/gpt-5.2
```

{% hint style="info" %}
**Format patterns:**
- **OpenAI:** `openai/<model>` -> `openai/gpt-5.2`, `openai/gpt-5-nano`
- **DeepInfra:** `deepinfra/<org>/<model>` -> `deepinfra/moonshotai/Kimi-K2-Instruct`
- **DeepSeek:** `deepseek/<org>/<model>` -> `deepseek/deepseek-ai/DeepSeek-V3.1`
- **Anthropic:** `anthropic/<model>` -> `anthropic/claude-sonnet-4-5`
- **Google:** `google/<model>` -> `google/gemini-3-flash-preview`
- **Azure OpenAI:** `azure-openai/<model>` -> `azure-openai/gpt-4.1`

Invalid formats (missing `/`) raise a `ValueError` with suggestions to use model constants.
{% endhint %}

## Custom Model Objects

When you need credentials, a base URL, or hyperparameters that do not belong in the shared catalog, use `Model`.

```python
from glaip_sdk import Agent
from glaip_sdk.models import Model

agent = Agent(
    name="kimi-agent",
    instruction="You are a helpful AI assistant.",
    model=Model(
        id="custom/kimi-k2.5",
        base_url="https://api.moonshot.ai/v1",
        credentials="sk-xxxx",
        hyperparameters={
            "temperature": 1.0,
            "max_tokens": 32768,
            "top_p": 0.95,
        },
    ),
)
```

{% hint style="info" %}
`Model.id` still uses the same `provider/model` style. Use `custom/<name>` for ad hoc or local-only endpoints.
{% endhint %}

### DeepInfra example

```python
from glaip_sdk import Agent
from glaip_sdk.models import Model

agent = Agent(
    name="custom-deepinfra",
    instruction="You are a helpful assistant.",
    model=Model(
        id="deepinfra/moonshotai/Kimi-K2-Instruct",
        credentials="your-deepinfra-api-key",
        hyperparameters={
            "temperature": 0.7,
            "max_tokens": 4096,
        },
    ),
)
```

{% hint style="warning" %}
Credential precedence:
1. `Model.credentials`
2. environment variables like `DEEPINFRA_API_KEY` or `OPENAI_API_KEY`
3. credential files or default locations
{% endhint %}

## Local vs Remote Execution

_When to use:_ understand how configuration behaves when switching between `agent.run()` and `agent.deploy()`.

| Execution mode | Model config | Behavior |
| --- | --- | --- |
| Local (`agent.run()`) | `Model` object with `base_url`, `credentials`, `hyperparameters` | Full configuration is used directly by `aip_agents` |
| Local | String like `deepinfra/moonshotai/Kimi-K2-Instruct` | SDK resolves `base_url` from built-in provider mappings; credentials come from env vars or explicit fields |
| Remote (`agent.deploy()`) | `language_model_id` or `provider` + `model_name` | Server resolves the shared catalog entry and uses server-side credentials |
| Remote | `Model` object or string | Used to resolve the shared model when possible; changes require redeploy |

### Local execution with a known provider

```python
from glaip_sdk import Agent

agent = Agent(
    name="research",
    instruction="You are a research assistant.",
    model="deepinfra/moonshotai/Kimi-K2-Instruct",
)

result = agent.run("Research quantum computing")
```

### Switching to remote

```python
from glaip_sdk import Agent

agent = Agent(
    name="my-agent",
    instruction="You are helpful.",
    model="openai/gpt-5.2",
)

result = agent.run("Hello!")
agent.deploy()
result = agent.run("Hello!")
```

{% hint style="warning" %}
Local and remote execution are isolated:
- local config uses your environment
- remote config uses the AIP server catalog and its credentials
- changing local config does not change a deployed agent until you deploy again
{% endhint %}

## Using Catalog Models in AIP

If the model already exists in the AIP catalog, register it once and reference the returned `language_model_id` from your agents.

```json
{
  "name": "support-agent",
  "type": "config",
  "framework": "langchain",
  "language_model_id": "8cfc2f58-1f1e-4f38-b7d8-4a4e8df8ad5d"
}
```

If the model is not in the catalog yet, use the REST create endpoint and then re-list models before updating agents.

## Gemma and OpenAI-Compatible Providers

This is the path for Gemma-style usage when the provider exposes an OpenAI-compatible endpoint.

```bash
curl --location "$AIP_API_URL/language-models/" \
  --header "Content-Type: application/json" \
  --header "X-API-Key: $AIP_API_KEY" \
  --data '{
    "lm_invoker_type": "openai-compatible",
    "name": "google/gemma-4-31B-it",
    "display_name": "Gemma 4 31B IT",
    "base_url": "https://api.deepinfra.com/v1/openai",
    "credentials": "your-api-key-here",
    "hyperparameters": {
      "temperature": 0.2
    }
  }'
```

Seed data already includes DeepInfra-backed models such as `deepinfra/Kimi-K2-Instruct`, `deepinfra/Kimi-K2.5`, `deepinfra/Qwen3-30B-A3B`, `deepinfra/Qwen3-32B`, and `deepinfra/Qwen3-235B-A22B-Instruct-2507`.

## Seeded Model Examples

The current seed catalog includes these representative entries:

| Provider family | Examples |
| --- | --- |
| OpenAI | `openai/gpt-5.4-mini`, `openai/gpt-5.4-nano`, `openai/gpt-5.2`, `openai/gpt-5.1`, `openai/gpt-5` |
| Anthropic | `anthropic/claude-3-5-sonnet-latest`, `anthropic/claude-3-7-sonnet-latest`, `anthropic/claude-sonnet-4-5`, `anthropic/claude-opus-4-1` |
| Google | `google/gemini-2.5-flash`, `google/gemini-2.5-pro`, `google/gemini-3-flash-preview`, `google/gemini-3-pro-preview` |
| Azure OpenAI | `azure-openai/gpt-4o`, `azure-openai/gpt-4o-mini`, `azure-openai/gpt-4.1` |
| DeepInfra | `deepinfra/Kimi-K2-Instruct`, `deepinfra/Kimi-K2.5`, `deepinfra/Qwen3-30B-A3B`, `deepinfra/Qwen3-32B`, `deepinfra/GLM-4.5` |
| DeepSeek | `deepseek/deepseek-chat`, `deepseek/deepseek-ai/DeepSeek-V3.1` |
| Bedrock | `bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0`, `bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0` |

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Agent still uses the old model | The deployed agent was not re-synced | Re-run `agent.deploy()` or update the agent payload and confirm the `language_model_id` |
| `400 Unknown model` errors | The model is not present in the target environment | Use `client.list_language_models(force_refresh=True)` or `aip models list` and confirm the provider/name pair |
| `Forbidden` on update/delete | You are mutating a model outside your scope | Use the matching tenant key, or update a seeded model with a master key |
| Missing `base_url` or `credentials` in the response | By design | Fetch internal execution config through the service layer, not the public response |
| Duplicate model errors | Same scoped `provider_name`, `provider_display_name`, or `display_name` already exists | Rename the entry or update the existing record |
| Streaming stalls | The chosen model or endpoint does not support it | Disable streaming or choose a streaming-capable model |

## FAQ

### Should I use `language_model_id` or `provider` + `model_name`?

Use `language_model_id` for shared catalog entries. Use `provider` + `model_name` mainly when you are targeting a seeded master record by name.

### Can I create catalog entries from the CLI?

Not today. The CLI can list models, but catalog writes are REST-only.

### Can I keep using local custom endpoints?

Yes. Use `Model(...)` for local execution. If you need the same model in remote AIP execution, register it in the catalog first.

### What about `agent_config.lm_provider` and `agent_config.lm_name`?

They are legacy aliases that still resolve, but new payloads should prefer `language_model_id`.

## Related Documentation

- [Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) - attach `language_model_id` or legacy model selectors to agents
- [Python SDK reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk) - `client.list_language_models()`
- [REST API: Language Models](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/language-models) - catalog CRUD endpoints
- [CLI commands reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands) - list the catalog with `aip models list`
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) - script discovery and promotion across environments
