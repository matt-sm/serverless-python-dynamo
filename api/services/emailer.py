import boto3
from api.models import Email, EmailRequest


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
