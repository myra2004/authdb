from fastapi import APIRouter, HTTPException, status, Response
from app.db import *
from app.models import *
from app.utils import *

from app.schema import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post('/registration', response_model=AuthRegistrationResponse)
async def registration(db: db_dep,
                       user: AuthRegistration):

    db_user = User(
        username=user.username,
        password = hash_password(user.password),
        role = 'user'
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post('/login', response_model=AuthLoginResponse)
async def login(db: db_dep,
                user: AuthLogin):

    db_user = db.query(User).filter(User.username==user.username).first()
    is_correct = verify_password(user.password, db_user.password)

    if not db_user or not is_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    user_dict = user.model_dump()
    user_dict.update({'role': db_user.role})


    access_token = create_access_token(user.model_dump())
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }


"""
access token generatsiya qilish nimaga kerak
"""