#!/bin/bash
# Start a PostgreSQL container with default credentials and database

# Load environment variables from .env
set -a
source .env
set +a


# Check if the container exists
if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "Container $CONTAINER_NAME already exists. Starting it..."
  docker start $CONTAINER_NAME
else
  echo "Creating and starting new container $CONTAINER_NAME..."
  docker run --name $CONTAINER_NAME \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e POSTGRES_DB=$POSTGRES_DB \
    -p $POSTGRES_PORT:5432 \
    -d postgres
fi

export DATABASE_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:$POSTGRES_PORT/$POSTGRES_DB"
echo "Postgres is running in Docker!"
echo "DATABASE_URL set to: $DATABASE_URL"

# Wait for Postgres to be ready
until docker exec $CONTAINER_NAME pg_isready -U $POSTGRES_USER; do
  echo "Waiting for Postgres to be ready..."
  sleep 1
done

# Run Diesel migrations
diesel migration run


echo "Migrations applied!"

# Start the Rust server
echo "Starting Rust server..."
cargo run
