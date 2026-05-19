---
icon: key-skeleton
---

# Authentication

Welcome to the Authentication guide for the GL Smart Search API. This system is designed to provide secure and flexible access management using a **client-user-token** structure. Below is an overview of the system's components:

1. **Clients**: A **client** represents an entity (such as a company or application) that interacts with the GL Smart Search API. Each client receives a unique **API key** upon creation, which is used to create users associated with that client. Only the Master user can create clients.
2. **Users**: A **user** is an individual account tied to a specific client. Users are created via the `/user` endpoint by providing the client's API key in the `x-api-key` header. Each user receives a unique `identifier` and `secret` for token generation.
3. **Tokens**: A **token** is a JWT-based authentication credential used to access protected API endpoints. Users generate tokens using their `identifier` and `secret`. The system supports backward compatibility - tokens can be created with or without providing a client API key in the header.
4. **Token Verification**: The system implements a multi-layer verification process that validates JWT signatures, checks expiration, verifies tokens against the database, and ensures tokens haven't been revoked. This provides enhanced security compared to JWT-only validation.
5. **Master User**: The **Master** user has the highest level of access within the system. Only the Master user can create new **clients** using master credentials (`MASTER_USERNAME` and `MASTER_PASSWORD`). User creation is delegated to anyone with a valid client API key.

This authentication system ensures secure access control, allowing the Master user to manage client and user creation, while enabling users to authenticate their API requests through tokens.
