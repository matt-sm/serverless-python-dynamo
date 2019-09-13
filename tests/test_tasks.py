import os
import json
from api.functions.task import create, get

def test_add_task():
    os.environ['TASK_DYNAMODB_TABLE'] = 'serverless-python-dynamo-task-dev'
    event = {'IS_OFFLINE': True}
    response = create(event, None)
    assert response['statusCode'] == 200

    body = json.loads(response['body'])
    assert body['status'] == 'created'
    assert body['createdAt'] == body['updatedAt']    

def test_get_task():
    os.environ['TASK_DYNAMODB_TABLE'] = 'serverless-python-dynamo-task-dev'
    event = {'IS_OFFLINE': True}
    response = create(event, None)
    task = json.loads(response['body'])

    event = {'IS_OFFLINE': True, 'pathParameters' : {'id': task['id']}}
    response = get(event, None)
    assert response['statusCode'] == 200
    assert task == json.loads(response['body'])
