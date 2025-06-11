#!/bin/bash

# Check if the app exists
HEROKU_APP_EXISTS=$(heroku apps:info $APP_NAME 2>&1 | grep -c "=== $APP_NAME")

if [ "$HEROKU_APP_EXISTS" -eq 0 ]; then
  echo "Creating Heroku app: $APP_NAME"
  heroku apps:create $APP_NAME
else
  echo "Heroku app $APP_NAME already exists"
fi

# Set stack to container
heroku stack:set container -a $APP_NAME

# Add required addons
echo "Adding PostgreSQL and Redis addons..."
heroku addons:create heroku-postgresql:hobby-dev -a $APP_NAME
heroku addons:create heroku-redis:hobby-dev -a $APP_NAME

# Set environment variables
echo "Setting environment variables..."
heroku config:set SECRET_KEY="$(openssl rand -hex 32)" -a $APP_NAME
heroku config:set ALLOWED_HOSTS="$APP_NAME.herokuapp.com,localhost,127.0.0.1" -a $APP_NAME
heroku config:set DEBUG="False" -a $APP_NAME

# Check if we need to set any other environment variables from .env file
if [ -f .env ]; then
  echo "Setting environment variables from .env file..."
  while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue

    # Extract variable name and value
    key=$(echo "$line" | cut -d '=' -f 1)
    value=$(echo "$line" | cut -d '=' -f 2-)

    # Skip DATABASE_URL and REDIS_URL as they are provided by Heroku
    [[ "$key" == "DATABASE_URL" || "$key" == "REDIS_URL" || "$key" == "CELERY_BROKER_URL" || "$key" == "CELERY_RESULT_BACKEND" ]] && continue

    # Set the variable
    heroku config:set "$key=$value" -a $APP_NAME
  done < .env
fi

echo "Heroku app $APP_NAME is ready for deployment!"
echo "To deploy, run: git push heroku main"
