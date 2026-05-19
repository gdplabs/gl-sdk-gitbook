---
icon: scroll
---

# Logger Manager

## What is LoggerManager?

`LoggerManager` is a singleton that centralizes logging configuration across all GLLM components.

1. It initializes the **root logger** exactly once.
2. It configures a **default handler and formatter** based on the `LOG_FORMAT` environment variable.
3. It provides a simple API to **get loggers**, **change formats/levels**, and **attach custom handlers**.
4. It ensures that child loggers from different parts of the SDK share consistent behavior.

Internally, `LoggerManager` lives in `gllm_core.utils.logger_manager.LoggerManager` and is used by components such as `Component` to obtain properly configured loggers.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-core"
```
{% endtab %}
{% endtabs %}

## Quickstart

A minimal usage pattern looks like this:

```python
import logging
from gllm_core.utils.logger_manager import LoggerManager


manager = LoggerManager()
logger = manager.get_logger("my_app")

logger.info("Application started")
logger.debug("Debug details", extra={"error_code": "SAMPLE"})
```

End-to-end behavior:

1. `LoggerManager()` creates (or returns) the singleton instance and initializes the root logger on first use.
2. `get_logger("my_app")` returns a **child logger** under the shared root.
3. Child loggers reuse the same handlers and formatter as the root logger.
4. Messages you log are formatted according to the active log mode (text, simple, or JSON).

## Logging Modes

`LoggerManager` supports three logging modes, controlled by the `LOG_FORMAT` environment variable.

1. **Text mode**
   1. Activated when `LOG_FORMAT=text` (or when `LOG_FORMAT` is unset and the default is used).
   2. Uses `TextRichHandler`, a `RichHandler` subclass with per-level colors and `[LoggerName]` prefixes.
   3. Typical for local development where rich, human-readable logs are preferred.
2. **Simple mode**
   1. Activated when `LOG_FORMAT=simple`.
   2.  Uses `SimpleRichHandler`, a thin wrapper around `logging.StreamHandler` that prints lines such as:

       ```log
       [2025-10-08T09:26:16.123 LoggerName DEBUG] This is a debug message.
       ```
   3. Keeps Rich coloring but avoids column-based layout.
3. **JSON mode**
   1. Activated when `LOG_FORMAT=json`.
   2. Uses a standard `StreamHandler` with `AppJSONFormatter`.
   3.  Outputs structured JSON objects, for example:

       ```log
       {"timestamp": "2025-10-08T11:23:43+0700", "name": "LoggerName", "level": "DEBUG", "message": "..."}
       ```
   4. Best suited for log aggregation systems and machine parsing.

If `LOG_FORMAT` is not set or contains an unsupported value, `LoggerManager` falls back to **text mode**.

## Getting Loggers

Use `get_logger` to obtain either the root logger or a named child logger.

```python
manager = LoggerManager()

# 1. Root logger
root_logger = manager.get_logger()

# 2. Child logger for a specific module or component
component_logger = manager.get_logger("gllm_core.my_component")
```

Behavior summary:

1. Calling `get_logger()` with no name returns the **root logger**.
2. Calling `get_logger(name)` returns a **child logger** with that name.
3. Child loggers:
   1. Have `propagate = False` to avoid double-logging.
   2. Inherit handlers from the root if they do not have handlers yet.
4. All loggers share the same formatter and respect the same log level set on the root.

## Configuring Levels and Formats

`LoggerManager` exposes methods to adjust logging behavior at runtime.

1.  **Set log level for the entire hierarchy**

    ```python
    import logging
    manager = LoggerManager()
    manager.set_level(logging.DEBUG)
    ```

    1. Updates the level of the **root logger**.
    2. Affects all child loggers unless they override the level individually.
2.  **Set a custom log format string**

    ```python
    manager = LoggerManager()
    manager.set_log_format("[%(asctime)s %(name)s %(levelname)s] %(message)s")
    ```

    1. Rebuilds the formatter using the new format string.
    2. Applies the new formatter to **all registered handlers**.
    3. Preserves the current date format (or default) unless changed separately.
3.  **Set a custom date format**

    ```python
    manager = LoggerManager()
    manager.set_date_format("%Y-%m-%d %H:%M:%S")
    ```

    1. Rebuilds the formatter with the new date format.
    2. Keeps the existing message format string.
    3. Updates all handlers to use the new formatter.

## Adding Custom Handlers

You can add extra handlers (for example, file or HTTP handlers) while retaining the central formatting logic.

```python
import logging
from gllm_core.utils.logger_manager import LoggerManager


