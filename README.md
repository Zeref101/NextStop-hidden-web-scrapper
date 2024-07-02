# NextStop-hidden-web-scrapper

It's a high performant web scrapper created for a very specific Maqsad.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Poetry for Python package management

## Installation

To set up the project environment, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/Zeref101/NextStop-hidden-web-scrapper.git
cd NextStop-hidden-web-scrapper
```

2. Install dependencies using Poetry:

```bash
poetry install
```

## Running the Application

To run the FastAPI application:

```bash
poetry run uvicorn app.main:app --reload --port 8000
```

This command will start the Uvicorn server with `--reload` option to enable auto-reload on code changes and the application runs at port 8000.

## Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── main.py          # Entry point of the FastAPI app
|   ├── services         # functions used by services
│   └── routes           # Web route definitions
│       └── __init__.py

├── pyproject.toml       # Poetry dependency file
└── README.md
```

## API Documentation

Once the application is running, you can visit `http://127.0.0.1:8000/docs` in your web browser to view the automatic interactive API documentation provided by Swagger UI.
