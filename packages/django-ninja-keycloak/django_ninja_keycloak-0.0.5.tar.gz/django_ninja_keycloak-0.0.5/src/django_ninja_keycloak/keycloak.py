from jwt import PyJWKClient
from keycloak import KeycloakOpenID


class Keycloak:
    def __init__(self, server_url: str, client_id: str, realm_name: str, client_secret_key: str, roles: (list, None),
                 options: (map, None), algorithm: str):
        self.openID = KeycloakOpenID(server_url=server_url,
                                     client_id=client_id,
                                     realm_name=realm_name,
                                     client_secret_key=client_secret_key)
        if roles is None:
            roles = []
        if options is None:
            options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
        self.jwks_client = self.initiate_jwks_client(server_url, realm_name)
        self.client_id = client_id
        self.roles = roles
        self.options = options
        self.algorithm = algorithm

    @staticmethod
    def initiate_jwks_client(host: str, realm: str) -> PyJWKClient:
        url = f"{host}realms/{realm}/protocol/openid-connect/certs"
        return PyJWKClient(url)

    def decode(self, token: str) -> PyJWKClient:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token)
        return self.openID.decode_token(token, key=[signing_key.key], algorithms=self.algorithm,
                                        options=self.options)

    def create_response(self, payload: map) -> map:
        user_roles = []
        if "resource_access" in payload and self.client_id in payload["resource_access"]:
            user_roles = payload["resource_access"][self.client_id]["roles"]

        user_info = {
            "email_verified": payload["email_verified"],
            "preferred_username": payload["preferred_username"],
            "name": payload["name"],
            "given_name": payload["given_name"],
            "family_name": payload["family_name"],
            "email": payload["email"],
            "sub": payload["sub"],
        }

        return {
            "userInfo": user_info,
            "roles": user_roles
        }

    def is_authorized(self, user_roles: list) -> bool:
        has_role = False
        for role in user_roles:
            if role in self.roles:
                has_role = True
        return has_role
