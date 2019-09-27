import boto3
from pydantic import BaseModel


class EmailSender(BaseModel):
    name: str
    email: str


class EmailRequest(BaseModel):
    sender: EmailSender
    recipient: str
    text: str
    subject: str


class Email(BaseModel):
    messageId: str


def send_email(request: EmailRequest) -> Email:
    sender = f"{request.sender.name} <{request.sender.email}>"
    charset = "UTF-8"

    client = boto3.client("ses", region_name="us-east-1")

    response = client.send_email(
        Destination={"ToAddresses": [request.recipient]},
        Message={
            "Body": {"Text": {"Charset": charset, "Data": request.text}},
            "Subject": {"Charset": charset, "Data": request.subject},
        },
        Source=sender,
    )

    return Email(messageId=response["MessageId"])
