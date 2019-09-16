import os
import boto3
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from dacite import from_dict

@dataclass
class Task:
     id: str = str(uuid.uuid1())
     status: str = 'created'
     createdAt: str = str(datetime.utcnow().timestamp())
     updatedAt: str = ''

     def __post_init__(self):
        if self.updatedAt == '':
            self.updatedAt = self.createdAt


class TaskDb(object):
    def __init__(self, isOffline: bool):
        if isOffline:
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000/')
        else:
            dynamodb = boto3.resource('dynamodb')

        self.table = dynamodb.Table(os.environ['TASK_DYNAMODB_TABLE'])
    
    def create(self) -> Task:
        task = Task()
        self.table.put_item(Item=asdict(task))
        return task

    def get(self, id: int) -> Task:
        result = self.table.get_item(
            Key={
                'id': id
            }
        )

        return from_dict(data_class=Task, data=result['Item'])
