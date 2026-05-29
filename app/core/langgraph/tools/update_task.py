from langchain_core.tools import tool
from app.services.zoho_client import ZohoClient

@tool
async def update_task(user_id: str) -> str:
    """update_task tool"""

    client = ZohoClient(user_id)

    return str({"tool": "update_task"})
