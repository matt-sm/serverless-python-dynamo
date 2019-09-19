import functools
import json
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, validator, ValidationError
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Error(BaseModel):
    code: int
    message: str


class Response(GenericModel, Generic[DataT]):
    data: DataT


def api_data(func):
    @functools.wraps(func)
    def wrapper_decorator(*args):
        # Do something before
        data = json.loads(args[0]["body"])
        value = func(data)
        # Do something after
        if isinstance(value, Error):
            return {
                "statusCode": value.code,
                "body": json.dumps({"data": value.message}),
            }
        if isinstance(value, ValidationError):
            return {"statusCode": 400, "body": '{"data": ' + value.json() + "}"}
        data = value.data
        if isinstance(value.data, BaseModel):
            data = value.data.dict()
        return {"statusCode": 200, "body": json.dumps({"data": data})}

    return wrapper_decorator
