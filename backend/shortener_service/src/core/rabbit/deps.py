from fastapi import Request, Depends
from .publisher import RabbitPublisher


def get_rmq_broker(req: Request):
    return req.app.state.rabbit


def get_publisher(broker=Depends(get_rmq_broker)) -> RabbitPublisher:
    return RabbitPublisher(broker)
