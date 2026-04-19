from faststream.rabbit.fastapi import RabbitRouter

from core.config import cfg_obj

msg_router = RabbitRouter(cfg_obj.RMQ_DSN)

@msg_router.subscriber("sh_click")
async def handle_sh_click(message: dict):
    
