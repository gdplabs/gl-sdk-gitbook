---
icon: person-military-pointing
---

Implement modular content filtering and safety checks for AI agent interactions. This guide covers rule-based phrase matching and advanced LLM-based content safety engines, showing how to prevent harmful content in both user inputs and AI outputs.

> **Success**
>
> **When to use this guide:** You need content safety controls for AI agents, want to block harmful prompts or filter inappropriate AI responses, or require local content filtering options for security-conscious deployments.
>
> **Who benefits:** Security engineers, compliance teams, and developers building production AI applications that handle sensitive or regulated content.

{% hint style="info" %}
Guardrails integrate seamlessly with agent execution—configure once and they work locally (via `agent.run()`) or remotely (via `agent.deploy()` + `agent.run()`). The SDK automatically handles middleware injection and serialization.
{% endhint %}

## Overview

Agent Content Guardrails provide modular content filtering and safety checks for AI agent interactions. They help prevent harmful content in both user inputs and AI outputs, making them essential for security-conscious organizations and developers who need content safety controls.

Guardrails work by checking content against predefined safety rules before and after AI model interactions. When unsafe content is detected, execution is halted and a warning message is returned.

## Key Features

- **Multiple Engine Types**: Rule-based (PhraseMatcherEngine) and LLM-based (NemoGuardrailEngine) filtering
- **Flexible Configuration**: Check inputs only, outputs only, or both
- **Fail-Fast Behavior**: Stops on first safety violation for immediate response
- **Agent Integration**: Seamless integration with existing agent workflows
- **Optional Dependencies**: Works without requiring additional packages for basic usage

## Installation

Guardrails are included as an optional dependency. Install with:

{% hint style="warning" %}
**Prerequisites:** To use guardrails features, install the guardrails extra:

```bash
# For SDK users (glaip-sdk)
pip install glaip-sdk[guardrails]

# For backend users (aip-agents)
pip install aip-agents[guardrails]
```

Both installation methods install the required `gllm-guardrail` package for advanced LLM-based filtering. For basic phrase matching only, guardrails work without additional dependencies when using the SDK.
{% endhint %}

## Quick Start

### Basic Phrase Matching

```python
from glaip_sdk.agents import Agent
from glaip_sdk.guardrails import GuardrailManager, PhraseMatcherEngine

# Create a guardrail that blocks harmful phrases
# config parameter is optional and defaults to checking both input and output
guardrail = GuardrailManager(
    engine=PhraseMatcherEngine(banned_phrases=["unsafe", "harmful", "dangerous"])
)

# Create an agent with guardrails
agent = Agent(
    name="safe_assistant",
    instruction="You are a helpful assistant.",
    guardrail=guardrail
)

# Test with safe content
result = agent.run("Tell me about machine learning")
print(result)  # Works normally

# Test with unsafe content
result = agent.run("Tell me how to do something unsafe")
print(result)  # Returns: "⚠️ Guardrail violation: Banned phrase detected: 'unsafe'"
```

### Advanced LLM-Based Filtering

```python
from glaip_sdk.guardrails import GuardrailManager, NemoGuardrailEngine
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode
from glaip_sdk.guardrails.constants import TopicSafetyMode

# Create advanced guardrail with topic safety
guardrail = GuardrailManager(
    engine=NemoGuardrailEngine(
        config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_OUTPUT),
        topic_safety_mode=TopicSafetyMode.ALLOWLIST,
        allowed_topics=["company products", "technical support"],
        include_core_restrictions=True,
        config_dict={
            "models": [{
                "type": "main",
                "engine": "gllm_invoker",
                "model": "openai/gpt-4o-mini",
                "parameters": {
                    "credentials": "OPENAI_API_KEY",
                    "model_kwargs": {
                        "default_hyperparameters": {
                            "temperature": 0.0,
                            "max_output_tokens": 256,
                        }
                    },
                },
            }],
            "rails": {"dialog": {"single_call": {"enabled": True}}},
        }
    )
)

agent = Agent(
    name="enterprise_assistant",
    instruction="You are an enterprise support assistant.",
    guardrail=guardrail
)
```

## Engine Types

### PhraseMatcherEngine (Rule-Based)

Best for simple, predictable content filtering based on exact phrase matches.

