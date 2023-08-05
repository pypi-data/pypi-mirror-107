from typing import Optional, Any

from jose import JWTError
from ninja.security import HttpBearer

from .keycloak import Keycloak


class ServiceUnavailableError(Exception):
    pass


class KeycloakAuthBearer(HttpBearer, Keycloak):
    def __init__(self,
                 server_url: str,
                 client_id: str,
                 realm_name: str,
                 client_secret_key: str,
                 algorithm='RS256',
                 options=None,
                 roles=None):
        Keycloak.__init__(self, server_url, client_id, realm_name, client_secret_key, roles, options, algorithm)
        HttpBearer.__init__(self)

    def authenticate(self, request, token) -> Optional[Any]:
        try:
            payload = self.decode(token)
        except JWTError:
            return None

        response = self.create_response(payload)
        if (not self.roles) | self.is_authorized(response["roles"]):
            return response
