import os
import json
import http.client
from flask import request, _request_ctx_stack, abort, Response
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from settings import setup_environment

setup_environment()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS = os.getenv("ALGORITHMS")
API_AUDIENCE = os.getenv("API_AUDIENCE")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def get_access_token():

    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = "{\"client_id\":\""+AUTH0_CLIENT_ID + \
        "\",\"client_secret\":\""+AUTH0_CLIENT_SECRET + \
        "\",\"audience\":\"https://dev-y5wb70ja.auth0.com/api/v2/\",\
            \"grant_type\":\"client_credentials\"}"

    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    return json.loads(data.decode("utf-8"))['access_token']


def get_role_id(role_name):
    token = get_access_token()
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    headers = {"authorization": "Bearer {}".format(token)}
    conn.request("GET", "/api/v2/roles", headers=headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    conn.close()

    for role in json_data:
        if role['name'] == role_name:
            return(role['id'])


def get_fitStat_clients():

    token = get_access_token()
    # make clients and change this to clients
    client_role_id = get_role_id("fitStat-Client")
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    headers = {"authorization": "Bearer {}".format(token)}
    conn.request(
        "GET", "/api/v2/roles/{}/users".format(
            client_role_id), headers=headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    conn.close()

    client_list = []

    for user in json_data:
        user_obj = {
            "id": user["user_id"],
            "email": user["email"],
            "name": user["name"]
        }
        client_list.append(user_obj)

    return client_list


def check_permissions(permissions, payload):
    '''this is a test payload with no permissions property'''
    # payload = {
    #     'iss': 'https://dev-y5wb70ja.auth0.com/',
    #     'sub': 'auth0|5dacac0df0c1a50e0de64ee5',
    #     'aud': 'drinks',
    #     'iat': 1571617080,
    #     'exp': 1571624280,
    #     'azp': '4KLyPcC6GX5yKHM7fPByy6uOAej4mnsW',
    #     'scope': ''}

    if payload.get('permissions') is not None:
        for permission in permissions:
            if permission not in payload['permissions']:
                abort(403)


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check audience/issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=[]):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            try:
                token = get_token_auth_header()

                # print(token)

                payload = verify_decode_jwt(token)
                # print(payload)

                check_permissions(permission, payload)

            except AuthError as err:
                # print(err)
                # print(err.status_code)

                abort(401, err.error)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
