# Kubernetes Deployment Guide

This document describes how to deploy the Grocery API application using Kubernetes.

## Architecture Overview

The application consists of the following components:
- Web API (Django)
- Celery Workers
- PostgreSQL Database
- Redis (for Celery broker and caching)

## Prerequisites

- Kubernetes cluster (Minikube, kind, or other)
- kubectl configured with cluster access
- Docker for building local images

## Components

### Database (PostgreSQL)
- Deployment: `k8s/db-deployment.yaml`
- Service: `k8s/db-service.yaml`
- Persistent Volume Claim: `k8s/postgres-data-persistentvolumeclaim.yaml`

### Redis
- Deployment: `k8s/redis-deployment.yaml`
- Service: `k8s/redis-service.yaml`
- Persistent Volume Claim: `k8s/redis-data-persistentvolumeclaim.yaml`

### Web Application
- Deployment: `k8s/web-deployment.yaml`
- Service: `k8s/web-service.yaml`
- ConfigMap: `k8s/web-cm0-configmap.yaml`
- Environment ConfigMap: `k8s/env-configmap.yaml`

### Celery Workers
- Deployment: `k8s/celery-deployment.yaml`
- ConfigMap: `k8s/celery-cm0-configmap.yaml`

### Storage (Local Development)
For local development, the following hostPath volumes are used:
- PostgreSQL data: `/tmp/postgres-data`
- Redis data: `/tmp/redis-data`
- Media files: `/tmp/media-volume`
- Static files: `/tmp/static-volume`

For production deployment, configure appropriate PersistentVolumeClaims instead.

## Deployment Steps

1. Create namespace (optional):
   ```bash
   kubectl create namespace grocery-api
   kubectl config set-context --current --namespace=grocery-api
   ```

2. Apply ConfigMaps:
   ```bash
   kubectl apply -f k8s/env-configmap.yaml
   kubectl apply -f k8s/web-cm0-configmap.yaml
   kubectl apply -f k8s/celery-cm0-configmap.yaml
   ```

3. Build the application image locally:
   ```bash
   docker build -t grocery_api:latest .
   ```

4. Deploy Database and Redis:
   ```bash
   kubectl apply -f k8s/db-deployment.yaml
   kubectl apply -f k8s/db-service.yaml
   kubectl apply -f k8s/redis-deployment.yaml
   kubectl apply -f k8s/redis-service.yaml
   ```

5. Deploy Web Application:
   ```bash
   kubectl apply -f k8s/web-deployment.yaml
   kubectl apply -f k8s/web-service.yaml
   ```

6. Deploy Celery Workers:
   ```bash
   kubectl apply -f k8s/celery-deployment.yaml
   ```

## Monitoring

Check deployment status:
```bash
kubectl get pods
kubectl get services
kubectl get deployments
```

View logs:
```bash
kubectl logs -f deployment/web
kubectl logs -f deployment/celery
```

## Volume Management

### Local Development
The application uses hostPath volumes for local development:
- `/tmp/postgres-data`: For database persistence
- `/tmp/redis-data`: For Redis persistence
- `/tmp/media-volume`: For user-uploaded content
- `/tmp/static-volume`: For application static files

These directories will be created automatically by Kubernetes.

### Production Deployment
For production, replace hostPath volumes with appropriate PersistentVolumes and PersistentVolumeClaims based on your cloud provider or storage solution.

## Configuration

The application configuration is managed through ConfigMaps:
- `env-configmap.yaml`: Common environment variables
- `web-cm0-configmap.yaml`: Web-specific configuration
- `celery-cm0-configmap.yaml`: Celery-specific configuration

## Scaling

To scale components:
```bash
# Scale web servers
kubectl scale deployment web --replicas=3

# Scale celery workers
kubectl scale deployment celery --replicas=2
```

## Troubleshooting

1. Check pod status:
   ```bash
   kubectl describe pod <pod-name>
   ```

2. View container logs:
   ```bash
   kubectl logs <pod-name> -c <container-name>
   ```

3. Common issues:
   - Image pulling errors: Ensure images are built locally with `docker build -t grocery_api:latest .`
   - Volume mount failures: Check that hostPath directories are accessible
   - Database connection issues: Ensure the database Pod is running and service is accessible
   - Redis connectivity problems: Verify Redis Pod status and service connectivity

4. Checking Pod status:
   ```bash
   # Get detailed pod information
   kubectl describe pod <pod-name>

   # Get pod logs
   kubectl logs <pod-name>

   # Check all resources
   kubectl get all

   # Check specific pod logs with previous logs if pod restarted
   kubectl logs <pod-name> --previous
   ```

## Cleanup

To remove all resources:
```bash
kubectl delete -f k8s/
```

Note: This will not delete persistent volumes. To delete them as well:
```bash
kubectl delete pvc --all
```
