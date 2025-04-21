from fastapi import APIRouter, HTTPException, Depends
from app.db import *
from app.utils import *
from app.models import *

from typing import Annotated

current_user_dep = Annotated[User, Depends(get_current_user)]
admin_user_dep = Annotated[User, Depends(get_current_user)]


router = APIRouter(
    tags=["book"],
    prefix="/book",
)

@router.get("/")
async def books_list(
    db: db_dep,
    user: admin_user_dep
):
    current_user = user.username
    res = ["book 1", "book 2"]
    print(">>> User data:", user, user.id, user.role, user.username, user.password)
    return res