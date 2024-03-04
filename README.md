# api-movies


## Usage

To run the microservice, use the following Docker Compose command:

```bash
docker-compose up api-movies --build
```

## Access

- The service will be accessible at *http://api-movies.localhost/swagger/* 
- To access the admin panel, visit *http://api-movies.localhost/admin/* 

## Authentication

To interact with the microservice endpoints, a user token is required.
To generate access token, use /login/ endpoint from api-auth microservice

**Authorization: {*generated_access_token*}**

## User Access

Users can only access Movies data if they are authenticated.

## Running Tests

To run tests and generate coverage reports, use the following command:

```bash
docker-compose run --no-deps api-movies bash -c "coverage run manage.py test connector; coverage report -m; coverage html; coverage xml"
```

## Pre-commit Checks

Ensure code quality and formatting by running pre-commit checks:

```bash
pre-commit run --all-files
```

## Environment Configuration

### Setting up Environment Variables

For local development, setting up environment variables is necessary. Copy the provided `.env.api-movies.sample` file to
create your own `.env.api-movies` file. Update the values according to your configuration.

#### Step 1: Copy the Sample Environment File

Copy the contents of `.env.api-movies.sample`:

```bash
cp .env.api-movies.sample .env.api-movies
```

#### Step 2: Update Environment Variables

Open the newly created .env.api-movies file and update the values based on your specific configuration.
This file contains essential settings for the database, Django, and other environment-specific variables.

## Files

- **docker-compose.yml**: Docker Compose configuration file.
- **Dockerfile**: Docker configuration file for building the microservice image.
- **config/requirements.txt**: List of Python dependencies.
- **pre-commit.yml**: Configuration file for pre-commit hooks.
- **pyproject.toml**: TOML configuration file for the project.
- **.env.api-movies.sample**: sample for environment variables