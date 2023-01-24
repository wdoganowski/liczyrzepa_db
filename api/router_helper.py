from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()

app = APIGatewayRestResolver()

@tracer.capture_method
def build_response(data: dict = None, status: str = 'OK', code: int = 200, error: str = None, override_default: bool = False) -> dict:
    '''
    Build the response based on params, by defualt assume OK and if override_default is not specified, checks if 
    the data is not empty and otherwise returns 404
    
    e.g. result {"data": mountain_data, "function": app.current_event.path, "params": app.current_event.query_string_parameters, "status": "NOT_FOUND"}, 404
    '''
    logger.debug(f"data: {data}")
    if not override_default and (data == None or len(data) == 0):
        status = 'NOT_FOUND'
        code = 404
        logger.info(f"overriting the status code to 404 NOT_FOUND")
    return{
        "data": data, 
        "function": app.current_event.path, 
        "params": app.current_event.query_string_parameters, 
        "status": status,
        "error": error,
        "code": code
    }, code