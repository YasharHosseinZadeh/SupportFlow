# SupportFlow API

SupportFlow is a RESTful API for managing support tickets. It provides user authentication, role-based access control, ticket management, comments, and analytics.

This project was built to practice backend development with Python and FastAPI.

## Features

- User registration and login
- JWT-based authentication
- Role-based access control for customers, agents, and managers
- Create, retrieve, update, and delete support tickets
- Update ticket status (`open`, `in_progress`, `closed`)
- Add comments to tickets
- Ticket analytics and status statistics
- SQLAlchemy database integration
- Database migrations with Alembic
- Automated tests with Pytest
- Continuous Integration with GitHub Actions
- Docker support
- Deployment on Render

## Technologies

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- SQLite for local development
- Alembic
- Pydantic
- JWT Authentication
- Pytest
- Docker
- GitHub Actions
- Render

## Project Structure

```text
supportflow/
├── .github/
│   └── workflows/
├── alembic/
├── core/
├── models/
├── routers/
├── schemas/
├── services/
├── tests/
├── .dockerignore
├── .gitignore
├── alembic.ini
├── database.py
├── dependencies.py
├── Dockerfile
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YasharMhz/SupportFlow.git
cd SupportFlow
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Add the following variables:

```env
DATABASE_URL=sqlite+aiosqlite:///./supportflow.db
SECRET_KEY=replace_with_a_secure_secret
```

Replace the example secret with a securely generated value. Never commit your actual `.env` file or secrets to GitHub.

For production, configure the appropriate PostgreSQL connection URL and secret in your deployment environment.

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can use these interfaces to explore endpoints and send requests to the API.

## Authentication and Authorization

SupportFlow uses JWT (JSON Web Tokens) to authenticate users.

After logging in, clients can use the returned token to access protected endpoints.

The API supports three roles:

| Role | Description |
|---|---|
| Customer | Accesses permitted customer features |
| Agent | Accesses permitted support and ticket-management features |
| Manager | Accesses permitted management features |

Access to protected endpoints depends on the user's role and the permissions configured for each endpoint.

## Main API Features

The API includes endpoints for:

- **Users:** Registration and user management
- **Authentication:** Login and JWT token generation
- **Tickets:** Ticket creation and management
- **Ticket Status:** Updating ticket status
- **Comments:** Adding and managing ticket comments
- **Analytics:** Viewing ticket statistics

For the complete list of routes, HTTP methods, request parameters, and response formats, start the application and visit `/docs`.

## Database

SupportFlow uses SQLAlchemy for database operations.

- SQLite is used for local development.
- PostgreSQL is used for the deployed application.
- Alembic manages database schema migrations.

The local development database and production database contain separate data.

## Testing

Run the automated test suite with:

```bash
pytest
```

The tests help verify application behavior, including authentication, ticket operations, and access permissions.

## Continuous Integration

GitHub Actions runs the project's automated tests when changes are pushed to the repository.

This helps detect problems before changes are deployed.

## Docker

The project includes a `Dockerfile` and a `compose.yaml` file for container-related workflows.

Use the configuration files in the repository to run the application with Docker.

## Deployment

SupportFlow is deployed on Render.

The deployed application uses PostgreSQL for persistent data storage.

To test the deployed API, open its deployment URL and visit `/docs`.

## Future Improvements

Potential future improvements include:

- Pagination and filtering for ticket lists
- More advanced analytics
- Improved logging and monitoring
- Additional automated tests

## Author

**Yashar Hossein Zadeh**

- GitHub: [YasharHosseinZadeh](https://github.com/YasharHosseinZadeh)
- LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/yashar-hossein-zadeh-0537b042b/)