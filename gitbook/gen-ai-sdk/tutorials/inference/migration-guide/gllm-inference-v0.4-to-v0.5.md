---
icon: arrow-progress
---

# GLLM Inference v0.4 to v0.5

As you may have noticed, several legacy modules in GLLM Inference v0.4 have been marked as deprecated for a while. If your application is still using them, you should have received warning logs.

Backward compatibility will be **removed** in the upcoming minor version `v0.5.0`. Please review this migration guide to ensure a smooth transition.

{% hint style="info" %}
Note: If you've set the GLLM Inference dependency in your app as `^0.4.0`, you don't have to do this migration immediately, as you're locked to `v0.4.x`. You will only migrate to `0.5.0` when you choose to do so by updating your dependency to `^0.5.0`.

However, its still recommended to do so ASAP to be able to access new features that will be added in the future.
{% endhint %}

#### Part 1: Prompt Builder

1. The following modules are deprecated:
   1. `AgnosticPromptBuilder`
   2. `HuggingFacePromptBuilder`
   3. `LlamaPromptBuilder`
   4. `MistralPromptBuilder`
   5. `OpenAIPromptBuilder`
   6. `MultimodalPromptBuilder`
2. All capability to build prompts to be consumable by `LM invoker` will be replaced by the new [PromptBuilder](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-inference/gllm_inference/prompt_builder/prompt_builder.py#L28) class. `LMRP` will only support this class. The prompt builder no longer has interface and subclasses.
3. If you want to use the `format_as_string` capability previously provided by the deprecated subclasses, please use the new [PromptFormatter](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/prompt_formatter) modules. However, you shouldnt need this to work with `LM invoker` and `LMRP`.

#### Part 2: LM Invoker

1. All `...MultimodalLMInvoker` are deprecated and are replaced with their `...LMInvoker` counterpart.
   1. e.g., `OpenAIMultimodalLMInvoker` is replaced by `OpenAILMInvoker`.
2. Google classes have been merged into a single class: `GoogleLMInvoker`.
3. All LM invoker has been migrated to:
   1. Use native providers SDK instead of LangChain implementation.
   2. Support multimodality, tool calling, structured output, analytics, retry, timeout, and some provider-specific features.
4. `bind_tool_params` param is deprecated and is replaced by `tools` param.
5. `with_structured_output_params` param is deprecated and is replaced by `response_schema` param.

#### Part 3: EM Invoker

1. All `...MultimodalEMInvoker` are deprecated and are replaced with their `...LMInvoker` counterpart.
   1. e.g., `TwelveLabsMultimodalEMInvoker` is replaced by `TwelveLabsEMInvoker`.
2. Google classes have been merged into a single class: `GoogleEMInvoker`.
3. All EM invoker has been migrated to use native providers SDK instead of LangChain implementation.

#### Part 4: Catalog

1. Catalogs has been simplified.
2. Prompt builder catalog will only require these columns:
   1. `name`
   2. `system`
   3. `user`
3. LMRP catalog will only require these columns:
   1. `name`
   2. `system_template`
   3. `user_template`
   4. `model_id`, e.g. `openai/gpt-4.1-nano`
   5. `credentials`, will be loaded from env var, e.g. `OPENAI_API_KEY`
   6. `config`, dictionary to be passed to the LM invoker, e.g. `{"default_hyperparameters": {"temperature": 0.7}}`
   7. `output_parser_type` , either `none` or `json`
4. Example:
   1. [Prompt builder catalog new format](https://docs.google.com/spreadsheets/d/12IwSKv8hMhyWXSQnLx9LgCj0cxaR1f9gOmbEDGleurE/edit)
   2. [LMRP catalog new format](https://docs.google.com/spreadsheets/d/1Mmqk8xVz7iJ8MVEwistKr9ENP1ctSH1D3BMw7NoHizI/edit)

#### Part 5: Miscellaneous Stuff

1. `ModelId` and `ModelProvider` should now be imported from `gllm_inference.schema` instead of `gllm_inference.builder`
2. `retry` and `RetryConfig` should now be imported from `gllm_core.utils.retry` instead of `gllm_inference.utils.retry`
