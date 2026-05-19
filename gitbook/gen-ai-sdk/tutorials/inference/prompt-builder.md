---
icon: square-code
---

# Prompt Builder

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [prompt-builder.md](prompt-builder.md "mention")| **Use Case**: [utilize-language-model-request-processor](../../guides/utilize-language-model-request-processor/ "mention") | [API Reference](https://api.python.docs.glair.ai/generative-internal/library/gllm_inference/api/catalog.html#gllm_inference.catalog.PromptBuilderCatalog)

## What's a Prompt Builder?

The **prompt builder** is a module designed to manage prompt templates and seamlessly build a list of messages ready to be sent to a language model. In this tutorial, you'll learn how to utilize the `PromptBuilder` in **just a few lines of code**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-inference
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-inference
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-inference
```
{% endtab %}
{% endtabs %}

## Quickstart

Let’s jump into a basic example using `PromptBuilder`. Prompt builder cannot be empty, which means it must have at least a system template, a user template, or both.

```python
from gllm_inference.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(
    system_template="Talk like a pirate.",
    user_template="What is the capital city of Indonesia?",
)
messages = prompt_builder.format()
print(messages)
```

**Expected Output**

```
[
    Message(role='system', contents=['Talk like a pirate.']),
    Message(role='user', contents=['What is the capital city of Indonesia?'])
]
```

## Prompt Variables

One of the most useful feature of the prompt builder is the ability to add prompt variables.

Basically, we can add a placeholder in the prompt templates using curly braces (`{}`). These placeholder can then be replaced with the actual value that we want during runtime. This allows us to easily customize just certain parts of the prompts, while the common parts can be stored in the prompt builder during initialization.

In the following example, let's try to assign `{role}` and `{country}` as prompt variables!

```python
from gllm_inference.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(
    system_template="Talk like a {role}.",
    user_template="What is the capital city of {country}?",
)
messages = prompt_builder.format(role="pirate", country="Indonesia")
print(messages)
```

**Expected Output**

```
[
    Message(role='system', contents=['Talk like a pirate.']),
    Message(role='user', contents=['What is the capital city of Indonesia?'])
]
```

## Adding History

Prompt builder allows adding history to handle multiturn conversations. History passed to the prompt builder will be positioned **in between** the system message and the user message.

```python
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import Message

prompt_builder = PromptBuilder(
    system_template="Talk like a {role}.",
    user_template="What is the capital city of {country}?",
)
history = [
    Message.user("Hi, there!"),
    Message.assistant("Hello!"),
]
messages = prompt_builder.format(role="pirate", country="Indonesia", history=history)
print(messages)

```

**Expected Output**

```
[
    Message(role='system', contents=['Talk like a pirate.']),
    Message(role='user', contents=['Hi, there!'])
    Message(role='assistant', contents=['Hello!'])
    Message(role='user', contents=['What is the capital city of Indonesia?'])
]
```

## Adding Extra Contents

Prompt builder also allows adding extra contents to be passed to the language model, such as extra texts, attachments, tool calls, and many more. Extra contents passed to the prompt builder will be added to the user message contents.

```python
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import Attachment

image = Attachment.from_path("path/to/image.png")

prompt_builder = PromptBuilder(
    system_template="Talk like a {role}.",
    user_template="What is the capital city of {country}?",
)
messages = prompt_builder.format(
    role="pirate",
    country="Indonesia",
    extra_contents=[image],
)
print(messages)

```

**Expected Output**

```
[
    Message(role='system', contents=['Talk like a pirate.']),
    Message(
        role='user',
        contents=[
            'What is the capital city of Indonesia?',
            Attachment(..., filename='image.png'),
        ]
    ),
]
```

## Templating Strategies

The Prompt Builder supports two templating strategies for variable substitution, implemented by `StringFormatStrategy` and `JinjaFormatStrategy` respectively.

### 1. String Format Strategy (`StringFormatStrategy`, default)

By default, the Prompt Builder uses `StringFormatStrategy`, which applies Python's `str.format()` method with curly braces `{}` for variables:

```python
from gllm_inference.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(
    system_template="You are a {role}.",
    user_template="Tell me about {topic}."
)
messages = prompt_builder.format(role="teacher", topic="Python")
print(messages)
```

### 2. Jinja Format Strategy (`JinjaFormatStrategy`)

For more advanced templating needs (loops, conditionals, filters), you can enable `JinjaFormatStrategy` by passing `use_jinja=True`:

````python
from gllm_inference.prompt_builder import PromptBuilder

# Using Jinja with restricted environment (recommended for security)
prompt_builder = PromptBuilder(
    system_template="You are a helpful AI assistant. Use the provided examples to infer the correct transformation style.\n\n{% for ex in examples -%}\nExample {{ loop.index }}:\nInput: {{ ex.input }}\nOutput: {{ ex.output }}\n\n{%- endfor %}",
    user_template="Query:\n```{{ query }}```",
    use_jinja=True,
    jinja_env="restricted"  # or "jinja_default"
)

messages = prompt_builder.format(
    examples=[
        {"input": "What is AI?", "output": "Define AI"},
        {"input": "How does ML work?", "output": "Explain ML"}
    ],
    query="What are neural networks?"
)
print(messages)
````

**Jinja Environment Options:**

* `"restricted"`: Sandboxed environment with limited features (recommended for security)
* `"jinja_default"`: Full Jinja2 environment with all features
* Custom dict: Provide custom Jinja2 environment configuration
