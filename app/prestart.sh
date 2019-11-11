#! /usr/bin/env bash

echo "This is knope prestart!"

# I'm sure there's a better way to do this.. I've just tried a lot
# of them and can't find one. Very open to suggestions!
if [ -z "$PORT" ]
then
  echo "PORT is unset"
else
  echo "Copying PORT env ${PORT} to LISTEN_PORT"
  echo "LISTEN_PORT=${PORT}" | cat - /entrypoint.sh > temp && mv temp /entrypoint.sh 
fi
chmod +x /entrypoint.sh
/entrypoint.sh

echo "End of knope prestart!"