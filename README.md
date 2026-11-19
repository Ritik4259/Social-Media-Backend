# Social Media Backend

A REST API for a social media application built with **FastAPI**, **SQLAlchemy 2**, and **PostgreSQL**. The API supports user registration, JWT authentication, post management, and post voting.

## Features

- User registration with Argon2 password hashing through `pwdlib`
- JWT bearer-token authentication
- PostgreSQL persistence through SQLAlchemy 2 and Psycopg 3
- Alembic database migrations
- Create, read, update, and delete posts
- Ownership checks for post updates and deletion
- Pagination and title search for posts
- Add and remove votes
- CORS enabled for all origins
- Interactive Swagger UI and ReDoc documentation
- Database connectivity health check

## Tech stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy 2
- PostgreSQL
- Psycopg 3
- Alembic
- Pydantic Settings
- PyJWT
- pwdlib

## Project structure

```text
app/
├── main.py              # FastAPI application, CORS, health check, and routers
├── config.py            # Environment-backed settings
├── database.py          # PostgreSQL engine and database sessions
├── models.py            # User, post, and vote SQLAlchemy models
├── schemas.py           # Request and response schemas
├── routers/
│   ├── auth.py          # Login and JWT token generation
│   ├── post.py          # Post CRUD, pagination, and search
│   ├── user.py          # User registration and retrieval
│   └── vote.py          # Add and remove votes
└── utils/
    └── security.py      # Password hashing and JWT helpers

alembic/
├── env.py               # Alembic environment and database URL
└── versions/            # Database migration revisions
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- PostgreSQL

### 1. Clone the repository

```bash
git clone https://github.com/Ritik4259/Social-Media-Backend.git
cd Social-Media-Backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the pinned dependencies from the repository:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_postgres_password
DATABASE_NAME=social_media
DATABASE_USERNAME=postgres

SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Create the PostgreSQL database named by `DATABASE_NAME` before running migrations.

### 5. Apply database migrations

```bash
alembic upgrade head
```

The migrations create the `users`, `posts`, and `votes` tables. To create a new migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the schema change"
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API runs at <http://127.0.0.1:8000>.

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Authentication

Login uses OAuth2 form data. Send the user's email in the `username` field:

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secure-password"
```

The response contains a JWT access token:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Use the token on protected routes:

```http
Authorization: Bearer <access_token>
```

## API endpoints

### Authentication

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/login` | Authenticate a user and return a JWT | No |

The login request uses `application/x-www-form-urlencoded` with `username` and `password` fields.

### Users

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/users/create` | Register a user | No |
| `GET` | `/users/` | List all users | Bearer token |
| `GET` | `/users/{id}` | Get a user by ID | No |

Registration body:

```json
{
  "email": "user@example.com",
  "password": "secure-password"
}
```

Passwords are hashed before they are stored. User responses contain the ID, email, and creation timestamp, but never the password.

### Posts

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/posts/` | List posts with vote counts | Bearer token |
| `GET` | `/posts/{id}` | Get one post with its vote count | No |
| `POST` | `/posts/create` | Create a post for the authenticated user | Bearer token |
| `PATCH` | `/posts/{id}` | Update an owned post | Bearer token |
| `DELETE` | `/posts/{id}` | Delete an owned post | Bearer token |

Create a post with:

```json
{
  "title": "My first post",
  "content": "Hello from the API",
  "published": true
}
```

`PATCH /posts/{id}` accepts any subset of these fields:

```json
{
  "title": "An updated title",
  "content": "Updated content",
  "published": false
}
```

`GET /posts/` supports these query parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `limit` | `10` | Number of posts to return, from 1 to 100 |
| `offset` | `0` | Number of posts to skip |
| `search` | none | Filter posts by a matching title string |

Post list and detail responses contain the post, its owner, and the total vote count:

```json
{
  "post": {
    "id": 1,
    "title": "My first post",
    "content": "Hello from the API",
    "published": true,
    "created_at": "2026-01-01T12:00:00Z",
    "owner_id": 1,
    "owner": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-01-01T12:00:00Z"
    }
  },
  "votes": 0
}
```

### Votes

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/vote/` | Add or remove the authenticated user's vote | Bearer token |

Send `dir: 1` to add a vote or `dir: 0` to remove an existing vote:

```json
{
  "post_id": 1,
  "dir": 1
}
```

A user can vote only once per post. Adding an existing vote returns `409 Conflict`; removing a vote that does not exist returns `404 Not Found`.

### Database health check

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/test-db` | Check the PostgreSQL connection and return the current database name |

Example response:

```json
{
  "connected": true,
  "database": "social_media"
}
```

## License

No license has been specified yet.
