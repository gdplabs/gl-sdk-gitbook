---
icon: key
---

# Authentication

To use GL Smart Search, you need an authentication token. This token allows you to securely access GL Smart Search services.

---

## How to Get Your Token

### Step 1: Contact GL Smart Search Team

Reach out to the GL Smart Search Team to request access. They will provide you with:

- **User Identifier** – Your unique username
- **User Secret** – Your password for authentication

### Step 2: Generate Your Token

Once you have your identifier and secret, generate your authentication token by making a request to the token endpoint:

**Endpoint:**
```
POST https://search.glair.ai/token
```

**Request:**

```bash
curl -X POST "https://search.glair.ai/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "identifier=your_identifier" \
  -d "secret=your_secret"
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_at": "2019-08-24T14:15:22Z"
}
```

### Step 3: Use Your Token

Save the `token` value from the response. You'll use this token to authenticate all your requests to GL Smart Search.

Set it as an environment variable:

```bash
export SMARTSEARCH_TOKEN="your-token-here"
```

Or include it in the `Authorization` header of your requests:

```bash
Authorization: Bearer your-token-here
```

---

## Next Steps

Now that you have your token, you're ready to:

- Complete the [Prerequisites](../prerequisites.md) guide
- Start using GL Smart Search with the [Getting Started](../getting-started.md) guide

---

## Need Help?

If you need assistance getting your credentials or have questions about authentication, please contact the GL Smart Search Team.
