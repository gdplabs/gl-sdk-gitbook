---
icon: rectangle-terminal
---

# Logs

In modern distributed systems, logs are essential for debugging, but they often unintentionally capture sensitive data. This is problematic because it violates privacy compliance standards such as GDPR, SOC2, and UU PDP.

GL Observability provides components for PII Redaction for logger to ensure your logs are both secure and useful. You can select either regex-based masking for speed and simplicity or Named Entity Recognition (NER)-based masking for advanced, context-aware detection. This ensures sensitive information in logs is automatically masked while maintaining log readability and usefulness.

## Integration Guide

To help you integrate PII-safe logging into your application, this section provides step-by-step guidance on using the available logger handlers from GL Observability.

{% stepper %}
{% step %}
#### Import Components

```python
import logging

# Regex based logger
from gl_observability.logs.regex_pii_logger_handler import init_regex_pii_logging_handler

# NER API based logger
from gl_observability.logs.ner_pii_logger_handler import init_ner_pii_logging_handler
```
{% endstep %}

{% step %}
#### Initializing PII Logging Handler

{% hint style="warning" %}
The PII Logging handler must be initialized before adding any logging handler. It is critical to follow this order because order matters in logging handler. If you add a data-exporting handler before the PII Logging handler, it will receive and transmit the original, unmasked sensitive data.
{% endhint %}

When initializing the PII Logger, you will need to provide specific parameters depending on which handler you choose. The configuration options reflect the underlying mechanism (regex-based or NER-based) used for PII redaction.

**Regex based logger**

```python
init_regex_pii_logging_handler(
    logger_name="logger-name", 
    pii_regex_process_enabled=True
)
```

**Parameters**:

* `logger_name: str` — Name of the logger to attach the handler to.
* `pii_regex_process_enabled: bool` — Enable/disable PII processing. Default to `False`.

**NER API based logger**

```python
init_ner_pii_logging_handler(
    logger_name="logger-name",
    api_url="your ner api url...",
    api_field="text",
    pii_ner_process_enabled=True
)
```

**Parameters**:

* `logger_name: str` — Name of the logger to attach the handler to.
* `api_url: str` — URL of the NER API endpoint.
* `api_field: str` — Field name for the text in the API request.
* `pii_ner_process_enabled: bool` — Enable/disable PII processing. Default to `False`.
{% endstep %}

{% step %}
#### Add Another Handler

After the PII Logging handler is initialized, you can now add other logging handlers (e.g., `StreamHandler`, `FileHandler`, etc).
{% endstep %}

{% step %}
#### Usage

Now, when you log messages containing sensitive data, the logger will automatically redact PII.

```python
sensitive_info = (
    "contoh nomor ktp 3525011212941001\n"
    "contoh email john.doe@example.com\n"
    "contoh nomor telepon +628121729819 dan 0812898029384.\n"
    "contoh npwp 01.123.456.7-891.234"
)

logger.info(f"Logging sensitive information for processing: \n{sensitive_info}")
```
{% endstep %}
{% endstepper %}

## Choosing Between Regex and NER Logging <a href="#choosing-between-regex-and-ner-logging" id="choosing-between-regex-and-ner-logging"></a>

When deciding between regex and NER based logging, consider the following trade-offs:

* **Regex-based Logging**:
  * Fast and efficient
  * Easy to customize
  * Ideal for environments with high logging throughput
  * Limited in detecting context-aware or varied formats
* **NER-based Logging:**
  * More accurate, especially for unstructured text
  * Suitable for sensitive or complex data types (e.g., names, locations, social URLs)
  * Depends on an external API (may introduce latency or downtime risk)

### Supported PII Types <a href="#supported-pii-types" id="supported-pii-types"></a>

The logger currently supports detection and masking for the following types of sensitive information:

| PII                               | NER Based | Regex Based |
| --------------------------------- | :-------: | :---------: |
| KTP number                        |     ✅     |      ✅      |
| NPWP number                       |     ✅     |      ✅      |
| Family card number                |     ✅     |      ✖️     |
| Person name                       |     ✅     |      ✖️     |
| Organization name                 |     ✅     |      ✖️     |
| Location name                     |     ✅     |      ✖️     |
| Phone number                      |     ✅     |      ✅      |
| Email address                     |     ✅     |      ✅      |
| International bank account number |     ✅     |      ✖️     |
| Credit card number                |     ✅     |      ✖️     |
| Cryptocurrency wallet number      |     ✅     |      ✖️     |
| IP address                        |     ✅     |      ✖️     |
| Facebook account URL              |     ✅     |      ✖️     |
| LinkedIn account URL              |     ✅     |      ✖️     |
