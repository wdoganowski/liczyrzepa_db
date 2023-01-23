# Based on https://awslabs.github.io/aws-lambda-powertools-python/1.26.6/
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

# routers
import router_country

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

app.include_router(router_country.router, prefix="/country")

@app.not_found
@tracer.capture_method
def handle_not_found_errors(exc: NotFoundError) -> Response:
    logger.info(f"Not found route: {app.current_event.path}")
    return Response(status_code=404, content_type=content_types.APPLICATION_JSON, body={"message": exc.message})


@app.get(rule="/bad-request-error")
def bad_request_error():
    raise BadRequestError("Missing required parameter")  # HTTP  400


@app.get(rule="/unauthorized-error")
def unauthorized_error():
    raise UnauthorizedError("Unauthorized")  # HTTP 401


@app.get(rule="/not-found-error")
def not_found_error():
    raise NotFoundError  # HTTP 404


@app.get(rule="/internal-server-error")
def internal_server_error():
    raise InternalServerError("Internal server error")  # HTTP 500


@app.get(rule="/service-error", cors=True)
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
