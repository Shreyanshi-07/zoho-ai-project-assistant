from langchain_core.tools import tool

from app.core.langgraph.tools.helpers import get_current_user
from app.services.zoho_client import ZohoClient


@tool
async def create_project(project_name: str) -> str:
    """
    Create a new Zoho project.

    Use this whenever the user asks:
    - create project
    - new project
    - add project
    """

    user = get_current_user()

    if not user:
        return "User not authenticated"

    client = ZohoClient(
        access_token=user.access_token,
        portal_id=user.portal_id,
    )

    response = await client.create_project(
        project_name=project_name,
    )

    return f"Project '{project_name}' created successfully."