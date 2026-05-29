from langchain_core.tools import tool
from app.services.zoho_client import ZohoClient

@tool
async def list_project_members(user_id: str) -> str:
    """list_project_members tool"""

    client = ZohoClient(user_id)

    return str({"tool": "list_project_members"})
