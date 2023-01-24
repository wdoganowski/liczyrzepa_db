# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/

import json

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    ServiceError,
    UnauthorizedError,
)
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

# routers
import router_country
import router_region
import router_range
import router_mountain

app.include_router(router_country.router, prefix="/country")
app.include_router(router_region.router, prefix="/region")
app.include_router(router_range.router, prefix="/range")
app.include_router(router_mountain.router, prefix="/mount")

from router_helper import build_response

@app.exception_handler(ValueError)
def handle_invalid_limit_qs(ex: ValueError):  # receives exception raised
    metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
    logger.error(f"Malformed request: {ex}", extra=metadata)
    return Response(
        status_code=400,
        content_type=content_types.APPLICATION_JSON,
        #body=json.dumps({"data": None, "function": app.current_event.path, "params": app.current_event.query_string_parameters, "status": "BAD_REQUEST", "error": f"{ex}")
        body=json.dumps(build_response(status = 'BAD_REQUEST', code = 400, error = f"{ex}", override_default = True)[0]) # skip additional error code
    )


@app.not_found
@tracer.capture_method
def handle_not_found_errors(exc: NotFoundError) -> Response:
    logger.info(f"Not found route: {app.current_event.path}")
    return Response(status_code=404, content_type=content_types.APPLICATION_JSON, body=exc)


@app.get(rule="/bad-request-error")
@tracer.capture_method
def bad_request_error():
    raise BadRequestError("Missing required parameter")  # HTTP  400


@app.get(rule="/unauthorized-error")
@tracer.capture_method
def unauthorized_error():
    raise UnauthorizedError("Unauthorized")  # HTTP 401


@app.get(rule="/not-found-error")
@tracer.capture_method
def not_found_error():
    raise NotFoundError  # HTTP 404


@app.get(rule="/internal-server-error")
@tracer.capture_method
def internal_server_error():
    raise InternalServerError("Internal server error")  # HTTP 500


@app.get(rule="/service-error", cors=True)
@tracer.capture_method
def service_error():
    raise ServiceError(502, "Something went wrong!")

# Main lambda handler
@ logger.inject_lambda_context(correlation_id_path = correlation_paths.API_GATEWAY_REST)
@ tracer.capture_lambda_handler
def lambda_handler(event, context) -> dict:
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        #api-gateway-simple-proxy-for-lambda-input-format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    return app.resolve(event, context)
