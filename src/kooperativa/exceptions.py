"""Exceptions raised by the Kooperativa SDK."""

from __future__ import annotations

from typing import Optional


class KooperativaApiError(Exception):
    """Raised when the Kooperativa API returns a non-2xx response.

    Attributes:
        status: HTTP status code returned by the API.
        code: Stable, machine-readable error code from the response body
            (e.g. "NOT_FOUND", "LICENSE_INACTIVE"). Switch on this rather
            than the message, whose wording may change.
    """

    def __init__(self, status: int, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.status = status
        self.code = code

    def __repr__(self) -> str:
        return f"KooperativaApiError(status={self.status}, code={self.code!r}, message={str(self)!r})"
