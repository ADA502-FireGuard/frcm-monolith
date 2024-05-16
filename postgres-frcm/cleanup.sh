#!/bin/bash

# Env var for non-interactive login
export PGPASSWORD=password

# Connect to the PostgreSQL database and execute the cleanup SQL query
psql -h postgres-frcm_postgres_1 -U admin -d fireriskdb -c "DELETE FROM fireriskdata WHERE CURRENT_TIMESTAMP >= ExpirationDate;"