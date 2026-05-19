---
description: Link to how to utilize Connector MCP easily
icon: book-bookmark
---

# Connector MCP Cookbook

{% hint style="warning" %}
We are currently in the process of updating this Cookbook. Please bear with us as we navigate this change.
{% endhint %}

{% hint style="success" %}
Cookbook link: [https://github.com/gdplabs/gl-aip-sdk-cookbook/tree/main/examples/bosa-mcp](https://github.com/gdplabs/gl-aip-sdk-cookbook/tree/main/examples/bosa-mcp)
{% endhint %}

The cookbook shows how to use the Connector MCP and call its tools directly. There are two ways of utilizing the MCP Cookbook, via the Interactive Setup, or the Direct Execution Setup. Having said that, we need to clone the repository and set it up first.

## First Steps

Ensure the following pre-requisites are installed first:

* **Python 3.12 or higher**
* [**uv**](https://github.com/astral-sh/uv) **package manager** - Fast Python package installer and resolver
* **Connector Account** - Access to Connector API services
* **GitHub Account** - For GitHub integration features (we utilize Connector's Github MCP for example)

{% stepper %}
{% step %}
**Clone the Repository**

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gl-aip/examples/bosa-mcp
```
{% endstep %}

{% step %}
**Install Dependencies**

```bash
uv sync
```
{% endstep %}
{% endstepper %}

## Interactive Setup

{% stepper %}
{% step %}
**Run the Interactive Application (One-CLI)**

```bash
uv run example_interactive.py
```
{% endstep %}

{% step %}
**Follow the program run**

1. The application will open up a browser which opens up [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention") so you can setup your account there.
2. Fill in the Client Key into the application
3. Fill in the User Token into the application
4. Then you may follow the Github setup as well (it will open up an OAuth2 page for you to authorize).
5. Finally, you will be asked to select one Issue from a Github (we are using "Get Issue Details" for the Cookbook)
{% endstep %}

{% step %}
**You're done!**

You can now check the `.env` file to see what variables are set and how to utilize it next time. Afterwards, you can then check the Direct Execution for more granular control!
{% endstep %}
{% endstepper %}

## Direct Execution

{% stepper %}
{% step %}
**Copy .env.example to .env**

```bash
cp .env.example .env
```
{% endstep %}

{% step %}
**Fill the appropriate variables**

For this particular method, you need to utilize all the variables needed in [credentials.md](../api/credentials.md "mention"); from Connector Client Key, to Connector Identifier and Connector User Secret.

```
# Required: Connector API Configuration
BOSA_API_URL=https://connectors.gdplabs.id

# For manual authentication
BOSA_CLIENT_KEY=your-client-key-here
BOSA_IDENTIFIER=your-user-identifier
BOSA_USER_SECRET=your-user-secret
```
{% endstep %}

{% step %}
**(Optional Step) Setup Github Integration**

The cookbook will setup a Github Integration for that particular Connector Account, so this step is optional if you have already set it up.
{% endstep %}

{% step %}
**Follow the program run**

Same with the interactive setup, you will be asked to select one Issue from a Github (we are using "Get Issue Details" for the Cookbook)
{% endstep %}

{% step %}
**You're done!**
{% endstep %}
{% endstepper %}
