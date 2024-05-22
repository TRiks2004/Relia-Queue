# Base image
FROM python:3.12

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# CONTAINER
ENV FAST_API_TITLE FastAPI
ENV FAST_API_DOCS_URL /docs
ENV FAST_API_DEBUG True

ENV PORT_CONTAINER_API 8200


# Set work directory
WORKDIR /code

# Install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-dev build-essential

# Install wkhtmltopdf
RUN apt-get install -y xvfb libfontconfig wkhtmltopdf

# Upgrade pip and install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Add pyproject.toml and install dependencies
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Expose port 8200
EXPOSE 8200

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["poetry", "run", "python", "uvicorn_service.py"]
