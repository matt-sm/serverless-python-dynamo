from pydantic import BaseModel
from api.functions import Request, api
from api.db.task import Task


class TaskRequest(BaseModel):
    status: str


@api
def create(request: Request) -> Task:
    return request.db.create()


@api
def get(request: Request) -> Task:
    return request.db.get(request.params["id"])


@api
def update(request: Request) -> Task:
    task_request = TaskRequest(**request.body)

    return request.db.update(request.params["id"], task_request.status)
