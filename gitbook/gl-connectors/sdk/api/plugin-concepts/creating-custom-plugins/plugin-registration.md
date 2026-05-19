---
description: Registering your shiny new plugin for GL Connector!
icon: id-card
---

# Plugin Registration

{% hint style="warning" %}
**Repository**: GL Connectors
{% endhint %}

While registering a plugin is as simple as plugging it into the appropriate Plugin Manager, as of the time of writing, we have _two_ Plugin Handlers; for our standard HTTP Manager, and the MCP Manager (do note that MCP Manager is also an MCP Handler). All of this will be handled in Connector API's `app.py` located [here](https://github.com/GDP-ADMIN/gl-connectors/blob/main/applications/gl-connectors-api/gl_connectors_api/app.py).

## Registering the Plugin for HTTP Manager

The variable name for the normal HTTP manager is `plugin_manager`. To register your plugin, you simply need to add it by registering it as such:

```python
plugin_manager.register_plugin(PluginClass)
```

That's it! You have successfully added the new plugin for GL Connector!

## Registering the Plugin for MCP Manager

Adding the plugin for MCP Manager is a little more tricky, because of the lifetime it requires to setup Streamable HTTP. As such, there are two places you need to register the plugin in:

In the MCP Generator [here](https://github.com/GDP-ADMIN/bosa-platform/blob/main/applications/bosa-api/bosa_api/app.py#L114-L115):

```python
mcp_generator = McpGenerator()
mcps = mcp_generator.generate_fastmcp(
    plugin_classes=[
        # ...other plugins,
        PluginClass
        # *acidev_plugins
    ]
)
```

And finally, in the actual plugin manager named `mcp_plugin_manager` [here](https://github.com/GDP-ADMIN/gl-connectors/blob/main/applications/gl-connectors-api/gl_connectors_api/app.py#L102-L103):

```python
mcp_plugin_manager.register_plugin(PluginClass)
```
