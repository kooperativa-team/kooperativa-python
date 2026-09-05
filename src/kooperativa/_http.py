"""Internal HTTP client. Not part of the public API surface."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .exceptions import KooperativaApiError


class HttpClient:
    def __init__(self, api_key: str, base_url: str, session: Optional[requests.Session] = None) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._session = session or requests.Session()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("POST", path, json_body=json_body)

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("DELETE", path, params=params)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        clean_params = _drop_empty(params) if params else None
        response = self._session.request(
            method,
            url,
            params=clean_params,
            json=json_body,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=30,
        )

        try:
            data = response.json() if response.content else None
        except ValueError:
            data = None

        if not response.ok:
            error_message = response.text
            code = None
            if isinstance(data, dict):
                error_message = data.get("error", error_message)
                code = data.get("code")
            raise KooperativaApiError(response.status_code, error_message, code)

        return data


def _drop_empty(params: Dict[str, Any]) -> Dict[str, Any]:
    """Drop None/empty values so they are omitted from the query string,
    rather than sent as literal "None" or empty-string parameters."""
    return {k: v for k, v in params.items() if v is not None and v != ""}
