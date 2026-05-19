---
icon: user
---

# User

Understanding the User object returned from authentication.

{% hint style="info" %}
**When to use**: After login or validate, to access user properties and check permissions.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Login](/broken/pages/70e495103ab305fdfcba6cdc17d9a7499195c67a)
* Have a `user` object from `authenticate()` or `validate_session()`

</details>

## 5-Line Core

```python
# User has identity info
print(user.id, user.email, user.display_name)
# User has authorization info
print(user.roles, user.permissions)
# User has helper methods
user.has_permission("documents:read")
```

## User Properties

| Property          | Type          | Description            |
| ----------------- | ------------- | ---------------------- |
| `id`              | `str`         | Unique user identifier |
| `email`           | `str`         | User's email address   |
| `display_name`    | `str \| None` | Display name           |
| `username`        | `str \| None` | Username               |
| `roles`           | `list[str]`   | Assigned roles         |
| `permissions`     | `list[str]`   | Direct permissions     |
| `organization_id` | `str`         | Current organization   |
| `is_active`       | `bool`        | Account active status  |
| `created_at`      | `datetime`    | Account creation time  |

## User Methods

| Method                       | Returns | Description                        |
| ---------------------------- | ------- | ---------------------------------- |
| `has_permission(perm)`       | `bool`  | Check single permission            |
| `has_all_permissions([...])` | `bool`  | Check all permissions (AND)        |
| `has_any_permission([...])`  | `bool`  | Check any permission (OR)          |
| `has_role(role)`             | `bool`  | Check raw role string              |
| `has_standard_role(role)`    | `bool`  | Check standard role with hierarchy |
| `get_standard_roles()`       | `list`  | Get mapped standard roles          |

## Step-by-Step

{% stepper %}
{% step %}
#### Access Identity Info

```python
print(f"User ID: {user.id}")
print(f"Email: {user.email}")
print(f"Name: {user.display_name}")
```
{% endstep %}

{% step %}
#### Access Authorization Info

```python
print(f"Roles: {user.roles}")
print(f"Permissions: {user.permissions}")
```
{% endstep %}

{% step %}
#### Check Permissions

```python
if user.has_permission("documents:read"):
    print("User can read documents")

if user.has_all_permissions(["documents:read", "documents:write"]):
    print("User has full document access")
```
{% endstep %}

{% step %}
#### Check Roles

```python
from gl_iam.core.roles import StandardRole

if user.has_standard_role(StandardRole.ORG_ADMIN):
    print("User is an admin")
```
{% endstep %}

{% step %}
#### Expected Output

```
User ID: 550e8400-e29b-41d4-a716-446655440000
Email: alice@example.com
Name: Alice
Roles: ['org_member']
Permissions: ['documents:read', 'documents:write']
User can read documents
User has full document access
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You understand the User object!
{% endhint %}

## Complete Example

```python
"""GL IAM User Object Example."""

from gl_iam.core.roles import StandardRole


def inspect_user(user):
    """Inspect a User object."""
    # Identity
    print("=== Identity ===")
    print(f"ID: {user.id}")
    print(f"Email: {user.email}")
    print(f"Display Name: {user.display_name}")

    # Authorization
    print("\n=== Authorization ===")
    print(f"Roles: {user.roles}")
    print(f"Permissions: {user.permissions}")

    # Permission checks
    print("\n=== Permission Checks ===")
    print(f"Can read docs: {user.has_permission('documents:read')}")
    print(f"Can delete docs: {user.has_permission('documents:delete')}")

    # Role checks
    print("\n=== Role Checks ===")
    print(f"Is member: {user.has_standard_role(StandardRole.ORG_MEMBER)}")
    print(f"Is admin: {user.has_standard_role(StandardRole.ORG_ADMIN)}")


# Use after login
user, token = (await gateway.authenticate(creds, org)).unwrap()
inspect_user(user)
```

## Next Steps

* [Validate](validate.md) - Get User from token on protected endpoints
* [Standard Roles](../authorization/standard-roles.md) - Deep dive into role checking
* [Permissions](../authorization/permissions.md) - Deep dive into permission checking

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fuser-authentication%2Fuser).
{% endhint %}
