import json
import boto3
import logging
from api.db.task import Task, TaskDb
from dataclasses import dataclass, asdict
from typing import Any, Dict, NewType
from botocore.exceptions import ClientError

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

def send(event: Event, context: Any) -> Response:
    data = json.loads(event['body'])

    sender = f"{data['sender']['name']} <{data['sender']['email']}>"
    recipient = data['recipient']
    aws_region = "us-east-1"
    subject = "Amazon SES Test (SDK for Python)"
    body_text = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                )
                
    body_html = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """            

    charset = "UTF-8"
    client = boto3.client('ses',region_name=aws_region)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])

    response = Response({
        "statusCode": 200,
        "body": "email sent"
    })

    return response


def createDb(event: Event) -> TaskDb:
    return TaskDb('IS_OFFLINE' in event)
