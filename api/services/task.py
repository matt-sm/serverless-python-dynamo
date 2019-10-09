import os
import uuid
from datetime import datetime
import boto3
from pydantic import BaseModel


class Task(BaseModel):
    id: str = str(uuid.uuid1())
    status: str = "created"
    created_at: str = str(datetime.utcnow().timestamp())
    updated_at: str = ""


class TaskDb:
    def __init__(self):
        if os.environ["IS_OFFLINE"]:
            dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000/")
        else:
            dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.Table(os.environ["TASK_DYNAMODB_TABLE"])

    def create(self) -> Task:
        task = Task()
        task.updated_at = task.created_at
        self.table.put_item(Item=task.dict())
        return task

    def get(self, id_: int) -> Task:
        result = self.table.get_item(Key={"id": id_})
        return Task(**result["Item"])

    def update(self, id_: int, status: str) -> Task:
        timestamp = str(datetime.utcnow().timestamp())

        result = self.table.update_item(
            Key={"id": id_},
            ExpressionAttributeNames={"#task_status": "status"},
            ExpressionAttributeValues={":status": status, ":updated_at": timestamp},
            UpdateExpression="SET #task_status = :status, " "updated_at = :updated_at",
            ReturnValues="ALL_NEW",
        )
        return Task(**result["Attributes"])


taskdb = TaskDb()  # pylint: disable=invalid-name
