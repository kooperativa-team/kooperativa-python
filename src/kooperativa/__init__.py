"""Official Python SDK for the Kooperativa API."""

from .client import Kooperativa
from .exceptions import KooperativaApiError

__all__ = ["Kooperativa", "KooperativaApiError"]
__version__ = "0.1.0"
