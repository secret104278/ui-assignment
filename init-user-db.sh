#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ui_test;
    CREATE DATABASE ui_test;
    GRANT ALL PRIVILEGES ON DATABASE ui_test TO ui_test;
EOSQL
