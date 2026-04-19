from faststream.rabbit import RabbitBroker

from core.config import cfg_obj


async def create_rmq_connection():
    broker = RabbitBroker(cfg_obj.RMQ_DSN)
    return broker
