from jwt import decode, encode
from datetime import datetime
from time import time
from decouple import config

JWT_SECRET = config("Secret_KEY")
JWT_ALGO = config("algorithm")

def token_resp(token : str):
    def __getitem__(self, item):
        return getattr(self, item)
    return {
        "access_token" : token
    }

def sign_JWT(userId : str):
    payload = {
        "userID" : userId,
        "issuedAt" : time(),
        "expiry" : time() + 600
    }
    token = encode(payload, JWT_SECRET, algorithm = JWT_ALGO)
    return (token_resp(token))
