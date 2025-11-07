from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
security = HTTPBearer()

def create_access_token(data: dict):
    """
    data expected: {"sub": username, "role": "user" or "admin"}
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def admin_only(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admins only")

        return payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
def employer_only(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Restrict route access to employer accounts only
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("role") != "employer":
            raise HTTPException(status_code=403, detail="Employers only")

        return payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
