---
icon: arrow-progress
---

# GLLM Inference v0.5 to v0.6

As you may have noticed, several legacy modules in GLLM Inference v0.5 have been marked as deprecated for a while. If your application is still using them, you should have received warning logs.

Backward compatibility will be **removed** in the upcoming minor version `v0.6.0`. Please review this migration guide to ensure a smooth transition.

{% hint style="info" %}
Note: If you've set the GLLM Inference dependency in your app as `>=0.5.0, <0.6.0`, you don't have to do this migration immediately, as you're locked to `v0.5.x`. You will only migrate to `0.6.0` when you choose to do so by updating your dependency to `>=0.6.0`.

However, its still recommended to do so ASAP to be able to access new features that will be added in the future.
{% endhint %}

{% hint style="warning" %}
Note: This guide is still a work in progress. More contents will be added gradually.
{% endhint %}

## Builder

1. The `gllm_inference.builder` path is removed:
   1.  To use EM invoker builder util, please use this new path:

       ```python
       from gllm_inference.em_invoker import build_em_invoker
       ```
   2.  To use LM invoker builder util, please use this new path:

       ```python
       from gllm_inference.lm_invoker import build_lm_invoker
       ```
   3.  To use LM request processor builder util, please use this new path:

       ```python
       from gllm_inference.request_processor import build_lm_request_processor
       ```
   4. The `build_output_parser` util is removed along with the output parser modules. For more information, please refer to the [output parser section](gllm-inference-v0.5-to-v0.6.md#output-parser).

## EM Invoker

1. `OpenAICompatibleEMInvoker` is removed. To use OpenAI Embeddings API compatible providers, please use the `OpenAIEMInvoker` by providing a `base_url`.
2. The temporary `twelevelabs_em_invoker` module (with misspelling) is removed. If you were importing from this module, please update your imports to use `twelvelabs_em_invoker` (correct spelling) instead.

## LM Invoker

1. `OpenAICompatibleLMInvoker` is removed. To use OpenAI Chat Completions API compatible providers, please use the `OpenAIChatCompletionsLMInvoker` by providing a `base_url`.
2. LM invokers' `invoke()` method will now **always** return an `LMOutput` object regardless of whether it has non-text attributes or not. It will no longer return `str` outputs.
3. Legacy streaming events format support is removed.
   1. The new streaming events format can be achieved in `gllm_inference-v0.5` by setting the `simplify_events` param to `True`. This temporary param is also removed in `gllm_inference-v0.6`.
4.  LangChain Tool support is removed. Use GLLM Core's `tool` decorator or `Tool` class or instead:

    ```python
    @tool
    def custom_tool(query: str) -> str:
        ...
    # or
    class CustomTool(Tool) -> str:
        ...
    ```
5.  Provider-specific reasoning and thinking parameters are removed from all LM invokers. Use `ThinkingConfig` instead. You can obtain the keyword arguments for the provider by inspecting the provider's docs. Examples:

    ```python
    invoker = OpenAILMInvoker(
        "gpt-4-turbo",
        api_key="key",
        thinking=ThinkingConfig(enabled=True, kwargs={"effort": "high"})
    )

    invoker = AnthropicLMInvoker(
        "claude-3-7-sonnet",
        api_key="key",
        thinking=ThinkingConfig(enabled=True, kwargs={"budget_tokens": 2048}
    )
    ```
6.  The `Reasoning` class is renamed to `Thinking`. Update all imports and usages:

    ```python
    # before (v0.5)
    from gllm_inference.schema import Reasoning

    output.add_thinking(Reasoning(reasoning="I'm thinking..."))

    # after (v0.6)
    from gllm_inference.schema import Thinking

    output.add_thinking(Thinking(thinking="I'm thinking..."))
    ```

    Note: The attribute name also changed from `reasoning` to `thinking` to better reflect the extended thinking capability.
7.  Removed `GoogleLMInvoker` support for passing Google Generative Language API `/files/` URLs as regular `Attachment` objects. Use `UploadedAttachment` instead:

    ```python
    # before
    content = Attachment(url="https://generativelanguage.googleapis.com/v1beta/files/...")

    # after
    content = UploadedAttachment(id="", provider=ModelProvider.GOOGLE, url="https://generativelanguage.googleapis.com/v1beta/files/...")
    ```

## Output Parser

1. The output parser modules under `gllm_inference.output_parser` are removed altogether.
   1.  If you're previously using `JSONOutputParser`, please try to substitute it by assigning `JSONOutputTransformer` to your LM invoker as such:<br>

       ```python
       lm_invoker = OpenAILMInvoker(..., output_transformer="json")
       output = await lm_invoker.invoke(...)
       parsed_output = output.structured_output
       ```

## LM Request Processor

1. LMRP's `process()` method will now **always** return an `LMOutput` object regardless of whether it has non-text attributes or not. It will no longer return `str` outputs.
2.  The `prompt_kwargs` parameter in `process()` method is removed. Pass prompt kwargs as keyword arguments instead:

    ```python
    # before
    await processor.process(prompt_kwargs={"query": "What is AI?"})

    # after
    await processor.process(query="What is AI?")
    ```
3. The `key_defaults` parameter is removed. Use `prompt_builder_kwargs` instead:
   1.  in catalog:

       ```json
       {
         ...
         "prompt_builder_kwargs": "{\"key_defaults\": {\"query\": \"default query\"}}"
       }
       ```
   2.  in `build_lm_request_processor()`:

       ```python
       build_lm_request_processor(
           ...,
           prompt_builder_kwargs={"key_defaults": {"query": "default query"}}
       )
       ```

## Prompt Builder

1. The `ignore_extra_keys` parameter is removed from `PromptBuilder.__init__()`. Extra keys in `kwargs` will now always raise a warning.
2.  The `kwargs` column is now required in PromptBuilder catalog CSV/JSON files. For example:

    ```json
    {
      "name": "my_builder",
      "system": "You are helpful.",
      "user": "{query}",
      "kwargs": "{\"key_defaults\": {\"query\": \"default query\"}}"
    }
    ```

## LM Output Schema

1. The following properties have been removed:
   1. `response`: Replaced by `text`.
   2. `reasoning`: Replaced by `thinkings`.
2. Setting LM output items either directly during init or by setting attributes are no longer supported. Instead, please use the provided adder methods.

```python
output = LMOutput()
output.add_text("Hi there!")
output.add_structured_output({"id": "123", "name": "John"})
```

## Realtime Chat

1. Realtime chat modules are removed, as they've been directly replaced by **realtime session** modules.
