import os
import json
import requests


def test_task():
    os.environ["TASK_DYNAMODB_TABLE"] = "serverless-python-dynamo-task-dev"
    response = requests.post("http://localhost:3000/tasks")
    task = json.loads(response.text)["data"]

    response = requests.get(f"http://localhost:3000/tasks/{task['id']}")
    assert response.status_code == 200
    assert task == json.loads(response.text)["data"]

    response = requests.put(
        f"http://localhost:3000/tasks/{task['id']}", data='{"status": "processing"}'
    )

    body = json.loads(response.text)["data"]
    assert response.status_code == 200
    assert body["status"] == "processing"
    assert body["createdAt"] != body["updatedAt"]
