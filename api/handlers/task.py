from pydantic import BaseModel
from api.request import Request, http_handler
from api.services.task import Task, taskdb


class TaskRequest(BaseModel):
    status: str


@http_handler
def create(request: Request) -> Task:  # pylint: disable=unused-argument
    return taskdb.create()


@http_handler
def get(request: Request) -> Task:
    return taskdb.get(request.params["id"])


@http_handler
def update(request: Request) -> Task:
    task_request = TaskRequest(**request.body)
    return taskdb.update(request.params["id"], task_request.status)
