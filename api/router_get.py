# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/
import requests
from requests import Response

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router

tracer = Tracer()
logger = Logger()
router = Router()


@router.get("/", compress=True)
@tracer.capture_method
def get() -> dict:
    logger.info("get")
    return {"message": "get"}


@router.get("/<id>")
@tracer.capture_method
def get_item(id: str) -> dict:
    logger.info("get_item")
    return {"message": f"get_item {id}"}
