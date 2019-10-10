import os
import boto3


def queue_message(message: str):
    sqs = boto3.resource("sqs")

    queue = sqs.get_queue_by_name(QueueName=os.environ["TASK_QUEUE"])  # pylint: disable=no-member

    response = queue.send_message(MessageBody=message)
    print(response.get("MessageId"))
