# Environment Variables for Grocery API

This document describes all environment variables used by the Grocery API application and how to set them up for various environments.

## Essential Environment Variables

These variables are required for the application to function properly:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Auto-generated for Heroku | Yes |
| `DEBUG` | Enable debug mode | `False` in production | No |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `APP_NAME.herokuapp.com,localhost,127.0.0.1` | Yes |
| `DATABASE_URL` | Database connection URL | Provided by Heroku PostgreSQL addon | Yes |
| `REDIS_URL` | Redis connection URL | Provided by Heroku Redis addon | Yes |

## Africa's Talking SMS API

These variables are required for SMS functionality:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `AFRICAS_TALKING_ENVIRONMENT` | Environment (`sandbox` or `production`) | `sandbox` | Yes |
| `AFRICAS_TALKING_API_KEY` | API key for Africa's Talking | `dummy-key-for-collectstatic` in collectstatic | Yes for SMS |
| `AFRICAS_TALKING_USERNAME` | Username for Africa's Talking | `sandbox` | Yes for SMS |
| `AFRICAS_TALKING_SENDER_ID` | Sender ID for branded messages | Empty | No |

## Authentication and OAuth

These variables are for social authentication:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `OIDC_PROVIDER_ID` | OIDC Provider ID | `your-oidc-provider` | No |
| `OIDC_PROVIDER_NAME` | OIDC Provider Name | `Your OIDC Provider` | No |
| `OIDC_SERVER_URL` | OIDC Server URL | `https://your-oidc-provider.com` | No |
| `OIDC_CLIENT_ID` | OIDC Client ID | `your-client-id` | No |
| `OIDC_CLIENT_SECRET` | OIDC Client Secret | `your-client-secret` | No |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | None | No |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | None | No |

## Celery Configuration

These variables are for Celery task queue:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/0` | Yes for Celery |
| `CELERY_RESULT_BACKEND` | Celery result backend URL | `redis://localhost:6379/0` | Yes for Celery |

## JWT Authentication

These variables are for JWT token configuration:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | Access token lifetime in minutes | `60` | No |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | Refresh token lifetime in days | `1` | No |

## Setting Up Environment Variables

### Local Development

For local development, create a `.env` file in the project root with your environment variables.

### Heroku Deployment

Environment variables for Heroku are set with the `heroku config:set` command:

```bash
heroku config:set VARIABLE_NAME=value -a your-app-name
```

The `scripts/setup_heroku.sh` script automatically sets essential environment variables and transfers variables from your local `.env` file if it exists.

### Docker Deployment

When using Docker, environment variables can be set in the `docker-compose.yml` file or passed to the `docker run` command.
