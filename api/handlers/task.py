from pydantic import BaseModel
from api.request import Request, http_handler
from api.services.task_repository import Task, task_repository


class TaskRequest(BaseModel):
    status: str


@http_handler
def create(request: Request) -> Task:  # pylint: disable=unused-argument
    data = {"test": "data"}
    return task_repository.create(data)


@http_handler
def get(request: Request) -> Task:
    return task_repository.get(request.params["id"])


@http_handler
def update(request: Request) -> Task:
    task_request = TaskRequest(**request.body)
    return task_repository.update(request.params["id"], task_request.status)
