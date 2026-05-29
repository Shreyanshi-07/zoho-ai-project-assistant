from langchain_core.tools import tool

from app.core.langgraph.tools.helpers import get_current_user
from app.services.zoho_client import ZohoClient


@tool
async def list_projects() -> str:
    """
    Fetch all Zoho Projects for authenticated user.
    """

    user = get_current_user()

    if not user:
        return "User not authenticated"

    client = ZohoClient(
        access_token=user.access_token,
        portal_id=user.portal_id,
    )

    projects = await client.get_projects()

    return str(projects)