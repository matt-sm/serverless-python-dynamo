import functools
import json
import traceback
from pydantic import BaseModel, ValidationError
from api.models import Request


def http_handler(**kwargs):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper_decorator(*args):
            event = args[0]
            body = {}
            params = {}
            status_code = 200

            if "body" in event and event["body"] is not None:
                body = json.loads(event["body"])
            if "pathParameters" in event and event["pathParameters"] is not None:
                params = event["pathParameters"]
            try:
                value = func(request=Request(body=body, params=params))
                data = value
                if isinstance(value, BaseModel):
                    data = value.dict()
                if "status_code" in kwargs:
                    status_code = kwargs["status_code"]

                return {"statusCode": status_code, "body": json.dumps({"data": data})}
            except ValidationError as ex:
                print(traceback.format_exc())
                return {"statusCode": 400, "body": '{"data": ' + ex.json() + "}"}
            except Exception as ex:  # pylint: disable=broad-except
                print(traceback.format_exc())
                return {"statusCode": 500, "body": json.dumps({"data": "An error occured"})}

        return wrapper_decorator

    return real_decorator
