from api.request import Request, http_handler
from api.services.email import Email, EmailRequest, send_email


@http_handler
def send(request: Request) -> Email:
    email_request = EmailRequest(**request.body)
    return send_email(email_request)
