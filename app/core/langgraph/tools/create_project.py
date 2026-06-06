from langchain_core.tools import tool
from app.core.langgraph.tools.helpers import get_current_user
from app.services.zoho_client import ZohoClient
from app.core.langgraph.tools.ask_human import ask_human
import json


@tool
async def create_project(project_name: str) -> str:
    """
    Create a new Zoho Project.

    Use when user asks:
    - create project
    - add project
    - new project
    """

    user = get_current_user()

    if not user:
        return "User not authenticated"

    confirmation = ask_human.invoke(
        {
            "question": f"""
Please confirm project creation.

Project: {project_name}

Reply YES to continue.
Reply NO or CANCEL to abort.
"""
        }
    )

    confirmation = confirmation.strip().upper()

    if confirmation in ["NO", "CANCEL"]:
        return "Project creation cancelled by user."

    if confirmation != "YES":
        return "Invalid response. Project creation cancelled."

    client = ZohoClient(
        access_token=user.access_token,
        portal_id=user.portal_id,
    )

    response = await client.create_project(
        project_name=project_name
    )

    return json.dumps({
        "success": True,
        "project_name": project_name,
        "zoho_response": response,
        "message": "Project created successfully"
    })