from api.functions import Request, api
from api.db.email import Email, EmailRequest, send_email


@api
def send(request: Request) -> Email:
    email_request = EmailRequest(**request.body)
    return send_email(email_request)
