---
icon: function
---

# SDK Method API

#### Connector Instance Methods

The connector instance provides several methods for configuring and executing actions:

* `get_available_modules()`: get all available connector modules
* `get_connector(name)` : get an instance of connector modules
* `connect(name)`: Create a connector instance to a service
* `action(name)`: Specify the action to execute
* `params(dict)`: Set request parameters (including pagination parameters like page and per\_page). Note that params for each plugin and action could be different
* `token(str)`: Set the Connector user token
* `identifier(str)`: Specify Connector integration used on the request
* `headers(dict)`: Set custom request headers
* `max_attempts(number)`: Set the maximum number of retry attempts (default: 1) Execution Methods:
* `run()`: Execute and return ActionResponse for advanced data handling
* `execute()`: Execute and return data and status for basic data handling. The data part of the return value can be a ConnectorFile object when the API returns a non-JSON response (such as a file download).

#### Response Handling (ActionResponse)

The ActionResponse class provides methods for handling the response and pagination:

* `get_data()`: Get the current page data (returns the data field from the response). This can return a ConnectorFile object when the API returns a non-JSON response (such as a file download).
* `get_meta()`: Get the metadata information from the response (e.g., pagination details, total count)
* `get_status()`: Get the HTTP status code
* `is_list()`: Check if response is a list
* `has_next()`: Check if there is a next page
* `has_prev()`: Check if there is a previous page
* `next_page()`: Move to and execute next page
* `prev_page()`: Move to and execute previous page
* `get_all_items()`: Get all items from all pages (returns a list of objects containing data and meta for each page)

### Data Models

The SDK uses the following data models:

* `ActionResponseData`: Contains the response data structure with `data` (list, object, or ConnectorFile instance) and `meta` (metadata) fields
* `InitialExecutorRequest`: Stores the initial request parameters used for pagination and subsequent requests
* `ConnectorFile`: Represents a file in requests and responses with these properties:
  * `file`: Raw bytes content of the file
  * `filename`: Optional name of the file
  * `content_type`: Optional MIME type of the file
  * `headers`: Optional HTTP headers for the file

### Configuration Parameters

* `api_base_url`: The base URL of your Connector API endpoint (default: [https://connectors.gdplabs.id](https://connectors.gdplabs.id/)). This parameter is extremely important as it determines the URL of the Connector API you are connecting to, and it will be used to populate the available actions/endpoints and their parameters upon initialization.
* `api_key`: Your Connector API key for authentication. This is different from plugin-specific API keys, which are managed separately by the Connector system.

### Execution Parameters

* `connector`: The name of the connector to use. This parameter is used to determine the connector's available actions and their parameters.
* `action`: The name of the action to execute. This parameter is automatically populated by the connector based on the available actions and their parameters. The list of available actions per connector can be found in [sdk-method-api.md](sdk-method-api.md "mention") and are populated through [https://connectors.gdplabs.id/connectors/names](https://connectors.gdplabs.id/connectors/names).
* `identifier`: The identifier of the Connector integration to use for the request. Connector supports multiple integrations per connector. The default value is `None`, which causes the connector to use its default integration if the user has any integrations.
* `max_attempts`: The maximum number of attempts to make the API request. If the request fails, the connector will retry the request up to this number of times. The default value is 1 if not provided.
  * The retries are handled automatically by the connector, with exponential backoff.
  * The retries are only done for errors that are considered retryable (429 or 5xx).
*   `input_`: The input parameters for the action. This parameter is a dictionary that contains the parameters for the action. The connector will validate the input parameters against the action's schema.

    * To filter response fields, simply add the `response_fields` parameter to the input dictionary. This parameter is a list of field names that will be returned in the response. For nested fields, you can use dot notation, e.g. `user.login` will return the following:

    ```json
    {
      "user": {
        "login": "userlogin"
      }
    }
    ```
* `token`: Optional Connector User Token for authenticating requests. When provided, the connector will include this token in the request headers. This is required for user-specific actions or when working with third-party integrations.

### How It Works

1. **Initialization**: When you create a `GLConnectors` instance, and trigger an `execute()`, the connector will first populate and cache the available actions and their parameters. This is done automatically.
2. **Action Discovery**: The connector expects the Connector API to expose an endpoint that lists all available actions and their parameters. This is handled automatically by Connector's REST API Interface.
3. **Execution**: When you call `execute()`, the connector:
   * Validates your input parameters against the action's schema
   * Handles authentication
   * Makes the API request
   * Returns the formatted response
