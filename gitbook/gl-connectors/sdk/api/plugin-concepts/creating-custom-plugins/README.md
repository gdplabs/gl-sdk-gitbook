---
icon: layer-plus
---

# Plugin Concepts

To create our own Custom endpoint in Connector, you need to create a plugin, using GL SDK's Plugin Architecture.

## Pre-requisites

1. Access to GL Connectors SDK repository ([https://github.com/GDP-ADMIN/gl-connectors-sdk](https://github.com/GDP-ADMIN/gl-connectors-sdk)) for Connectors Server Plugins and Connectors Core (for installation)
2. Access to GL Connectors repository ([https://github.com/GDP-ADMIN/gl-connectors](https://github.com/GDP-ADMIN/gl-connectors)) to register the newly created Plugin
3. Python 3.11+
4. Poetry (package manager)

## Simple HTTP Plugin

{% hint style="warning" %}
**Why do we only support POST endpoints (i.e., RPC Styled Endpoints)**?

We do support other endpoints like GET, PUT, DELETE. `ThirdPartyIntegrationPlugin` below shows that we do support other HTTP Methods. Having said that, **the Server Plugins work under the concept of "actions"**; therefore, it doesn't make sense for other HTTP Methods to exist under this particular concept except on a very specific exceptions. See [#concept-3.1-actions](http-plugin-concepts.md#concept-3.1-actions "mention") for more details.

_**Example**_: Instead of `/github/issues/{id}` or `/github/issues/{id}/comments`, we do: `/github/get_issue` and `/github/get_issue_comments`, which make it easier for the Plugin Manager and HTTP Handler to automate and unify, and for clients and our SDK to handle as well.
{% endhint %}

To create a simple endpoint, you only need to create a simple class that extends the Plugin class from GL Plugin. The following code will generate the following:

* REST Endpoint: `POST /connectors/hello/say_hello`
* MCP Server `{BASE_URL}/hello/mcp` with a tool named `say_hello`

```python
from gl_plugin import Plugin
from gl_connectors_plugins.handler.router import Router

@Plugin.for_handler(HttpPlugin)
class HelloPlugin(Plugin):

    name = "hello"
    version = "0.0.1"
    description = "Hello Plugin"

    router: Router

    def __init__(self):
        @self.router.post("/say_hello")
        async def hello():
            return {
                "message": "Hello, world!"
            }
```

## Third Party Integration Plugin

Simple HTTP Plugin only shows how to create a simple "hello world" endpoints for the Server Plugins. Most third party integrations have custom behavior and authentication that isn't included in the base HTTP Handler. Having said that, this class is a superset of HTTP Plugin with custom handling. Because it is more complex, check [third-party-integration-plugin.md](plugin-handler/third-party-integration-plugin.md "mention") page for in-depth overview of the Third Party Integration.

To give a general overview, aside from doing the same thing a HTTP Plugin does, this class also creates a few new methods that need to be implemented when implementing a Third Party Integration Plugin.

* `initialize_authorization`: To initialize an OAuth2-based Plugin. The return type **must** be an OAuth2 Login URL that the user can follow to authorize.
* `initialize_custom_configuration`: To initialize a custom configuration that will be used entirely to activate the plugin. See [custom-configurations](../custom-configurations/ "mention") to see.
* `success_authorize_callback`: This method is used to accept callbacks from the OAuth2 provider (e.g., Google, Github, etc.) to handle and finish the authentication flow.
* `remove_integration`: To remove the integration of that user; i.e., if that user wishes to revoke their third party token.
* `user_has_integration`: Checks whether or not the user has at least one active integration for a particular module.
* `select_integration`: This method needs to be implemented to support multiple integrations; the user can select an integration to make it the currently active one.
* `get_integration`: Retrieves the currently selected integration (from above method); _must_ select at least one if the user has not selected a specific one.

## MCP Handler

When we create a new Plugin, we try to make it as friendly as possible for our converter to turn the REST endpoints to MCP. Having said that, you don't need to do anything special to handle it; refer to [#concept-6-mcp](http-plugin-concepts.md#concept-6-mcp "mention") for the general concept of how we handle MCP and [#mcp-handler](./#mcp-handler "mention") for more in-depth information.

## Registering Plugin

See [plugin-registration.md](plugin-registration.md "mention") to register your new plugin in GL Connectors. Note that you need to have access to the [GL Connectors](https://github.com/gdp-admin/gl-connectors) repository as outlined in the pre-requisites above. In general, registering a plugin to a compatible handler works as outlined in [plugin-handlers.md](../../../../../common-modules/tutorials/plugin/plugin-handlers.md "mention") Architecture's Page, but with additional steps that is outlined in [Plugin Registration](plugin-registration.md) page.
