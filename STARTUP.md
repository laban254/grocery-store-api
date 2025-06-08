# Starting the Dockerized Grocery API

This guide will help you start the Grocery API using Docker for the first time.

## Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd grocery_api
```

## Step 2: Set Up Environment Variables

```bash
cp .env.docker .env
```

Edit the `.env` file to customize your configuration if needed. The default database settings are:

```
DATABASE_URL=postgres://grocery_user:your_password@db:5432/grocery_api
POSTGRES_DB=grocery_api
POSTGRES_USER=grocery_user
POSTGRES_PASSWORD=your_password
```

For Redis configuration:
```
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## Step 3: Start the Services

Option 1: Using the setup script:
```bash
./docker/setup.sh
```

Option 2: Manual startup:
```bash
docker-compose up -d
```

## Step 4: Check Service Status

```bash
docker-compose ps
```

All services should be running. If any service has exited, check the logs:

```bash
docker-compose logs <service-name>
```

For example:
```bash
docker-compose logs web
docker-compose logs db
docker-compose logs redis
docker-compose logs celery
```

## Step 5: Access the Application

- API: http://localhost:8000/
- Admin interface: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/schema/swagger-ui/

## Step 6: Create an Admin User (Optional)

```bash
docker-compose exec web python src/manage.py createsuperuser
```

## Troubleshooting

### Port Conflicts

If you see an error like:
```
Error starting userland proxy: listen tcp4 0.0.0.0:6379: bind: address already in use
```

This means one of the ports required is already in use on your system. The docker-compose.yml already maps Redis to port 6380 to avoid conflicts with local Redis installations.

### Database Connection Issues

If the web service fails to connect to the database, ensure:
1. The database service is running: `docker-compose ps db`
2. The database environment variables are correct in the .env file
3. Check the logs: `docker-compose logs db`

Common issues and solutions:
- If you see a "database 'grocery_api' does not exist" error, the PostgreSQL container might not have initialized the database correctly. You can try:
  ```bash
  docker-compose down -v
  docker-compose up -d
  ```
- If you see a "role 'grocery_user' does not exist" error, check if your database settings in `.env` match the ones used in `docker-compose.yml`
- Ensure that your `DATABASE_URL` in `.env` matches the PostgreSQL settings (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)

### Redis Connection Issues

If Celery fails to connect to Redis, ensure:
1. The Redis service is running: `docker-compose ps redis`
2. Check the logs: `docker-compose logs redis`
3. Verify that your Redis configuration in `.env` is correct:
   ```
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```
   Note that inside Docker, the hostname is `redis` and the port is `6379`, but from your host machine, Redis is accessible at port `6380`.

## Stopping the Services

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (this will delete all data):
```bash
docker-compose down -v
```
