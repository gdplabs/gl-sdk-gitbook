# Master Authentication

In this system, only the **Master** user has the ability to create new **clients** and **users**. This ensures that access to these resources is tightly controlled.

The **Master** user is authenticated using a set of credentials that are stored securely in environment variables:

* **`MASTER_USERNAME`**: The username of the Master user.
* **`MASTER_PASSWORD`**: The password of the Master user.

These credentials are used when making requests to the endpoints that create clients and users. When the correct **Master** credentials are provided, the request is validated, and the creation of new clients and users is authorized.

**Important Note**: The Master user has the highest level of access and can manage the entire system's authentication flow by creating and managing clients and users.
