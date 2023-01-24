# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/
from db_range import db_get_range, db_get_range_mountains

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router

from router_helper import build_response

tracer = Tracer()
logger = Logger()
router = Router()

# Base path is /range

@router.get("/<range>")
@tracer.capture_method
def get_range(range: str) -> dict:
    range_data = db_get_range(range)
    logger.info(f"get_range {range} -> {range_data}")
    return (build_response(range_data))


@router.get("/<range>/mounts")
@tracer.capture_method
def get_range_mountains(range: str) -> dict:
    rmountains_data = db_get_range_mountains(range)
    logger.info(f"get_range_mountains {range} -> {rmountains_data}")
    return (build_response(rmountains_data))
