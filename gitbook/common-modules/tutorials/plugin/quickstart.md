---
icon: bolt-lightning
---

# Quickstart

## Prerequisites

1. Python 3.11+
2. Python package manager
   1. We recommend [UV](https://docs.astral.sh/uv/)

## Getting Started

{% stepper %}
{% step %}
#### Installation

```shellscript
uv add gl-plugin
```
{% endstep %}

{% step %}
#### A working example

A fully working example you can just immediately execute is as follows:

<pre class="language-python" data-title="main.py" data-overflow="wrap" data-line-numbers><code class="lang-python">from gl_plugin.plugin.plugin import Plugin
from gl_plugin.plugin.handler import PluginHandler
from gl_plugin.plugin.manager import PluginManager
from typing import Any, Dict

<strong># The handler
</strong>class HelloPluginHandler(PluginHandler):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def create_injections(cls, instance: Any) -> Dict[str, Any]:
        return dict()

    @classmethod
    def initialize_plugin(cls, instance: Any, plugin: Any) -> None:
        pass

# The plugin
@Plugin.for_handler(HelloPluginHandler)
class HelloPlugin(Plugin):
    name = "HelloPlugin"
    version = "0.1.0"
    description = "A simple greeting plugin"

    def greet(self, name: str) -> str:
        return f"Hello, {name}!"

# Execution
handler = HelloPluginHandler()
manager = PluginManager(handlers=[handler])
manager.register_plugin(HelloPlugin)

hello_plugin = manager.get_plugin("HelloPlugin")

print(hello_plugin.greet("samuel"))
</code></pre>
{% endstep %}

{% step %}
#### Executing the Code

You can execute the code by simply running:

```shellscript
uv run main.py
```

You should get the following as the output:

```
$ uv run main.py
Hello, samuel!
```
{% endstep %}

{% step %}
#### Explaining the Components

**Plugin Handler**

{% code title="plugin_handler.py" lineNumbers="true" %}
```python
from gl_plugin.plugin.handler import PluginHandler
from typing import Any, Dict

class HelloPluginHandler(PluginHandler):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def create_injections(cls, instance: Any) -> Dict[str, Any]:
        return dict()  # No injections for this example

    @classmethod
    def initialize_plugin(cls, instance: Any, plugin: Any) -> None:
        pass  # No custom initialization needed
```
{% endcode %}

Every handler requires two class methods:

* `create_injections()` — Returns services to inject into plugins (empty dict if none)
* `initialize_plugin()` — Runs when a plugin is registered (leave empty if no setup needed)

We will go in-depth of what kind of injections are possible, and how to instantiate them in your plugin once you create it!

**Creating the Plugin**

{% code title="plugin.py" lineNumbers="true" %}
```python
from gl_plugin.plugin.plugin import Plugin

@Plugin.for_handler(HelloPluginHandler)
class HelloPlugin(Plugin):
    name = "HelloPlugin"
    version = "0.1.0"
    description = "A simple greeting plugin"

    def greet(self, name: str) -> str:
        return f"Hello, {name}!"
```
{% endcode %}

Use the `@Plugin.for_handler()` decorator to bind your plugin to its handler. Define the required metadata (`name`, `version`, `description`), then add your own methods.

**Wiring up into the Manager**

{% code title="" lineNumbers="true" %}
```python
from gl_plugin.plugin.manager import PluginManager

manager = PluginManager(handlers=[HelloPluginHandler()])
manager.register_plugin(HelloPlugin)

hello_plugin = manager.get_plugin("HelloPlugin")
print(hello_plugin.greet("samuel"))  # Output: Hello, samuel!
```
{% endcode %}

Create your handler instance, pass it to the manager, register your plugin, and retrieve it by name.
{% endstep %}
{% endstepper %}

Congratulations! You've just built your first plugin-based service. To dive deeper into the concepts behind GL Plugin and learn best practices, explore the sections below.

* Understanding [plugin-handlers.md](plugin-handlers.md "mention")
* Understanding how [service-injection.md](service-injection.md "mention") works in GL Plugin
