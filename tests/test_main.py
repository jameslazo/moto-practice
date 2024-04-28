import unittest
# from decimal import Decimal
import boto3
from moto import mock_aws
from src import main



class DDBMotoTest(unittest.TestCase):

    @mock_aws
    def test_ddb_operations_put(self):
        main.dynamo_resource = None
        boto3.setup_default_session()
        client = boto3.client("dynamodb", region_name="us-east-1")
        client.create_table(
            TableName="test-table",
            KeySchema=[
                {"AttributeName": "partitionKey", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "partitionKey", "AttributeType": "S"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
        event = "put_item"
        response = main.ddb_operations(event)
        self.assertEqual(200, response["ResponseMetadata"]["HTTPStatusCode"])
        self.assertEqual(
            {
            'partitionKey': {'S': 'id'},
            'name': {'S': 'testname'},
            'value': {'N': '1'}
            },
            client.get_item(
                TableName="test-table",
                Key={"partitionKey": {"S": "id"}}
                )["Item"]
        )
    
    @mock_aws
    def test_ddb_operations_scan(self):
        main.dynamo_resource = None
        boto3.setup_default_session()
        client = boto3.client("dynamodb", region_name="us-east-1")
        client.create_table(
            TableName="test-table",
            KeySchema=[
                {"AttributeName": "partitionKey", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "partitionKey", "AttributeType": "S"}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        record = {
            'partitionKey': {'S': 'id'},
            'name': {'S': 'testname'},
            "value": {'N': '1'}
        }
        client.put_item(
            TableName="test-table",
            Item=record
        )
        event = "scan"
        self.assertEqual(
            [
            {
            'partitionKey': 'id',
            'name': 'testname',
            'value': 1
            }
            ],
            main.ddb_operations(event)
        )

if __name__ == '__main__':
    unittest.main()