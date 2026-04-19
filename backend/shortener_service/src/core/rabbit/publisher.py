from faststream.rabbit import RabbitBroker
from .schemas import RedirectRequestInfo


class RabbitPublisher:
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def publish(self, message: dict, queue: str) -> None:
        async with self._broker as broker:
            await broker.publish(message, queue)

    async def handle_redirect(self, info: RedirectRequestInfo) -> None:
        await self.publish(
            {"ip": info.ip, "slug": info.slug, "agent": info.agent},
            queue="sh_redirect",
        )
