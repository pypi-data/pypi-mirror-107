import json

def serverless(function):
    def wrapper(req, context) -> object:
        try:
            response = function(req)
            statusCode, body = response.values()

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
                "body": json.dumps({'error': True, 'message': str(e)}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

    return wrapper
