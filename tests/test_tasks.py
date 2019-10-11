import json
import requests


def test_task():
    response = requests.post("http://localhost:3000/tasks", data='{"data": {"foo": "bar"}}')
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
    assert body["created_at"] != body["updated_at"]
