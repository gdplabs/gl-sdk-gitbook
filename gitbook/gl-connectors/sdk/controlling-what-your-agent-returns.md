---
icon: database
---

# Controlling What Your Agent Returns

By default, API responses can return far more data than your agent actually needs. Passing large, unfiltered responses to an AI agent wastes tokens, slows things down, and increases cost. `response_fields` and `response_filters` let you tell the agent exactly what to keep — so it works faster and smarter.

> 💡 Both are **post-processing filters** — they don't change what gets fetched from the API. They only shape what gets returned to you.

***

### Where to Use This

You can apply `response_fields` and `response_filters` in two ways:

* **In your code** — pass them directly as parameters in your tool call request alongside your other inputs.
* **In your system instruction or prompt** — write them into your agent's instruction so they're applied automatically on every tool call.

Not sure which applies to you? If you're configuring an agent through a UI or prompt editor, jump to the [Prompt Examples](controlling-what-your-agent-returns.md#prompt-examples) section. If you're building programmatically, pass them as part of your request body.

***

### Quick Start

Here's the simplest pattern to get going:

```json
"response_fields": ["id", "name", "status"],
"response_filters": [
  { "type": "string", "field_name": "status", "value": "open" }
]
```

`response_fields` keeps only the fields you list. `response_filters` removes items that don't match your criteria. The sections below explain every available option.

***

### response\_fields

Use `response_fields` to **keep only the fields you care about**. Everything else is dropped from the response.

#### Syntax

```json
"response_fields": ["field1", "nested.field", "list_field.sub_field"]
```

#### How it works

| Path type           | Example       | What it keeps                                               |
| ------------------- | ------------- | ----------------------------------------------------------- |
| Top-level field     | `"id"`        | The entire `id` value, including any sub-fields             |
| Nested field        | `"user.name"` | Only `name` inside `user`; other keys in `user` are dropped |
| Field inside a list | `"items.id"`  | Only `id` from each object in the `items` list              |

If `response_fields` is omitted or set to `null`, **all fields are returned**.

#### Examples

**Keep only basic metadata from a list of items:**

```json
"response_fields": ["id", "name", "status"]
```

**Keep selected nested fields:**

```json
"response_fields": ["id", "user.name", "user.email"]
```

**Keep sub-fields from a payload object:**

```json
"response_fields": ["payload.headers", "payload.body"]
```

**Keep sub-fields from items inside a list:**

```json
"response_fields": ["items.id", "items.name"]
```

***

### response\_filters

Use `response_filters` to **remove items that don't match your criteria**. Works on list responses — items that don't pass the filter are excluded entirely.

All filters use **AND logic**: an item must pass every filter in your list to be kept.

#### Filter Types

**`string` — Exact string match**

Keeps items where the field equals a specific string value.

```json
{
  "type": "string",
  "field_name": "status",
  "value": "open",
  "ignore_case": true
}
```

| Field         | Required | Default | Description                             |
| ------------- | -------- | ------- | --------------------------------------- |
| `value`       | ✅        | —       | The string to match                     |
| `ignore_case` | ❌        | `true`  | Match regardless of uppercase/lowercase |

***

**`string_list` — Match any value from a list**

Keeps items where the field matches **any** value in your list.

```json
{
  "type": "string_list",
  "field_name": "status",
  "values": ["open", "in_progress"],
  "ignore_case": true
}
```

| Field         | Required | Default | Description                                      |
| ------------- | -------- | ------- | ------------------------------------------------ |
| `values`      | ✅        | `[]`    | Allowed string values. Empty list = no filtering |
| `ignore_case` | ❌        | `true`  | Match regardless of uppercase/lowercase          |

***

**`date_range` — Filter by date range**

Keeps items where the date field falls within a specified window.

```json
{
  "type": "date_range",
  "field_name": "created_at",
  "from_date": "2024-01-01",
  "to_date": "2024-12-31"
}
```

| Field       | Required | Description                                          |
| ----------- | -------- | ---------------------------------------------------- |
| `from_date` | ❌        | Start of range (inclusive). Omit to skip lower bound |
| `to_date`   | ❌        | End of range (inclusive). Omit to skip upper bound   |

**Supported date formats:** `YYYY-MM-DD`, `YYYY-MM-DD HH:MM:SS`, `YYYY-MM-DDTHH:MM:SSZ`

***

**`number` — Exact number match**

Keeps items where the numeric field equals a specific value.

```json
{
  "type": "number",
  "field_name": "priority",
  "value": 1
}
```

| Field   | Required | Description                        |
| ------- | -------- | ---------------------------------- |
| `value` | ✅        | The number to match (int or float) |

