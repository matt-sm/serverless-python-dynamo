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
## install test dependencies
```
# setup local sqs
docker pull pafortin/goaws
docker run -d --name goaws -p 4100:4100 pafortin/goaws
aws --endpoint-url http://localhost:4100 sqs create-queue --queue-name serverless-python-dynamo-task-dev

# start serverless offline
export TEST_EMAIL=<verified SES email>
serverless offline start
```
## start tests
```
pytest
```
