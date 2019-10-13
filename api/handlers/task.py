from api.decorators import http_handler
from api.models import Request, Response, Task, TaskCreateRequest, TaskUpdateRequest
from api.services.task_repository import task_repository


@http_handler
def create(request: Request) -> Response[Task]:
    task_request = TaskCreateRequest(**request.body)
    task = task_repository.create(task_request.data)
    return Response[Task](data=task, status_code=201)


@http_handler
def get(request: Request) -> Response[Task]:
    task = task_repository.get(request.params["id"])
    if task is None:
        return Response[Task](status_code=404)

    return Response[Task](data=task, status_code=200)


@http_handler
def update(request: Request) -> Response[Task]:
    task_request = TaskUpdateRequest(**request.body)
    task = task_repository.update(request.params["id"], task_request.status)
    if task is None:
        return Response[Task](status_code=404)

    return Response[Task](data=task, status_code=200)
