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

    def get_user_data(self, cognito_sub):
        try:
            response = self.table.get_item(Key={"cognito_sub": cognito_sub})
            if "Item" not in response:
                return None, "User data not found"
            return response.get("Item"), None
        except ClientError as e:
            logging.error(
                f"ClientError in get_user_data: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in get_user_data: {str(e)}")
            return None, str(e)
    
    def get_available_times(self, cognito_sub):
        try:
            response = self.table.get_item(Key={"cognito_sub": cognito_sub})
            if "Item" not in response or "availableTimes" not in response["Item"]:
                return [], "Available times not found"
            return response["Item"]["availableTimes"], None
        except ClientError as e:
            logging.error(
                f"ClientError in get_available_times: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in get_available_times: {str(e)}")
            return None, str(e)

    def update_available_times(self, cognito_sub, data):
        try:
            available_times, error = self.get_available_times(cognito_sub)

            if error and "Available times not found" not in error:
                return None, error

            if available_times is None:
                available_times = []

            if data in available_times:
                return None, "Available time already exists"

            response = self.table.update_item(
                Key={"cognito_sub": cognito_sub},
                UpdateExpression="SET availableTimes = list_append(if_not_exists(availableTimes, :empty_list), :new_data)",
                ExpressionAttributeValues={":new_data": [data], ":empty_list": []},
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in update_available_times: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in update_available_times: {str(e)}")
            return None, str(e)

    def delete_available_times(self, cognito_sub, details):
        try:
            response = self.table.get_item(Key={"cognito_sub": cognito_sub})
            if "Item" not in response or "availableTimes" not in response["Item"]:
                return None, "Available times not found"
            available_times = response["Item"]["availableTimes"]
            if details in available_times:
                available_times.remove(details)
            else:
                return None, "Available time not found"
            response = self.table.update_item(
                Key={"cognito_sub": cognito_sub},
                UpdateExpression="SET availableTimes = :availableTimes",
                ExpressionAttributeValues={":availableTimes": available_times},
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in delete_available_times: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]

    def get_user_cards(self, sub):
        try:
            response = self.table.get_item(Key={"cognito_sub": sub})
            if "Item" not in response or "qrCodes" not in response["Item"]:
                return None, "QR codes not found"
            return response["Item"]["qrCodes"], None
        except ClientError as e:
            logging.error(
                f"ClientError in get_user_cards: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in get_user_cards: {str(e)}")
            return None, str(e)

    def get_user_cards_data(self, sub):
        cards, error = self.get_user_cards(sub)
        if error:
            return None, error

        try:
            card_data = []
            if cards:
                for card in cards:
                    card_data.append(
                        {
                            "UID": card.get("UID"),
                            "note": card.get("note", ""),
                            "numberofscans": card.get("numberofscans", 0),
                        }
                    )
            return card_data, None
        except Exception as e:
            logging.error(f"Error in get_user_cards_data: {str(e)}")
            return None, str(e)

    def add_cards_to_user(self, sub, uids, urls):
        try:
            response = self.table.update_item(
                Key={"cognito_sub": sub},
                UpdateExpression="SET qrCodes = list_append(if_not_exists(qrCodes, :empty_list), :qrCodes), UIDs = list_append(if_not_exists(UIDs, :empty_uid_list), :newUIDs)",
                ExpressionAttributeValues={
                    ":qrCodes": [
                        {
                            "UID": uid,
                            "URL": url,
                            "note": "",
                            "numberofscans": 0,
                        }
                        for uid, url in zip(uids, urls)
                    ],
                    ":empty_list": [],
                    ":newUIDs": uids,
                    ":empty_uid_list": [],
                },
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in add_cards_to_user: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in add_cards_to_user: {str(e)}")
            return None, str(e)


    def update_card(self, sub, uid, note):
        try:
            response = self.table.update_item(
                Key={"cognito_sub": sub},
                UpdateExpression="SET qrCodes[0].note = :note",
                ExpressionAttributeValues={":note": note},
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in update_card: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in update_card: {str(e)}")
            return None, str(e)

    def delete_card(self, sub, uid):
        try:
            response = self.table.update_item(
                Key={"cognito_sub": sub},
                UpdateExpression="REMOVE qrCodes[0]",
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in delete_card: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in delete_card: {str(e)}")
            return None, str(e)

    def delete_all_cards(self, sub):
        try:
            response = self.table.update_item(
                Key={"cognito_sub": sub},
                UpdateExpression="REMOVE cards_keys, qrCodes, UIDs",
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in delete_all_cards: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in delete_all_cards: {str(e)}")
            return None, str(e)

    def get_dates_for_user(self, cognito_sub):
        try:
            response = self.table.get_item(Key={"cognito_sub": cognito_sub})
            if "Item" not in response:
                return [], "User not found."
            dates = response["Item"].get("dates", [])
            return dates, None
        except ClientError as e:
            logging.error(
                f"ClientError in get_dates_for_user: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in get_dates_for_user: {str(e)}")
            return None, str(e)

    def remove_specific_date(self, cognito_sub, date, time, uid):
        try:
            # Fetch the current list of dates
            response = self.table.get_item(Key={"cognito_sub": cognito_sub})
            dates = response.get("Item", {}).get("dates", [])

            # Find the index of the item to remove
            index_to_remove = None
            for index, entry in enumerate(dates):
                if (
                    entry["date"] == date
                    and entry["time"] == time
                    and entry["uid"] == uid
                ):
                    index_to_remove = index
                    break

            if index_to_remove is None:
                return False, "Date not found"

            # Perform the removal operation with the correct index
            update_response = self.table.update_item(
                Key={"cognito_sub": cognito_sub},
                UpdateExpression=f"REMOVE dates[{index_to_remove}]",
                ReturnValues="UPDATED_NEW",
            )
            return True, None
        except ClientError as e:
            logging.error(
                f"ClientError in remove_specific_date: {e.response['Error']['Message']}"
            )
            return False, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in remove_specific_date: {str(e)}")
            return False, str(e)
        
    def delete_all_dates(self, cognito_sub):
        try:
            response = self.table.update_item(
                Key={"cognito_sub": cognito_sub},
                UpdateExpression="REMOVE dates",
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in delete_all_dates: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in delete_all_dates: {str(e)}")
            return None, str(e)

    def get_media_key(self, cognito_sub, media_type):
        try:
            item, error = self.get_user_data(cognito_sub)
            if error:
                return None, error  # Change from [] to None
            media_key = item.get(f"{media_type}_key")
            if isinstance(media_key, list):
                media_key = media_key[0] if media_key else None
            return media_key, None
        except ClientError as e:
            logging.error(
                f"ClientError in get_media_key: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in get_media_key: {str(e)}")
            return None, str(e)

    def update_media_key(self, cognito_sub, media_type, s3_key):
        try:
            update_expression = f"SET {media_type}_key = :updated_key"
            expression_attribute_values = {":updated_key": s3_key}

            response = self.table.update_item(
                Key={"cognito_sub": cognito_sub},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in update_media_key: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in update_media_key: {str(e)}")
            return None, str(e)

    def update_social_media(self, cognito_sub, social_media_handles):
        try:
            update_expression = "SET social_media = :social"
            expression_attribute_values = {":social": social_media_handles}
            response = self.table.update_item(
                Key={"cognito_sub": cognito_sub},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
            return response, None
        except ClientError as e:
            logging.error(
                f"ClientError in update_social_media: {e.response['Error']['Message']}"
            )
            return None, e.response["Error"]["Message"]
        except Exception as e:
            logging.error(f"Error in update_social_media: {str(e)}")
            return None, str(e)