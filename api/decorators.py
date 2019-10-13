import functools
import json
import traceback
from pydantic import BaseModel, ValidationError
from api.models import Request


def http_handler(func):
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
            response = func(request=Request(body=body, params=params))
            data = response.data
            if isinstance(data, BaseModel):
                data = data.dict()
            if response.status_code is not None:
                status_code = response.status_code

            return {"statusCode": status_code, "body": json.dumps({"data": data})}
        except ValidationError as ex:
            print(traceback.format_exc())
            return {"statusCode": 400, "body": '{"data": ' + ex.json() + "}"}
        except Exception as ex:  # pylint: disable=broad-except
            print(traceback.format_exc())
            return {"statusCode": 500, "body": json.dumps({"data": "An error occured"})}

    return wrapper_decorator
