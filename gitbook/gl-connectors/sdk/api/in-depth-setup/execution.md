---
icon: circle-bolt
---

# Execution

### Basic Example (Direct Execution)

It is the basic way to execute actions, where you need to provide the connector name, action name, and user token. The response will contain the data and status:

```python
params = {
    "owner": "gdp-admin",
    "author": "samuellusandi",
    "per_page": 1,
}
data = connector.execute("github", "search_commits", token=user_token, input_=params)
print(data)
```

### Alternative Approach (Fluent Interface)

For more complex scenarios or more control over the execution, you can use the fluent interface. We're recommending this approach if you:

* Need to execute multiple actions with different parameters
* Expecting list response
* Need to execute actions in a loop

```python
params = {
    "owner": "gdp-admin",
    "author": "samuellusandi",
    "per_page": 1,
}
github = connector.connect('github')
response = github.action('list_pull_requests')\
    .params(params)\
    .max_attempts(3)\
    .token('user-token')\
    .run()  # Execute and return ActionResponse for advanced data handling

# Get initial data
initial_data = response.get_data()

# Iterate the following next pages
while response.has_next():
    response = response.next_page(
    data = response.get_data()
    # Process data here

# You can also navigate backwards
while response.has_prev():
    response = response.prev_page()
    data = response.get_data()
    # Process data here

# Execute multiple independent actions using the same connector instance
commits_response = github.action('list_commits')\
    .params({
        'owner': 'GDP-ADMIN',
        'repo': 'gl-connectors',
        'page': 1,
        'per_page': 10
    })\
    .token('user-token')\
    .run()
```

`run` method also available for direct execution from connector instance, without using fluent interface.

```python
params = {
    "owner": "gdp-admin",
    "author": "samuellusandi",
    "per_page": 1,
}

response = connector.run('github', 'list_pull_requests', input_=params)
print(response.get_data())
```

### Working with Files using ConnectorFile

When working with APIs that require file uploads or return file downloads, use the `ConnectorFile` model. Here are the examples of how to uplaod or download files using GL Connectors.

#### Uploading Files

<pre class="language-python"><code class="lang-python">from gl_connectors_sdk.models.file import ConnectorFile

# For uploads: Create a ConnectorFile object
with open("document.pdf", "rb") as f:
    upload_file = ConnectorFile(
        file=f.read(),
        filename="document.pdf",
        content_type="application/pdf"
    )

params = {
  "file": upload_file,
  "name": "My Document"
}
<strong>result = connector.execute("google_drive", "upload_file", input_=params)
</strong></code></pre>

#### Downloading Files

```python
from gl_connectors_sdk.models.file import ConnectorFile

file_result = connector.execute("google_drive", "download_file", input_={"file_id": "123"})
if isinstance(file_result, ConnectorFile):
    with open(file_result.filename or "downloaded_file", "wb") as f:
        f.write(file_result.file)
```
