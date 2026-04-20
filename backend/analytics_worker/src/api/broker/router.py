from faststream.rabbit.fastapi import RabbitRouter
from fastapi import Depends

from logging import Logger

from core.logging import get_logger

from core.config import cfg_obj

from .dependencies import get_service
from .schemas import ClickInfo, LinkAction
from .service import WorkerService

msg_router = RabbitRouter(cfg_obj.RMQ_DSN)


@msg_router.subscriber("sh_redirect")
async def handle_sh_click(
    message: dict,
    service: WorkerService = Depends(get_service),
    logger: Logger = Depends(get_logger),
):
    msg = ClickInfo(**message)
    await service.handle_link_redirect(msg)
    logger.info(f"Redirected by shortified link with slug: {msg.slug}")
    return


@msg_router.subscriber("links_actions")
async def handle_link_action(
    message: dict,
    service: WorkerService = Depends(get_service),
    logger: Logger = Depends(get_logger),
):
    msg = LinkAction(**message)
    await service.handle_link_operation(msg)
    logger.info(f"Handled operation '{msg.operation}' with slug: '{msg.slug}'")
    return
