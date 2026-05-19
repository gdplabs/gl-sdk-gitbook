---
icon: book-open
---

# Catalog

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial:** [catalog.md](catalog.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/catalog.html)

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts and components:

1. [prompt-builder.md](prompt-builder.md "mention")
2. [#message-roles](lm-invoker/#message-roles "mention")

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

## Prompt Builder Catalog

**Prompt Builder Catalog** enables you to **load and manage multiple prompt builders** from various data sources like Google Sheets, CSV files, or Python records. This allows you to **centralize prompt management**, making it easier to maintain, version, and share prompts across your applications.

For example, instead of hard-coding prompts in your code, you can store them in a Google Sheet with names like "summarize", "transform_query", and "draft_document", then load them all at once using the catalog.

### Catalog Configuration

The `PromptBuilderCatalog` can be configured using a table (such as a CSV file or Google Sheet), or directly from a list of Python dictionaries (records). To function correctly, the table or records must include specific columns or keys:

**Required Columns:**

1. **name**: The unique identifier for the prompt builder
2. **system**: The system template (instructions for the AI)
3. **user**: The user template (how user input is formatted)

**Optional Column:**

1. **kwargs**: Advanced prompt builder configuration (JSON format) for Jinja templating, defining `key_defaults` , etc.

{% hint style="info" %}
**Important Notes:**

- At least one of `system` or `user` columns must be filled
- Templates support variable placeholders using `{variable_name}` syntax
  {% endhint %}

### Loading Catalog

#### Option 1: From Google Sheets

{% stepper %}
{% step %}
**Obtain Worksheet ID and Credentials**

From your Google Sheets URL, you can obtain:

- **`sheet_id`**: between `/d/` and `/edit`
- **`worksheet_id`**: `0` (usually `0` for the first sheet)
  {% endstep %}

{% step %}
**Obtain Google Service Account JSON Credentials**

Follow these steps:

1. [Create a Google service account](https://developers.google.com/workspace/guides/create-credentials#create_a_service_account).
2. [Create JSON credentials for the service account](https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account).
   {% endstep %}

{% step %}
**Load with** `.from_gsheets()` **method**

```python
from gllm_inference.catalog.prompt_builder_catalog import PromptBuilderCatalog

# Method 1: Using client email and private key
catalog = PromptBuilderCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    client_email="your_service_account_email",
    private_key="your_private_key",
)

# Method 2: Using credential file
catalog = PromptBuilderCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    credential_file_path="path/to/credentials.json" #contains client_email and private_key
)
```

{% endstep %}
{% endstepper %}

#### Option 2: From CSV File

{% stepper %}
{% step %}
**Download/create CSV file**

Prepare a CSV file that contains your prompt catalog definitions. You can download a template from: [prompt_builder_catalog_template.csv](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/resources/catalog/prompt_builder_catalog_template.csv)
{% endstep %}

{% step %}
**Load with `.`**`from_csv`**`()` method**

```python
catalog = PromptBuilderCatalog.from_csv(csv_path="path/to/prompt_builder_catalog.csv")
prompt_builder = catalog.transform_query
```

{% endstep %}
{% endstepper %}

#### Option 3: From JSON File

{% stepper %}
{% step %}
**Download/create JSON file**

Prepare a JSON file that contains your prompt catalog definitions. You can download a template from: [prompt_builder_catalog_template.json](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/resources/catalog/prompt_builder_catalog_template.json)
{% endstep %}

{% step %}
**Load with `.from_json()` method**

```python
import json

# Load from JSON file
with open("path/to/prompt_builder_catalog.json") as f:
    records = json.load(f)

catalog = PromptBuilderCatalog.from_records(records=records)
prompt_builder = catalog.summarize
```

{% endstep %}
{% endstepper %}

#### Option 4: From Python Records

{% stepper %}
{% step %}
**Define the catalog**

Provide the records in the format of list of dictionaries. An example can be found below:

`````python
records = [
    {
        "name": "summarize",
        "system": "You are an AI expert\nSummarize the following context.\n\nContext:\n```{context}```",
        "user": "",
        "kwargs": None
    },
    {
        "name": "transform_query",
        "system": "",
        "user": "Transform the following query into a simpler form.\n\nQuery:\n```{query}```",
        "kwargs": None
    },
    {
        "name": "draft_document",
        "system": "You are an AI expert.\nDraft a document following the provided format and context.\n\nFormat:\n```{format}```",
        "user": "User instruction:\n{query}",
        "kwargs": {
            "key_defaults": {
                "format": "I. Background\nII. Content\nIII. Conclusion"
            }
        }
    },
    {
        "name": "transform_query_jinja",
        "system": "You are a helpful AI assistant. Use the provided examples to infer the correct transformation style.\n\n{% for ex in examples -%}\nExample {{ loop.index }}:\nInput: {{ ex.input }}\nOutput: {{ ex.output }}\n\n{%- endfor %}\nNow transform the following query consistently with the examples.",
        "user": None,
        "kwargs": {
            "use_jinja": True,
            "jinja_env": "restricted"
        }
    },
]````
`````

{% endstep %}

{% step %}
**Load using** \`.from_records()\` **method**

```
catalog = PromptBuilderCatalog.from_records(records=records)
```

{% endstep %}
{% endstepper %}

### Using Catalog

Once loaded, you can access any prompt builder by its name:

```python
# Use the prompt builders
summary_prompt = catalog.summarize.format(context="Some text to summarize")
query_prompt = catalog.transform_query.format(query="Complex query here")

# This uses the default format from key_defaults
document_prompt = catalog.draft_document.format(
    context="Background information",
    query="Write a summary report"
)

# Or override the default format
document_prompt = catalog.draft_document.format(
    format="Custom Format",
    context="Background information",
    query="Write a summary report"
)

# Using Jinja templates with dynamic data
jinja_prompt = catalog.transform_query_jinja.format(
    examples=[
        {"input": "What is AI?", "output": "Define AI"},
        {"input": "How does ML work?", "output": "Explain ML"}
    ],
    query="What are neural networks?"
)
```

---

## LM Invoker Catalog

**LM Invoker Catalog** enables you to **load and manage multiple LM invokers** from data sources like Google Sheets, CSV files, or Python records. This helps you **centralize model configurations** (model IDs, credentials, and optional prompt templates) and reuse them across different pipelines.

For example, instead of initializing each invoker manually in code, you can store entries like `router`, `query_transformer`, and `chat_with_history` in one catalog and access them by name.

### Catalog Configuration

The `LMInvokerCatalog` can be configured using a table (such as a CSV file or Google Sheet), or directly from a list of Python dictionaries (records). To function correctly, the table or records must include specific columns or keys:

**Required Columns:**

1. **name**: The unique identifier for the LM invoker
2. **model_id**: The model identifier used to build the invoker
3. **credentials**: Credentials env-var key (or JSON mapping of invoker credential keys to env-var keys)
4. **config**: Additional LM invoker configuration (JSON format)

**Optional Columns:**

1. **system_template**: Optional system template for prompt operations
2. **user_template**: Optional user template for prompt operations
3. **prompt_builder_kwargs**: Advanced prompt builder configuration (JSON format), such as Jinja settings and history formatter

{% hint style="info" %}
**Important Notes:**

- `model_id` supports environment variable substitution using `${ENV_VAR_KEY}` syntax
- `credentials` can be a single env-var key or a JSON object that maps credential field names to env-var keys
- If `system_template`, `user_template`, or `prompt_builder_kwargs` is provided, prompt operations are automatically configured for the invoker
- Empty `credentials` and `config` values are allowed and use default invoker behavior
  {% endhint %}

### Loading Catalog

#### Option 1: From Google Sheets

{% stepper %}
{% step %}
**Obtain Worksheet ID and Credentials**

From your Google Sheets URL, you can obtain:

- **`sheet_id`**: between `/d/` and `/edit`
- **`worksheet_id`**: `0` (usually `0` for the first sheet)
  {% endstep %}

{% step %}
**Obtain Google Service Account JSON Credentials**

Follow these steps:

1. [Create a Google service account](https://developers.google.com/workspace/guides/create-credentials#create_a_service_account).
2. [Create JSON credentials for the service account](https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account).
   {% endstep %}

{% step %}
**Load with** `.from_gsheets()` **method**

```python
from gllm_inference.catalog.lm_invoker_catalog import LMInvokerCatalog

# Method 1: Using client email and private key
catalog = LMInvokerCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    client_email="your_service_account_email",
    private_key="your_private_key",
)

# Method 2: Using credential file
catalog = LMInvokerCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    credential_file_path="path/to/credentials.json"
)
```

{% endstep %}
{% endstepper %}

#### Option 2: From CSV File

{% stepper %}
{% step %}
**Download/create CSV file**

Prepare a CSV file that contains your LM invoker catalog definitions. You can download a template from: [lm_invoker_catalog_template.csv](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/resources/catalog/lm_invoker_catalog_template.csv)
{% endstep %}

{% step %}
**Load with** `.from_csv()` **method**

```python
catalog = LMInvokerCatalog.from_csv(csv_path="path/to/lm_invoker_catalog.csv")
router_invoker = catalog.router
```

{% endstep %}
{% endstepper %}

#### Option 3: From JSON File

{% stepper %}
{% step %}
**Download/create JSON file**

Prepare a JSON file that contains your LM invoker catalog definitions. You can download a template from: [lm_invoker_catalog_template.json](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/resources/catalog/lm_invoker_catalog_template.json)
{% endstep %}

{% step %}
**Load with `.from_records()` method**

```python
import json

