from fastapi import Depends


async def get_service(repo=Depends(get_repo)):
    pass


async def get_repo():
    pass
