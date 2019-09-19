import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel, ValidationError
from api.functions import Response, Error, api_data


class EmailSender(BaseModel):
    name: str
    email: str


class EmailRequest(BaseModel):
    sender: EmailSender
    recipient: str
    text: str
    subject: str


@api_data
def send(data: dict) -> Response:

    try:
        request = EmailRequest(**data)
    except ValidationError as ex:
        return ex

    sender = f"{request.sender.name} <{request.sender.email}>"

    charset = "UTF-8"
    client = boto3.client("ses", region_name="us-east-1")

    try:
        client.send_email(
            Destination={"ToAddresses": [request.recipient]},
            Message={
                "Body": {"Text": {"Charset": charset, "Data": request.text}},
                "Subject": {"Charset": charset, "Data": request.subject},
            },
            Source=sender,
        )
    except ClientError as ex:
        return Error(code=500, message=ex.response["Error"]["Message"])

    return Response[str](data="email sent")
