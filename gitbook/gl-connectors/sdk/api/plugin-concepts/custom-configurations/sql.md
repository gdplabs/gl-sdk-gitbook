---
icon: database
---

# SQL

{% hint style="success" %}
**Module name: `sql`**
{% endhint %}

The **GLConnectors SQL Connector** provides a powerful and flexible way to connect to and query your SQL databases directly from GL Connectors' servers. By leveraging the robustness of SQLAlchemy, it supports a wide range of database systems, allowing you to seamlessly integrate your existing data infrastructure.

This guide will walk you through configuring and how to use the SQL Connector.

## Configuration Parameters

You can configure a new database integration in two ways: by providing a full connection **`url`** or by specifying **individual connection parameters**.

When initiating the integration, you pass a configuration dictionary. If the `url` field is provided, all other connection-specific fields are ignored.

### Required Fields

{% tabs %}
{% tab title="Using URL" %}
This is the simplest method. Provide the full database connection string.

**Required Fields:**

* `url`: The full URL to the database, including the protocol and hostname.

```python
config = {
    "url": "postgresql://myuser:mypassword@myhost:5432/mydatabase",
    "identifier": "My-Production-DB" # Optional, but highly recommended
}
```
{% endtab %}

{% tab title="Using Individual Parameters" %}
Use this method if you prefer to provide each connection detail separately.

**Required Fields:**

* `host`: The hostname of the database.
* `port`: The port of the database.
* `database`: The name of the database.
* `username`: The username for authentication.
* `password`: The password for authentication.
* `driver`: The SQLAlchemy driver to use for the connection.

```python
config = {
    "host": "db.example.com",
    "port": 3306,
    "database": "analytics_db",
    "username": "analyst",
    "password": "secure_password_123",
    "driver": "mysql+pymysql",
    "identifier": "MySQL-Analytics" # Optional, but highly recommended
}
```
{% endtab %}
{% endtabs %}

### Additional Optional Fields

* `identifier`: A custom string to help you identify this specific integration later. While this field is optional, it is **highly recommended**. If not provided, the identifier defaults to a concatenated string of connection details (`driver:host:port:username:database`), which can become long and difficult to read. Setting a clear, human-readable identifier is best practice.
* `extra_config`: A dictionary for any extra parameters required by the database driver (e.g., SSL settings).

### Drivers

{% hint style="warning" %}
If the connection fails because we currently do not support the database (see below), please contact GL Connectors Team. As long as there is a driver available that can be installed that supports that SQL database type, we are willing to provide the support as needed.
{% endhint %}

Drivers must follow SQLAlchemy's supported engine that can be found [here](https://docs.sqlalchemy.org/en/20/core/engines.html). The following database types have been tested:

<table><thead><tr><th width="426">Database Type</th><th>Driver Name</th></tr></thead><tbody><tr><td>MySQL</td><td><code>mysql</code></td></tr><tr><td>MariaDB</td><td><code>mysql</code> or <code>mariadb</code></td></tr><tr><td>PostgreSQL</td><td><code>postgresql</code></td></tr><tr><td>AWS Athena</td><td><code>awsathena+rest</code></td></tr><tr><td>Microsoft SQL Server</td><td><code>mssql+pymssql</code></td></tr></tbody></table>

## Usage Example

{% tabs %}
{% tab title="PostgreSQL" %}
<pre class="language-python"><code class="lang-python">from gl_connectors_sdk.connector import GLConnectors

<strong>connector = GLConnectors(api_base_url="https://connector.gdplabs.id", api_key="your_api_key")
</strong>
user_token = "a_unique_user_token"

has_integration = connector.user_has_integration("sql", user_token)

if not has_integration:
    print("User has no SQL integration. Initiating a new one...")

    config = {
        "url": "postgresql://postgres:postgres@localhost:5432/gl-connectors",
        "identifier": "PSQLGLConnectors" # A custom name for this integration
    }

    integration_result = connector.initiate_plugin_configuration("sql", user_token, config)
    print("Integration initiated:", integration_result)

else:
    print("User already has an SQL integration.")

# 4. Connect to the SQL service and execute a query
print("Executing query...")
sql = connector.connect('sql')

response = sql.action("query") \
    .token(user_token) \
    .params({
        "query": "SELECT * FROM third_party_integration_auths WHERE connector = :conn",
        "variables": {
            "conn": "sql"
        }
    }) \
    .execute()

print("Query response:", response)

</code></pre>
{% endtab %}

{% tab title="Athena" %}
Connecting to Athena is slightly trickier. We need to use `awsathena+rest` for the driver name, and the rest of the configuration requires the AWS configuration data as follows:

**Variable Descriptions:**

* `{AWS_CLIENT_ID}`: Your AWS Access Key ID.
* `{AWS_CLIENT_SECRET}`: Your AWS Secret Access Key.
* `{AWS_REGION}`: The AWS region where your Athena instance is running (e.g., `us-east-1`).
* `{ATHENA_DB_SOURCE}`: The name of your Athena database or data source (often `AwsDataCatalog`).
* `{AWS_ATHENA_S3}`: The S3 bucket name used by Athena to store query results (e.g., `my-athena-query-results-bucket`).
* `{AWS_WORKGROUP}`: The Athena workgroup you want to use (e.g., `primary`).

```python
from gl_connectors_sdk.connector import GLConnectors

connector = GLConnectors(api_base_url="https://connector.gdplabs.id", api_key="your_api_key")

user_token = "a_unique_user_token"

has_integration = connector.user_has_integration("sql", user_token)

if not has_integration:
    print("User has no SQL integration")

    print("Initiating SQL integration...")
    config = {
        "identifier": "connector_athena_custom_url",
        "url": "awsathena+rest://{AWS_CLIENT_ID}:{AWS_CLIENT_SECRET}@athena.{AWS_REGION}.amazonaws.com:443/{ATHENA_DB_SOURCE}?s3_staging_dir=s3://{AWS_ATHENA_S3}&work_group={AWS_WORKGROUP}"
    }
    integration_result = connector.initiate_custom_integration("sql", user_token, config)
    print(integration_result)

else:
    print("User has SQL integration")

sql = connector.connect('sql')
response = sql.action("query") \
    .token(user_token) \
    .params({
        "query": "SELECT * FROM ckvm_employees LIMIT 10",
    }) \
    .execute()

print(response)

```

You can also use the following configuration following the individual parameters guide:

```python
config = {
    "driver": "awsathena+rest",
    "host": "athena.ap-southeast-3.amazonaws.com",
    "port": 443,
    "database": "athena_db",
    "username": "AWS_CLIENT_ID",
    "password": "AWS_CLIENT_SECRET",
    "identifier": "identifier_dev",
    "extra_config": {
        "s3_staging_dir": "s3://output_dir",
        "work_group": "workgroup"
    }
}
```
{% endtab %}
{% endtabs %}
