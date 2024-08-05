FROM python:3.12-slim

ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /src

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code to the container
COPY . .

# Command to run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
