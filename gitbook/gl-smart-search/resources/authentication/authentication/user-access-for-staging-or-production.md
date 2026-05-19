# User Access for Staging/Production

In staging and production environments, you may need to provide predefined access to specific users. These users are typically system-level or integration users tied to known external clients or services.

**🧑‍💼 Predefined Users**

Examples of predefined users:

* `glchat_user`
* `catapa_user`
* `glair_user`

Each of these users is created in advance using the `/user` endpoint by the GL Smart Search Team. Once created, we will issue a unique **identifier** and **secret**.

***

**🔐 Credential Distribution**

For both **staging** and **production** environments:

* GL Smart Search Team will provide each integration partner or internal system with:
  * `identifier`: The user ID (e.g., `glchat_user`)
  * `secret`: The associated password-like secret

These credentials are delivered securely and used solely to obtain authentication tokens from the `/token` endpoint.

***

**✅ Token Retrieval Example**

Once a user has their credentials, they can call:

**Endpoint:**

```
POST /token
```

**Request Body:**

```json
{
  "identifier": "glchat_user",
  "secret": "provided_secret_here"
}
```

This process is identical across environments. The only variation is which identifier/secret pair is provided, depending on whether the environment is staging or production.
