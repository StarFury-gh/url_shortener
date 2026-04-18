FROM postgres:14

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=shortener

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/