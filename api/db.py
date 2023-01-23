import boto3

TableName = 'Liczyrzepa'

def db_client():
    if not hasattr(db_client, 'client'):
        db_client.client = boto3.client('dynamodb')
    return db_client.client
