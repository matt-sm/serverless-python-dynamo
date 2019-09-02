import json
import logging
import os
import time
import uuid
from datetime import datetime

import boto3
dynamodb = boto3.resource('dynamodb')


def compute(event, context):
    for r in event['Records']:
        print(r)
    return
