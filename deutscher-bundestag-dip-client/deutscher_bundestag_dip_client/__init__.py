"""A client library for accessing Deutscher Bundestag - DIP"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
