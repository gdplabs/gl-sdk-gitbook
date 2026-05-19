# Security Considerations

To maintain the integrity of your authentication system, it's important to follow key security best practices around credentials, token handling, and environment management.

**🔐 Master Credentials**

* The **Master username and password** are highly sensitive and used **only for client creation**.
* These should **never be hardcoded** or exposed in source code or logs.
* Store them securely using environment variables:
  * `MASTER_USERNAME`
  * `MASTER_PASSWORD`
* Restrict access to environments that hold Master credentials (e.g., CI/CD, server runtime).
* Master credentials are **not required** for user creation - use client API keys instead.

***

**🔑 Client API Keys**

* Each client receives a unique **API key** upon creation.
* Client API keys are used to create users associated with that client.
* Store client API keys securely and treat them as sensitive credentials.
* Never expose API keys in:
  * Public repositories
  * Client-side code
  * Application logs
  * Error messages
* Use the `x-api-key` header to pass API keys in requests.
* For backward compatibility, the system can fall back to `CLIENT_API_KEY` environment variable for token creation.
* Rotate API keys periodically and when compromised.

***

**🔑 Token Security**

* Tokens should be **treated like passwords**.
* Always transmit them over HTTPS to prevent interception.
* Tokens should have a reasonable **expiration time** (`expires_in`) to reduce long-term risk if compromised. For now, Token have default 30 days lifetime.
* Do not store tokens in client-side locations that are vulnerable (e.g., `localStorage` in browsers, if exposed to XSS).

***

**🧾 User Secrets**

* User **secrets** are generated automatically during user creation and returned **only once**.
* Store user secrets securely immediately after creation - they cannot be retrieved later.
* When distributing secrets to users or partners, ensure the channel is encrypted and trusted.
* User secrets combined with identifiers are used to generate authentication tokens.

***

**🏷️ Environment Separation**

* Clearly separate **staging** and **production** environments:
  * Use different master credentials
  * Use different client API keys
  * Maintain separate client/user records per environment
  * Use different JWT secret keys
* Never share secrets, API keys, or tokens across environments.
* Configure `CLIENT_API_KEY` environment variable differently per environment.

***

**🔒 Token Verification Security**

* The system implements **multi-layer token verification** for enhanced security:
  * **JWT signature validation** ensures token integrity
  * **Expiration checks** prevent use of expired tokens
  * **Database validation** verifies token existence and prevents deleted token usage
  * **Revocation checks** immediately invalidate compromised tokens
* This approach is more secure than JWT-only validation as it allows immediate token invalidation.
* Tokens are validated on every API request to protected endpoints.
* If a token is compromised, it can be revoked in the database and will be rejected immediately.

***

**📜 Logging**

* Avoid logging sensitive information like:
  * Master credentials
  * Client API keys
  * User secrets
  * Bearer tokens
  * JWT token contents
* Use structured logging and redact sensitive fields if necessary.
* Log authentication failures for security monitoring, but never log the credentials that failed.
