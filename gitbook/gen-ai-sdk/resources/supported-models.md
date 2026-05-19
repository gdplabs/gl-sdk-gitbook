---
icon: gear
---

# Supported Models

This page provides a list of all supported language models and embedding models.

## Language Models (LMs)

LMs are used to generate natural language responses, either directly from user prompts or based on retrieved context in a RAG pipeline. Use one of the model IDs below to configure the language model component.

### **Anthropic**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>anthropic/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>anthropic/claude-sonnet-4-6</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>ANTHROPIC_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://console.anthropic.com/settings/keys">Create Anthropic API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.anthropic.com/en/docs/about-claude/models/overview">Anthropic Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import AnthropicLMInvoker

lm_invoker = AnthropicLMInvoker("claude-sonnet-4-6")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="anthropic/claude-sonnet-4-6")
```

### **Azure OpenAI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>azure-openai/azure-endpoint:azure-deployment</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>azure-openai/https://my-resource.openai.azure.com:my-deployment</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>AZURE_OPENAI_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><p><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource">Create Resource</a></p><p><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model">Deploy Model</a></p></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions">Azure OpenAI Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import AzureOpenAILMInvoker

lm_invoker = AzureOpenAILMInvoker(
    azure_endpoint="https://my-resource.openai.azure.com",
    azure_deployment="my-deployment",
)
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(
    model_id="azure-openai/https://my-resource.openai.azure.com:my-deployment"
)
```

### **Bedrock**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>bedrock/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><p><code>AWS_ACCESS_KEY_ID</code></p><p><code>AWS_SECRET_ACCESS_KEY</code></p></td></tr><tr><td><strong>Setup Guide</strong></td><td><p><a href="https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html">Create AWS Account</a></p><p><a href="https://docs.aws.amazon.com/keyspaces/latest/devguide/create.keypair.html">Create Access Keys</a></p></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html">AWS Bedrock Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import BedrockLMInvoker

lm_invoker = BedrockLMInvoker("us.anthropic.claude-sonnet-4-20250514-v1:0")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0")
```

### **DeepSeek**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>deepseek/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>deepseek/deepseek-v4-flash</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>DEEPSEEK_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://platform.deepseek.com/api_keys">Create DeepSeek API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://api-docs.deepseek.com/quick_start/pricing">DeepSeek Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import DeepSeekLMInvoker

lm_invoker = DeepSeekLMInvoker("deepseek-v4-flash")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="deepseek/deepseek-v4-flash")
```

### **Google Gen AI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>google/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>google/gemini-2.5-flash-lite</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>GOOGLE_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://aistudio.google.com/app/apikey">Create Gemini API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://ai.google.dev/gemini-api/docs/models">Google Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import GoogleLMInvoker

lm_invoker = GoogleLMInvoker("gemini-2.5-flash-lite")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="google/gemini-2.5-flash-lite")
```

### **Google Vertex AI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>google/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>google/gemini-2.5-flash-lite</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td>Not supported</td></tr><tr><td><strong>Setup Guide</strong></td><td><p><a href="https://developers.google.com/workspace/guides/create-credentials#create_a_service_account">Create Google Service Account</a></p><p><a href="https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account">Create JSON Credentials</a></p></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://ai.google.dev/gemini-api/docs/models">Google Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import GoogleLMInvoker

lm_invoker = GoogleLMInvoker("gemini-2.5-flash-lite")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="google/gemini-2.5-flash-lite")
```

### **LangChain**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>langchain/&#x3C;package>.&#x3C;class>:model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>langchain/langchain_openai.ChatOpenAI:gpt-5.4-nano</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td>Varies depending on the package and class.</td></tr><tr><td><strong>Setup Guide</strong></td><td>Varies depending on the package and class.</td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://python.langchain.com/docs/integrations/chat/#featured-providers">LangChain Providers</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import LangChainLMInvoker

lm_invoker = LangChainLMInvoker(
    model_class_path="langchain_openai.ChatOpenAI",
    model_name="gpt-5.4-nano",
)
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="langchain/langchain_openai.ChatOpenAI:gpt-5.4-nano")
```

### **LiteLLM**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>litellm/provider/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>litellm/openai/gpt-5.4-nano</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td>Varies depending on the provider.</td></tr><tr><td><strong>Setup Guide</strong></td><td>Varies depending on the provider.</td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.litellm.ai/docs/providers/">LiteLLM Providers</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import LiteLLMLMInvoker

lm_invoker = LiteLLMLMInvoker("openai/gpt-5.4-nano")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="litellm/openai/gpt-5.4-nano")
```

