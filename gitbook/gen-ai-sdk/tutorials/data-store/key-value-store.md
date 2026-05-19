---
icon: key
---

# Key-Value Storage

[**`gllm_datastore.key_value_store`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-datastore/gllm_datastore/key_value_store) | **Tutorial**: [key-value-store.md](key-value-store.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_datastore/api/key_value.html)

## What's Key-Value Storage?

**Key-Value Storage** is a versioned secret management system designed for storing and retrieving sensitive data like API keys, credentials, tokens, and configuration. Unlike traditional key-value stores, this implementation provides version control, soft-deletion, and atomic update capabilities through Check-and-Set (CAS) operations.

Every write operation creates a new version of the secret, allowing you to track changes over time and rollback to previous versions when needed. Soft-delete operations mark versions as deleted without permanently destroying them, providing a safety net against accidental data loss. The CAS mechanism prevents concurrent modification conflicts by ensuring updates only succeed when the expected version matches the current version.

This abstraction provides a unified interface across different secret backends, starting with OpenBao (an open-source fork of HashiCorp Vault). The consistent API means switching backends requires only changing the constructor—your code that reads, writes, and manages secrets stays the same.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

**Additional requirements:**

- Access to an OpenBao server (or compatible secret backend)
- Valid authentication token for the secret backend
- Network connectivity to the secret backend endpoint

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-datastore
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-datastore"
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-datastore
```

{% endtab %}
{% endtabs %}

## Quick Start

```python
from gllm_datastore.key_value_store.openbao_key_value_store import OpenBaoKeyValueStore

# Initialize the key-value store
kv_store = OpenBaoKeyValueStore(
    base_url="https://openbao.example.com",
    token="your-auth-token",
    mount_point="secret",
)

# Write a secret (creates version 1)
kv_store.write(
    path="myapp/database",
    data={
        "username": "admin",
        "password": "secure_password",
        "host": "db.example.com",
    },
)

# Read the secret
secret = kv_store.read("myapp/database")
print(secret.data)  # {"username": "admin", "password": "secure_password", ...}
print(secret.metadata.version)  # 1
```

The key-value store automatically handles authentication, versioning, and error handling. Each write operation creates a new version, and you can retrieve any version using read options.

## Core Operations

### Reading Secrets

Read the latest version of a secret:

```python
secret = kv_store.read("myapp/config")
print(secret.data)  # Dictionary of secret data
print(secret.metadata.version)  # Current version number
print(secret.metadata.created_time)  # Timestamp
```

Read a specific version:

```python
from gllm_datastore.key_value_store.key_value_store import ReadOption

secret = kv_store.read(
    "myapp/config",
    options=ReadOption(version=3),
)
```

### Writing Secrets

Write a complete secret (creates a new version):

```python
kv_store.write(
    path="myapp/api-keys",
    data={
        "openai": "sk-...",
        "anthropic": "sk-ant-...",
    },
)
```

Write with Check-and-Set to prevent conflicts:

```python
from gllm_datastore.key_value_store.key_value_store import WriteOption

# Only write if current version is 5
kv_store.write(
    path="myapp/config",
    data={"key": "new_value"},
    options=WriteOption(cas=5),
)
```

{% hint style="info" %}
**Check-and-Set (CAS)**: The `cas` parameter ensures atomic updates by verifying the current version matches your expectation before writing. If another process modified the secret, the write fails with a 409 error, preventing lost updates.
{% endhint %}

### Partial Updates

Merge new keys into an existing secret without replacing the entire secret:

```python
# Existing secret: {"username": "admin", "password": "old_pass"}
kv_store.patch(
    path="myapp/database",
    data={"password": "new_pass"},  # Only update password
)
# Result: {"username": "admin", "password": "new_pass"}
```

The patch operation merges only the provided keys into the existing secret while preserving the rest of the data.

### Listing Keys

List all keys at a given path:

```python
keys = kv_store.list("myapp")
print(keys)  # ["database", "api-keys", "config"]
```

Paths ending with `/` indicate subdirectories:

```python
keys = kv_store.list("myapp/services")
# ["auth/", "payment/", "notification"]
```

## Version Management

### Soft-Delete

Mark specific versions as deleted without permanently destroying them:

```python
# Soft-delete versions 1 and 2
kv_store.delete("myapp/config", versions=[1, 2])
```

Soft-deleted versions can be restored later using `undelete()`.

### Restore Deleted Versions

Restore previously soft-deleted versions:

```python
# Restore versions 1 and 2
kv_store.undelete("myapp/config", versions=[1, 2])
```

### Permanent Destruction

Permanently destroy versions (irreversible):

```python
# Permanently destroy versions 1 and 2
kv_store.destroy("myapp/config", versions=[1, 2])
```

{% hint style="warning" %}
**Destroy is irreversible**: Once a version is destroyed, it cannot be recovered. Use soft-delete for temporary removal and destroy only when you're certain the data should be permanently removed.
{% endhint %}

## Advanced Patterns

### Atomic Updates with Retry

Handle concurrent modifications gracefully:

```python
max_retries = 3
for attempt in range(max_retries):
    # Read current version
    secret = kv_store.read("myapp/counter")
    current_value = int(secret.data["count"])

    # Increment
    new_value = current_value + 1

    try:
        # Write with CAS
        kv_store.write(
            "myapp/counter",
            {"count": str(new_value)},
            options=WriteOption(cas=secret.metadata.version),
        )
        break  # Success
    except requests.RequestException as e:
        if attempt < max_retries - 1 and hasattr(e.response, "status_code"):
            if e.response.status_code in [400, 409]:
                continue  # Retry on conflict
        raise  # Give up or non-retryable error
