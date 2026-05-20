# from .deps import get_redis
from .decorators import use_cache
from .client import get_redis, close_redis, init_redis

__all__ = ["get_redis", "use_cache", "close_redis", "init_redis"]
