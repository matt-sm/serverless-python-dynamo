# serverless-python-dynamo
A python api built with the serverless framework that utilizes api gateway, lambda, dynamodb and streams.
## local dev
```
# serverless offline dependencies
npm i

python3 -m venv venv
source ./venv/bin/activate

pip3 install pip-tools
pip-sync dev-requirements.txt requirements.txt

serverless offline start

# now hit a local endpoint
curl -X POST localhost:3000/tasks
```
## run tests
```
export TEST_EMAIL=<verified email>
serverless offline start
pytest
```
