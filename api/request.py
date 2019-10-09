import functools
import json
import traceback
from pydantic import BaseModel, ValidationError


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
        except Exception as ex:  # pylint: disable=broad-except
            print(traceback.format_exc())
            return {"statusCode": 500, "body": json.dumps({"data": "An error occured"})}

    return wrapper_decorator
