import os
from binascii import b2a_hex

from flask import request
from flask_restful import Resource

from models.auth_results import AuthResult
from api.initializer import limiter


def verify_auth(args: dict) -> AuthResult:
    """
    Verify authentication given the request arguments

    ## Attributes

        `args: dict`:
            summary: Request arguments dictionary, like the needed `auth_key`

    ## Return value

        `AuthResult`:
            summary: Enumerable with information about the result of the authentication
            example: `AuthResult.NoKey`

    """
    auth_key = args.get('auth_key')
    if auth_key is None:
        return AuthResult.NoKey

    for entry in authentication_keys.values():
        if entry == auth_key:
            return AuthResult.Success

    return AuthResult.WrongKey


authentication_keys = {}


class Authenticate(Resource):
    """
    Authentication resource, accessible at the `/authenticate` endpoint via the `POST` HTTP method

    Returns the authentication key that needs to be used with every other API call.
    """

    decorators = [limiter.limit("10/minute", methods=["POST"])]

    def post(self):
        args = request.form

        username = args['username']
        password = args['password']
        if username is None or username == '':
            return {
                'description': 'no username provided'
            }, 400
        if password is None or password == '':
            return {
                'description': 'no password provided'
            }, 400
        if username == 'admin' and password == 'AdminPassword':
            # Key generation via random bytes
            key = b2a_hex(os.urandom(32)).decode('utf-8')

            # Assign it to the global keys map
            authentication_keys[username] = key
            return {
                'description':
                'success',
                'key':
                key}, 200

        return {
            'description':
            'unauthorized'
        }, 401
