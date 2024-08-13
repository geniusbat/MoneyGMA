
#!/usr/bin/bash

#Remember to run as root and using "source <shell_script.sh>"

echo "Setting environment variables"
export MGMA_KEY="<value>"
export MGMA_DEBUG="<value>"
export MGMA_DB="<value>"
export MGMA_USER="<value>"
export MGMA_PASS="<value>"

echo "Creating db"
if [ "$MGMA_USER" != "postgres" ]
then
        echo "Creating user $MGMA_USER"
        psql -U postgres -c "CREATE USER $MGMA_USER WITH PASSWORD '$MGMA_PASS'"
fi
su postgres -c "createdb $MGMA_DB --owner $MGMA_USER"

echo "Run makemigrations and/or migrate"
