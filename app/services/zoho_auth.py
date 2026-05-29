import httpx
from app.core.config import settings
from urllib.parse import urlencode
from app.core.config import settings

class ZohoAuthService:

    @staticmethod
    def get_authorization_url() -> str:
        scopes = ",".join([
            "ZohoProjects.portals.READ",

            "ZohoProjects.projects.ALL",

            "ZohoProjects.tasks.ALL",

            "ZohoProjects.users.READ",
        ])

        params = {
            "response_type": "code",
            "client_id": settings.ZOHO_CLIENT_ID,
            "scope": scopes,
            "redirect_uri": settings.ZOHO_REDIRECT_URI,
            "access_type": "offline",
            "prompt": "consent",
        }
        return (
            "https://accounts.zoho.in/oauth/v2/auth?"
            + urlencode(params)
        )
    @staticmethod
    async def exchange_code_for_tokens(code: str):
        url = "https://accounts.zoho.in/oauth/v2/token"

        params = {
            "grant_type": "authorization_code",
            "client_id": settings.ZOHO_CLIENT_ID,
            "client_secret": settings.ZOHO_CLIENT_SECRET,
            "redirect_uri": settings.ZOHO_REDIRECT_URI,
            "code": code,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params)

        return response.json()
