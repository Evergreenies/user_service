# User Service

**User Service Endpoints:**

**1. User Management:**

- **POST /users:** Creates a new user account.

  - **Request Body:**
    - `username`: Unique username for the user (required).
    - `password`: User's password (required).
    - `email`: User's email address (required, unique).
    - `first_name`: User's first name (optional).
    - `last_name`: User's last name (optional).
  - **Response:**
    - `201 Created`: User created successfully, returns the newly created user object.
    - `400 Bad Request`: Invalid or missing required fields in the request body.
    - `409 Conflict`: Username or email already exists.

- **GET /users/{user_id}:** Retrieves a specific user's information.

  - **Path Parameter:**
    - `user_id`: Unique identifier of the user (required).
  - **Response:**
    - `200 OK`: User found, returns the user object.
    - `404 Not Found`: User with the specified ID not found.

- **PUT /users/{user_id}:** Updates an existing user's profile.

  - **Path Parameter:**
    - `user_id`: Unique identifier of the user (required).
  - **Request Body:**
    - Any fields that need to be updated (optional).
  - **Response:**
    - `200 OK`: User updated successfully, returns the updated user object.
    - `400 Bad Request`: Invalid or missing fields in the request body.
    - `404 Not Found`: User with the specified ID not found.

- **DELETE /users/{user_id}:** Deletes a user account.
  - **Path Parameter:**
    - `user_id`: Unique identifier of the user (required).
  - **Response:**
    - `204 No Content`: User deleted successfully.
    - `404 Not Found`: User with the specified ID not found.
    - `409 Conflict`: User cannot be deleted due to associated borrowings (consider returning a more informative error message).

**2. Authentication:**

- **POST /users/login:** Logs a user in and returns an authentication token.

  - **Request Body:**
    - `username`: User's username (required).
    - `password`: User's password (required).
  - **Response:**
    - `200 OK`: Login successful, returns an authentication token and optionally other user information.
    - `401 Unauthorized`: Invalid username or password.
    - `400 Bad Request`: Missing username or password in the request body.

- **POST /users/logout:** Logs a user out and invalidates their authentication token.
  - **Request Headers:**
    - `Authorization`: Bearer token (required).
  - **Response:**
    - `200 OK`: Logout successful.
    - `401 Unauthorized`: Invalid or expired token.

**3. Borrowing History:**

- **GET /users/{user_id}/borrowings:** Retrieves a user's borrowing history.
  - **Path Parameter:**
    - `user_id`: Unique identifier of the user (required).
  - **Response:**
    - `200 OK`: Borrowing history retrieved successfully, returns a list of borrowed book details or relevant information.
    - `404 Not Found`: User with the specified ID not found.

**Database Structure:**

**Users Table:**

```
|-------------|---------------|
| Column Name | Data Type     |
|-------------|---------------|
| id          | INT           |
| username    | VARCHAR(255)  |
| password    | VARCHAR(255)  |
| email       | VARCHAR(255)  |
| first_name  | VARCHAR(255)  |
| last_name   | VARCHAR(255)  |
| created_at  | DATETIME      |
| updated_at  | DATETIME      |
| active      | BOOLEAN       |
|-------------|---------------|
```

**Additional Considerations:**

- Implement robust password hashing and salting using industry-standard algorithms (e.g., bcrypt, Argon2).
- Securely store and transmit authentication tokens (e.g., using HTTPS, JWT with appropriate claims and signing

