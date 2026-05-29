from langchain_core.tools import tool
from app.services.zoho_client import ZohoClient

@tool
async def delete_task(user_id: str) -> str:
    """delete_task tool"""

    client = ZohoClient(user_id)

    return str({"tool": "delete_task"})