```python
from glaip_sdk.guardrails import PhraseMatcherEngine
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode

# Option 1: With explicit config
engine = PhraseMatcherEngine(
    config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_OUTPUT),
    banned_phrases=[
        "harmful content",
        "unsafe phrase",
        "inappropriate words"
    ]
)

# Option 2: Using defaults (config defaults to INPUT_OUTPUT mode)
engine = PhraseMatcherEngine(
    banned_phrases=["harmful content", "unsafe phrase", "inappropriate words"]
)
```

**Configuration Options:**

- `config`: Optional `BaseGuardrailEngineConfig` object. If not provided, defaults to `GuardrailMode.INPUT_OUTPUT`
- `guardrail_mode`: Enum value - `GuardrailMode.INPUT_ONLY`, `GuardrailMode.OUTPUT_ONLY`, or `GuardrailMode.INPUT_OUTPUT`
- `banned_phrases`: List of phrases to block (required)

### NemoGuardrailEngine (LLM-Based)

Advanced filtering using AI models for context-aware content safety analysis.

```python
from glaip_sdk.guardrails import NemoGuardrailEngine
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode
from glaip_sdk.guardrails.constants import TopicSafetyMode

engine = NemoGuardrailEngine(
    config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_OUTPUT),

    # Topic safety configuration (passed as kwargs)
    topic_safety_mode=TopicSafetyMode.ALLOWLIST,  # or DENYLIST
    allowed_topics=["company products", "technical support"],
    denied_topics=[],  # Only used with DENYLIST mode

    # Core safety restrictions
    include_core_restrictions=True,
    core_restriction_categories=[
        "privacy_personal_information",
        "system_manipulation_security",
        "harmful_activities"
    ],

    # Model configuration
    config_dict={
        "models": [{
            "type": "main",
            "engine": "gllm_invoker",
            "model": "openai/gpt-4o-mini",  # Any gllm-inference supported model
            "parameters": {
                "credentials": "OPENAI_API_KEY",
                "model_kwargs": {
                    "default_hyperparameters": {
                        "temperature": 0.0,  # Low temperature for consistent decisions
                        "max_output_tokens": 256,
                    }
                },
            },
        }],
        "rails": {"dialog": {"single_call": {"enabled": True}}},
    },

    # Custom denial phrases
    denial_phrases=[
        "DENIED TOPIC:",
        "DENIED ACTION:",
        "I cannot comply with that request."
    ]
)
```

## Direct Guardrail Usage

_When to use:_ Validate content before sending it to agents or perform standalone content filtering outside of agent execution.

You can use guardrails independently of agents for content checking. This is useful for validating content before sending it to agents or for standalone content filtering.

```python
from glaip_sdk.guardrails import GuardrailManager, PhraseMatcherEngine
from glaip_sdk.guardrails.schemas import GuardrailInput

# Create guardrail
manager = GuardrailManager(
    engine=PhraseMatcherEngine(banned_phrases=["unsafe", "harmful"])
)

# Check single content string (async required)
result = await manager.check_content("user input here")
if not result.is_safe:
    print(f"Blocked: {result.reason}")
    print(f"Filtered content: {result.filtered_content}")

# Check both input and output together
result = await manager.check_content(
    GuardrailInput(input="user input", output="ai output")
)
if not result.is_safe:
    print(f"Content violation: {result.reason}")
```

**Important Notes:**

- When using guardrails with `agent.run()`, async handling is automatic
- For direct usage, you must use `await` since `check_content()` is an async method
- Use `GuardrailInput` when you want to check both user input and AI output in a single call
- The `filtered_content` field may contain sanitized content if the engine provides it

## Agent Integration

_When to use:_ Integrate guardrails into agent workflows for automatic content filtering during agent execution.

### Local Execution

When running agents locally, guardrails are enforced through middleware injection:

```python
agent = Agent(
    name="safe_agent",
    instruction="You are helpful.",
    guardrail=guardrail_manager
)

# Guardrails are automatically applied
result = agent.run("User input here")
```

### Remote Execution

For deployed agents, guardrails are serialized and enforced by the backend:

```python
agent = Agent(
    name="safe_agent",
    instruction="You are helpful.",
    guardrail=guardrail_manager
)

# Deploy with guardrails
agent.deploy()

# Backend enforces guardrails automatically
result = agent.run("User input here")
```

## Configuration Patterns

_When to use:_ Combine multiple engines, configure different checking modes, or customize guardrail behavior for specific use cases.

