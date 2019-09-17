import json
import boto3
import logging
from api.db.task import Task, TaskDb
from typing import Any, Dict, NewType
from botocore.exceptions import ClientError
from api.functions import Event
from pydantic import BaseModel, ValidationError
import functools


class Response(BaseModel):
    statusCode: int = 200
    body: str


class BadRequest(BaseModel):
    statusCode: int = 400
    body: str


class InternalError(BaseModel):
    statusCode: int = 500
    body: str


class EmailSender(BaseModel):
    name: str
    email: str


class EmailRequest(BaseModel):
    sender: EmailSender
    recipient: str
    text: str
    subject: str


def api(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value.dict()

    return wrapper_decorator


@api
def send(event: Event, context: Any) -> Response:
    data = json.loads(event["body"])

    try:
        request = EmailRequest(**data)
    except ValidationError as e:
        return BadRequest(body=e.json())

    sender = f"{request.sender.name} <{request.sender.email}>"

    charset = "UTF-8"
    client = boto3.client("ses", region_name="us-east-1")

    try:
        response = client.send_email(
            Destination={"ToAddresses": [request.recipient]},
            Message={
                "Body": {"Text": {"Charset": charset, "Data": request.text}},
                "Subject": {"Charset": charset, "Data": request.subject},
            },
            Source=sender,
        )
    except ClientError as e:
        return InternalError(body=json.dumps({"error": e.response["Error"]["Message"]}))

    return Response(body=json.dumps({"message": "email sent"}))
