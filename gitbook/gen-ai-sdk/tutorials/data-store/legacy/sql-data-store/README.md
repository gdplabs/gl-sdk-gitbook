---
icon: database
---

# SQL Data Store

## What's a SQL Data Store?

If you're familiar with traditional databases or need to work with structured, tabular data, SQL datastores are your go-to choice. These datastores provide traditional relational database functionality with support for structured data operations. They are suitable for:

* **Structured data** with well-defined schemas
* **Transactional operations** requiring ACID compliance
* **Complex queries** with joins and aggregations
* **Reporting and analytics** on structured datasets

**Available Implementations:**

* SQLAlchemy SQL Data Store

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../../../gen-ai-sdk/prerequisites.md "mention") page.

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
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-datastore"
```
{% endtab %}
{% endtabs %}

## Managing Data

The SQL Data Store provides comprehensive CRUD (Create, Read, Update, Delete) operations for managing structured data. Here's how to use each operation effectively:

```python
from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define your SQLAlchemy model
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Initialize SQL store
sql_store = SQLAlchemySQLDataStore(engine_or_url="sqlite:///data.db")
```

### **Create**

The `create()` method is used to insert new records into the database. It accepts either a single model instance or a list of model instances as parameters.

```python
# Create a single user
new_user = User(
    name="Alice Johnson",
    email="alice@example.com",
    age=28
)
sql_store.create(new_user)

# Create multiple users at once (batch insert)
users_to_save = [
    User(name="Bob Smith", email="bob@example.com", age=32),
    User(name="Carol Davis", email="carol@example.com", age=25),
    User(name="David Wilson", email="david@example.com", age=35)
]
sql_store.create(users_to_save)
```

### **Read**

The `read()` method retrieves data from the database using structured queries with optional filters and options. It provides a type-safe interface for querying data.

<pre class="language-python"><code class="lang-python">from gllm_datastore.sql_data_store.types import QueryFilter, QueryOptions

# Read all users with age = 25, ordered by name
results = sql_store.read(
    model_class=User,
    filters=QueryFilter(
        conditions={"age": 25}
<strong>    ),
</strong>    options=QueryOptions(
        columns=["name", "email", "age"],
        order_by="name",
        order_desc=False,
        limit=10
    )
)
</code></pre>

{% hint style="info" %}
Alternatively, you could also use SQL query directly using the `query()` method.

```python
# Execute raw SQL query for complex operations
results = await sql_store.query(
    "SELECT * FROM users WHERE age = 25 ORDER BY name"
)
```
{% endhint %}

### **Update**

The `update()` method modifies existing records in the database. It requires a model class, update values, and optional filters to specify which records to update.

```python
# Update Alice's age to 29
sql_store.update(
    model_class=User,
    update_values={"age": 29},
    filters=QueryFilter(conditions={"email": "alice@example.com"})
)

# Update multiple users at once
sql_store.update(
    model_class=User,
    update_values={"age": 30},
    filters=QueryFilter(conditions={"age": {"operator": "<", "value": 30}})
)
```

### **Delete**

The `delete()` method removes records from the database. It requires a model class and filters to specify which records to delete, with safety measures to prevent accidental deletion of all records.

```python
# Delete a specific user by email
sql_store.delete(
    model_class=User,
    filters=QueryFilter(conditions={"email": "david@example.com"})
)

# Delete multiple users (with safety check)
sql_store.delete(
    model_class=User,
    filters=QueryFilter(conditions={"age": {"operator": "<", "value": 18}}),
    allow_delete_all=False  # Safety flag to prevent accidental deletion
)
```
