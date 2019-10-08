import functools
import json
import traceback
import os
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, ValidationError
from api.db.task import TaskDb, Task

DataT = TypeVar("DataT")


class Request(BaseModel):
    body: dict
    params: dict

    class Config:
        arbitrary_types_allowed = True


def http_handler(func):
    @functools.wraps(func)
    def wrapper_decorator(*args):
        event = args[0]
        body = {}
        params = {}

        if "body" in event and event["body"] is not None:
            body = json.loads(event["body"])
        if "pathParameters" in event and event["pathParameters"] is not None:
            params = event["pathParameters"]
        try:
            value = func(request=Request(body=body, params=params))
            data = value
            if isinstance(value, BaseModel):
                data = value.dict()
            return {"statusCode": 200, "body": json.dumps({"data": data})}
        except ValidationError as ex:
            print(traceback.format_exc())
            return {"statusCode": 400, "body": '{"data": ' + ex.json() + "}"}
        except Exception as ex:
            print(traceback.format_exc())
            return {"statusCode": 500, "body": json.dumps({"data": str(ex)})}

    return wrapper_decorator
