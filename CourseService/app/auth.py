import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from decouple import config
from .config.logger import logger

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(credentials=Depends(security)):
    token = credentials.credentials
    logger.info(f" Received token: {token}")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        id = payload.get("id")
        role = payload.get("role")

        logger.info(f" Decoded JWT payload: id={id}, role={role}")

        if not id or not role:
            logger.warning("Missing id or role in JWT payload.")
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        return {"id": id, "role": role}

    except jwt.ExpiredSignatureError:
        logger.error(" JWT token has expired.")
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        logger.error("  Invalid JWT token.")
        raise HTTPException(status_code=401, detail="Invalid token")
