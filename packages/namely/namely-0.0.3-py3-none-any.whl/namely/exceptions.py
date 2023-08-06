"""
Standard exceptions
"""
from requests.exceptions import RequestException


def get_reason(response):
    """Function to get an exception reason"""
    if "message" in response.json():
        reason = response.json()["message"]
    elif isinstance(response, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = response.reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = response.reason.decode("iso-8859-1")
    else:
        reason = response.reason

    return reason


class EntityNotFound(RequestException):
    """
    Exception raised when an entity is not found in the API.

    Has extra field `response` containing requests.Response
    """

    def __init__(self, response):
        reason = get_reason(response)
        http_error_msg = "%s Client Error: %s for url: %s" % (
            response.status_code,
            reason,
            response.url,
        )
        super().__init__(http_error_msg, response=response)


class AccessDenied(RequestException):
    """
    Exception raised when an access denied to the certain resource.

    Has extra field `response` containing requests.Response
    """

    def __init__(self, response):
        reason = get_reason(response)
        http_error_msg = "%s Access Denied Error: %s for url: %s" % (
            response.status_code,
            reason,
            response.url,
        )
        super().__init__(http_error_msg, response=response)


class RequestError(RequestException):
    """RequestError Class"""

    def __init__(self, response):
        reason = get_reason(response)

        if 400 <= response.status_code < 500:
            if response.status_code == 403:
                pass
            http_error_msg = "%s Client Error: %s for url: %s" % (
                response.status_code,
                reason,
                response.url,
            )

        elif 500 <= response.status_code < 600:
            http_error_msg = (
                f"{response.status_code} Server Error: {reason} for url: {response.url}"
            )
        else:
            http_error_msg = (
                f"Unexpected response code [{response.status_code}] "
                f"from API: {reason} for url: {response.url}"
            )

        super().__init__(http_error_msg, response=response)
