---
icon: hands
---

# Plugin Handlers

## Handlers

### What is a Handler?

A **Handler** is the bridge between the Plugin Manager and your Plugins. It defines _how_ a category of plugins should behave—what services they receive and what happens when they're initialized.

Think of it this way:

* The **Manager** orchestrates everything
* The **Handler** defines the rules for a plugin category
* The **Plugins** follow those rules and implement functionality

Every plugin must be attached to a handler. The handler is responsible for:

1. **Injecting services** — Providing dependencies your plugins need
2. **Initialization logic** — Running setup code when a plugin is registered

***

### Anatomy of a Handler

To create a handler, extend `PluginHandler` and implement two required class methods:

```python
from gl_plugin.plugin.handler import PluginHandler
from typing import Any, Dict

class MyHandler(PluginHandler):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def create_injections(cls, instance: Any) -> Dict[str, Any]:
        # Define what services to inject into plugins
        return {}

    @classmethod
    def initialize_plugin(cls, instance: Any, plugin: Any) -> None:
        # Run setup logic after a plugin is instantiated
        pass
```

#### `create_injections(cls, instance)`

This method returns a dictionary of services that will be injected into every plugin attached to this handler. The injection happens automatically—plugins receive these services as instance attributes.

**Parameters:**

* `instance` — The handler instance (useful for accessing handler properties)

**Returns:**

* A dictionary mapping types to service instances or factories

#### `initialize_plugin(cls, instance, plugin)`

This method runs after a plugin is instantiated and its services are injected. Use it for any setup logic that requires the fully-constructed plugin.

**Parameters:**

* `instance` — The handler instance
* `plugin` — The newly created plugin instance

***

### Handler Properties

Handlers can define their own properties to configure behavior. These properties are accessible in both `create_injections()` and `initialize_plugin()` via the `instance` parameter.

```python
class MyHandler(PluginHandler):
    def __init__(self, some_config: str = "default") -> None:
        super().__init__()
        self.some_config = some_config

    @classmethod
    def create_injections(cls, instance: "MyHandler") -> Dict[str, Any]:
        # Access handler properties via instance
        print(instance.some_config)
        return {}
```

***

### Example: Building a Calculator Handler

Let's build a handler that provides a `CalculatorService` to its plugins.

{% stepper %}
{% step %}
#### Define the Service

First, create the service that will be injected:

```python
class CalculatorService:
    """A simple calculator service."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b
```
{% endstep %}

{% step %}
#### Create the Handler

Now create a handler that injects this service:

```python
from gl_plugin.plugin.handler import PluginHandler
from typing import Any, Dict, Type

class CalculatorHandler(PluginHandler):
    """Handler for calculator-based plugins."""

    def __init__(self, precision: int = 2) -> None:
        super().__init__()
        self.precision = precision

    @classmethod
    def create_injections(cls, instance: "CalculatorHandler") -> Dict[Type, Any]:
        return {
            CalculatorService: CalculatorService()
        }

    @classmethod
    def initialize_plugin(cls, instance: "CalculatorHandler", plugin: Any) -> None:
        # Store precision config in the plugin if needed
        plugin._precision = instance.precision
```

**What's happening here:**

* `create_injections()` returns a dictionary with `CalculatorService` as the key and an instance as the value
* Since `CalculatorService` is stateless, all plugins can safely share the same instance
* `initialize_plugin()` passes the handler's `precision` config to each plugin
{% endstep %}

{% step %}
#### Create an Abstract Plugin for the Handler

