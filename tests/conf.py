import os

TABLE_NAME = "serverless-python-dynamo-task-dev"

os.environ["IS_OFFLINE"] = "True"
os.environ["TASK_DYNAMODB_TABLE"] = TABLE_NAME
os.environ["TASK_QUEUE"] = TABLE_NAME
os.environ["AWS_DEFAULT_PROFILE"] = "serverless"
