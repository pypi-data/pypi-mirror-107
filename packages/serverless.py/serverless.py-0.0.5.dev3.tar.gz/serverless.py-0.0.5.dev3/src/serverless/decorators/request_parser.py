import json

def request_parser(function):
    def wrapper(req, context) -> object:
        try:
            response = function(req)

            if not 'body' in response:
                raise Exception('The response of @serverless function needs a body')

            body = response['body']

            if 'statusCode' in response:
                statusCode = response['statusCode']
            else:
                statusCode = 200

            return {
                "statusCode": statusCode,
                "body": json.dumps(body),
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({'error': True, 'message': str(e) or None}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

    return wrapper