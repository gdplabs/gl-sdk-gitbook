---
icon: link
---

# Integration Setup

{% hint style="info" %}
For more detailed GL Connectors SDK Capabilities, please check [sdk-method-api.md](../sdk-method-api.md "mention")
{% endhint %}

## Authentication

{% hint style="warning" %}
Please see [credentials.md](../credentials.md "mention") for a more comprehensive details on how to manage user credentials.
{% endhint %}

Before executing the integration actions, you need to authenticate and obtain the user token first. Outside of [connectors-console.md](../tools-and-interfaces/connectors-console.md "mention"), we provide a multi-tenant environment that requires you to manage your Client API Key and User Credentials yourself.

### Register user

{% hint style="danger" %}
Make sure you save the `user_data.secret` after you create the Connectors user, as we will only show this once after you register the user
{% endhint %}

To create a new user, you need to input your identifier for your user.

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="https://connectors.gdplabs.id", api_key="YOUR_API_KEY")

user = connector.create_user("your-user-identifier")
user_secret = user_data.secret # store this securely! we only show this once!
```

### Logging in and Retrieving User Token

After creating the user, you can authenticate (login) with your Connector API key.

```python
from gl_connectors_sdk.connector import GLConnectors

# Initialize the connector
connector = GLConnectors(api_base_url="https://connector.gdplabs.id", api_key="YOUR_API_KEY")

user = connector.authenticate("identifier", "sk-user-xxx")
user_token = user.token  # eyJ... (the Bearer Token)
```

Once you have the token, use it to connect to the connectors. For most configurations, we will generate an URL that you can follow to authenticate. But some connectors require custom configuration.

## Setting up an Integration

{% hint style="warning" %}
For a complete list of supported Connectors and their list of tools, see [agentic-tools-and-model-context-protocol-mcp](../../agentic-tools-and-model-context-protocol-mcp/ "mention").
{% endhint %}

To set up a certain integration (e.g., github, google, gdrive, etc.), you need to request a connector authentication, which will create an OAuth2 login URL, which you can then follow to link an integration to your account.

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url=API_URL, api_key=API_KEY)
user = connector.authenticate(identifier, secret)
has_integration = connector.user_has_integration("github", user.token)

auth_url = connector.initiate_connector_auth("github", user.token, "https://your-callback-uri.com")
print(f"Please visit {auth_url} to complete authentication.")
```

### Setting up a Custom Integration

{% hint style="warning" %}
For a more comprehensive documentation on what requires Custom Configurations, check [custom-configurations](../plugin-concepts/custom-configurations/ "mention").
{% endhint %}

Unlike the previous section, this section highlights if you need to bring a custom configuration to modules that support it. For example, SQL Connection. The complete documentation can be found here in [sql.md](../plugin-concepts/custom-configurations/sql.md "mention").

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="http://localhost:8000", api_key="your_api_key")
user = connector.authenticate(identifier, secret)

config = {
    "url": "postgresql://postgres:postgres@localhost:5432/gl-connectors",
    "identifier": "PSQLGLConnectors"
}

integration_result = connector.initiate_plugin_configuration("sql", user.token, config)
print("Integration initiated:", integration_result)
```

### Multiple Integration

A GL Connector user may add multiple integrations to a connector. When running the connector, you can choose an integration; otherwise the first integration added (the default) is used. The default integration can be changed or deleted.

#### Execute with Specific Integration

There are two ways to specify which integration to use when executing connector:

1. Parameter `identifier: str` on `execute(...)`

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="http://localhost:8000", api_key="your_api_key")
user = connector.authenticate(identifier, secret)

params = {
    "limit": 10,
    "page": 1,
    "owner": "GDP-ADMIN",
    "repo": "gl-connectors",
    "token": user.token
}
execute_result = connector.execute(
    "github", 
    "list_pull_requests", 
    identifier="my-github-account",
    **params,
)
print("Execute result:", execute_result)
```

2. Method `identifier(identifier: str | None = None)` on GL Connectors Fluent.

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="https://connector.gdplabs.id", api_key=API_KEY)
user = connector.authenticate(identifier, secret)

# input parameters
params = {
    "limit": 10,
    "page": 1,
    "owner": "GDP-ADMIN",
    "repo": "gl-connectors",
}
# execution
response = connector.connect('github') \
    .action('list_pull_requests') \
    .params(params) \
    .max_attempts(3) \
    .token(user.token) \
    .identifier('my-github-account')
    .run()

# Print the result
print(response.get_data())
```

#### Change Default Integration

The default integration can be changed. See the example code below.

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="http://localhost:8000", api_key="your_api_key")
user = connector.authenticate(identifier, secret)

select_result = connector.select_integration("github", user.token, "my-github-account")
print("Integration selected:", select_result)
```

#### Delete Integration

An integration can be deleted. If the default integration is deleted, the most recently created integration becomes the new default. Example code for deleting an integration is shown below.

<pre class="language-python"><code class="lang-python">from gl_connectors_sdk.connector import GLConnectors

<strong>connector = GLConnectors(api_base_url="http://localhost:8000", api_key="your_api_key")
</strong>user = connector.authenticate(identifier, secret)

delete_result = connector.remove_integration("github", user.token, "my-github-account")
print("Integration deleted:", delete_result)
</code></pre>