### **OpenAI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>openai/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>openai/gpt-5.4-nano</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>OPENAI_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://platform.openai.com/api-keys">Create OpenAI API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://platform.openai.com/docs/pricing">OpenAI Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import OpenAILMInvoker

lm_invoker = OpenAILMInvoker("gpt-5.4-nano")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="openai/gpt-5.4-nano")
```

### OpenAI Chat Completions

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>openai-chat-completions/base-url:model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>openai-chat-completions/https://api.groq.com/openai/v1:llama3-8b-819</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td>Varies depending on the provider.</td></tr><tr><td><strong>Setup Guide</strong></td><td>Varies depending on the provider.</td></tr><tr><td><strong>Available Models</strong></td><td><p>Compatible endpoints include but are not limited to:</p><ol><li><a href="https://deepinfra.com/">DeepInfra</a></li><li><a href="https://deepseek.com/">DeepSeek</a></li><li><a href="https://groq.com/">Groq</a></li><li><a href="https://openrouter.ai/">OpenRouter</a></li><li><a href="https://github.com/huggingface/text-generation-inference">Text Generation Inference</a></li><li><a href="https://together.ai/">Together.ai</a></li><li><a href="https://vllm.ai/">vLLM</a></li></ol></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import OpenAIChatCompletionsLMInvoker

lm_invoker = OpenAIChatCompletionsLMInvoker(
    "llama3-8b-819", base_url="https://api.groq.com/openai/v1"
)
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(
    model_id="openai-chat-completions/https://api.groq.com/openai/v1:llama3-8b-819"
)
```

### Portkey

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>portkey/model-name</code> or <code>portkey/catalog-name/model-name</code>  </td></tr><tr><td><strong>Model ID Example</strong></td><td><code>portkey/gpt-5.4-nano</code><br><code>portkey/@google-custom-slug/gemini-2.5-pro</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><p><code>PORTKEY_API_KEY</code></p><p>Varies depending on the provider and authentication method.</p></td></tr><tr><td><strong>Setup Guide</strong></td><td>Varies depending on the provider.</td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://portkey.ai/docs/integrations/llms">Portkey Providers</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import PortkeyLMInvoker

lm_invoker = PortkeyLMInvoker("gpt-5.4-nano")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="portkey/gpt-5.4-nano")
```

### xAI

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>xai/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>xai/grok-3</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>XAI_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://console.anthropic.com/settings/keys">Create xAI API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.anthropic.com/en/docs/about-claude/models/overview">xAI Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.lm_invoker import XAILMInvoker

lm_invoker = XAILMInvoker("grok-3")
```

Initialize with builder helper:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="xai/grok-3")
```

## Embedding Models (EMs)

Embedding models are used to convert text into vector representations, enabling similarity search and document retrieval. Use one of the model IDs below to configure the embedding model component.

### **Azure OpenAI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>azure-openai/azure-endpoint:azure-deployment</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>azure-openai/https://my-resource.openai.azure.com:my-deployment</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>AZURE_OPENAI_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><p><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource">Create Resource</a></p><p><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model">Deploy Model</a></p></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions">Azure OpenAI Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import AzureOpenAIEMInvoker

em_invoker = AzureOpenAIEMInvoker(
    azure_endpoint="https://my-resource.openai.azure.com",
    azure_deployment="my-deployment",
)
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(
    model_id="azure-openai/https://my-resource.openai.azure.com:my-deployment"
)
```

### **Bedrock**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>bedrock/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>bedrock/amazon.titan-embed-text-v2:0</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><p><code>AWS_ACCESS_KEY_ID</code></p><p><code>AWS_SECRET_ACCESS_KEY</code></p></td></tr><tr><td><strong>Setup Guide</strong></td><td><p><a href="https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html">Create AWS Account</a></p><p><a href="https://docs.aws.amazon.com/keyspaces/latest/devguide/create.keypair.html">Create Access Keys</a></p></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html">AWS Bedrock Embedding Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import BedrockEMInvoker

