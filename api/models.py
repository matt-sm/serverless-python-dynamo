import uuid
from datetime import datetime
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


class TaskCreateRequest(BaseModel):
    data: dict


class TaskUpdateRequest(BaseModel):
    status: str


class Task(BaseModel):
    id: str = str(uuid.uuid1())
    status: str = "created"
    data: dict = {}
    created_at: str = str(datetime.utcnow().timestamp())
    updated_at: str = ""


class Request(BaseModel):
    body: dict
    params: dict

    class Config:
        arbitrary_types_allowed = True
