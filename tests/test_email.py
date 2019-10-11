import os
import json
import requests
from tests import conf  # pylint: disable=unused-import
from api.handlers.email import process
from api.services.queue import receive_messages


def test_email():

    response = requests.post(
        "http://localhost:3000/email/send",
        data='{"sender": {"name": "test", "email": "'
        + os.environ["TEST_EMAIL"]
        + '"}, "recipient": "success@simulator.amazonses.com", "text": "email text", "subject": "test subject"}',  # pylint: disable=line-too-long
    )

    body = json.loads(response.text)["data"]
    assert response.status_code == 202
    assert body["status"] == "created"
    task_id = body["id"]

    # check the task was queued
    messages = receive_messages()
    assert task_id == messages["Records"][0]["body"]

    # simulate lambda being triggered from sqs
    process(messages, None)

    response = requests.get(f"http://localhost:3000/tasks/{task_id}")
    assert response.status_code == 200
    assert json.loads(response.text)["data"]["status"] == "completed"
