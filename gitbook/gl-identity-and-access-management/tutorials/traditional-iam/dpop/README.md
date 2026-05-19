---
description: Tutorials for Demonstrating Proof-of-Possession (DPoP)
icon: shield-keyhole
---

# DPoP

## What is DPoP?

[DPoP](https://datatracker.ietf.org/doc/html/rfc9449), or Demonstrating Proof of Possession, is an extension that describes a technique to cryptographically bind access tokens to a particular client when they are issued.

## Why DPoP? <a href="#why-dpop" id="why-dpop"></a>

Bearer Token:

<figure><img src="../../../../.gitbook/assets/image (1) (1) (2).png" alt=""><figcaption></figcaption></figure>

DPoP-bound Token:

<figure><img src="../../../../.gitbook/assets/image (2) (2).png" alt=""><figcaption></figcaption></figure>

## How DPoP Works? <a href="#how-dpop-works" id="how-dpop-works"></a>

<figure><img src="../../../../.gitbook/assets/image (3) (2).png" alt=""><figcaption></figcaption></figure>

## Key Concepts

| Concept           | Description                                                       |
| ----------------- | ----------------------------------------------------------------- |
| DPoP Proof        | A JWT signed with the client's private key that proves possession |
| JWK Thumbprint    | SHA-256 hash of the public key, used as key identifier            |
| Token Binding     | Links access token to a specific key pair via cnf.jkt claim       |
| Nonce             | Server-generated random value to prevent replay attacks           |
| Replay Protection | Each proof is bound to specific HTTP method + URL + timestamp     |
| ath Claim         | Access Token Hash - confirms proof matches the token being used   |

## Tutorials

{% stepper %}
{% step %}
**Protect Your API**

[Protect Your API](protect-your-api.md)

What You'll Learn: Protect bearer token with DPoP.
{% endstep %}

{% step %}
**Generate Proof**

[Generate Proof](generate-proof.md)

What You'll Learn: Generate proof for auth server.
{% endstep %}
{% endstepper %}

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fdpop).
{% endhint %}
