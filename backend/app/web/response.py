import json
import datetime
import decimal

def json_serializer_default(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return str(obj)


class Response:

    def __init__(
        self,
        data=None,
        status_code=200,
        message=None,
        error=None,
        pagination=None
    ):

        self.status_code = status_code

        self.headers = {
            "Content-Type": "application/json"
        }

        self.body = {
            "success": status_code < 400
        }

        if data is not None:
            self.body["data"] = data

        if message is not None:
            self.body["message"] = message

        if pagination is not None:
            self.body["pagination"] = pagination

        if error is not None:
            self.body["error"] = error    

    def to_bytes(self):
        return json.dumps(
            self.body,
            default=json_serializer_default
        ).encode("utf-8")