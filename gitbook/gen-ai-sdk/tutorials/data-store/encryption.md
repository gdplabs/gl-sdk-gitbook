---
icon: lock
---

# Encryption

## Encryption in Data Store

The **Encryption Capability** provides transparent field-level encryption for data store chunks. It encrypts chunk content and metadata fields automatically during write operations and decrypts them during read operations, working seamlessly with fulltext and vector capabilities.

Encryption operates transparently—you don't need to access it directly. Once configured, it's automatically used by fulltext and vector capabilities whenever you create, update, or retrieve chunks.

{% hint style="info" %}
**Semantic Search Support**: Even with encryption enabled, vector search remains fully functional. Embeddings are generated from the plaintext content _before_ encryption, ensuring semantic search accuracy without compromising security.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts and components:

1. [README.md](README.md "mention")
2. The fulltext capability overview in [README.md](README.md#fulltext-capability "mention")
3. The vector capability overview in [README.md](README.md#vector-capability "mention")

</details>

## How Encryption Works

### Transparent Operation

Encryption integrates directly with fulltext and vector capabilities. When you enable encryption on a data store:

1. **During Write Operations**: Content and metadata fields specified in the encryption configuration are encrypted before being stored.
2. **During Read Operations**: Encrypted fields are automatically decrypted when chunks are retrieved.
3. **Embedding Generation**: For vector capability, embeddings are generated from plaintext content before encryption.

### Field-Level Configuration

You can encrypt specific fields:

1. **Content field**: Encrypt the chunk content using `"content"`.
2. **Metadata fields**: Encrypt specific metadata fields using dot notation, e.g., `"metadata.secret_api_key"`.
3. **Nested metadata**: Support for nested metadata fields, e.g., `"metadata.user.email"`.

## Choose an Encryptor

The data store supports multiple encryptor types:

### AES-GCM Encryptor

Use `AESGCMEncryptor` for simple encryption with a direct key:

```python
from gllm_datastore.encryptor.aes_gcm_encryptor import AESGCMEncryptor
import os

# Generate a 256-bit key (32 bytes)
encryption_key = os.urandom(32)
encryptor = AESGCMEncryptor(key=encryption_key)
```

{% hint style="warning" %}
**Key Management**: Store your encryption key securely. If you lose the key, you cannot decrypt your data. Consider using a key management service for production applications.
{% endhint %}

### Key Rotating Encryptor

Use `KeyRotatingEncryptor` for scenarios requiring key rotation:

```python
from gllm_datastore.encryptor.aes_gcm_encryptor import AESGCMEncryptor
from gllm_datastore.encryptor.key_ring.in_memory_key_ring import InMemoryKeyRing
from gllm_datastore.encryptor.key_rotating_encryptor import KeyRotatingEncryptor
import os

# Create a key ring and add multiple keys
key_ring = InMemoryKeyRing()
key_ring.add("key_v1", AESGCMEncryptor(key=os.urandom(32)))
key_ring.add("key_v2", AESGCMEncryptor(key=os.urandom(32)))

# Create encryptor with active key
encryptor = KeyRotatingEncryptor(
    key_ring=key_ring,
    active_key_id="key_v1"
)
```

### KMS Encryptor

Use `KmsEncryptor` for production scenarios where encryption keys are managed by a Key Management Service (KMS). This encryptor implements **envelope encryption**: a Data Encryption Key (DEK) is generated and encrypted by the KMS, and the DEK is then used with AES-GCM to encrypt the actual data.

```python
import base64
import os

from gllm_datastore.encryptor.kms_encryptor import KmsEncryptor
from gllm_datastore.kms.kms import BaseKeyManagementService

class SampleKMSImplementation(BaseKeyManagementService):
    def get_dek(self):
        dek = os.urandom(32)
        encrypted_dek = base64.b64encode(dek).decode()
        return dek, encrypted_dek

    def decrypt(self, encrypted_dek: bytes):
        return base64.b64decode(encrypted_dek)


kms = SampleKMSImplementation()
encryptor = KmsEncryptor(kms=kms)
```

{% hint style="info" %}
`KmsEncryptor` delegates key generation and key encryption to the KMS, so the plaintext DEK is never stored. This is the recommended approach for regulated environments.
{% endhint %}

## Enable Encryption

Enable encryption using the `.with_encryption()` method. This method can be chained with other capability registration methods.

### Example: Chroma Data Store

```python
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_datastore.encryptor.aes_gcm_encryptor import AESGCMEncryptor
from gllm_inference.em_invoker import OpenAIEMInvoker
import os

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

encryptor = AESGCMEncryptor(key=os.urandom(32))

store = (
    ChromaDataStore(
        collection_name="secure-docs",
        client_type=ChromaClientType.MEMORY,
    )
    .with_encryption(
        encryptor=encryptor,
        fields={"content", "metadata.secret_key"}
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

## Using Encrypted Data Store

Once encryption is enabled, use the data store normally. Encryption and decryption happen automatically:

```python
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import QueryOptions, filter as F

# Create chunks with sensitive data
chunks = [
    Chunk(
        id="doc-1",
        content="Sensitive medical record...",    # Encrypted
        metadata={
            "role": "patient",                    # Plaintext (safe for filtering)
            "ssn": "000-00-0000"                  # Encrypted
        }
    )
]

# 2. Store (encryption happens automatically)
await store.fulltext.create(chunks)

# 3. Retrieve using a plaintext field
results = await store.fulltext.retrieve(filters=F.eq("metadata.role", "patient"))

# 4. Access data (decryption happens automatically)
print(results[0].content)
print(results[0].metadata["ssn"])
```

## ⚠️ STRICT WARNING: Filtering & Sorting

{% hint style="danger" %}
**DO NOT use encrypted fields for filtering or sorting.**

Filtering or sorting on encrypted fields (`order_by`, `F.eq`, etc.) will fail or yield incorrect results because the database stores randomized ciphertext (different every time), not the plaintext value.

**ALWAYS use plaintext fields (like `id` or non-sensitive metadata) for filtering and sorting.**
{% endhint %}

### Correct vs. Incorrect Usage

✅ **Correct**: Filter by `id` or plaintext metadata, then read encrypted data.

```python
results = await store.fulltext.retrieve(
    filters=F.eq("metadata.role", "patient")
)
```

❌ **Incorrect**: Attempting to filter by the encrypted field itself.

```python
results = await store.fulltext.retrieve(
    filters=F.eq("metadata.ssn", "000-00-0000")
)
```

❌ **Incorrect**: Sorting by an encrypted field.

```python
results = await store.fulltext.retrieve(
    options=QueryOptions(order_by="metadata.ssn", order_desc=True)
)
```
