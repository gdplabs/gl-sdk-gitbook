---
icon: lightbulb-gear
---

# Skills

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [skills.md](skills.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `AnthropicLMInvoker`

## What is Skill?







## Skill Operation

Skill operation is a feature that allows the language model to **manage custom skills** on the provider's server side. Skills are reusable capabilities that can be uploaded, versioned, and invoked during model interactions. This feature enables you to extend the model's functionality with custom tools and behaviors.

Skill operation is only available for certain LM invokers. This feature can be accessed via the `skill` attribute of the LM invoker. As an example, let's try managing skills using `AnthropicLMInvoker`.

{% hint style="info" %}
**Note:** Skill operations are currently only supported by `AnthropicLMInvoker` and use the Anthropic Skills beta API.
{% endhint %}

### Init an LM Invoker

First of all, let's create an `AnthropicLMInvoker` that we will use to manage skills:

```python
from dotenv import load_dotenv
load_dotenv()

from gllm_inference.lm_invoker import AnthropicLMInvoker

lm_invoker = AnthropicLMInvoker("claude-sonnet-4-5")
```

### Create a Skill

Next, let's create a skill. Skills can be uploaded as either:

1. a ZIP archive containing a `SKILL.md` file at the root, or&#x20;
2. as a single markdown file.&#x20;

The `create()` method will output a `Skill` object to be used in later operations.

```python
from gllm_inference.schema import Attachment

# Upload a skill from a markdown file
skill_file = Attachment.from_path('path/to/skill.md')
skill = await lm_invoker.skill.create(file=skill_file, name="My Custom Skill")

print(f"Created skill: {skill.id}")
```

Alternatively, you can upload a ZIP archive:

```python
# Upload a skill from a ZIP archive
skill_zip = Attachment.from_path('path/to/skill.zip')
skill = await lm_invoker.skill.create(file=skill_zip, name="My Custom Skill")
```

### List Skills

We can verify that the skill has been successfully created by using the `list()` method.

```python
skills = await lm_invoker.skill.list()

if not skills:
    print("No skills found.")

for skill in skills:
    print(f" - {skill.id}: {skill.skill_type} (version: {skill.version})")
```

### Retrieve a Skill

To get detailed information about a specific skill, use the `retrieve()` method:

```python
skill_info = await lm_invoker.skill.retrieve(skill.id)
print(f"Skill ID: {skill_info.id}")
print(f"Type: {skill_info.skill_type}")
print(f"Version: {skill_info.version}")
print(f"Metadata: {skill_info.metadata}")
```

### Create a New Skill Version

To create a new version of a skill, upload a new file using `skill.version.create()`:

```python
updated_file = Attachment.from_path('path/to/updated_skill.md')
updated_skill = await lm_invoker.skill.version.create(skill.id, file=updated_file)

print(f"Created new version: {updated_skill.version}")
```

### List Skill Versions

Skills support versioning. You can list all versions of a skill using `skill.version.list()`:

```python
versions = await lm_invoker.skill.version.list(skill.id)

for version in versions:
    print(f" - Version {version.version}: {version.metadata.get('name', 'N/A')}")
```

### Retrieve a Skill Version

To get details about a specific skill version, use `skill.version.retrieve()`:

```python
version = await lm_invoker.skill.version.retrieve(skill.id, version="v1")

print(f"Version: {version.version}")
print(f"Metadata: {version.metadata}")
```

### Delete a Skill Version

To delete a specific version of a skill, use `skill.version.delete()`:

```python
await lm_invoker.skill.version.delete(skill.id, version="v1")
```

### Delete a Skill

Finally, if a skill is no longer needed, it can be deleted via the `delete()` method. This will delete all versions of the skill.

```python
await lm_invoker.skill.delete(skill.id)
```

{% hint style="warning" %}
**Note:** Deleting a skill will remove all of its versions. The Anthropic Skills beta API requires all versions to be deleted before the skill itself can be deleted. The SDK handles this automatically, but you may encounter server errors when deleting the latest version due to API limitations.
{% endhint %}

### Skill File Format

Skills must be provided in one of the following formats:

1. **Single Markdown File**: A `.md` file that will be automatically wrapped in a ZIP archive with the name `SKILL.md`
2. **ZIP Archive**: A `.zip` file containing a `SKILL.md` file at the root directory

The `SKILL.md` file should define the skill's capabilities, parameters, and behavior according to Anthropic's skill specification format.

## Using Skill in LM Invoker

Skills can be used during model invocation by referencing them as native tools. Once a skill is created and uploaded to the provider's server, you can invoke it by passing it as a tool to the LM invoker:

Skills can be used during model invocation by referencing them as native tools. Once a skill is created and uploaded to the provider's server, you can invoke it by passing it as a tool to the LM invoker.

#### Using an Existing Skill

If you already have a skill ID, you can reference it directly:

```python
from gllm_inference.schema import NativeTool

# Create a skill reference as a native tool
skill_tool = NativeTool.skill(skill_id="your-skill-id", name="My Custom Skill")

# Use the skill during invocation
output = await lm_invoker.invoke(
    "Use the custom skill to process this request",
    tools=[skill_tool]
)
```

#### Creating and Using a Skill in One Flow

Alternatively, you can create a skill and immediately use it in an invocation:

```python
from gllm_inference.schema import Attachment, NativeTool
from gllm_inference.lm_invoker import AnthropicLMInvoker

# Initialize the LM invoker
lm_invoker = AnthropicLMInvoker("claude-sonnet-4-20250514")

# Create a new skill
skill_file = Attachment.from_path('path/to/skill.md')
skill = await lm_invoker.skill.create(file=skill_file, name="My Custom Skill")

# Immediately use the created skill in an invocation
output = await lm_invoker.invoke(
    "Use the custom skill to process this request",
    tools=[NativeTool.skill(skill=skill)
)

print(f"Output: {output.text}")
```

The model will then be able to call the skill during its reasoning process, extending its capabilities beyond the standard built-in tools.
