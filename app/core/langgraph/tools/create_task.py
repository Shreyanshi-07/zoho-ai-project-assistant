from langchain_core.tools import tool
import json
from app.core.langgraph.tools.helpers import get_current_user
from app.services.zoho_client import ZohoClient
from app.core.langgraph.tools.ask_human import ask_human

@tool
async def create_task(project_name: str, task_name: str) -> str:
    """
    Create a new task in a Zoho project.

    Use this whenever the user asks:
    - create task
    - add task
    - make task
    - new task

    Inputs:
    - exact project name
    - task name
    """

    user = get_current_user()

    if not user:
        return "User not authenticated"

    client = ZohoClient(
        access_token=user.access_token,
        portal_id=user.portal_id,
    )
    
    projects_data = await client.get_projects()

    projects = projects_data.get("projects", [])

    matching_project = None

    for project in projects:

        if project["name"].lower() == project_name.lower():
            matching_project = project
            break

    if not matching_project:
        return f"Project '{project_name}' not found"

    project_id = matching_project["id_string"]
    confirmation = ask_human.invoke(
        {
            "question": f"""
    Please confirm task creation.

    Project: {project_name}
    Task: {task_name}

    Reply YES to continue.
    Reply NO or CANCEL to abort.
    """
        }
    )
    tasklists = await client.get_tasklists(project_id)

    confirmation = confirmation.strip().upper()

    if confirmation in ["NO", "CANCEL"]:
        return "Task creation cancelled by user."

    if confirmation != "YES":
        return "Invalid response. Task creation cancelled."
    response = await client.create_task(
        project_id=project_id,
        task_name=task_name,
    )

    print("CREATE TASK RESPONSE")
    print(response)
    
    return json.dumps({
        "success": True,
        "project_name": project_name,
        "task_name": task_name,
        "zoho_response": response,
        "message": "Task created successfully"
    })