# Social Media Backend

A REST API for a social media application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The API supports user registration, JWT authentication, and creating, reading, updating, and deleting posts.

## Features

- User registration with secure password hashing
- JWT bearer-token authentication
- PostgreSQL database integration
- User and post management
- Post pagination and content search
- Automatic interactive API documentation

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Pydantic Settings
- PyJWT
- pwdlib

## Project Structure

```text
app/
├── main.py              # FastAPI application and lifecycle setup
├── config.py            # Environment-backed settings
├── database.py          # PostgreSQL connection and database session
├── models.py            # SQLAlchemy models
├── schemas.py           # Request and response schemas
├── routers/
│   ├── auth.py          # Login and token generation
│   ├── post.py          # Post endpoints
│   └── user.py          # User endpoints
└── utils/
    └── security.py      # Password and JWT helpers
```

## Getting Started

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

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy "psycopg[binary]" pydantic-settings \
  email-validator pwdlib pyjwt python-multipart
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

Create the PostgreSQL database named in `DATABASE_NAME` before starting the application. Tables are created automatically when the application starts.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>.

Interactive documentation:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API Endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | `/login` | Authenticate a user and return an access token | No |

`/login` uses OAuth2 form fields:

- `username`: the user's email address
- `password`: the user's password

### Users

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | `/users/create` | Register a user | No |
| `GET` | `/users/` | List users | Bearer token |
| `GET` | `/users/{id}` | Get a user by ID | No |

Example registration request:

```json
{
  "email": "user@example.com",
  "password": "secure-password"
}
```

### Posts

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| `GET` | `/posts/` | List posts | Bearer token |
| `GET` | `/posts/{id}` | Get a post by ID | No |
| `POST` | `/posts/create` | Create a post | Bearer token |
| `PATCH` | `/posts/{id}` | Update an owned post | Bearer token |
| `DELETE` | `/posts/{id}` | Delete an owned post | Bearer token |

The post list endpoint supports:

- `limit`: number of posts to return, from 1 to 100; default `10`
- `offset`: number of posts to skip; default `0`
- `search`: case-insensitive search against post content

Authenticated requests should include:

```http
Authorization: Bearer <access_token>
```

### Database Health Check

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/test-db` | Check the PostgreSQL connection |

## License

No license has been specified yet.
