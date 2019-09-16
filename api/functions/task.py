import json
import boto3
from api.db.task import Task, TaskDb
from dataclasses import dataclass, asdict
from typing import Any, Dict, NewType

Response = NewType('Response', Dict[str, Any])
Event = NewType('Event', dict)

def create(event: Event, context: Any) -> Response:
    db = createDb(event)
    task = db.create()

    response = Response({
        "statusCode": 200,
        "body": json.dumps(asdict(task))
    })

    return response

def get(event: Event, context: Any) -> Response:
    db = createDb(event)
    task = db.get(event['pathParameters']['id'])

    response = Response({
        "statusCode": 200,
        "body": json.dumps(asdict(task))
    })

    return response

def createDb(event: Event) -> TaskDb:
    return TaskDb('IS_OFFLINE' in event)
