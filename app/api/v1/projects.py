from fastapi import APIRouter, Request

from app.services.zoho_client import ZohoClient

router = APIRouter()


@router.get("/projects")
async def get_projects(request: Request):

    access_token = request.session.get("access_token")
    portal_id = request.session.get("portal_id")

    if not access_token:
        return {"projects": []}

    client = ZohoClient(
        access_token=access_token,
        portal_id=portal_id,
    )

    projects_data = await client.get_projects()

    return projects_data