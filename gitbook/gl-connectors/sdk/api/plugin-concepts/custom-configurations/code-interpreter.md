---
icon: code
---

# Code Interpreter

{% hint style="success" %}
**Module name: `code_interpreter`**
{% endhint %}

{% hint style="warning" %}
**Currently only support `Python` code execution**
{% endhint %}

The **Code Interpreter** provides a sandbox for remote code execution by leveraging E2B. Additionally, the sandbox supports third-party packages installed using pip, allowing you to use a wide collection of external libraries and modules.

This guide will walk you through configuring and how to use the Code Interpreter.

## Configuration Parameters

**You do not need to configure anything for Code Interpreter as of right now**. All users are granted access to Connector's Code Interpreter instance immediately, and as such, can use its services directly upon the creation of their account.

## Usage Example

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="https://connectors.gdplabs.id", api_key="your_api_key")

user_token = "a_unique_user_token"

print("Executing code...")
code_interpreter = connector.connect('code_interpreter')

response = code_interpreter.action("execute_code") \
    .token(user_token) \
    .params({
        "code": "print(\"Hello world!\")",
    }) \
    .execute()

print("Execute code response:", response)
```
