from langchain_core.tools import tool
import json
from app.core.langgraph.tools.helpers import get_current_user
from app.services.zoho_client import ZohoClient


@tool
async def update_task_status(
    project_name: str,
    task_name: str,
    status: str,
) -> str:
    """
    Update status of a task in a Zoho project.

    Use this whenever the user asks:
    - complete task
    - close task
    - reopen task
    - mark task done
    - change task status

    Inputs:
    - exact project name
    - exact task name
    - status
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

    tasks_response = await client.get_tasks(project_id)

    task_list = tasks_response.get(
        "response",
        {}
    ).get("tasks", [])
    print("ALL TASKS")
    print(json.dumps(task_list, indent=2))
    matching_task = None

    for task in task_list:

        if task["name"].lower() == task_name.lower():
            matching_task = task
            print("MATCH FOUND")
            print("Task ID:", task["id_string"])
            print("Task Name:", task["name"])
            print("Current Status:", task["status"]["name"])

            break

    if not matching_task:
        return f"Task '{task_name}' not found"
    print("MATCHING TASK")
    print(json.dumps(matching_task, indent=2))
    task_id = matching_task["id_string"]
    STATUS_IDS = {
        "Open": "456611000000000185",
        "In Progress": "456611000000013001",
        "Closed": "456611000000000188",
    }
    status_id = STATUS_IDS.get(status)
    if not status_id:
        return f"Unknown status '{status}'"
    result = await client.update_task_status(
        project_id=project_id,
        task_id=task_id,
        status=status_id,
    )

    print("UPDATE RESULT")

    print(result)

    actual_status = (
        result["taskUpdateResponse"]
        ["TASK_ARRAY"][0]
        ["CUSTOM_STATUSNAME"]
    )

    return json.dumps({
        "success": actual_status.lower() == status.lower(),
        "expected": status,
        "actual": actual_status
    })
    