import boto3
from db import db_client, TableName
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()


@tracer.capture_method
def db_get_countries(filter: str = '') -> dict:
    client = db_client()
    resp = client.query(
        TableName = TableName,
        IndexName = 'GSI1',
        KeyConditionExpression = "#pk = :pk and begins_with(#sk, :sk)",
        ExpressionAttributeNames = {
            '#pk': 'GSI1PK',
            '#sk': 'GSI1SK'
        },
        ExpressionAttributeValues = {
            ':pk': {'S': f'CNTRY'},
            ':sk': {'S': f'CNTRY#{filter}'}
        }
    )
    countries = []
    try:
        for country in resp['Items']:
            countries.append(
                {
                    'CountryName': country['CountryName']['S']
                }
            )
    except KeyError:
        logger.info(f"country matching {filter} not found")

    logger.info(f"return countries matching {filter}: {countries}")
    return countries


@tracer.capture_method
def db_get_country(country: str) -> dict:
    client = db_client()
    resp = client.get_item(
        TableName = TableName,
        Key = {
            'PK': {'S': f'CNTRY#{country}'},
            'SK': {'S': f'CNTRY#{country}'}
        }
    )
    try:
        country = {
            'CountryName': resp['Item']['CountryName']['S']
        }
    except KeyError:
        logger.info(f"country {country} not found")
        country = None

    logger.info(f"return country {country}")
    return country


@tracer.capture_method
def db_get_country_regions(country: str) -> dict:
    client = db_client()
    resp = client.query(
        TableName = TableName,
        KeyConditionExpression = "#pk = :pk and begins_with(#sk, :sk)",
        ExpressionAttributeNames = {
            '#pk': 'PK',
            '#sk': 'SK'
        },
        ExpressionAttributeValues = {
            ':pk': {'S': f'CNTRY#{country}'},
            ':sk': {'S': f'REGIO#'}
        }
    )
    from pprint import pprint
    pprint(resp)
    regions = []
    try:
        for region in resp['Items']:
            try:
                regions.append(
                    {
                        'CountryName': region['CountryName']['S'],
                        'RegionName': region['RegionName']['S']
                    }
                )
            except KeyError:
                logger.info(f"region without a name")
    except KeyError:
        logger.info(f"region matching {country} not found")

    logger.info(f"return regions matching {country}: {regions}")
    return regions


# @tracer.capture_method
# def db_create_country(country: dict):
#     client = db_client()
#     resp = client.