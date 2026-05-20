FROM redis:8.6

# настройки пользователей
COPY redis-users.acl /usr/local/etc/redis/redis-users.acl

# конфиг
COPY redis.conf /usr/local/etc/redis/redis.conf

# директории для данных
RUN mkdir -p /data && chown redis:redis /data

EXPOSE 6379

# запуск
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
CMD [ "redis-cli ping | grep PONG || exit 1" ]

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]