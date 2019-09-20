import boto3
from pydantic import BaseModel
from api.functions import Response, Request, api


class EmailSender(BaseModel):
    name: str
    email: str


class EmailRequest(BaseModel):
    sender: EmailSender
    recipient: str
    text: str
    subject: str


@api
def send(request: Request) -> Response:
    request = EmailRequest(**request.body)

    sender = f"{request.sender.name} <{request.sender.email}>"
    charset = "UTF-8"

    client = boto3.client("ses", region_name="us-east-1")

    client.send_email(
        Destination={"ToAddresses": [request.recipient]},
        Message={
            "Body": {"Text": {"Charset": charset, "Data": request.text}},
            "Subject": {"Charset": charset, "Data": request.subject},
        },
        Source=sender,
    )

    return Response[str](data="email sent")
