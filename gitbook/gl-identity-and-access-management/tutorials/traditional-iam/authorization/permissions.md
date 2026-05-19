---
icon: check-to-slot
---

# Permissions

Check if a user has specific permissions for fine-grained access control.

{% hint style="info" %}
**When to use**: When you need action-level access control like "can user delete this document?"
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Login](../user-authentication/login.md)
* Have a user object from authentication

</details>

## 5-Line Core

```python
if user.has_permission("documents:delete"):
    delete_document(doc_id)
else:
    raise HTTPException(403, "Permission denied")
```

## Step-by-Step

{% stepper %}
{% step %}
**Check Single Permission**

```python
if user.has_permission("documents:read"):
    print("User can read documents")
```
{% endstep %}

{% step %}
**Check All Permissions (AND)**

```python
if user.has_all_permissions(["documents:read", "documents:write"]):
    print("User has full document access")
```
{% endstep %}

{% step %}
**Check Any Permission (OR)**

```python
if user.has_any_permission(["admin:all", "documents:manage"]):
    print("User can manage documents")
```
{% endstep %}

{% step %}
**View User's Permissions**

```python
print(f"Permissions: {user.permissions}")
```
{% endstep %}

{% step %}
**Expected Output**

```
User can read documents
Permissions: ['documents:read', 'documents:write']
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can check permissions!
{% endhint %}

## Complete Example

Create `permissions.py`:

```python
"""GL IAM Permissions Example."""

import asyncio

from gl_iam import IAMGateway
from gl_iam.core.types import PasswordCredentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Setup
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    # Login to get user
    result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )
    user, token = result.unwrap()

    print(f"User: {user.email}")
    print(f"Permissions: {user.permissions}")

    # Single permission check
    print("\n--- Single Permission ---")
    print(f"Can read docs: {user.has_permission('documents:read')}")
    print(f"Can delete docs: {user.has_permission('documents:delete')}")

    # All permissions (AND)
    print("\n--- All Permissions (AND) ---")
    if user.has_all_permissions(["documents:read", "documents:write"]):
        print("✓ Has full document access")
    else:
        print("✗ Missing some document permissions")

    # Any permission (OR)
    print("\n--- Any Permission (OR) ---")
    if user.has_any_permission(["admin:all", "documents:read"]):
        print("✓ Has at least one required permission")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run permissions.py
```

Expected output:

```
User: alice@example.com
Permissions: ['documents:read', 'documents:write']

--- Single Permission ---
Can read docs: True
Can delete docs: False

--- All Permissions (AND) ---
✓ Has full document access

--- Any Permission (OR) ---
✓ Has at least one required permission
```

## Roles vs Permissions

| Use Case           | Check                         |
| ------------------ | ----------------------------- |
| Admin panel access | Role (`has_standard_role`)    |
| Specific action    | Permission (`has_permission`) |
| Feature flag       | Permission                    |
| Billing access     | Role or Permission            |

## Common Pitfalls

| Pitfall                          | Solution                                                  |
| -------------------------------- | --------------------------------------------------------- |
| Using permissions for everything | Use roles for coarse access, permissions for fine-grained |
| Not validating token first       | Always validate session before checking permissions       |
| Wrong status code                | Permission denied is 403, invalid token is 401            |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fauthorization%2Fpermissions).
{% endhint %}
