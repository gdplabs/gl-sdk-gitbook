---
icon: sliders
---

# Custom Configurations

{% hint style="warning" %}
**New in version 0.1.12**
{% endhint %}

There are certain connectors that may require custom authentication or configuration, such as the SQL Plugin (which allows the client to connect to their own Database Configuration). Please check the custom configuration pages for certain connectors for more information.

## Custom Configuration Example

```python
glcon = GLConnectors(api_base_url="https://connectors.gdplabs.id", api_key="your_api_key")

user_token = "a_unique_user_token"

config = {
    "url": "postgresql://postgres:postgres@localhost:5432/bosa",
    "identifier": "PSQLBosa"
}

integration_result = glcon.initiate_plugin_configuration("sql", user_token, config)
print("Integration initiated:", integration_result)
```
