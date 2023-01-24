# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/
from db_region import db_get_region, db_get_region_ranges

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router

from router_helper import build_response

tracer = Tracer()
logger = Logger()
router = Router()

# Base path is /region

@router.get("/<region>")
@tracer.capture_method
def get_region(region: str) -> dict:
    region_data = db_get_region(region)
    logger.info(f"get_region {region} -> {region_data}")
    return build_response(region_data)


@router.get("/<region>/ranges")
@tracer.capture_method
def get_region_ranges(region: str) -> dict:
    ranges_data = db_get_region_ranges(region)
    logger.info(f"get_region_ranges {region} -> {ranges_data}")
    return build_response(ranges_data)


# @router.post("/")
# @tracer.capture_method
# def create_region() -> dict:
#     logger.info("create_region")

#     #region_data: dict = app.current_event.json_body  # deserialize json str to dict

#     return {"message": f"create_region {region_data}"}
