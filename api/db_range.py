from slugify import slugify
from db import db_client, TableName
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()


@tracer.capture_method
def db_get_range(range: str) -> dict:
    range = slugify(range)
    client = db_client()
    resp = client.get_item(
        TableName = TableName,
        Key = {
            'PK': {'S': f'RANGE#{range}'},
            'SK': {'S': f'RANGE#{range}'}
        }
    )
    try:
        range = {
            'CountryKey': resp['Item']['GSI1PK']['S'][6:],
            'RegionKey': resp['Item']['GSI2PK']['S'][6:],
            'RangenKey': range,
            'RangenName': resp['Item']['RangeName']['S']
        }
    except KeyError:
        logger.info(f"range {range} not found")
        range = None

    logger.info(f"return range {range}")
    return range


@tracer.capture_method
def db_get_range_mountains(range: str) -> dict:
    range = slugify(range)
    client = db_client()
    resp = client.query(
        TableName = TableName,
        IndexName = 'GSI3',
        KeyConditionExpression = "#pk = :pk and begins_with(#sk, :sk)",
        ExpressionAttributeNames = {
            '#pk': 'GSI3PK',
            '#sk': 'GSI3SK'
        },
        ExpressionAttributeValues = {
            ':pk': {'S': f'RANGE#{range}'},
            ':sk': {'S': f'MOUNT#'}
        }
    )
    mountains = []
    try:
        for mountain in resp['Items']:
            try:
                mountains.append(
                    {
                        'CountryKey': mountain['GSI1PK']['S'][6:],
                        'RegionKey': mountain['GSI2PK']['S'][6:],
                        'RangeKey': range,
                        'MountainKey': mountain['PK']['S'][6:],
                        'RangeName': mountain['MountainName']['S'],
                    }
                )
            except KeyError:
                logger.info(f"range without a name")
    except KeyError:
        logger.info(f"range matching range {range} not found")

    logger.info(f"return ranges matching range {range}: {mountains}")
    return mountains


# @tracer.capture_method
# def db_create_range(range: dict):
#     client = db_client()
#     resp = client.