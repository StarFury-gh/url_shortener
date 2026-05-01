FROM redis:8.6

EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD [ "redis-cli ping | grep PONG || exit 1" ]