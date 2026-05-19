# Authentication

## Authentication API

The External API uses OAuth2 Client Credentials flow for authentication. External systems receive a client\_id and client\_secret, exchange them for an access token, and use that token to access meeting data.

### Prerequisites

* An ExternalApplication must be created by a Meemo administrator
* The ExternalApplication links your OAuth2 credentials to one or more organizations
* You can access meetings belonging to all linked organizations
* Optionally, you can filter requests to a specific organization using the organization\_id parameter

### Obtain Credentials

Contact your Meemo administrator to create an ExternalApplication for your integration. You will receive:

* **client\_id** - Your application identifier
* **client\_secret** - Your secret key (keep this secure!)

### Get Access Token

Exchange your credentials for an access token using the OAuth2 token endpoint.

#### Request

```
POST /api/auth/token/
Content-Type: application/x-www-form-urlencoded
```

**Parameters**

| Parameter      | Value               |
| -------------- | ------------------- |
| grant\_type    | client\_credentials |
| client\_id     | Your client ID      |
| client\_secret | Your client secret  |

**Example (cURL)**

```bash
curl -X POST https://your-meemo-instance.com/api/auth/token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

#### Response

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 10800,
  "scope": "read write"
}
```

### Revoke Access Token

If you need to revoke an access token before it expires, use the revocation endpoint.

#### Request

```
POST /api/auth/revoke-token/
Content-Type: application/x-www-form-urlencoded
```

**Parameters**

| Parameter      | Value               |
| -------------- | ------------------- |
| client\_id     | Your client ID      |
| client\_secret | Your client secret  |
| token          | The token to revoke |

**Example (cURL)**

```bash
curl -X POST https://your-meemo-instance.com/api/auth/revoke-token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "token=YOUR_ACCESS_TOKEN"
```

### Token Expiration & Refresh

* Access tokens expire after 3 hours (10800 seconds) by default
* When your token expires, request a new one using the "Get Access Token" step above
* Store and reuse tokens until they expire to minimize token requests

#### Handling Expiration (Python Example)

```python
import requests
from datetime import datetime, timedelta

class MeemoClient:
    def __init__(self, client_id, client_secret, base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.access_token = None
        self.token_expires_at = None

    def get_token(self):
        if self.access_token and self.token_expires_at > datetime.now():
            return self.access_token

        response = requests.post(
            f"{self.base_url}/api/auth/token/",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )
        
        data = response.json()
        self.access_token = data["access_token"]
        self.token_expires_at = datetime.now() + timedelta(seconds=data["expires_in"] - 60)
        
        return self.access_token
```
