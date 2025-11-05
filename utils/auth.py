import jwt
from datetime import datetime, timedelta

# Secret key for JWT tokens (optional if you want to add JWT)
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 6


def create_admin_token(username: str) -> str:
    """
    Create a JWT token for the admin user
    """
    expiration = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"sub": username, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_admin_token(token: str) -> dict:
    """
    Verify a JWT token for admin
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != "admin":
            raise Exception("Not an admin")
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except:
        raise Exception("Invalid token")
