# Country Filter Service

Version: 1.0.0 

License: [MIT License](https://opensource.org/license/MIT)

## Overview

The Country Filter Service is an API designed to filter countries based on ISO codes and return 
corresponding country names in various languages. It is built using FastAPI, which is a modern, 
fast (high-performance), web framework for building APIs with Python 3.7+ based on standard 
Python type hints.

## Features

**ISO Code Filtering:** Filter countries by ISO 3166-1 alpha-2 or alpha-3 codes. 

**Multi-language Support:** Returns country names in various languages.

**Asynchronous:** Built with async support for high performance.

## Getting Started

### Prerequisites

- Python 3.12 or later
- Docker
- PostgreSQL for the database backend

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv venv source venv/bin/activate
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Set up the database:
```bash
docker-compose up -build
```
5. Run Alembic migrations to set up the database schema:
```bash
alembic upgrade head
```

## Usage

### Running the Service

To start the FastAPI server, run:
```bash
docker-compose up -build
# apply migrations
docker-compose run web alembic upgrade head
```
The service will be available at http://127.0.0.1:8000.

## API Documentation

FastAPI automatically generates interactive API documentation:
Swagger UI: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc

## API Endpoints

### POST /api/v1/match_country
Retrieve country names matches based on ISO codes.

**Example Request:**
```http
POST /api/v1/match_country

Request body:
{
	"iso": "svk",
	"countries": [
		"iran",
		"Slowakei",
		"Vatikan",
		"Slovaška",
		"Szlovakia",
		"Belgrade",
		"España",
		"Nizozemsko",
        "Slovakia",
        "Slovensko"
	]
}
```

**Example Response:**
```json
{
    "iso": "svk",
    "match_count": 3,
    "matches": [
        "Slowakei",
        "Slovakia",
        "Slovensko"
    ]
}
```

## Testing

To run the tests, ensure you have pytest installed and execute:
```bash
PYTHONPATH=$(pwd) pytest
```

Tests are located in the tests directory and cover various aspects of the API.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.