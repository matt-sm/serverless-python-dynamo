from api.decorators import http_handler
from api.models import Request, Task, TaskCreateRequest, TaskUpdateRequest
from api.services.task_repository import task_repository


@http_handler
def create(request: Request) -> Task:
    task_request = TaskCreateRequest(**request.body)
    return task_repository.create(task_request.data)


@http_handler
def get(request: Request) -> Task:
    return task_repository.get(request.params["id"])


@http_handler
def update(request: Request) -> Task:
    task_request = TaskUpdateRequest(**request.body)
    return task_repository.update(request.params["id"], task_request.status)
