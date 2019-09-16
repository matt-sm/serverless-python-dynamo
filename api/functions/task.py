import json
import boto3
import logging
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

def update(event: Event, context: Any) -> Response:
    data = json.loads(event['body'])
    if 'status' not in data:
        logging.error("Missing request body field: status")
        raise Exception("Task update failed.")
        return

    db = createDb(event)
    task = db.update(event['pathParameters']['id'], data['status'])

    response = Response({
        "statusCode": 200,
        "body": json.dumps(asdict(task))
    })

    return response

def createDb(event: Event) -> TaskDb:
    return TaskDb('IS_OFFLINE' in event)
