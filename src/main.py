import boto3
from boto3.dynamodb.conditions import Attr



dynamo_resource = None

def init_dynamodb():
    global dynamo_resource
    if dynamo_resource is None:
        dynamo_resource = boto3.resource("dynamodb", region_name="us-east-1")

def ddb_operations(event: any):
    init_dynamodb()
    table = dynamo_resource.Table("test-table")
    if event == "put_item":
        record = {
            "partitionKey": "id",
            "name": "testname",
            "value": 1
        }
        return table.put_item(Item=record)
    elif event == "scan":
        done = False
        start_key = None
        items = []
        while not done:
            if start_key:
                response = table.scan(FilterExpression=Attr("name").eq("testname"), ExclusiveStartKey=start_key)
            else:
                response = table.scan(FilterExpression=Attr("name").eq("testname"))
            for item in response.get("Items", []):
                items.append(item)
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
        return items
    else:
        return "Event not supported"
