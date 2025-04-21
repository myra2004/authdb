from passlib.context import CryptContext
from jose import jwt
from fastapi import Request, HTTPException, status, Depends

from datetime import datetime, timedelta, timezone

from app.models import *
from app.db import *


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
SECRET_KEY = "void@pointer"
ACCESS_TOKEN_EXPIRES = 30

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: float = None):

    """
    - Creates a new JWT token for logging in user
    """

    # Access tokenni nima bilan generatsiya qilaman?  --->
    # Access token qanaqa token? ---> JWT token

    delta = timedelta(minutes=expires_delta) if expires_delta else timedelta(days = ACCESS_TOKEN_EXPIRES)
    expire_time = datetime.now(timezone.utc) + delta
    data.update({'exp': expire_time})

    # data = {'username': <>, 'password': <>, 'role': <>, 'exp': <>}

    access_token = jwt.encode(
        data,
        SECRET_KEY ,
        ALGORITHM
    )


    return access_token


def get_current_user(
        request: Request,
        db: db_dep
):
    auth_header = request.headers.get('Authorization')
    is_bearer = auth_header.startswith('Bearer')
    token = auth_header.split(" ")[1] if auth_header else is_bearer


    if not auth_header and is_bearer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )


    try:
        decoded_jwt = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
        username = decoded_jwt.get('username')
        password = decoded_jwt.get('password')
        role = decoded_jwt.get("role")

        db_user = db.query(User).filter(User.username == username).first()

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

    return db_user


def get_admin_user(
        user: User = Depends(get_current_user)
):
    if user.role == 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have admin privillage'
        )

    return user
