# Diary API

A RESTful API for managing diary entries, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Create, read, update, and delete diary entries
- Mark entries as done/not done
- Automatic timestamps for creation and updates
- Proper database migrations using Alembic
- Comprehensive test coverage

## Technologies Used

- **Python 3.10+**
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **Poetry** - Dependency management
- **Pytest** - Testing framework

## Prerequisites

- Python 3.10 or higher
- PostgreSQL server running
- Poetry installed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/johniehuge/diary-api.git
cd diary-api
```

or

```bash
git clone git@github.com:johniehuge/diary-api.git
cd diary-api
```

2. Set up environment variables

- create .env in the project root directory

```bash
cp .env.template .env
```

- add your database credentials to .env

```text
DB_URL=postgresql://username:password@localhost/diary_db
```

3. Install dependencies using Poetry

```bash
poetry install
```

## Database Setup

1. Create a database (ensure that PostgreSQL is running)

```bash
createdb diary_db
```

2. Run migrations

```bash
poetry run alembic upgrade head
```

## Running the application

Start the FastAPI development server:

```bash
poetry run uvicorn src.diary_api.main:app --reload
```

The API will be available at `http://localhost:8000/`

## API Documentation

After running the server the documentation is available at:

- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

## Testing

Run the tests with:

```bash
poetry run pytest tests/
```

## Future improvements

- Add user authentication
- Implement entry categories/tags
- Add search functionality
- Add rate limiting
