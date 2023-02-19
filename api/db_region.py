from slugify import slugify
from db import db_client, TableName
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()


@tracer.capture_method
def db_get_region(region: str) -> dict:
    region = slugify(region)
    client = db_client()
    resp = client.get_item(
        TableName = TableName,
        Key = {
            'PK': {'S': f'REGIO#{region}'},
            'SK': {'S': f'REGIO#{region}'}
        }
    )
    try:
        region = {
            'countryKey': resp['Item']['GSI1PK']['S'][6:],
            'regionKey': region,
            'regionName': resp['Item']['RegionName']['S']
        }
    except KeyError:
        logger.info(f"region {region} not found")
        region = None

    logger.info(f"return region {region}")
    return region


@tracer.capture_method
def db_get_region_ranges(region: str) -> dict:
    region = slugify(region)
    client = db_client()
    resp = client.query(
        TableName = TableName,
        IndexName = 'GSI2',
        KeyConditionExpression = "#pk = :pk and begins_with(#sk, :sk)",
        ExpressionAttributeNames = {
            '#pk': 'GSI2PK',
            '#sk': 'GSI2SK'
        },
        ExpressionAttributeValues = {
            ':pk': {'S': f'REGIO#{region}'},
            ':sk': {'S': f'RANGE#'}
        }
    )

    ranges = []
    try:
        for range in resp['Items']:
            try:
                ranges.append(
                    {
                        'countryKey': range['GSI1PK']['S'][6:],
                        'regionKey': region,
                        'rangeKey': range['PK']['S'][6:],
                        'rangeName': range['RangeName']['S'],
                    }
                )
            except KeyError:
                logger.info(f"range without a name")
    except KeyError:
        logger.info(f"range matching region {region} not found")

    logger.info(f"return ranges matching region {region}: {ranges}")
    return ranges


# @tracer.capture_method
# def db_create_region(region: dict):
#     client = db_client()
#     resp = client.