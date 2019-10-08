import os
from pydantic import BaseModel
from api.functions import Request, http_handler
from api.db.task import Task, TaskDb


class TaskRequest(BaseModel):
    status: str


DB = TaskDb(os.environ["IS_OFFLINE"])


@http_handler
def create(request: Request) -> Task:
    return DB.create()


@http_handler
def get(request: Request) -> Task:
    return DB.get(request.params["id"])


@http_handler
def update(request: Request) -> Task:
    task_request = TaskRequest(**request.body)

    return DB.update(request.params["id"], task_request.status)
