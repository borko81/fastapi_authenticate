from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.shema == "Bearer":
                raise HTTPException(status_code=403, detail="Error")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Error")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Error")

    def verify_jwt(self, jwttoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwttoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
