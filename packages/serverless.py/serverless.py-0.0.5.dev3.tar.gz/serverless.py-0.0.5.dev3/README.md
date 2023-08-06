<div align="center">
    <img src="https://raw.githubusercontent.com/mtwzim/serverless.py/main/serverlesspy.png" width="50%"/>
</div>

Decorators who avoid code repetition in their lambda function

## Installation

```$ pip install serverless```

## Usage
```
@serverless
def your_function(req):
    return {
        "statusCode": 200,
        "body": {
            message: "serverless.py"
        }
    }
```

