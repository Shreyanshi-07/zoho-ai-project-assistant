from langchain_core.tools.base import BaseTool
from app.core.langgraph.tools.create_task import create_task
from .duckduckgo_search import duckduckgo_search_tool
from .list_projects import list_projects
from .list_tasks import get_project_tasks
from .create_project import create_project
from app.core.langgraph.tools.update_task_status import update_task_status
tools = [
    duckduckgo_search_tool,
    list_projects,
    get_project_tasks,
    create_task,
    create_project,
    update_task_status,
]