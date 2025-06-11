#!/bin/bash

# Set the APP_NAME if not already set
if [ -z "$APP_NAME" ]; then
  APP_NAME="grocery-api-service"
fi

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

# Set essential environment variables
echo "Setting essential environment variables..."
heroku config:set SECRET_KEY="$(openssl rand -hex 32)" -a $APP_NAME
heroku config:set ALLOWED_HOSTS="$APP_NAME.herokuapp.com,localhost,127.0.0.1" -a $APP_NAME
heroku config:set DEBUG="False" -a $APP_NAME

# Set critical API environment variables with default values if they don't exist
echo "Setting critical API environment variables..."
heroku config:set AFRICAS_TALKING_ENVIRONMENT="sandbox" -a $APP_NAME
heroku config:set AFRICAS_TALKING_USERNAME="sandbox" -a $APP_NAME
heroku config:set AFRICAS_TALKING_API_KEY="${AFRICAS_TALKING_API_KEY:-dummy-key-for-heroku}" -a $APP_NAME

# Set other required environment variables
echo "Setting other required environment variables..."
heroku config:set DJANGO_SETTINGS_MODULE="grocery_api.settings" -a $APP_NAME
heroku config:set PYTHONPATH="/app/src" -a $APP_NAME

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

# Display all config variables for verification
echo "Current Heroku config variables:"
heroku config -a $APP_NAME

# Scale dynos properly
echo "Scaling dynos..."
heroku ps:scale web=1 worker=1 -a $APP_NAME

echo "Heroku app $APP_NAME is ready for deployment!"
echo "To deploy, run: git push heroku main"
