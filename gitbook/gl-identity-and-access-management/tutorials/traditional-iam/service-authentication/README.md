---
icon: server
---

# Service Authentication

Tutorials for authenticating services with API keys.

{% hint style="info" %}
Learn the concepts first? See [Introduction to GL IAM](../../../introduction-to-gl-iam.md).
{% endhint %}

## User vs Service Authentication

<figure><img src="../../../../.gitbook/assets/GL IAM - User vs Service Authentication.png" alt=""><figcaption></figcaption></figure>

## When to Use

| Scenario                      | Use                        |
| ----------------------------- | -------------------------- |
| Human logging into web app    | User Authentication        |
| Human logging into mobile app | User Authentication        |
| Backend service calling API   | **Service Authentication** |
| CI/CD pipeline                | **Service Authentication** |
| Automation scripts            | **Service Authentication** |

## API Key Lifecycle

<figure><img src="../../../../.gitbook/assets/GL IAM - API Key Lifecycle.png" alt=""><figcaption></figcaption></figure>

## Tutorials

{% stepper %}
{% step %}
**Create API Key**

[Create API Key](create-api-key.md)

What You'll Learn: Generate new API key
{% endstep %}

{% step %}
**Validate API Key**

[Validate API Key](validate-api-key.md)

What You'll Learn: Verify incoming API key
{% endstep %}

{% step %}
**Rotate API Key**

[Rotate API Key](rotate-api-key.md)

What You'll Learn: Rotate an API key with an optional grace period (zero-downtime rotation)
{% endstep %}

{% step %}
**Revoke API Key**

[Revoke API Key](revoke-api-key.md)

What You'll Learn: Invalidate API key
{% endstep %}
{% endstepper %}

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fservice-authentication).
{% endhint %}
