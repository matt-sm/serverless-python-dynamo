# serverless-python-dynamo

## local dev
```
npm i

python3 -m venv venv
source ./venv/bin/activate

pip3 install pip-tools
pip-sync dev-requirements.txt requirements.txt
```
## run tests
```
serverless offline start
pytest
```
