from slugify import slugify
from db import db_client, TableName
from aws_lambda_powertools import Logger, Tracer
import json

tracer = Tracer()
logger = Logger()


@tracer.capture_method
def json_convert(j: str) -> dict:
    if "'" in j:
        j=j.replace("'", '"')
    j = j.replace('True', 'true').replace('False','false').replace('None','null')
    j = json.loads(j)
    return j

@tracer.capture_method
def mountain_info(mountain: dict) -> dict:
    print(mountain['Attributes']['S'])
    return {
            'countryKey': mountain['GSI1PK']['S'][6:],
            'regionKey': mountain['GSI2PK']['S'][6:],
            'rangeKey': mountain['GSI3PK']['S'][6:],
            'mountainsKey': mountain['PK']['S'][6:],
            'mountainName': mountain['MountainName']['S'],
            'attributes': json_convert(mountain['Attributes']['S'])
        }


@tracer.capture_method
def db_get_mountain(mountain: str) -> dict:
    mountain = slugify(mountain)
    client = db_client()
    resp = client.get_item(
        TableName = TableName,
        Key = {
            'PK': {'S': f'MOUNT#{mountain}'},
            'SK': {'S': f'MOUNT#{mountain}'}
        }
    )
    try:
        mountain = mountain_info(resp['Item'])
    except KeyError:
        logger.info(f"mountain {mountain} not found")
        mountain = None

    logger.info(f"return mountain {mountain}")
    return mountain



@tracer.capture_method
def db_get_mounts_by_elevation(min: str, max: str, country: str = None, region: str = None, range: str = None) -> dict:
    if country != None:
        index = 'GSI4'
        key = f'CNTRY#{country}'
    elif region != None:
        index = 'GSI5'
        key - f'REGIO#{region}'
    elif range != None:
        index = 'GSI6'
        key = f'RANGE#{range}'
    else:
        logger.info(f"elevation search without criteria")
        return None

    client = db_client()
    resp = client.query(
        TableName = TableName,
        IndexName = index,
        KeyConditionExpression = "#pk = :pk and #sk betwen :min and :max)",
        ExpressionAttributeNames = {
            '#pk': f'{index}PK',
            '#sk': f'{index}SK'
        },
        ExpressionAttributeValues = {
            ':pk': {'S': key},
            ':min': {'S': min},
            ':max': {'S': max}
        }
    )
    mountains = []
    try:
        for mountain in resp['Items']:
            try:
                mountains.append(mountain_info(mountain))
            except KeyError:
                logger.info(f"range without a name")
    except KeyError:
        logger.info(f"range matching range {range} not found")

    logger.info(f"return ranges matching range {range}: {mountains}")
    return mountains