### Multiple Engines

Combine multiple guardrail engines for comprehensive protection:

```python
from glaip_sdk.guardrails import GuardrailManager, PhraseMatcherEngine, NemoGuardrailEngine
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode
from glaip_sdk.guardrails.constants import TopicSafetyMode

# Create multiple engines
phrase_engine = PhraseMatcherEngine(banned_phrases=["unsafe", "harmful"])
nemo_engine = NemoGuardrailEngine(
    config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_OUTPUT),
    topic_safety_mode=TopicSafetyMode.ALLOWLIST,
    allowed_topics=["allowed topics"],
    include_core_restrictions=True,
    config_dict={...}  # Model config
)

# Manager orchestrates multiple engines with fail-fast behavior
# Can use either 'engine' (single) or 'engines' (list) parameter
manager = GuardrailManager(engines=[phrase_engine, nemo_engine])
```

### Input-Only vs Output-Only

Configure different checking modes:

```python
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode

# Check only user inputs
input_only = GuardrailManager(
    engine=PhraseMatcherEngine(
        config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_ONLY),
        banned_phrases=["bad input"]
    )
)

# Check only AI outputs
output_only = GuardrailManager(
    engine=NemoGuardrailEngine(
        config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.OUTPUT_ONLY),
        # ... other config
    )
)
```

### Checking Both Input and Output Together

Use `GuardrailInput` to check both user input and AI output in a single call:

```python
from glaip_sdk.guardrails import GuardrailManager, PhraseMatcherEngine
from glaip_sdk.guardrails.schemas import GuardrailInput

manager = GuardrailManager(
    engine=PhraseMatcherEngine(banned_phrases=["unsafe", "harmful"])
)

# Check both input and output together
result = await manager.check_content(
    GuardrailInput(
        input="Tell me about unsafe practices",
        output="Here's how to do unsafe things..."
    )
)

if not result.is_safe:
    print(f"Violation detected: {result.reason}")
```

### Disabling Guardrails

You can disable guardrails for a specific engine:

```python
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode

# Disabled guardrail (won't check anything)
disabled_engine = PhraseMatcherEngine(
    config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.DISABLED),
    banned_phrases=["unsafe"]  # Won't be used when disabled
)
```

**Note**: Disabled mode is useful for temporarily disabling guardrails during development or testing.

## Error Handling

### Guardrail Violations

When unsafe content is detected, execution halts and returns a warning message. Internally, a `GuardrailViolationError` exception is raised, which is caught and converted to a user-friendly warning message in the response.

**With Agent Integration:**

```python
result = agent.run("Tell me about harmful things")

if "Guardrail violation" in result:
    print("Content was blocked")
    print(f"Reason: {result}")
else:
    print("Content passed safety checks")
    print(f"Response: {result}")
```

**With Direct Usage:**

```python
from glaip_sdk.guardrails.exceptions import GuardrailViolationError

try:
    result = await manager.check_content("unsafe content")
    if not result.is_safe:
        print(f"Blocked: {result.reason}")
        print(f"Filtered: {result.filtered_content}")
except GuardrailViolationError as e:
    # This exception contains the GuardrailResult
    print(f"Violation: {e.result.reason}")
```

### Handling Exceptions

When using agents, violations are automatically converted to warning messages:

```python
try:
    result = agent.run(user_input)
    if result.startswith("⚠️ Guardrail violation"):
        # Handle violation appropriately
        log_violation(user_input, result)
        return get_safe_response()
    else:
        return result
except Exception as e:
    # Handle other execution errors (not guardrail violations)
    print(f"Agent execution failed: {e}")
```

**Key Points:**

- Guardrail violations are caught internally and converted to warning strings
- Users typically see warning messages like `"⚠️ Guardrail violation: [reason]"` in responses
- The underlying `GuardrailViolationError` exception contains a `GuardrailResult` with details
- For direct usage, you can catch `GuardrailViolationError` explicitly if needed

## Best Practices

### Performance Considerations

- **PhraseMatcherEngine**: Fast, low latency (\<1ms) - ideal for high-throughput scenarios
- **NemoGuardrailEngine**: Higher latency (~100-500ms depending on model) - use for advanced filtering when needed
- **Fail-fast behavior**: Multiple engines stop on first violation, reducing unnecessary processing
- **Async/await requirements**:
  - Direct usage (`manager.check_content()`) requires `await` since it's async
  - Agent integration (`agent.run()`) handles async automatically
