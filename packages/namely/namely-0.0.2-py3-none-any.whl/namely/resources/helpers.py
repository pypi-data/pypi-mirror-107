from requests import Session

from ..exceptions import EntityNotFound, AccessDenied, RequestError


class BaseResource:
    """Base class for resources"""

    def __init__(self, session: Session):
        self.session = session

    def _get_json(self, path: str):
        resp = self.session.get(path)

        if 200 <= resp.status_code < 300:
            return resp.json()
        elif resp.status_code == 404:
            raise EntityNotFound(resp)
        elif resp.status_code == 403:
            raise AccessDenied(resp)
        else:
            raise RequestError(resp)
