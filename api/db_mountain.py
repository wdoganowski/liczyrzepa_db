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
def extract_value(mountain: dict, key: str, type:str) -> str:
    try:
      return mountain[key][type]
    except KeyError:
      return None

@tracer.capture_method
def mountain_info(mountain: dict) -> dict:
    countryKey = extract_value(mountain, 'GSI1PK', 'S')[6:]
    regionKey = extract_value(mountain, 'GSI2PK', 'S')[6:]
    rangeKey = extract_value(mountain, 'GSI3PK', 'S')[6:]
    mountainKey = extract_value(mountain, 'PK', 'S')[6:]
    mountainName = extract_value(mountain, 'MountainName', 'S')
    elevation = extract_value(mountain, 'Elevation', 'S')
    latitude = extract_value(mountain, 'Latitude', 'S')
    longitude = extract_value(mountain, 'Longitude', 'S')
    geoCordinates = extract_value(mountain, 'GeoCordinates', 'S')
    attributes = extract_value(mountain, 'Attributes', 'S')
    return {
            'countryKey': countryKey,
            'regionKey': regionKey,
            'rangeKey': rangeKey,
            'mountainKey': mountainKey,
            'mountainName': mountainName,
            'elevation': elevation,
            'latitude': latitude,
            'longitude': longitude,
            'geoCordinates': geoCordinates,
            'attributes': json_convert(attributes)
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
    logger.info(f"get mount by elevation {min} {max} {country} {region} {range}")
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
    expression = "#pk = :pk and #sk between :min and :max"
    names = {
            '#pk': f'{index}PK',
            '#sk': f'{index}SK'
        }
    values = {
            ':pk': {'S': key},
            ':min': {'S': f'MTELV#{min:0>5s}'},
            ':max': {'S': f'MTELV#{max:0>5s}'}
        }
    logger.info(f"{expression} {names} {values}")
    resp = client.query(
        TableName = TableName,
        IndexName = index,
        KeyConditionExpression = expression,
        ExpressionAttributeNames = names,
        ExpressionAttributeValues = values
    )
    mountains = []
    try:
        for mountain in resp['Items']:
            try:
                mountains.append(mountain_info(mountain))
            except KeyError:
                logger.info(f"mountain without a name? {mountain}")
    except KeyError:
        logger.info(f"no matching mountains for {country} {region} {range}")

    logger.info(f"return mountains matching range {country} {region} {range}: {mountains}")
    return mountains

