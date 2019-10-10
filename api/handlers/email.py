from api.request import Request, http_handler
from api.services.models import Task, EmailRequest
from api.services.task_repository import task_repository
from api.services.emailer import send_email
from api.services.queue import queue_message


@http_handler
def send(request: Request) -> Task:
    email_request = EmailRequest(**request.body)
    task = task_repository.create(email_request.dict())
    queue_message(task.id)
    return task


def process(event, context):  # pylint: disable=unused-argument
    print(event)
    for record in event["Records"]:
        task = task_repository.update(record["body"], "processing")
        send_email(EmailRequest(**task.data))
        task_repository.update(task.id, "completed")