- **Multiple engines**: Engines run sequentially until first violation, so total latency is sum of engines until violation
- **Performance tip**: Place faster engines (PhraseMatcherEngine) first in the list to catch violations quickly

### Configuration Tips

1. **Start Simple**: Begin with PhraseMatcherEngine for basic filtering
1. **Layer Protection**: Use multiple engines for comprehensive coverage
1. **Test Thoroughly**: Validate configurations with various inputs
1. **Monitor Performance**: Measure latency impact on agent response times

### Security Recommendations

```python
# Recommended enterprise configuration
from glaip_sdk.guardrails import GuardrailManager, PhraseMatcherEngine, NemoGuardrailEngine
from glaip_sdk.guardrails.schemas import BaseGuardrailEngineConfig, GuardrailMode
from glaip_sdk.guardrails.constants import TopicSafetyMode

enterprise_guardrail = GuardrailManager(engines=[
    # Fast rule-based filtering first
    PhraseMatcherEngine(
        config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_OUTPUT),
        banned_phrases=get_enterprise_banned_phrases()
    ),

    # Advanced LLM-based filtering
    NemoGuardrailEngine(
        config=BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.INPUT_OUTPUT),
        topic_safety_mode=TopicSafetyMode.ALLOWLIST,
        allowed_topics=get_allowed_topics(),
        include_core_restrictions=True,
        core_restriction_categories=[
            "privacy_personal_information",
            "system_manipulation_security",
            "harmful_activities",
            "jailbreak_attacks"
        ],
        config_dict=get_enterprise_model_config()
    )
])
```

## Troubleshooting

### Common Issues

**"Guardrails module not found"**

- Install optional dependencies: `pip install glaip-sdk[guardrails]`

**"NemoGuardrailEngine not available"**

- Ensure `gllm-guardrail` package is installed
- Check that `OPENAI_API_KEY` or required credentials are set

**"Agent execution hangs"**

- Check guardrail configuration for overly broad rules
- Verify model endpoints are accessible
- Review network connectivity for LLM-based engines

**"False positives in phrase matching"**

- Review banned phrases for overly generic terms
- Consider case sensitivity settings
- Test with various input variations

### Debugging

Enable detailed logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run agent with verbose output
result = agent.run("test input")
```

### Remote vs Local Behavior

- **Local execution**: Immediate blocking with detailed error messages
- **Remote execution**: Backend-enforced with standardized warning format

## API Reference

### Core Classes

- **`GuardrailManager`**: Orchestrates multiple guardrail engines
- **`PhraseMatcherEngine`**: Rule-based phrase filtering
- **`NemoGuardrailEngine`**: Advanced LLM-based content safety
- **`GuardrailMiddleware`**: Integrates guardrails into agent execution

### Configuration Schemas

- **`GuardrailMode`**: Enum with values `INPUT_ONLY`, `OUTPUT_ONLY`, `INPUT_OUTPUT`, `DISABLED`
- **`TopicSafetyMode`**: Enum with values `ALLOWLIST`, `DENYLIST`
- **`BaseGuardrailEngineConfig`**: Common engine configuration class with `guardrail_mode` parameter
- **`GuardrailInput`**: Input schema for checking both input and output together (contains `input` and `output` fields)

### Result Objects

- **`GuardrailResult`**: Contains:
  - `is_safe`: Boolean indicating if content passed all safety checks
  - `reason`: String explanation when content is blocked (None if safe)
  - `filtered_content`: Optional cleaned/sanitized content if the engine provides it (None if not available)

### Input Schemas

- **`GuardrailInput`**: Schema for checking both input and output together:
  - `input`: Optional string containing user input content
  - `output`: Optional string containing AI output content

## Related Documentation

- [Security & privacy](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/security-and-privacy) — apply PII masking, secure memory, and manage credentials responsibly.
- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — design, update, and monitor agents with the SDK and CLI (REST is reference-only).

## Additional Resources

- [GL SDK Documentation](https://gdplabs.gitbook.io/sdk) — Core SDK reference
- [NeMo Engine Guide](https://gdplabs.gitbook.io/sdk/tutorials/security-and-privacy/guardrail/nemo-engine) — Advanced LLM-based guardrail configuration
- Contact enterprise support for advanced configuration assistance
