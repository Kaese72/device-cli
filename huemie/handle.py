"""API Handle"""

from typing import Any, Dict, List, Optional

import requests


class APIHandle:
    """Handle for the API"""

    def __init__(self, base_url: str) -> None:
        assert not base_url.endswith("/"), "base_url may not end with /"
        self.base_url = base_url
        self.request_timeout = 30

    def __path(self, path: str, queries: List[str]) -> str:
        assert not path.startswith("/"), "path may not start with /"
        return f"{self.base_url}/{path}?{'&'.join(queries)}"

    def get_json(self, path: str, queries: Optional[List[str]] = None) -> Any:
        """Get JSON from the API"""
        queries = queries or []
        resp = requests.get(self.__path(path, queries), timeout=self.request_timeout)
        resp.raise_for_status()
        return resp.json()

    def post_json(self, path: str, data: Dict[str, Any]) -> None:
        """Post JSON to the API"""
        resp = requests.post(
            self.__path(path, []),
            json=data,
            timeout=self.request_timeout,
        )
        resp.raise_for_status()

    def put_json(self, path: str, data: Dict[str, Any]) -> None:
        """Put JSON to the API"""
        resp = requests.put(
            self.__path(path, []),
            json=data,
            timeout=self.request_timeout,
        )
        resp.raise_for_status()
