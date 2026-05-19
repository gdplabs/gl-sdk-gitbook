---
icon: truck-fast
---

# Quickstart

{% hint style="warning" %}
This page assumes you have fulfilled the [prerequisites.md](../../prerequisites.md "mention") in your environment. To summarize, you need:

* Python 3.11+
* [UV](https://docs.astral.sh/uv/) Package Manager
* GL Connectors [credentials.md](credentials.md "mention")
{% endhint %}

### Getting Started <a href="#pre-requisites" id="pre-requisites"></a>

{% stepper %}
{% step %}
**Installation**

```shellscript
uv add gl-connectors-sdk
```
{% endstep %}

{% step %}
**Setting Up the Integration**

{% hint style="warning" %}
Note that the Connectors Console currently requires you to have an allowlisted email domain. You need to log in using your @gdplabs.id email in order to access the Console, otherwise your access will be rejected.
{% endhint %}

The API Key and User Token are accessible through our console. To use the console, please see the following page: [connectors-console.md](tools-and-interfaces/connectors-console.md "mention"), or if you want to go directly to the console, it is [here in Connectors Console](https://connectors.glair.ai/console).

In the dashboard, to activate one of the integration, we will use our **Google Drive Integration** to search for files.

1. Under `Google_drive` module, click `Add New Integration` button
2. Follow the generated URL and complete the authentication
3. Later, you will have an active integration for `google_drive` under your email.

<figure><img src="../../../.gitbook/assets/image (1) (2).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Quickstart Example**

This example uses `search_files` action to get 10 files at maximum from `google_drive` integration that contains `"wfo"` within the file itself. For this example, we will utilize GL Connectors' [**Fluent Style** **execution**](https://en.wikipedia.org/wiki/Fluent_interface) **for readability**.

{% include "../../../.gitbook/includes/consolecreds.md" %}

To run the following script, you will need to replace the following strings in the script below with the appropriate values:

* `GL_CONNECTORS_API_KEY` (**required**) - Use your Client API Key, see above
* `GL_CONNECTORS_USER_TOKEN` (**required**) - Obtained User Token from the console, see above

<pre class="language-python" data-title="connectors_quickstart.py" data-overflow="wrap" data-line-numbers data-full-width="true"><code class="lang-python">from gl_connectors_sdk.connector import GLConnectors

<strong>connector = GLConnectors(api_base_url = "https://connectors.glair.ai", api_key="GL_CONNECTORS_API_KEY")
</strong>
response = (connector.connect('google_drive')
    .action('search_files')
    .params({"query": "name contains 'wfo'"})
    .token('GL_CONNECTORS_USER_TOKEN')
    .run())

print(response.get_data())
</code></pre>

{% hint style="danger" %}
Note that you can also authenticate and get the token using the SDK. For more details about authentication and advanced setup, please check [in-depth-setup](in-depth-setup/ "mention") and [credentials.md](credentials.md "mention") for more information.
{% endhint %}
{% endstep %}

{% step %}
**Running the File**

You can then simply run one of the following command depending on your package manager:

* `python connectors_quickstart.py`
* `uv run connectors_quickstart.py`
{% endstep %}

{% step %}
**Understanding the Code**

1. Line 1: Only one import is needed for `GLConnectors`
2. Line 3: Instantiates the Connectors with the API Key you've obtained from the Console.
3. Line 5 - 9: [Fluent-style](in-depth-setup/#execution) execution. We also offer direct style execution, see the link for complete information. It can be shorter, but for readability, we recommend fluent-style.
   1. Connects to the Connector (for a list of Connector, see [here](https://connectors.gdplabs.id/mcps/list?source=internal))
   2. Selects the action to execute (the list of Connector above also lists the possible actions)
   3. Sets the parameters in the form of a dictionary (key, value pair).
   4. Sets the User Token as obtained above. Note that you may retrieve the token from other means. See [credentials.md](credentials.md "mention") for more information.
   5. Executes the Connector and retrieves the response data and status code.
4. Line 11: Prints it to STDOUT.
{% endstep %}
{% endstepper %}
