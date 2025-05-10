# Implement

## Technologies used
```bash
Python FastAPI + DynamoDB + Docker Compose
Using pynamodb
Redis for caching
Mailhog for testing send email at local
Logger: setup log to show on stream and also recored to file in logging folder
Using pre-commit to format source code every time having new commit
```

# FOR TESTING:
1. Run API /api/v1/fixture_data/create to create fixture data for testing
Sample curl:
```bash
curl --location --request POST 'localhost:8080/api/v1/fixture_data/create' \
--data-raw ''
```
2. API filter user: /api/v1/users/filter
Sample curl:
```bash
curl --location --request POST 'localhost:8080/api/v1/users/filter' \
--header 'Content-Type: application/json' \
--data-raw '{
    "company": "Initech",
    "job_title": "Designer",
    "city": "San Francisco",
    "state": "",
    "hosted_range": [1, 50],
    "attended_range": [1, 100],
    "page": 1,
    "limit": 10,
    "sort_by": "first_name"
}
'
```
3. API send_email: /api/v1/users/send-email
Sample curl:
```bash
curl --location --request POST 'localhost:8080/api/v1/users/send-email' \
--header 'Content-Type: application/json' \
--data-raw '{
    "company": "Initech",
    "job_title": "Designer",
    "city": "San Francisco",
    "state": "",
    "hosted_range": [1, 50],
    "attended_range": [1, 100],
    "sort_by": "first_name",
    "is_send_email": true,
    "batch_send_email": 100
}
'
```

## Implement Code

Must install pre-commit to format all line code before commit
(Will add UT to pre-commit late)

```bash
pre-commit install
```


## Build local

```bash
python -m venv env

source env/bin/activate
```

# Build

## Build Docker

```bash
docker compose up --build
```

# Check DynamoDB local:
First, must install aws-cli
List all table in DynamoDB:

```bash
aws dynamodb list-tables \
  --endpoint-url http://localhost:8000 \
  --region eu-east-1
```