with open("path/to/lm_invoker_catalog.json") as f:
    records = json.load(f)

catalog = LMInvokerCatalog.from_records(records=records)
query_transformer = catalog.query_transformer
```

{% endstep %}
{% endstepper %}

#### Option 4: From Python Records

{% stepper %}
{% step %}
**Define the catalog**

```python
records = [
    {
        "name": "router",
        "model_id": "openai/gpt-4.1-nano",
        "credentials": "OPENAI_API_KEY",
        "config": "{\"default_hyperparameters\": {\"temperature\": 0.2}}",
        "system_template": "You are a routing assistant.",
        "user_template": "Select the best route for: {query}",
        "prompt_builder_kwargs": "{\"use_jinja\": false}",
    }
]
```

{% endstep %}

{% step %}
**Load using** `.from_records()` **method**

```python
catalog = LMInvokerCatalog.from_records(records=records)
router_invoker = catalog.router
```

{% endstep %}
{% endstepper %}

### Using Catalog

Once loaded, you can access any LM invoker by its name:

```python
import asyncio

router_output = asyncio.run(catalog.router.invoke("How should I answer this finance question?"))
print(router_output.text)

query_transformer_output = asyncio.run(
    catalog.query_transformer.invoke("Transform this query into search keywords: GDP trend this quarter")
)
print(query_transformer_output.text)
```

---

## LM Request Processor Catalog

{% hint style="warning" %}
**Deprecation Notice:** `LMRequestProcessor` is planned to be deprecated in a future release. For new implementations, please use **LM Invoker Catalog** with prompt-builder fields (`system_template`, `user_template`, and `prompt_builder_kwargs`) and continue with [LM Invoker Prompt Operations](lm-invoker/prompt-operations.md) as the replacement pattern.
{% endhint %}

**LM Request Processor Catalog** enables you to **load and manage multiple LM request processors** from various data sources like Google Sheets, CSV files, or Python records. This allows you to **centralize the configuration of complete AI pipelines**, including prompts, models, credentials, and output parsing in one place.

For example, instead of manually configuring each LM request processor with its model, credentials, and prompts, you can store all configurations in a Google Sheet and load them by name like "summarizer", "question_answerer", and "code_generator".

Think of it as:

> LM Request Processor Catalog is like having a configuration management system for your AI pipelines, where each row defines a complete, ready-to-use AI processor.

### Catalog Configuration

The `LMRequestProcessorCatalog` can be configured using a table (such as a CSV file or Google Sheet), or directly from a list of Python dictionaries (records). To function correctly, the table or records must include specific columns or keys:

**Required Columns:**

1. **name**: The unique identifier for the LM request processor
2. **system_template**: The system template for the prompt builder
3. **user_template**: The user template for the prompt builder
4. **model_id**: The model identifier for the LM invoker
5. **credentials**: Authentication credentials for the model
6. **output_parser_type**: Type of output parser to use

**Optional Columns:**

1. **config**: Additional configuration for the LM invoker (JSON format)
2. **prompt_builder_kwargs**: Advanced prompt builder configuration (JSON format) for Jinja templating and other features

{% hint style="info" %}
**Important Notes:**

- At least one of `system_template` or `user_template` must be filled
- `model_id` supports environment variable substitution using `${ENV_VAR_KEY}` syntax
- `credentials` and `config` are optional but provide advanced functionality
- `prompt_builder_kwargs` enables advanced features like Jinja templating and history formatting
  {% endhint %}

### Loading Catalog

#### Option 1: From Google Sheets

{% stepper %}
{% step %}
**Obtain Worksheet ID and Credentials**

From your Google Sheets URL, you can obtain:

- **`sheet_id`**: between `/d/` and `/edit`
- **`worksheet_id`**: `0` (usually `0` for the first sheet)
  {% endstep %}

{% step %}
**Obtain Google Service Account JSON Credentials**

Follow these steps:

1. [Create a Google service account](https://developers.google.com/workspace/guides/create-credentials#create_a_service_account).
2. [Create JSON credentials for the service account](https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account).
   {% endstep %}

{% step %}
**Load with** `.from_gsheets()` **method**

```python
from gllm_inference.catalog.lm_request_processor_catalog import LMRequestProcessorCatalog

