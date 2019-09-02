import json
import logging
import os
import time
import uuid
from datetime import datetime

import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    timestamp = str(datetime.utcnow().timestamp())

    table = dynamodb.Table(os.environ['TASK_DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'status': None,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