***

**`number_list` — Match any value from a list of numbers**

Keeps items where the numeric field matches any value in your list.

```json
{
  "type": "number_list",
  "field_name": "priority",
  "values": 
}
```

| Field    | Required | Default | Description                                               |
| -------- | -------- | ------- | --------------------------------------------------------- |
| `values` | ✅        | `[]`    | Allowed numbers (int or float). Empty list = no filtering |

***

**`number_range` — Filter by numeric range**

Keeps items where the numeric field falls within a range.

```json
{
  "type": "number_range",
  "field_name": "score",
  "from_value": 50.0,
  "to_value": 100.0
}
```

| Field        | Required | Description                                             |
| ------------ | -------- | ------------------------------------------------------- |
| `from_value` | ❌        | Lower bound (inclusive). Omit to skip lower bound check |
| `to_value`   | ❌        | Upper bound (inclusive). Omit to skip upper bound check |

***

#### Root Filters

By default, `response_filters` operates on **top-level items** in a list response.

Use the `root` option when you need to filter elements inside a **nested array** within each item — without removing the parent item itself.

**Example: keep only specific email headers**

The response is a single email object with a `payload.headers` array. You want only `Content-Type` and `Authorization` headers:

```json
{
  "type": "string_list",
  "root": "payload.headers",
  "field_name": "name",
  "values": ["Content-Type", "Authorization"]
}
```

**Before:**

```json
{
  "payload": {
    "headers": [
      {"name": "Received", "value": "..."},
      {"name": "Content-Type", "value": "text/html"},
      {"name": "Authorization", "value": "Bearer ..."}
    ]
  }
}
```

**After:**

```json
{
  "payload": {
    "headers": [
      {"name": "Content-Type", "value": "text/html"},
      {"name": "Authorization", "value": "Bearer ..."}
    ]
  }
}
```

**Example: deeply nested array**

```json
{
  "type": "string_list",
  "root": "payload.parts.headers",
  "field_name": "name",
  "values": ["Content-Type"]
}
```

This traverses `payload` → `parts` (array) → for each part, filters its `headers` array.

> ⚠️ **Important:** The `root` path must resolve to an **array of objects**. If the path doesn't exist or isn't an array of objects, filtering is silently skipped. The `field_name` must be a key that exists within those objects.

***

### Combining Both

You can use `response_filters` and `response_fields` together.

**Order of operations:** filters run first (removes unwanted items), then fields are trimmed (removes unwanted keys from the remaining items).

```json
"response_filters": [
  {
    "type": "string_list",
    "field_name": "state",
    "values": ["open"]
  }
],
"response_fields": ["id", "title", "state", "created_at"]
```

This returns only open items, and for each item, only keeps `id`, `title`, `state`, and `created_at`.

***

### Prompt Examples

Use these as a starting point when writing your agent prompt or system instruction.

<details>

<summary>Filter by status and date range</summary>

**Prompt:**

> Fetch open GitHub issues created in 2024.

```json
"response_filters": [
  { "type": "string", "field_name": "status", "value": "open" },
  { "type": "date_range", "field_name": "created_at", "from_date": "2024-01-01", "to_date": "2024-12-31" }
],
"response_fields": ["id", "title", "status", "created_at", "assignee.login"]
```

</details>

<details>

<summary>Filter by priority level</summary>

**Prompt:**

> List all tasks with high or critical priority.

```json
"response_filters": [
  { "type": "number_list", "field_name": "priority", "values":  }
],
"response_fields": ["id", "title", "priority", "due_date"]
```

</details>

<details>

<summary>Filter by multiple statuses</summary>

**Prompt:**

> Retrieve all pull requests that are open or in progress.

```json
"response_filters": [
  { "type": "string_list", "field_name": "state", "values": ["open", "in_progress"] }
],
"response_fields": ["id", "title", "state", "author.name", "updated_at"]
```

</details>

<details>

<summary>Filter by numeric range</summary>

**Prompt:**

> Get search results with a relevance score above 70.

```json
"response_filters": [
  { "type": "number_range", "field_name": "score", "from_value": 70 }
],
"response_fields": ["id", "title", "score", "url"]
```

</details>

<details>

<summary>Filter inside a nested array</summary>

**Prompt:**

> Fetch the email and return only the Content-Type and Authorization headers.

```json
"response_filters": [
  {
    "type": "string_list",
    "root": "payload.headers",
    "field_name": "name",
    "values": ["Content-Type", "Authorization"]
  }
]
```

</details>

> 💡 Use `root` when you want to trim elements inside a nested array rather than filtering the top-level items themselves.

