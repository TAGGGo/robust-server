#!/bin/sh
# wait-for-postgres.sh

set -e
  
host="$1"
shift
if [ "$( PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname='postgres'" )" = '1' ]
then
    echo "Database already exists"
else
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "postgres" -f db.sql
    echo "Database does not exist, creating data right now..."
fi  
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done


>&2 echo "Postgres is up - finished data creation"

if [ "$AMAZON_SERVER_SWITCH" = "on" ]
then
    echo "Amazon server switch is true, creating data right now..."
    python /code/amazon_server/server.py &
fi

exec "$@"