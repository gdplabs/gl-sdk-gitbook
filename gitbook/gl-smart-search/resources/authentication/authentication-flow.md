---
icon: lock
---

# Authentication Flow

GL Smart Search implements a secure and modular authentication system to manage access across clients, users, and environments. The system now features enhanced token verification with database validation and support for client API key-based user creation.

The authentication documentation is divided into two main sections:

* [**Authentication** ](authentication/)– Covers the standard authentication process including client registration, user creation, token issuance, and access control logic.
* [**Admin Control Panel (AdminCP)**](admin-control-panel-admincp/) – Focuses on the administrative interface used to manage clients, users, and tokens via the Admin Control Panel.

Refer to the respective sections in the sidebar for detailed setup steps and best practices.

### &#x20;Authentication Flow Diagram

This diagram shows the complete authentication flow from client creation to API access:

```mermaid
flowchart TD
    A[Master User] -->|POST /client with master credentials| B[Create Client]
    B -->|Returns| C[Client API Key]

    D[Client/Admin] -->|POST /user with x-api-key header| E[Create User]
    E -->|Returns| F[User identifier + secret]

    G[Application/User] -->|POST /token with identifier + secret| H{x-api-key provided?}
    H -->|Yes| I[Use provided API key]
    H -->|No| J[Use CLIENT_API_KEY from env]
    I --> K[Generate JWT Token]
    J --> K
    K -->|Returns| L[Bearer Token]

    M[Client Application] -->|Request with Bearer token| N[Protected API Endpoint]
    N --> O[VerifyTokenService]
    O --> P{Token Valid?}
    P -->|Yes| Q[Decode JWT]
    Q --> R[Check expiration]
    R --> S[Validate in database]
    S --> T[Check revocation status]
    T --> U[Retrieve user info]
    U --> V[Validate scopes]
    V --> W[Grant Access]
    P -->|No| X[Return 401 Unauthorized]
```

***

### Entity Relationships

Visualize how clients, users, and tokens are structured:

```mermaid
graph TD
    Client[Client]
    Client --> User1[User: glchat_user]
    Client --> User2[User: catapa_user]
    Client --> User3[User: glair_user]

    User1 --> Token1A[Token 1]
    User1 --> Token1B[Token 2]

    User2 --> Token2A[Token 1]

    User3 --> Token3A[Token 1]
    User3 --> Token3B[Token 2]
```

* A **Client** can have multiple **Users**
* A **User** can have multiple active **Tokens**
* Only the **Master User** can create **Clients**
* **Users** can be created by anyone with a valid **Client API Key**
* **Tokens** support backward compatibility - the `x-api-key` header is optional

***

### Token Verification Architecture

The new token verification system provides enhanced security through multi-layer validation:

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant VerifyTokenService
    participant TokenRepository
    participant UserStorage
    participant Database

    Client->>API: Request with Bearer Token
    API->>VerifyTokenService: verify_token_and_get_user_id(token)

    VerifyTokenService->>VerifyTokenService: Decode JWT
    VerifyTokenService->>VerifyTokenService: Validate signature
    VerifyTokenService->>VerifyTokenService: Check expiration

    alt Token expired
        VerifyTokenService-->>API: UnauthorizedException: Token expired
        API-->>Client: 401 Unauthorized
    end

    VerifyTokenService->>VerifyTokenService: Extract user_id & token_id from claims
    VerifyTokenService->>TokenRepository: get_token(user_id, token_id)
    TokenRepository->>Database: Query token by user_id and token_id
    Database-->>TokenRepository: Token record

    alt Token not found
        TokenRepository-->>VerifyTokenService: None
        VerifyTokenService-->>API: UnauthorizedException: Token not found
        API-->>Client: 401 Unauthorized
    end

    alt Token revoked
        TokenRepository-->>VerifyTokenService: Token (is_revoked=true)
        VerifyTokenService-->>API: UnauthorizedException: Token revoked
        API-->>Client: 401 Unauthorized
    end

    TokenRepository-->>VerifyTokenService: Valid Token
    VerifyTokenService-->>API: user_id
    API->>UserStorage: get_user_by_id(user_id)
    UserStorage-->>API: User object
    API->>API: Validate scopes
    API-->>Client: 200 OK with response data
```

**Key Security Features:**

1. **JWT Validation**: Cryptographic signature verification ensures token integrity
2. **Expiration Enforcement**: Automatic rejection of expired tokens
3. **Database Verification**: Cross-references token against stored records
4. **Revocation Support**: Immediate invalidation of compromised tokens
5. **Scope-Based Authorization**: Fine-grained permission control per user