em_invoker = BedrockEMInvoker("amazon.titan-embed-text-v2:0")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="bedrock/amazon.titan-embed-text-v2:0")
```

### **Cohere**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>cohere/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>cohere/embed-english-v3.0</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>COHERE_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://dashboard.cohere.com/welcome/login">Create Cohere API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.cohere.com/reference/list-models">Cohere Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import CohereEMInvoker

em_invoker = CohereEMInvoker("embed-english-v3.0")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="cohere/embed-english-v3.0")
```

### **Google Gen AI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>google/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>google/text-embedding-004</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>GOOGLE_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://aistudio.google.com/app/apikey">Create Gemini API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings">Google Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import GoogleEMInvoker

em_invoker = GoogleEMInvoker("text-embedding-004")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="google/text-embedding-004")
```

### **Google Vertex AI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>google/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>google/text-embedding-004</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td>Not supported</td></tr><tr><td><strong>Setup Guide</strong></td><td><p><a href="https://developers.google.com/workspace/guides/create-credentials#create_a_service_account">Create Google Service Account</a></p><p><a href="https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account">Create JSON Credentials</a></p></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings">Google Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import GoogleEMInvoker

em_invoker = GoogleEMInvoker("text-embedding-004")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="google/text-embedding-004")
```

### **Jina**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>jina/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>jina/embed-english-v3.0</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>JINA_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://jina.ai/api-dashboard">Create Jina API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://jina.ai/models">Jina Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import JinaEMInvoker

em_invoker = JinaEMInvoker("embed-english-v3.0")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="jina/embed-english-v3.0")
```

### **LangChain**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>langchain/&#x3C;package>.&#x3C;class>:model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>langchain/langchain_openai.OpenAIEmbeddings:text-embedding-3-small</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td>Varies depending on the package and class.</td></tr><tr><td><strong>Setup Guide</strong></td><td>Varies depending on the package and class.</td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://python.langchain.com/docs/integrations/text_embedding/">LangChain Providers</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import LangChainEMInvoker

em_invoker = LangChainEMInvoker(
    model_class_path="langchain_openai.OpenAIEmbeddings",
    model_name="text-embedding-3-small",
)
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(
    model_id="langchain/langchain_openai.OpenAIEmbeddings:text-embedding-3-small"
)
```

### **OpenAI**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>openai/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>openai/text-embedding-3-small</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>OPENAI_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://platform.openai.com/api-keys">Create OpenAI API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://platform.openai.com/docs/pricing">OpenAI Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker("text-embedding-3-small")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
```

### **TwelveLabs**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>twelvelabs/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>twelvelabs/Marengo-retrieval-2.7</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>TWELVELABS_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://docs.twelvelabs.io/api-reference/authentication">Create TwelveLabs API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.twelvelabs.io/docs/concepts/models">TwelveLabs Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import TwelveLabsEMInvoker

em_invoker = TwelveLabsEMInvoker("Marengo-retrieval-2.7")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="twelvelabs/Marengo-retrieval-2.7")
```

### **Voyage**

<table data-header-hidden><thead><tr><th width="197.0390625"></th><th></th></tr></thead><tbody><tr><td><strong>Model ID Format</strong></td><td><code>voyage/model-name</code></td></tr><tr><td><strong>Model ID Example</strong></td><td><code>voyage/voyage-3.5-lite</code></td></tr><tr><td><strong>Credentials Default Environment Variables</strong></td><td><code>VOYAGE_API_KEY</code></td></tr><tr><td><strong>Setup Guide</strong></td><td><a href="https://docs.voyageai.com/docs/api-key-and-installation">Create Voyage API Key</a></td></tr><tr><td><strong>Available Models</strong></td><td><a href="https://docs.voyageai.com/docs/pricing">Voyage Models</a></td></tr></tbody></table>

Initialize with class invoker:

```python
from gllm_inference.em_invoker import VoyageEMInvoker

em_invoker = VoyageEMInvoker("voyage-3.5-lite")
```

Initialize with builder helper:

```python
from gllm_inference.em_invoker import build_em_invoker

em_invoker = build_em_invoker(model_id="voyage/voyage-3.5-lite")
```
