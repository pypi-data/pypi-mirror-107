from passlib.context import CryptContext
from fastapi import Request
from starlette.datastructures import URL
import os
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_verify(plain_text, hashed_text) -> bool:
    return crypt_context.verify(plain_text, hashed_text)
def hash_make(plain_text):
    return crypt_context.hash(plain_text)
def request_url(request: Request, graphql_app, url: str = 'graphql'):
    request._url = URL(url)
    return graphql_app.handle_graphql(request=request)
def req_auth(request: Request, graphql_app, auth):
    request.state.auth = auth
    return graphql_app.handle_graphql(request=request)

def file_exists(filename):
    current_location = os.path.join(os.getcwd(), filename)
    if os.path.exists(current_location) and os.path.isfile(current_location):
        return True
    return False
def file_exists_on_location(file_location):
    if os.path.exists(file_location) and os.path.isfile(file_location):
        return True
    return False

def load_environtment():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.getcwd(), '.env'))


