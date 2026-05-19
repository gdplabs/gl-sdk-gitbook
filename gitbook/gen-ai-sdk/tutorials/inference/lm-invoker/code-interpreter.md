---
icon: square-code
---

# Code Interpreter

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [code-interpreter.md](code-interpreter.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `AnthropicLMInvoker`, `GoogleLMInvoker`, `OpenAILMInvoker` , `XAILMInvoker`

## What is Code Interpreter?

Code interpreter is a native tool that allows the language model to write and run Python code in a sandboxed environment to solve complex problems in domains like data analysis, coding, and math. When it's enabled, code execution results are stored in the `outputs` attribute of the `LMOutput` object and can be accessed via the `code_exec_results` property.

Code interpreter tool can be enabled with several options:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as string
code_interpreter_tool = "code_interpreter"
# Option 2: as enum
code_interpreter_tool = NativeToolType.CODE_INTERPRETER
# Option 3: as dictionary (useful for providing custom kwargs)
code_interpreter_tool = {"type": "code_interpreter", **kwargs}
# Option 4: as native tool object (useful for providing custom kwargs)
code_interpreter_tool = NativeTool.code_interpreter(**kwargs)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[code_interpreter_tool])
```

When using `OpenAILMInvoker`'s code interpreter capability, the models internally recognize the code interpreter as the `Python tool`. Thus, it's recommended to explicitly instruct the model to use the `Python tool` to ensure more reliable code execution. Let's try it to solve a simple math problem!

```python
query = "Use the Python tool to calculate 4.77 * 7.44"
output = asyncio.run(lm_invoker.invoke(query))
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
```

**Output:**

```
=== Output item: 'code_exec_result' ===
CodeExecResult(
    id='ci_68a59ef2eee081958b15409834488d310c99b82ee9b2c6a9',
    code='print(4.77*7.44)',
    output=['35.4888\n'],
)

=== Output item: 'text' ===
35.4888
```

What's awesome about code intepreter is that it can produce **more than just a text**! In the example below, let's try creating a histogram using the code intrepreter. We're going to save any generated attachment to our local path.

```python
query = "Use the Python tool generate a histogram for the following data: [1, 1, 3, 2, 4, 1, 2]. Make it light blue."
output = asyncio.run(lm_invoker.invoke(query))
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")

# Saving the created image
for item in output.code_exec_results:
    for code_output in item.output:
        if isinstance(code_output, Attachment):
            code_output.write_to_file("path/to/output.png")
```

**Output:**

```
=== Output item: 'code_exec_result' ===
CodeExecResult(
    id='ci_68a5a079296c8195a47fc7027ff7850906af19557003f1ce',
    code="""
        # Generating and saving a histogram for the provided data
        import matplotlib.pyplot as plt

        data = [1, 1, 3, 2, 4, 1, 2]

        plt.figure(figsize=(6, 4))
        # Use bins centered on integer values 1-4
        plt.hist(data, bins=[0.5, 1.5, 2.5, 3.5, 4.5], color='lightblue', edgecolor='black')
        plt.xticks([1, 2, 3, 4])\r\nplt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Histogram of Given Data')
        plt.tight_layout()

        # Save the figure
        output_path = '/mnt/data/histogram.png'
        plt.savefig(output_path, dpi=150)
        plt.show()

        output_path"
    """,
    output=[
        Attachment(
            filename='f99f718d-30a5-493f-b4c8-97ac35cab552.png',
            extension='png',
            mime_type='image/png',
            url=None,
            data='89504e470d0a1a0a0000...'
        ),
        "'/mnt/data/histogram.png'",
    ]
)

=== Output item: 'text' ===
I've created the histogram and saved it.
```

Below is the generated histogram that has been saved in our local path. What an awesome way to use a language model!

<figure><img src="../../../../.gitbook/assets/image (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
