#!/bin/bash
set -e

UITEST_USER="ui_test"
UITEST_DB="ui_test"

psql -v ON_ERROR_STOP=1 --username "$UITEST_USER" --dbname "$UITEST_DB" <<-EOSQL
    CREATE TABLE users (
        acct varchar(255) NOT NULL,
        pwd varchar(255) NOT NULL,
        fullname varchar(255) NOT NULL,
        created_at timestamp,
        updated_at timestamp,
        PRIMARY KEY (acct)
    );
EOSQL