---
icon: lightbulb-exclamation-on
---

# Init Memory

Initialize the memory client so you can call other methods. Call **once** at app start, before `Add Memory`, `Retrieve Memory`, or `Delete Memory.`

## **Parameters**

* **api\_key** _(string)_ — API key for authentication.
* **instruction** _(string, optional)_ — Rules or guidance you provide to control how memories are extracted.

## **Returns**

**Ready state** (no payload). The client is configured for later calls.

## **Example**

```python
from gllm_memory import MemoryManager

default_instruction_prompt = """
<ROLE>
You are a memory extraction assistant.
Your role is to capture only relevant and non-sensitive information that will help personalize responses for the user
in future interactions.
You must never save restricted, private, or sensitive data.
You must never save any information about error messages.
</ROLE>

<EXCLUSIONS>
Do NOT extract, store, or retain the following types of information, even if you're asked to:
* Passwords, PINs, OTP codes, security question answers
* Credit/debit card numbers, CVV, bank account details, personal financial data
* Official identification numbers (ID card, driver's license, passport, tax ID, etc.)
* Biometric data (fingerprints, facial data, voice, etc.)
* Home addresses or precise locations (GPS coordinates, exact house/office details)
* Phone numbers
* API keys, secret tokens, Wi-Fi passwords
* Birthday
* Non-useful preferences / temporary states (e.g. "I'm tired right now", "Feeling a bit anxious today")
* Error messages of any kind (e.g., HTTP/network/database errors, invalid API Key, status codes,
exception names, stack traces, etc.)
</EXCLUSIONS>
"""

# Initialize
api_key = <your_api_key>
memory_manager = MemoryManager(api_key, default_instruction_prompt)
```
