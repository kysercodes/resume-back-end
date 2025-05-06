
import boto3
import json
import os
from decimal import Decimal

# Helper for converting Decimal to int in JSON
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def lambda_handler(event, context):
    # Create the DynamoDB resource inside the handler (important for moto)
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    table = dynamodb.Table("visitorCount")

    # Update visitor count
    response = table.update_item(
        Key={"id": "visitor_total"},
        UpdateExpression="ADD #c :inc",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW"
    
    )
    print("Updated visitor count:", response["Attributes"]["count"])

    # Return result as JSON-safe i changed
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(
            {"visitor_count": response["Attributes"]["count"]},
            default=decimal_default
        )
    }
