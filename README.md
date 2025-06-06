# Grocery API

A Django-based REST API for managing a grocery store, deployed on Kubernetes with a CI/CD pipeline.

## Key Features

- [Authentication & Authorization](accounts/) - JWT, OAuth, Phone Verification
- [Product Management](products/) - MPTT Categories, Advanced Search
- [Order Processing](orders/) - Async Processing, SMS Notifications
- [API Documentation](http://localhost:8000/api/schema/swagger-ui/) - OpenAPI/Swagger
- [Kubernetes Deployment](k8s/) - VM-based with GitHub Actions

## Technologies

### Application Stack
- Django 5.2 + DRF 3.16
- PostgreSQL 14 + Redis
- Celery + Africa's Talking
- JWT + OAuth Authentication

### Infrastructure
- Kubernetes (k3s)
- Docker + GitHub Actions
- VM Deployment
- SSH Remote Access

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (for Celery)
- Git

### Quick Start (Development)

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd grocery_api
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env  # Then edit .env with your settings
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   python manage.py migrate
   python manage.py runserver



5. Run migrations
   ```bash
   cd src
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Populate the database with sample data (optional)
   ```bash
   python manage.py populate_db
   ```

8. Start the development server
   ```bash
   python manage.py runserver
   ```

9. In a separate terminal, start Celery for background tasks
   ```bash
   cd src
   celery -A grocery_api worker --loglevel=info
   ```

### API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/
- Download OpenAPI schema: http://localhost:8000/api/schema/


## Project Structure

```
src/
  ├── manage.py
  ├── grocery_api/      # Project configuration
  ├── accounts/         # User management
  ├── products/         # Product catalog
  ├── orders/           # Order processing
  └── core/             # Shared functionality
```

## Development

### Running Tests

```bash
pytest --cov
```

### Code Quality

This project uses pre-commit hooks to maintain code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit manually on all files
pre-commit run --all-files
```

### Container Development

Run the full stack in containers:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec web python manage.py migrate
```

See [docker-compose.yml](docker-compose.yml) and [Dockerfile](Dockerfile) for details.


## Development Guidelines

### Local Development
1. Create feature branch from `main`
2. Run tests: `pytest --cov`
3. Submit PR with clear description
4. Address review comments
5. Merge after approval

### CI/CD Pipeline
- **On PR**: Tests, linting, security scans
- **On Merge**: Automated deployment to VM
- See [deploy-staging.yml](.github/workflows/deploy-staging.yml)

### Quality Assurance
- Pre-commit hooks for code quality
- Automated testing with pytest
- Coverage reporting via Codecov

## Deployment

### Prerequisites
- VM with Docker and k3s installed
- GitHub repository with necessary secrets configured

### GitHub Actions Secrets Required
```
VM_HOST             # VM IP or hostname
VM_USER             # SSH username
VM_SSH_KEY          # Private SSH key
VM_HOST_KEY         # VM's public key
SSH_PUBLIC_KEY      # Your public SSH key
K8S_REPO            # k8s config repository
GH_PAT              # GitHub Personal Access Token
```

### Deployment Process
1. Push to main branch triggers the workflow
2. GitHub Actions:
   - Builds Docker image
   - Transfers to VM via SSH
   - Applies k8s configurations
   - Updates services

See [deploy-staging.yml](.github/workflows/deploy-staging.yml) for details.

### Kubernetes Components
- `app-deployment.yaml` - API service deployment
- `app-service.yaml` - NodePort service config
- `postgres-deployment.yaml` - Database setup
- `configmap.yaml` - Environment variables
- `secrets.yaml` - Sensitive data

### Monitoring
- Access metrics at `/metrics`
- Use `kubectl` for logs and status

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