# Method 1: Using client email and private key
catalog = LMRequestProcessorCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    client_email="your_service_account_email",
    private_key="your_private_key",
)

# Method 2: Using credential file
catalog = LMRequestProcessorCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    credential_file_path="path/to/credentials.json"
)
```

{% endstep %}
{% endstepper %}

#### Option 2: From CSV File

{% stepper %}
{% step %}
**Download/create CSV file**

Prepare a CSV file that contains your LM request processor catalog definitions. You can download a template from: [lm_request_processor_catalog_template.csv](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/resources/catalog/lm_request_processor_catalog_template.csv)
{% endstep %}

{% step %}
**Load with** `.from_csv()` **method**

```python
catalog = LMRequestProcessorCatalog.from_csv(csv_path="path/to/lm_request_processor_catalog.csv")
```

{% endstep %}
{% endstepper %}

#### Option 3: From JSON File

{% stepper %}
{% step %}
**Download/create JSON file**

Prepare a JSON file that contains your LM request processor catalog definitions. You can download a template from: [lm_request_processor_catalog_template.json](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/resources/catalog/lm_request_processor_catalog_template.json)
{% endstep %}

{% step %}
**Load with `.from_json()` method**

```python
import json

# Load from JSON file
with open("path/to/lm_request_processor_catalog.json") as f:
    records = json.load(f)

