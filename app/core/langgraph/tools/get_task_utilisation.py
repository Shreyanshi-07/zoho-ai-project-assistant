from langchain_core.tools import tool
from app.services.zoho_client import ZohoClient

@tool
async def get_task_utilisation(user_id: str) -> str:
    """get_task_utilisation tool"""

    client = ZohoClient(user_id)

    return str({"tool": "get_task_utilisation"})
