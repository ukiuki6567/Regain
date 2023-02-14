FROM mariadb:latest

COPY ./init.sql /docker-entrypoint-initdb.d/

VOLUME [ "/var/lib/mysql" ]