from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class jwt_bearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwt_bearer, self).__init__(auto_error = auto_Error)
    
    async def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials = await super(jwt_bearer, self).__call__(request)
        if credentials:
            if not credentials.schema == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        else:
           raise HTTPException(status_code=403, detail="Invalid or expired token")

    def verify_jwt(self, jwtToken : str):
        isTokenValid : bool = False
        payload = 'a'
        if payload:
            isTokenValid = True
        return isTokenValid 
