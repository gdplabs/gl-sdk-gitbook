---
icon: puzzle-piece-simple
---

# Plugin Handler

{% hint style="warning" %}
**Repository:** GL Connectors Plugin ([https://github.com/GDP-ADMIN/connectors-sdk/tree/main/python/gl-connectors-plugins/gl\_connectors\_plugins](https://github.com/GDP-ADMIN/connectors-sdk/tree/main/python/gl-connectors-plugins/gl_connectors_plugins))
{% endhint %}

## HTTP Plugin Handler

HTTP Plugin, powered by the [plugin](../../../../../../common-modules/tutorials/plugin/ "mention") Architecture, is a framework-agnostic plugin handler that accepts HTTP handler such as FastAPI, Flask, etc. provided an appropriate handler is created. However, the concrete handler is beyond the scope of this document; in this document, we will focus on how we can utilize the HTTP Plugin Handler to create new endpoints that will be converted to both REST API endpoint and MCP Tool.

Having said that, this is the most basic form of HTTP Handler and can be found on [this file](https://github.com/GDP-ADMIN/connectors-sdk/blob/main/python/gl-connectors-plugins/gl_connectors_plugins/handler/interface.py#L26). This is where the injection for Router happens, and where you can add _general_ services in. While we can create normal Plugin directly to be assigned to HTTP Handler:

```python
@Plugin.for_handler(HTTPHandler)
class SomePlugin(Plugin):
```

It is generally not advised because it restricts the ability of the plugin to have their own integration and authentication that GL Connector Plugins provide. Refer to [third-party-integration-plugin.md](third-party-integration-plugin.md "mention") to implement an appropriate Third Party Integration Plugin instead!

## Do's

* **Always** have a plugin name
* **Always** document your methods appropriately (i.e., following the Google Standards). The OpenAPI document _relies_ on this for good descriptions.
* **Always** use `BaseRequestModel` to define Inputs
* **Try to** create a Pydantic Model as the response body for better documentation.
* **Use enums** for possible values when possible. Avoid using `str` if the value is predetermined.

## Don't's

* Use spaces in plugin name. Use only URL-Safe characters (`a-zA-Z0-9_-`)
* Use dictionaries in inputs if possible. Use a well-defined `BaseRequestModel` so the generated OpenAPI document is appropriately documented.
* Follow REST standard for path/tool naming; we use Actions here.
