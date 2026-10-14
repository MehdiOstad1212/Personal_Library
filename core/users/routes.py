from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from core.database import get_db
from users.models import UserModel
from users.schemas import *
from fastapi.responses import JSONResponse

router = APIRouter(tags=["users"], prefix="/users")

@router.post("/login")
async def login_user(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(user_name=request.user_name.lower()).first()
    if not user_obj or not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Login successful", "user_id": user_obj.id})

@router.post("/register")
async def register_user(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(user_name=request.user_name.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    user_obj = UserModel(user_name=request.user_name.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"detail": "User registered successfully",
                                 "user_id": user_obj.id})