FROM postgres:alpine3.17

COPY init_db.sql /docker-entrypoint-initdb.d/
