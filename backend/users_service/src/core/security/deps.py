from fastapi import Header, HTTPException, status


async def require_admin(authorization=Header(...)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin required"
        )
