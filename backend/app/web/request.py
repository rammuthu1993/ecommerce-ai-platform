import json

from ..core.exceptions import InvalidJsonException
from urllib.parse import urlparse, parse_qs


class Request:

    def __init__(
        self,
        method,
        path,
        headers=None,
        body=None,
        params=None
    ):

        self.method = method

        parsed_url = urlparse(path)

        self.path = parsed_url.path

        self.query_params = {
            key: values[0]
            for key, values in parse_qs(
                parsed_url.query
            ).items()
        }

        self.headers = headers or {}
        self.body = body
        self.params = params or {}

    def json(self):

        if not self.body:
            return {}

        try:

            return json.loads(self.body)

        except json.JSONDecodeError:

            raise InvalidJsonException()