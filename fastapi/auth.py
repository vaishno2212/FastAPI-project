import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from database.models import User, RevokedToken
from database.sessions import get_session

# load values from .env file
load_dotenv()

# JWT configuration (defaults provided so app runs even if .env is missing)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-jwt-key-replace-in-production-123456")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# scheme to look for "Bearer <token>" in the Authorization header
oauth_scheme = HTTPBearer()


# generates a jwt token that expires in 30 minutes
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# alias so both generate_token and create_access_token work
generate_token = create_access_token


# decodes and checks if the token is valid and not expired
def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user id",
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# checks if a token has been logged out/revoked
def is_token_revoked(token: str, session: Session) -> bool:
    revoked = session.exec(
        select(RevokedToken).where(RevokedToken.token == token)
    ).first()
    return revoked is not None


# marks a token as revoked in the database
def revoke_token(token: str, session: Session):
    if not is_token_revoked(token, session):
        session.add(RevokedToken(token=token))
        session.commit()


# dependency to protect routes: gets the user associated with the bearer token
def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth_scheme),
    session: Session = Depends(get_session),
) -> User:
    token = credentials.credentials

    # check if user has already logged out
    if is_token_revoked(token, session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked, please log in again",
        )

    user_id = verify_token(token)
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user