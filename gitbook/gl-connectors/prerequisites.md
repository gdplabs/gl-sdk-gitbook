---
icon: circle-exclamation
---

# Prerequisites

Before you begin building with GL Connectors, ensure you have the following handy.

{% stepper %}
{% step %}
#### Python 3.11+

Make sure you have [Python](https://www.python.org/) version 3.11 or later installed. We recommend installing version 3.12 at the time of writing. Use this to verify you have the right version.

```bash
python --version

# Python 3.12.3
```
{% endstep %}

{% step %}
#### UV Package Manager

While PIP works as a global installer, it's harder to manage the versions, lock versions, etc. We recommend using [UV](https://docs.astral.sh/uv/) as the package manager. All the guides will utilize UV.

```bash
uv --version

# uv 0.7.6
```
{% endstep %}

{% step %}
#### GL Connectors Credentials

{% hint style="info" %}
For users with @gdplabs.id email, you can retrieve the credentials from [connectors-console.md](sdk/api/tools-and-interfaces/connectors-console.md "mention") for ease-of-access.
{% endhint %}

If you're using GL Connectors (be it the API, MCP Server, or other features provided by GL Connectors), you will need to obtain the [credentials.md](sdk/api/credentials.md "mention") first. Afterwards, you can use it as environment variables. In general, you will need the following:

* Client Key (will serve as the API Key for your tenant/organization)
* User Identifier (will serve as the login username)
* User Secret (will serve as the login password)
* User Token (used after authenticating with the aforementioned identifier and secret)
{% endstep %}

{% step %}
#### GCloud CLI and Gen AI Google Cloud Repository

Some of our components such as [connectors-skills](sdk/connectors-skills/ "mention") and [tools](sdk/tools/ "mention") require access to our internal artifact registry.

1. **GCloud CLI:** Please refer to the [installation guide](https://cloud.google.com/sdk/docs/install) for gcloud CLI. After installing, please run `gcloud auth login` to authorize gcloud to access the Cloud Platform with Google user credentials.
2. **GenAI Google Cloud Repository:** Request access to Gen AI Google Cloud repositories by submitting this [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) (alternatively, from your manager or team lead)
{% endstep %}
{% endstepper %}
