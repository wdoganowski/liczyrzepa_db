FROM public.ecr.aws/lambda/python:3.9

COPY router.py router_get.py requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["router.lambda_handler"]
