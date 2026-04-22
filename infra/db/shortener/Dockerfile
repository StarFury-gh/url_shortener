FROM postgres:14

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=shortener

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/

HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=3 \
    CMD pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB} || exit 1