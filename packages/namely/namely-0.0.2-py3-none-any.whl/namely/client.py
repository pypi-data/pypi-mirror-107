"""Namely API Client"""

from urllib.parse import urljoin

import requests

from .resources.profiles import Profile


class APISession(requests.Session):
    """Class to define API session"""

    def __init__(self, base_url, token):
        self.api_token = token
        self.base_url = base_url
        super().__init__()

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):

        headers = headers or {}
        if "Authorization" not in headers and self.api_token is not None:
            headers["Authorization"] = "Bearer %s" % self.api_token

        if not url.startswith("http"):
            url = urljoin(self.base_url, url)

        return super().request(
            method,
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )


class Client:
    """Client class for Namely API"""

    def __init__(self, namely_url: str, api_token: str = None):
        self.namely_url = namely_url
        self.api_token = api_token
        self.session = APISession(namely_url, api_token)
        self._profiles = Profile(self.session)

    @property
    def profiles(self):
        """Property for profiles resource"""
        return self._profiles
