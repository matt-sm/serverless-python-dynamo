import json
import boto3
from api.db.task import Task, TaskDb
from dataclasses import asdict

def create(event, context):
    db = TaskDb(event)
    task = db.create()

    response = {
        "statusCode": 200,
        "body": json.dumps(asdict(task))
    }

    return response

def get(event, context):
    db = TaskDb(event)
    task = db.get(event['pathParameters']['id'])

    response = {
        "statusCode": 200,
        "body": json.dumps(asdict(task))
    }

    return response
