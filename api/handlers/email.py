import os
import boto3
from api.request import Request, http_handler
from api.services.models import Task, EmailRequest
from api.services.task_repository import task_repository


@http_handler
def send(request: Request) -> Task:
    email_request = EmailRequest(**request.body)
    task = task_repository.create(email_request.dict())
    sqs = boto3.resource("sqs")

    queue = sqs.get_queue_by_name(QueueName=os.environ["TASK_QUEUE"])

    response = queue.send_message(MessageBody=task.id)
    print(response.get("MessageId"))
    return task
