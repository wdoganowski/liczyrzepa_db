# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/
from db_mountain import db_get_mountain, db_get_mounts_by_elevation

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router

from router_helper import build_response

tracer = Tracer()
logger = Logger()
router = Router()

# Base path is /mountain

@router.get("/<mountain>")
@tracer.capture_method
def get_mount(mountain: str) -> dict:
    mountain_data = db_get_mountain(mountain)
    logger.info(f"get_mountain {mountain} -> {mountain_data}")
    return build_response(mountain_data)


@router.get("/by_elevation/<min>/<max>")
@tracer.capture_method
def get_mounts_by_elevation(min: str, max: str) -> dict:
    # verify min and max, if not int, error will rise
    m = int(min)
    m = int(max)

    mountain_data = db_get_mounts_by_elevation(min, max)
    logger.info(f"get_mounts_by_elevation {min} {max} -> {mountain_data}")
    return build_response(mountain_data)

