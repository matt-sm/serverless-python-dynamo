import boto3
from pydantic import BaseModel
from api.functions import Request, api


class EmailSender(BaseModel):
    name: str
    email: str


class EmailRequest(BaseModel):
    sender: EmailSender
    recipient: str
    text: str
    subject: str


@api
def send(request: Request) -> str:
    email_request = EmailRequest(**request.body)

    sender = f"{email_request.sender.name} <{email_request.sender.email}>"
    charset = "UTF-8"

    client = boto3.client("ses", region_name="us-east-1")

    client.send_email(
        Destination={"ToAddresses": [email_request.recipient]},
        Message={
            "Body": {"Text": {"Charset": charset, "Data": email_request.text}},
            "Subject": {"Charset": charset, "Data": email_request.subject},
        },
        Source=sender,
    )

    return "email sent"
