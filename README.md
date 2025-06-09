# Grocery API

A Django-based REST API for managing a grocery store with Kubernetes deployment support and CI/CD integration.

## Features

- Authentication & Authorization with JWT
- Product Management and Categories
- Asynchronous Order Processing with Celery
- API Documentation (OpenAPI/Swagger)
- Kubernetes Deployment Support
- CI/CD Pipeline with GitHub Actions

## Tech Stack

- Django 4.2.7 + DRF 3.14
- PostgreSQL 14 + Redis 6
- Celery 5.3.6 for Background Tasks
- Docker + Kubernetes
- GitHub Actions for CI/CD

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (for deployment)
- Git

### Local Development

1. Clone and start services:
   ```bash
   git clone <repository-url>
   cd grocery_api
   docker-compose up -d
   ```

2. Run migrations and create superuser:
   ```bash
   docker-compose exec web python src/manage.py migrate
   docker-compose exec web python src/manage.py createsuperuser
   ```

### API Documentation

Access the API documentation at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/


## Development

### Testing
```bash
# Run tests with coverage
docker-compose exec web pytest --cov
```

### Code Quality
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Useful Commands
```bash
# View logs
docker-compose logs -f

# Run Django commands
docker-compose exec web python src/manage.py [command]
```

For deployment instructions, see [KUBERNETES.md](KUBERNETES.md)

## Project Structure

```
src/
├── manage.py
├── grocery_api/      # Project configuration
├── accounts/         # User management
├── products/         # Product catalog
├── orders/          # Order processing
└── core/            # Shared functionality
```

## Additional Documentation

- [Docker Setup](DOCKER.md)
- [Kubernetes Deployment](KUBERNETES.md)
- [Application Startup](STARTUP.md)

## CI/CD Pipeline

The project includes a complete CI/CD pipeline using GitHub Actions:

### Continuous Integration (CI)
- Triggered on pull requests to main, staging, and dev branches
- Runs code quality checks (Black, Flake8)
- Executes tests with coverage reporting
- Validates database migrations

### Continuous Deployment (CD)
- Triggered on pushes to production branch or manual workflow dispatch
- Builds Docker image
- Deploys to Kubernetes cluster
- Applies all necessary Kubernetes configurations
- Verifies deployment success

For more details, see the workflow files in `.github/workflows/`.

## License

MIT License

## Troubleshooting

### Common Issues
1. **Pod Startup Failures**
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Database Connection**
   - Check PostgreSQL PVC status
   - Verify secrets are properly mounted
   - See `postgres-deployment.yaml`

3. **SSH Access**
   - Verify SSH keys in GitHub secrets
   - Check VM firewall settings
   - See `setup-ssh.sh`

### Getting Help
- [Submit an Issue](../../issues)
- Check existing issues
- Review deployment logs
