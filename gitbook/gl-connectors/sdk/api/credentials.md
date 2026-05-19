---
description: How to obtain credentials used in the Connectors Ecosystem.
icon: key
---

# Credentials

{% hint style="warning" %}
GL Connectors is a multi-tenant system that deals with multiple clients, where each client has their own sets of users. To understand more about the concepts of Clients, Users, and Integrations, please refer to [HTTP Plugin Concepts](plugin-concepts/creating-custom-plugins/http-plugin-concepts.md) to understand the relationship between them.
{% endhint %}

This guide utilizes [cli.md](tools-and-interfaces/cli.md "mention") for guide on how to use the credentials and interact with the GL Connector Ecosystem. Please refer to the page for more details on comprehensive activities using the GL Connectors CLI. This page utilizes only the most basic of interactions necessary to deal with GL Connectors systems.

### Console

There is an easy way to retrieve both Client Key and User Token. For starting out and for those who just want to experience or experiment with GL Connectors, we recommend checking the Console to retrieve the necessary values.

The documentation for utilizing the Console can be accessed here in [connectors-console.md](tools-and-interfaces/connectors-console.md "mention")

### Client API Key

A Client API Key is used to identify which client is trying to connect to GL Connectors. Typically, this is in the form of `sk-client-{random_string}`.

#### How to obtain

1. Contact your team lead (typically those that dealt with GL Connectors first).
2. Contact GL Connectors Team (bosa-eng@gdplabs.id) and request for the generation of a key. Provide what team you want it for, what's the purpose for the key.

### User

{% hint style="danger" %}
When you create a new user, **the secret is only shown once**. If you lose it, **you must contact GL Connectors Team** as we do not currently provide a way to reset the secret. We cannot restore or retrieve it for you, so we will have to reset it for you.
{% endhint %}

#### Creating a new User

After you get your API key, you need to create a new user. All you need to do is provide the username you want to create for in the CLI, using `glcon users create {username}` as follows. **Remember that the secret is only shown once**, so do **not** lose it!

```
$ glcon users create samuel
ℹ Creating user 'samuel'...
✓ User created successfully!


User Details
============
ℹ Username: samuel

⚠ The full user secret is only shown once and cannot be recovered.
ℹ Full secret: sk-user-secret
```

### Login

In essence, this is equivalent to logging in, except the "password" is system-generated. To do so, all you need to do is do the command `glcon auth login` and you will be prompted with the Client Key, Username, and Secret.

```bash
$ glcon auth login
Client API Key: sk-client-... (use the key provided above)
Username (User Identifier): username (your user as created above)
User Secret: sk-user-... (user secret as provided in "Creating a new User" above)
ℹ Authenticating...
✓ Authentication successful!
ℹ Logged in as: username
ℹ Token expires: 2025-10-29 06:52:29.663016
ℹ Session saved to: /home/user/.connector/config.json
✓ Authentication successful!
```

### User Token

After logging in following [#login](credentials.md#login "mention"), you can now retrieve the token used for authentication. To retrieve this information, you simply need to go to the file provided `glcon auth status` as provided below

```bash
$ glcon auth status

Authentication Status
=====================
ℹ Username: samuel
ℹ API URL: https://connectors.gdplabs.id
ℹ Client API Key: sk-client-...8VDA
ℹ Token: eyJh...7zis
ℹ Token Type: Bearer
ℹ Token Expires: 2025-10-29T07:43:20.209910
ℹ User ID: f03ff60d-cf81-41b1-b23d-542c6d6bc29d
ℹ Config File: /home/user/.connector/config.json
```

All the necessary information can be retrieved by accessing the file `/home/user/.connector/config.json` , or shortened to `~/.connector/config.json`. Here is the easiest way you can retrieve both API Key and Tokens (**only in Linux or Nix based systems**):

```bash
$ jq -r '.token' ~/.connector/config.json 
eyJhbGciOiJIUzI1NiIsInR5c....

$ jq -r '.client_api_key' ~/.connector/config.json 
sk-client-ZWM4Y...
```

### Third Party Integration

Please refer to [#integration-management](tools-and-interfaces/cli.md#integration-management "mention") to understand how we can initiate a new integration using the GL Connectors CLI, or [#setting-up-an-integration](quickstart.md#setting-up-an-integration "mention") using GL Connectors SDK. You can also use the aforementioned [connectors-console.md](tools-and-interfaces/connectors-console.md "mention") for an easy way adding new integrations.
