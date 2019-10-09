from api.services.task_repository import task_repository
from api.services.emailer import send_email
from api.services.models import EmailRequest


def hello(event, context):
    print(event)
    for record in event["Records"]:
        task = task_repository.update(record["body"], "processing")
        send_email(EmailRequest(**task.data))
        task_repository.update(task.id, "completed")
