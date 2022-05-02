#!/bin/bash

echo "run migrate in background"
/bin/bash /code/web/update-db.sh &
exec "$@"
