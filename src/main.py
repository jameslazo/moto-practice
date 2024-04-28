import boto3



dynamo_resource = None

def init_dynamodb():
    global dynamo_resource
    if dynamo_resource is None:
        dynamo_resource = boto3.resource("dynamodb", region_name="us-east-1")

def table_put_item():
    init_dynamodb()
    record = {
        "partitionKey": "id",
        "name": "testname",
        "value": 1
    }
    table = dynamo_resource.Table("test-table")
    return table.put_item(Item=record)
