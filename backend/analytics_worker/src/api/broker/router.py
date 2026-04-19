from faststream.rabbit.fastapi import RabbitRouter
from fastapi import Depends

from core.config import cfg_obj

from .dependencies import get_service
from .schemas import ClickInfo, LinkAction
from .service import WorkerService

msg_router = RabbitRouter(cfg_obj.RMQ_DSN)


@msg_router.subscriber("sh_redirect")
async def handle_sh_click(message: dict):
    msg = ClickInfo(**message)
    print(msg)
    return "Got message"


@msg_router.subscriber("links_actions")
async def handle_link_action(
    message: dict, service: WorkerService = Depends(get_service)
):
    msg = LinkAction(**message)
    print(msg)
    await service.handle_link_action(msg)
    return "Got message"