```

{% hint style="info" %}
**Patch behavior**: `patch()` is the preferred choice for partial updates because it updates only the provided keys instead of replacing the whole secret.
{% endhint %}

### Version History Tracking

Track changes over time by reading different versions:

```python
# Get current version
current = kv_store.read("myapp/config")
print(f"Current version: {current.metadata.version}")

# Compare with previous version
previous = kv_store.read(
    "myapp/config",
    options=ReadOption(version=current.metadata.version - 1),
)

# Identify changes
changed_keys = set(current.data.keys()) ^ set(previous.data.keys())
```

### Namespace Organization

Organize secrets hierarchically:

```python
# Application-level secrets
kv_store.write("myapp/database", {...})
kv_store.write("myapp/api-keys", {...})

# Environment-specific secrets
kv_store.write("myapp/prod/database", {...})
kv_store.write("myapp/staging/database", {...})

# Service-specific secrets
kv_store.write("myapp/services/auth/jwt-secret", {...})
kv_store.write("myapp/services/payment/api-key", {...})
```

## Configuration Options

### Constructor Parameters

| Parameter     | Type | Required | Description                                                          |
| ------------- | ---- | -------- | -------------------------------------------------------------------- |
| `base_url`    | str  | Yes      | Base URL of the secret backend (e.g., `https://openbao.example.com`) |
| `token`       | str  | Yes      | Authentication token for the secret backend                          |
| `mount_point` | str  | Yes      | Mount point for the KV v2 engine (e.g., `secret`)                    |
| `namespace`   | str  | No       | Namespace for multi-tenancy support. Defaults to None.               |
| `timeout`     | int  | No       | Request timeout in seconds. Defaults to 30.                          |

### Read Options

| Parameter | Type        | Description                                                  |
| --------- | ----------- | ------------------------------------------------------------ |
| `version` | int \| None | Specific version to read. If None, reads the latest version. |

### Write Options

| Parameter | Type        | Description                                                                       |
| --------- | ----------- | --------------------------------------------------------------------------------- |
| `cas`     | int \| None | Check-and-Set version. Write only succeeds if current version matches this value. |

## Error Handling

Common exceptions and how to handle them:

```python
import requests

try:
    kv_store.write("myapp/config", data, options=WriteOption(cas=5))
except requests.RequestException as e:
    if hasattr(e.response, "status_code"):
        if e.response.status_code == 400:
            print("Invalid request or CAS mismatch")
        elif e.response.status_code == 404:
            print("Secret not found")
        elif e.response.status_code == 409:
            print("Version conflict - secret was modified")
    else:
        print(f"Network or connection error: {e}")
```

## Takeaways

- Use versioned storage for secrets that change over time and require audit trails
- Leverage CAS operations to prevent concurrent modification conflicts
- Use `patch()` for partial updates with automatic retry logic
- Soft-delete provides a safety net; use destroy only when certain
- Organize secrets hierarchically using path namespaces
- The unified interface allows switching backends without code changes

## API Reference

For more information about the key-value storage, please take a look at our [API Reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_datastore/api/key_value.html).
