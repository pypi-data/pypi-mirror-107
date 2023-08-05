from jose import JWTError
from ninja.security import HttpBearer, HttpBasicAuth

from .keycloak import Keycloak


class KeycloakBasicAuth(HttpBasicAuth, Keycloak):
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

    def authenticate(self, request, username, password):
        try:
            token = self.openID.token(username, password)
            payload = self.decode(token)
        except JWTError:
            return None

        response = self.create_response(payload)
        if (not self.roles) | self.is_authorized(response["roles"]):
            return response
