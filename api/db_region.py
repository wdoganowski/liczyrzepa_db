import boto3
from db import db_client, TableName
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()


@tracer.capture_method
def db_get_region(country: str, region: str) -> dict:
    client = db_client()
    resp = client.get_item(
        TableName = TableName,
        Key = {
            'PK': {'S': f'CNTRY#{country}'},
            'SK': {'S': f'REGIO#{region}'}
        }
    )
    try:
        region = {
            'CountryName': resp['Item']['CountryName']['S'],
            'RegionName': resp['Item']['RegionName']['S']
        }
    except KeyError:
        logger.info(f"pair country {country} / region {region} not found")
        region = None

    logger.info(f"return region {region}")
    return region


@tracer.capture_method
def db_get_region_ranges(country: str, region: str) -> dict:
    client = db_client()
    resp = client.query(
        TableName = TableName,
        KeyConditionExpression = "#pk = :pk and begins_with(#sk, :sk)",
        ExpressionAttributeNames = {
            '#pk': 'PK',
            '#sk': 'SK'
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
                        'CountryName': range['CountryName']['S'],
                        'RegionName': range['RegionName']['S'],
                        'RangeName': range['RangeName']['S'],
                    }
                )
            except KeyError:
                logger.info(f"range without a name")
    except KeyError:
        logger.info(f"range matching pair country {country} / region {region} not found")

    logger.info(f"return ranges matching pair country {country} / region {region}: {ranges}")
    return ranges


# @tracer.capture_method
# def db_create_region(region: dict):
#     client = db_client()
#     resp = client.