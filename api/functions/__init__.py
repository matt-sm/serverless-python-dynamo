import functools
import json
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, validator, ValidationError
from pydantic.generics import GenericModel
from api.db.task import TaskDb

DataT = TypeVar("DataT")


class Request(BaseModel):
    db: TaskDb
    body: dict

    class Config:
        arbitrary_types_allowed = True


class Error(BaseModel):
    code: int
    message: str


class Response(GenericModel, Generic[DataT]):
    data: DataT


def create_db(event) -> TaskDb:
    return TaskDb("IS_OFFLINE" in event)


def api(func):
    @functools.wraps(func)
    def wrapper_decorator(*args):
        event = args[0]
        if "body" in event:
            body = json.loads(event["body"])
        try:
            value = func(Request(db=create_db(event), body=body))
            data = value.data
            if isinstance(value.data, BaseModel):
                data = value.data.dict()
            return {"statusCode": 200, "body": json.dumps({"data": data})}
        except ValidationError as ex:
            return {"statusCode": 400, "body": '{"data": ' + ex.json() + "}"}
        except Exception as ex:
            return {"statusCode": 500, "body": json.dumps({"data": str(ex)})}

    return wrapper_decorator
