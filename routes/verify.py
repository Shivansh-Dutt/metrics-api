from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

from constants import (
    PUBLIC_KEY,
    ISSUER,
    AUDIENCE,
)

router = APIRouter()


class TokenRequest(BaseModel):
    token: str


@router.post("/verify")
def verify(request: TokenRequest):

    try:

        payload = jwt.decode(
            request.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
        )

        return {
            "valid": True,
            "email": payload["email"],
            "sub": payload["sub"],
            "aud": payload["aud"],
        }

    except jwt.InvalidTokenError:

        return JSONResponse(
            status_code=401,
            content={"valid": False},
        )