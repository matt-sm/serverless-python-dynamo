import os
import boto3


def queue_message(message: str):
    if "IS_OFFLINE" in os.environ:
        sqs = boto3.resource("sqs", endpoint_url="http://localhost:4100/")
    else:
        sqs = boto3.resource("sqs")

    queue = sqs.get_queue_by_name(QueueName=os.environ["TASK_QUEUE"])  # pylint: disable=no-member

    queue.send_message(MessageBody=message)


def receive_messages() -> dict:
    if "IS_OFFLINE" in os.environ:
        sqs = boto3.resource("sqs", endpoint_url="http://localhost:4100/")
    else:
        sqs = boto3.resource("sqs")

    queue = sqs.get_queue_by_name(QueueName=os.environ["TASK_QUEUE"])  # pylint: disable=no-member

    messages = []
    for message in queue.receive_messages():
        messages.append({"body": message.body})
        message.delete()

    return {"Records": messages}
