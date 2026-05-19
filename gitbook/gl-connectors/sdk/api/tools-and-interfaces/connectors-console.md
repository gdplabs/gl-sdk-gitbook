---
description: An easy way to retrieve Connector User Information
icon: rectangle-code
---

# Connectors Console

{% hint style="danger" %}
**Important**: This method only works when you have a `@gdplabs.id` email to be logged in using Google.

With this method, you also **do not** have access to your secret credentials, so you **cannot use the SDK or API to login**. You _can_ use the premade token from the Console; you just cannot generate new tokens programmatically.
{% endhint %}

Based on the way to obtain [credentials.md](../credentials.md "mention"), there is an easier way to retrieve both the Client Key and Authorization Token for those who have email under `@gdplabs.id` domain, and that is via Console.

## Acquiring Credentials

{% stepper %}
{% step %}
**Go to Console**

Access the Console Page at [https://connectors.glair.ai/console](https://connectors.glair.ai/console)
{% endstep %}

{% step %}
**Click "Login with Google"**

<figure><img src="../../../../.gitbook/assets/image (27).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Login using your @gdplabs.id email**

{% hint style="danger" %}
Other email domains will not be accepted and you will be rejected back to the login page!
{% endhint %}
{% endstep %}

{% step %}
**Expand "Credentials"**

{% include "../../../../.gitbook/includes/consolecreds.md" %}
{% endstep %}
{% endstepper %}

Great! Now you have both the API Key (`sk-client-xxx`) and the Authorization Token (`eyJ...`) ready for use for GL Connector API, GL Connector SDK, and GL Connector MCP!

## Caveats

1. We do not have access to your user secret; therefore, you cannot login using the account registered via this method. Using this method, at any given moment, **you only have API Key and User Token**.
