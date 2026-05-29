import httpx
from datetime import datetime, timedelta

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.models.user_token import UserToken
from app.services.database import engine
from app.services.zoho_auth import ZohoAuthService
from app.services.zoho_client import ZohoClient

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    return RedirectResponse(
        ZohoAuthService.get_authorization_url()
    )


@router.get("/callback")
async def auth_callback(request: Request, code: str):

    tokens = await ZohoAuthService.exchange_code_for_tokens(code)

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in", 3600)

    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    user = UserToken(
        user_id="shreyanshi",
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        portal_id="60072610715",
    )

    with Session(engine) as session:
        session.merge(user)
        session.commit()

    request.session["access_token"] = access_token
    request.session["portal_id"] = "60072610715"
    request.session["user"] = "shreyanshi"

    client = ZohoClient(
        access_token=access_token,
        portal_id="60072610715",
    )

    return RedirectResponse(
        url="http://127.0.0.1:5173",
        status_code=302
    )