First, create an abstract base plugin that defines the contract. This is to ensure that **all** plugins implementing the CalculatorHandler has `calculate` (you don't have to, but this is highly recommended to ensure functional integrity):

```python
from gl_plugin.plugin.plugin import Plugin
from abc import abstractmethod

@Plugin.for_handler(CalculatorHandler)
class MathPlugin(Plugin):
    """Abstract base plugin for math operations."""

    name = "MathPlugin"
    version = "1.0.0"
    description = "Base plugin for math operations"

    calculator: CalculatorService  # Injected automatically!

    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """Perform a calculation. Must be implemented by subclasses."""
        pass
```
{% endstep %}

{% step %}
#### Create the Concrete Implementations

Now let's create the concrete implementations. For the purposes of this example, we shall only create the ones defined within the CalculatorService; you are definitely allowed and welcome to create your own implementation and flows:

```python
class AddPlugin(MathPlugin):
    """Plugin that performs addition."""

    name = "AddPlugin"
    version = "1.0.0"
    description = "Adds two numbers"

    def calculate(self, a: float, b: float) -> float:
        return self.calculator.add(a, b)


class SubtractPlugin(MathPlugin):
    """Plugin that performs subtraction."""

    name = "SubtractPlugin"
    version = "1.0.0"
    description = "Subtracts two numbers"

    def calculate(self, a: float, b: float) -> float:
        return self.calculator.subtract(a, b)


class MultiplyPlugin(MathPlugin):
    """Plugin that performs multiplication."""

    name = "MultiplyPlugin"
    version = "1.0.0"
    description = "Multiplies two numbers"

    def calculate(self, a: float, b: float) -> float:
        return self.calculator.multiply(a, b)
```

Notice that:

* `MathPlugin` defines the abstract `calculate()` method and receives the injected `CalculatorService`
* Concrete plugins inherit both the service injection and the contract
* Each implementation uses the same `calculator` service differently
{% endstep %}

{% step %}
#### Wire It Up

```python
from gl_plugin.plugin.manager import PluginManager

handler = CalculatorHandler(precision=3)
manager = PluginManager(handlers=[handler])

# Register all plugins
manager.register_plugin(AddPlugin)
manager.register_plugin(SubtractPlugin)
manager.register_plugin(MultiplyPlugin)

# Use them individually
add = manager.get_plugin("AddPlugin")
subtract = manager.get_plugin("SubtractPlugin")
multiply = manager.get_plugin("MultiplyPlugin")

print(add.calculate(10, 5))       # Output: 15.0
print(subtract.calculate(10, 5))  # Output: 5.0
print(multiply.calculate(10, 5))  # Output: 50.0

# Or iterate over all plugins for a handler type
plugins = manager.get_plugins(CalculatorHandler)
for plugin in plugins:
    print(f"{plugin.name}: {plugin.calculate(10, 5)}")
```

This pattern allows you to:

* Define a consistent interface via the base plugin
* Extend with new operations without modifying existing code
* Swap implementations at runtime
* Retrieve all plugins for a handler type with `get_plugins()`
{% endstep %}

{% step %}
#### The Completed Code

You can now simply paste this code and then run `uv run main.py` to execute it!

{% code title="main.py" lineNumbers="true" %}
```python
from gl_plugin.plugin.handler import PluginHandler
from gl_plugin.plugin.plugin import Plugin
from gl_plugin.plugin.manager import PluginManager

from abc import abstractmethod
from typing import Any, Dict, Type

class CalculatorService:
    """A simple calculator service."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

class CalculatorHandler(PluginHandler):
    """Handler for calculator-based plugins."""

    def __init__(self, precision: int = 2) -> None:
        super().__init__()
        self.precision = precision

    @classmethod
    def create_injections(cls, instance: "CalculatorHandler") -> Dict[Type, Any]:
        return {
            CalculatorService: CalculatorService()
        }

    @classmethod
    def initialize_plugin(cls, instance: "CalculatorHandler", plugin: Any) -> None:
        # Store precision config in the plugin if needed
        plugin._precision = instance.precision

@Plugin.for_handler(CalculatorHandler)
class MathPlugin(Plugin):
    """Abstract base plugin for math operations."""

    name = "MathPlugin"
    version = "1.0.0"
    description = "Base plugin for math operations"

    calculator: CalculatorService  # Injected automatically!

    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """Perform a calculation. Must be implemented by subclasses."""
        pass


class AddPlugin(MathPlugin):
    """Plugin that performs addition."""

    name = "AddPlugin"
    version = "1.0.0"
    description = "Adds two numbers"

    def calculate(self, a: float, b: float) -> float:
        return self.calculator.add(a, b)


class SubtractPlugin(MathPlugin):
    """Plugin that performs subtraction."""

    name = "SubtractPlugin"
    version = "1.0.0"
    description = "Subtracts two numbers"

    def calculate(self, a: float, b: float) -> float:
        return self.calculator.subtract(a, b)


class MultiplyPlugin(MathPlugin):
    """Plugin that performs multiplication."""

    name = "MultiplyPlugin"
    version = "1.0.0"
    description = "Multiplies two numbers"

    def calculate(self, a: float, b: float) -> float:
        return self.calculator.multiply(a, b)

handler = CalculatorHandler(precision=3)
manager = PluginManager(handlers=[handler])

# Register all plugins
manager.register_plugin(AddPlugin)
manager.register_plugin(SubtractPlugin)
manager.register_plugin(MultiplyPlugin)

# Use them individually
add = manager.get_plugin("AddPlugin")
subtract = manager.get_plugin("SubtractPlugin")
multiply = manager.get_plugin("MultiplyPlugin")

print(add.calculate(10, 5))       # Output: 15.0
print(subtract.calculate(10, 5))  # Output: 5.0
print(multiply.calculate(10, 5))  # Output: 50.0

# Or iterate over all plugins for a handler type
plugins = manager.get_plugins(CalculatorHandler)
for plugin in plugins:
    print(f"{plugin.name}: {plugin.calculate(10, 5)}")
```
{% endcode %}

The expected output should be:

```shellscript
$ uv run main.py
15
5
50
AddPlugin: 15
SubtractPlugin: 5
MultiplyPlugin: 50
```
{% endstep %}
{% endstepper %}

### Instance vs Factory Injection

In `create_injections()`, you can return either a direct instance or a factory function. The choice depends on whether plugins need **isolated** or **shared** services.

#### Shared Instance (Direct)

```python
@classmethod
def create_injections(cls, instance):
    return {
        CalculatorService: CalculatorService()
    }
```

The service is instantiated **once** when `create_injections()` is called. All plugins receive the **same instance**.

**Use when:**

* The service is stateless (like our `CalculatorService`)
* You _want_ shared state across plugins (e.g., a shared cache)
* The service doesn't hold plugin-specific data

#### Per-Plugin Instance (Factory)

```python
@classmethod
def create_injections(cls, instance):
    return {
        Router: lambda: Router()
    }
```

The factory function is called **each time** a plugin is instantiated. Every plugin receives its **own instance**.

**Use when:**

* The service holds plugin-specific state
* Plugins would conflict if sharing (e.g., routers with overlapping routes)
* Each plugin needs isolation

#### Example: Why Routers Need Factories

Consider an HTTP handler where plugins define their own routes:

```python
@classmethod
def create_injections(cls, instance):
    return {
        Router: lambda: Router()  # Factory - new router per plugin
    }
```

If we used `Router: Router()` instead, both plugins share the same Router instance:

* `GithubPlugin` registers `POST /webhook` → handler: `github_webhook_handler`
* `GooglePlugin` registers `POST /webhook` → handler: `google_webhook_handler`
* The second registration **overwrites** the first in the shared Router

Even if the HttpHandler correctly prefixes the paths (`/github/webhook` and `/google/webhook`), both routes now point to `google_webhook_handler` because the handler function was overwritten in the shared Router.

With `lambda: Router()`, each plugin gets its own Router instance:

* `GithubPlugin` → its own Router → `POST /webhook` → `github_webhook_handler`
* `GooglePlugin` → its own Router → `POST /webhook` → `google_webhook_handler`
* Each route correctly maps to its own handler function

***

#### Quick Reference

{% hint style="warning" %}
When in doubt, use a factory (`lambda`). Shared instances can cause subtle bugs that are difficult to trace when plugins unexpectedly affect each other's state.
{% endhint %}

| Syntax                       | Instantiation | Plugins Share? | Use Case                           |
| ---------------------------- | ------------- | -------------- | ---------------------------------- |
| `Service: Service()`         | Once          | Yes            | Stateless utilities, shared caches |
| `Service: lambda: Service()` | Per plugin    | No             | Routers, plugin-specific state     |

***

### Summary

| Method                | Purpose                      | When It Runs                  |
| --------------------- | ---------------------------- | ----------------------------- |
| `__init__`            | Configure handler properties | When handler is created       |
| `create_injections()` | Define services to inject    | During plugin instantiation   |
| `initialize_plugin()` | Post-injection setup         | After plugin is fully created |
