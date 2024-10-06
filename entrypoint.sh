#!/bin/bash

# Enable command printing for debugging
set -x

# Log file
LOGFILE=/var/log/entrypoint.log



echo 'Going to wait for flask until mariadb to start'



# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOGFILE
}



# Start logging
log "Starting entrypoint script"

pwd


# Wait for MariaDB to be ready
log "Waiting for MariaDB to be ready..."
timeout=60
while ! mysqladmin ping -h "db" -u "root" --silent && [ $timeout -gt 0 ]; do
    log "MariaDB is unavailable - sleeping"
    sleep 1
    timeout=$((timeout-1))
done


if [ $timeout -le 0 ]; then
    log "ERROR: MariaDB did not become available in time"
else
    log "MariaDB is up - executing command"

       # Execute SQL commands to set up the database and user
    log "Setting up the database and user..."
 # Fixed version:
mysql -h "db" -u "root" -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    CREATE DATABASE IF NOT EXISTS mydbc;
    USE mydbc;
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT
    );
    CREATE USER IF NOT EXISTS 'proteus'@'%' IDENTIFIED BY 'proteus';
    GRANT ALL PRIVILEGES ON mydbc.* TO 'proteus'@'%';
    FLUSH PRIVILEGES;
EOSQL
log "Database and user are set up"
fi


python3 app.py


# log "Entrypoint script completed"
log "Entrypoint script completed"


# Keep the container running
log "Keeping container alive"
tail -f /dev/null & # Run in background
wait $! # Wait for background process
