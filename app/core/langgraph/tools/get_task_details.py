from langchain_core.tools import tool
from app.services.zoho_client import ZohoClient

@tool
async def get_task_details(user_id: str) -> str:
    """get_task_details tool"""

    client = ZohoClient(user_id)

    return str({"tool": "get_task_details"})