catalog = LMRequestProcessorCatalog.from_records(records=records)
```

{% endstep %}
{% endstepper %}

#### Option 4: From Python Records

{% stepper %}
{% step %}
**Define the catalog**

Provide the records in the format of list of dictionaries. An example can be found below:

```python
records = [
    {
        "name": "router",
        "model_id": "openai/gpt-4.1-nano",
        "credentials": "OPENAI_API_KEY",
        "config": {
            "default_hyperparameters": {
                "temperature": 0.7,
                "max_output_tokens": 100
            }
        },
        "system_template": "You are an AI expert.\nYour job is to define which use case is the most suitable for the user query.\nUse case options:\n1. \"qa\": Question answering.\n2. \"sum\": Summarization.\n3. \"dd\": Document drafting.",
        "user_template": "Below is the user query:\n{query}",
        "prompt_builder_kwargs": {"use_jinja": False},
        "output_parser_type": "none"
    },
    {
        "name": "chat_with_history",
        "model_id": "openai/gpt-4.1-nano",
        "credentials": "OPENAI_API_KEY",
        "config": {
            "default_hyperparameters": {
                "temperature": 0.7,
                "max_tokens": 500
            }
        },
        "system_template": "You are a helpful AI assistant. Continue the conversation based on the chat history provided.",
        "user_template": "{{ history }}\n\n{{ message }}",
        "prompt_builder_kwargs": {
            "use_jinja": True,
            "jinja_env": "restricted",
            "history_formatter": {
                "prefix_user_message": "<user>",
                "suffix_user_message": "</user>",
                "prefix_assistant_message": "<assistant>",
                "suffix_assistant_message": "</assistant>"
            }
        },
        "output_parser_type": "none"
    }
]

```

{% endstep %}

{% step %}
**Load using** `.from_records()` **method**

```python
catalog = LMRequestProcessorCatalog.from_records(records=records)
```

{% endstep %}
{% endstepper %}

### Using Catalog

Once loaded, you can use the LM request processors directly:

```python
import asyncio

# Example: Router - determine use case
router_result = await catalog.router.process(
    query="What are the main benefits of renewable energy sources?"
)
print("Router Result:", router_result)


```

**Output**

```
[Build 'OpenAILMInvoker'] Config:
  {
    'model_name': 'gpt-4.1-nano',
    'default_hyperparameters': { 'temperature': 0.7, 'max_output_tokens': 100 }
  }

Available LM Request Processors:
  - router → Model: gpt-4.1-nano

Running examples:
  [Invoke LM] POST /v1/responses → 200
  [LM Result]
    "The most suitable use case for this query is: 1. 'qa' (Question answering)."

Router Result:
  The most suitable use case selected: "qa" (Question answering)

```
