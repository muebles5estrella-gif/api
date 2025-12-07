import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_clave_secreta_bro"
ALGORITHM = "HS256"

def verify_password(password: str, hashed) -> bool:
    # Handle both string and bytes
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
