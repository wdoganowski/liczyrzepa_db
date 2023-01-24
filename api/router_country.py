# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/
import requests
from requests import Response
from db_country import db_get_countries, db_get_country, db_get_country_regions

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router

tracer = Tracer()
logger = Logger()
router = Router()

# Base path is /country

@router.get("/")
@tracer.capture_method
def get_all_countries() -> dict:
    country_data = db_get_countries()
    logger.info(f"get all countries {country_data}")
    return {"message": f"get all countries {country_data}"}


@router.get("/<country>")
@tracer.capture_method
def get_country(country: str) -> dict:
    country_data = db_get_country(country)
    logger.info(f"get_country {country} -> {country_data}")
    return {"message": f"get_country {country} -> {country_data}"}


@router.get("/<country>/regions")
@tracer.capture_method
def get_country_regions(country: str) -> dict:
    regions_data = db_get_country_regions(country)
    logger.info(f"get_country_regions {country} -> {regions_data}")
    return {"message": f"get_country_regions {country} -> {regions_data}"}


# @router.post("/")
# @tracer.capture_method
# def create_country() -> dict:
#     logger.info("create_country")

#     #country_data: dict = app.current_event.json_body  # deserialize json str to dict

#     return {"message": f"create_country {country_data}"}
