# django-ninja-keycloak

  
For review- see https://gitlab.com/django-ninja/django-ninja-keycloak

**django-ninja-keycloak** is a not official Django Ninja package to providing easy to use bearer token or basic auth  authentication with django ninja flow


## Installation

### [Via Pypi Package](https://pypi.org/project/django-ninja-keycloak/#via-pypi-package):

`$ pip install django-ninja-keycloak`

or

`$ pipenv install django-ninja-keycloak`


## Dependencies

django-ninja-keycloak depends on:

-   Python 3
-   [python-keycloak](https://github.com/marcospereirampj/python-keycloak/)
-   [django-ninja](https://django-ninja.rest-framework.com/)

## Bug reports

Please report bugs and feature requests at  [https://gitlab.com/django-ninja/django-ninja-keycloak/issues](https://gitlab.com/django-ninja/django-ninja-keycloak/issues)

## Usage

### Bearer Auth

   
    keycloak_bearer_auth = KeycloakAuthBearer('https://keyclaokhost/auth/',
                                             'client_id',
                                             'realm_name',
                                             'client_secret_key',
                                             'algorithm',            # optionnal  default='RS256'
                                             options,                # optionnal  default= {"verify_signature": True, "verify_aud": True, "verify_exp": True}
                                             roles)                  # optionnal  default= []

    @api.get("/bearer", auth=keycloak_bearer_auth)
    def bearer(request):
        return {"token": request.auth}`


### Basic Auth


    keycloak_basic_auth = KeycloakBasicAuth('https://keyclaokhost/auth/',
                                             'client_id',
                                             'realm_name',
                                             'client_secret_key',
                                             'algorithm',            # optionnal  default='RS256'
                                             options,                # optionnal  default= {"verify_signature": True, "verify_aud": True, "verify_exp": True}
                                             roles)                  # optionnal  default= []

    @api.get("/basic", auth=keycloak_basic_auth)
    def bearer(request):
        return {"token": request.auth}`

### Request.auth payload



        {
            "userInfo": {
                "email_verified": '',
                "preferred_username": '',
                "name": '',
                "given_name": '',
                "family_name": '',
                "email": '',
                "sub": '',
            },
            "roles": []
        }