manager = LoggerManager()
file_handler = logging.FileHandler("app.log")

manager.add_handler(file_handler)
logger = manager.get_logger("gllm_core.my_component")

logger.info("This will go to both the console and app.log")
```

The handler integration process is:

1. `add_handler` sets the **current formatter** on the new handler.
2. The handler is attached to the root logger.
3. The handler is stored in the manager’s internal handler list.
4. Future `get_logger` calls ensure child loggers inherit this handler when needed.

This allows you to:

1. Configure one or more **console handlers** via log mode.
2. Attach additional targets (files, sockets, streams) using the same formatting and mode.
3. Keep all configuration coordinated through a single `LoggerManager` instance.

## JSON Error Payloads

When running in JSON mode, error-related fields are grouped under an `error` key by `AppJSONFormatter`.

1. The formatter keeps only a small set of top-level fields:
   1. `timestamp`
   2. `name`
   3. `level`
   4. `message`
2. The following extra fields, when present, are remapped:
   1. `exc_info` → `error.message`
   2. `stack_info` → `error.stacktrace`
   3. `error_code` → `error.code`
3. The resulting JSON object only includes an `error` block if at least one of those fields is non-empty.

Example usage:

```python
logger = LoggerManager().get_logger("payment_service")

try:
    process_payment()
except Exception:
    logger.error(
        "Payment failed",
        exc_info=True,
        extra={"error_code": "PAYMENT_DECLINED"},
    )
```

In JSON mode this yields a structure similar to:

```json
{
  "timestamp": "2025-10-08T11:23:46+0700",
  "name": "payment_service",
  "level": "ERROR",
  "message": "Payment failed",
  "error": {
    "message": "Traceback ...",
    "stacktrace": "...",
    "code": "PAYMENT_DECLINED"
  }
}
```

## Rich-Based Handlers

Two handlers leverage Rich for colored, readable logs.

1. **TextRichHandler**
   1. Subclasses `rich.logging.RichHandler`.
   2. Applies a color from `TEXT_COLOR_MAP` based on the log level.
   3. Wraps messages with `[color][LoggerName] ...[/]` and escapes internal close tags.
   4. Best when you want column-based, rich console output.
2. **SimpleRichHandler**
   1. Subclasses `logging.StreamHandler`.
   2. Uses a `rich.console.Console` bound to the handler’s stream.
   3. Prints formatted log lines with color, but without the full Rich logging layout.
   4. Useful for simple colored logs that still look like classic log lines.

Both handlers benefit from:

1. Centralized formatter configuration through `LoggerManager`.
2. A shared `TEXT_COLOR_MAP` so levels have consistent colors.
3. Escape logic for Rich close tags to avoid breaking markup when messages themselves contain `[/`.

## Best Practices

1. **Use LoggerManager everywhere**
   1. Prefer `LoggerManager().get_logger(__name__)` over `logging.getLogger(__name__)` directly.
   2. This keeps configuration centralized and consistent.
2. **Pick a log mode per environment**
   1. `LOG_FORMAT=text` for local development.
   2. `LOG_FORMAT=simple` for minimal, colored logs.
   3. `LOG_FORMAT=json` for production environments with log shipping.
3. **Avoid reconfiguring handlers manually**
   1. Let `LoggerManager` manage the root logger and its handlers.
   2. Use `add_handler`, `set_log_format`, and `set_date_format` instead of calling `logging.basicConfig` in multiple places.
4. **Attach structured error information**
   1. Use `extra={"error_code": "..."}` when logging errors.
   2. Enable `exc_info=True` to capture stack traces.
   3. This pays off especially in JSON mode for observability.
5. **Keep log levels appropriate**
   1. Use `DEBUG` for development and detailed troubleshooting.
   2. Use `INFO` for standard runtime information.
   3. Use `WARNING`, `ERROR`, `CRITICAL` for exceptional situations.
