import os
import json
import requests
import boto3

NAME = "serverless-python-dynamo-task-dev"


def test_email():
    os.environ["IS_OFFLINE"] = "True"
    os.environ["TASK_DYNAMODB_TABLE"] = NAME
    os.environ["AWS_DEFAULT_PROFILE"] = "serverless"

    response = requests.post(
        "http://localhost:3000/email/send",
        data='{"sender": {"name": "test", "email": "'
        + os.environ["TEST_EMAIL"]
        + '"}, "recipient": "success@simulator.amazonses.com", "text": "email text", "subject": "test subject"}',  # pylint: disable=line-too-long
    )

    body = json.loads(response.text)["data"]
    assert response.status_code == 200
    assert body["status"] == "created"
    task_id = body["id"]

    sqs = boto3.resource("sqs", endpoint_url="http://localhost:4100/")
    queue = sqs.get_queue_by_name(QueueName=NAME)  # pylint: disable=no-member

    messages = []
    for message in queue.receive_messages():
        messages.append({"body": message.body})
        message.delete()

    # check the task was queued
    assert task_id == messages[0]["body"]

    from api.handlers.email import process

    # simulate lambda being triggered from sqs
    process({"Records": messages}, None)

    response = requests.get(f"http://localhost:3000/tasks/{task_id}")
    assert response.status_code == 200
    assert json.loads(response.text)["data"]["status"] == "completed"
