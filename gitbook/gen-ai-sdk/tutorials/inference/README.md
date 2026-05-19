---
icon: messages-question
---

# Inference

## What is inference?

Inference is a core process in our SDK, responsible for invoking models and retrieving their outputs. The inference modules provide a unified interface to access a wide range of model providers, making it easy to integrate, switch, and extend models in a plug-and-play manner. The inference involves two types of models:

1. **Language Models (LM):** A model that understands natural language and generates outputs based on the provided inputs. Often used for tasks like text generation, summarization, and many more. LM inference in the SDK involves the following components:
   1. [LM Invoker](lm-invoker/)
   2. [Prompt Builder](prompt-builder.md)
   3. [LM Request Processor](lm-request-processor.md)
2. **Embedding Model (EM):** A model that converts inputs into numerical vector representations. Often used for tasks like semantic search, clustering, similarity comparisons, and many more. EM inference in the SDK involves the following components:
   1. [EM Invoker](em-invoker.md)
3. **Realtime Model:** A model that has the capability to perform realtime interactions through various media, such as text, audio, and even image. Realtime model inference in the SDK involves the following components:
   1. **\[Beta]** [Realtime session](realtime-session.md)
