import os
import json
import requests


def test_task():
    response = requests.post(
        "http://localhost:3000/email/send",
        data='{"sender": {"name": "test", "email": "'
        + os.environ["TEST_EMAIL"]
        + '"}, "recipient": "success@simulator.amazonses.com", "text": "email text", "subject": "test subject"}',
    )

    body = json.loads(response.text)["data"]
    assert response.status_code == 200
    assert "messageId" in body
