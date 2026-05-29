from langchain_core.tools import tool

from app.core.langgraph.tools.helpers import get_current_user
from app.services.zoho_client import ZohoClient
import json

@tool
async def get_project_tasks(project_name: str) -> str:
    """
    Use this tool whenever the user asks:
    - show tasks
    - list tasks
    - project tasks
    - open tasks

    Input should be the EXACT Zoho project name.

    Example:
    TEST PROJECT
    """

    print("GET PROJECT TASKS TOOL EXECUTED")

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

    tasks = await client.get_tasks(project_id)
    print("RAW TASK RESPONSE:")
    print(tasks)

    task_list = tasks.get("response", {}).get("tasks", [])

    formatted_tasks = []

    if not task_list:
        return "No tasks found."

    for task in task_list:

        formatted_tasks.append({
            "name": task.get("name"),
            "status": task.get("status", {}).get("name"),
            "completed": task.get("completed"),
            "task_key": task.get("key"),
        })

    return json.dumps(formatted_tasks)