import boto3
import logging
from botocore.exceptions import ClientError


class DynamoDBService:
    def __init__(self, config):
        self.table_name = config["DYNAMODB_TABLE"]
        self.config = config
        self.table = self.initialize_table()

    def initialize_table(self):
        try:
            dynamodb = boto3.resource("dynamodb", region_name=self.config["AWS_REGION"])
            return dynamodb.Table(self.table_name)
        except Exception as e:
            logging.error(f"Error initializing DynamoDB table: {str(e)}")
            return None
        
    def add_uid(self, uid):
        try:
            response = self.table.put_item(Item={"UID": uid})
            return response
        except ClientError as e:
            logging.error(f"ClientError in add_uid: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            logging.error(f"Error in add_uid: {str(e)}")
            return None
        
    def get_uid(self, uid):
        try:
            response = self.table.get_item(Key={"UID": uid})
            if "Item" not in response:
                return None
            return response["Item"]
        except ClientError as e:
            logging.error(f"ClientError in get_uid: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            logging.error(f"Error in get_uid: {str(e)}")
            return None

    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            if "Item" not in response:
                return None
            return response["Item"]
        except ClientError as e:
            logging.error(f"ClientError in get_item: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            logging.error(f"Error in get_item: {str(e)}")
            return None
        
    def update_item(self, key, update_expression, expression_attribute_values):
        try:
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
            return response
        except ClientError as e:
            logging.error(
                f"ClientError in update_item: {e.response['Error']['Message']}"
            )
            return None
        except Exception as e:
            logging.error(f"Error in update_item: {str(e)}")
            return None
        
    def delete_item(self, key):
        try:
            response = self.table.delete_item(Key=key)
            return response
        except ClientError as e:
            logging.error(
                f"ClientError in delete_item: {e.response['Error']['Message']}"
            )
            return None
        except Exception as e:
            logging.error(f"Error in delete_item: {str(e)}")
            return None