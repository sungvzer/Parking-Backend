from binascii import b2a_hex
from flask_restful import Resource, reqparse
from flask import request
import os

from enum import Enum


class AuthResult(Enum):
    Success = 0
    NoKey = 1
    WrongKey = 2


def verify_auth(args: dict) -> AuthResult:
    auth_key = args.get('auth_key')
    if auth_key is None:
        return AuthResult.NoKey

    for entry in authentication_keys.values():
        if entry == auth_key:
            return AuthResult.Success

    return AuthResult.WrongKey


authentication_keys = {}


class Authenticate(Resource):

    def post(self):
        args = request.json
        print(args)

        username = args['username']
        password = args['password']
        if username is None:
            return {
                'description': 'no username provided'
            }, 400
        if password is None:
            return {
                'description': 'no password provided'
            }, 400
        if username == 'admin' and password == 'AdminPassword':
            key = b2a_hex(os.urandom(32)).decode('utf-8')
            print(key)
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
