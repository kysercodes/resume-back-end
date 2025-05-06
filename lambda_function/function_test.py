
from moto import mock_aws
import boto3
import os
import json
from lambda_function import lambda_handler

# Set default region for boto3
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_lambda_handler():
    # Create a fake DynamoDB table inside the mock
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="visitorCount",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    # Optional: Seed data
    table.put_item(Item={"id": "visitor_total", "count": 0})

    # Simulate Lambda call
    event = {"httpMethod": "GET"}
    context = {}
    response = lambda_handler(event, context) 
    # calls the function

    assert response["statusCode"] == 200
    assert "visitor_count" in response["body"]
    print(response)
