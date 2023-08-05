from typing import Optional, Generic, TypeVar
from datetime import datetime, timedelta
from jose import ExpiredSignatureError, jwt, JWTError
from graphql import GraphQLError
from .auth_model import AuthorizationResult
from fastapi import Depends, Request
class UserNotFound(Exception):
    pass

class UnkownJWTModel(Exception):
    pass

class Auth:
    def __init__(self, configs):
        auth_config = configs['auth']
        self.default_auth = auth_config['default']
        self.provider = self.default_auth['provider']
        self.driver = self.provider['driver']

    def access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        self.plain_data = data.copy()
        plain_data = data.copy()
        if expires_delta:
            self.expire = datetime.utcnow() + expires_delta
        else:
            self.expire = datetime.utcnow() + timedelta(minutes=30)
        plain_data.update({"exp": self.expire, "ref": "auth"})
        self.token_encoded = jwt.encode(plain_data, self.default_auth["secret_key"], algorithm=self.default_auth["algorithm"])

    def with_refresh_token(self):
        if self.token_encoded:
            plain_data = self.plain_data.copy()
            expire = self.expire + timedelta(minutes=10)
            plain_data.update({"exp": expire, "ref": "refresh"})
            self.refresh_token_encode = jwt.encode(plain_data, self.default_auth["secret_key"], algorithm=self.default_auth["algorithm"])

    def create(self):
        if self.token_encoded:
            jwt_token = {"token": self.token_encoded}
            if self.refresh_token_encode:
                jwt_token.update({"refresh": self.refresh_token_encode})
            return jwt_token
        return None
    
    def authorization(self, request: Request, user: str = 'user') -> AuthorizationResult:
        authorize: str = request.headers.get("Authorization")
        if not authorize:
            return AuthorizationResult()
        _, token = authorize.split(" ")
        try:
            payload = jwt.decode(token, self.default_auth["secret_key"], algorithms=self.default_auth["algorithm"])
            referance = payload.get("ref")
            if referance != "auth":
                raise JWTError()
            getUser = payload.get("user")
            if getUser is None:
                raise UnkownJWTModel()
            return AuthorizationResult(**{"authenticated": True, "message":"Signature passed", "status": 1, "auth": { "user": getUser }})
        except ExpiredSignatureError:
            return AuthorizationResult(**{"authenticated": False, "message":"Signature has expired", "status": 2})
        except JWTError:
            return AuthorizationResult(**{"authenticated": False, "message":"Signature invalid", "status": 2})
        except:
            return AuthorizationResult(**{"authenticated": False, "message":"Unkown Error", "status": 2})
        



def require_auth(func):
    def wrap(*args, **kwargs):
        _, info = args
        if "request" in info.context and info.context["request"].state.auth:
            auth = info.context["request"].state.auth
            kwargs["auth"] = auth
            return func(*args, **kwargs)
        raise GraphQLError('authenticate required')
    return wrap


    