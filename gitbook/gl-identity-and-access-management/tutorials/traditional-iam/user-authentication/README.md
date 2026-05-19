---
icon: user-check
---

# User Authentication

Tutorials for authenticating human users with GL IAM.

{% hint style="info" %}
Learn the concepts first? See [Introduction to GL IAM](../../../introduction-to-gl-iam.md).
{% endhint %}

## Session Lifecycle

<figure><img src="../../../../.gitbook/assets/GL IAM - User Authentication.png" alt=""><figcaption></figcaption></figure>

## Token Types

| Token         | Lifetime          | Purpose            | Store Where?   |
| ------------- | ----------------- | ------------------ | -------------- |
| Access Token  | Short (15-60 min) | API calls          | Memory         |
| Refresh Token | Long (7-30 days)  | Renew access token | Secure storage |

## Tutorials

{% stepper %}
{% step %}
**Login**

[Login](login.md) — `authenticate()` - create session
{% endstep %}

{% step %}
**User**

[User](user.md) — Understanding the User object
{% endstep %}

{% step %}
**Validate**

[Validate](validate.md) — `validate_session()` - verify token
{% endstep %}

{% step %}
**Refresh**

[Refresh](refresh.md) — `refresh_session()` - renew token
{% endstep %}

{% step %}
**Logout**

[Logout](logout.md) — `logout()` - end session
{% endstep %}
{% endstepper %}

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fuser-authentication).
{% endhint %}
