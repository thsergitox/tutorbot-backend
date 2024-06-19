from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from fastapi import Depends

from db.models import User
from db.session import SessionLocal

router = APIRouter()


class CreateUser(BaseModel):
    username: str
    name: str
    password: str
    email: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
async def create_user(user: CreateUser, db: Session = Depends(get_db)) -> dict:
    try:
        new_user = User(
            username=user.username,
            name=user.name,
            password=user.password,
            email=user.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {'message': 'User created'}

    except DatabaseError:
        return {'message': 'Username has already existed'}


@router.get('/user')
async def get_user_data(username: str, password: str, email: str, db: Session = Depends(get_db)) -> dict:
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and user.password == password and user.email == email:
            return {'user_id': user.id, 'username': user.username, 'name': user.name, 'email': user.email}
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except HTTPException as http_exc:
        raise http_exc
    except DatabaseError:
        return {'error': 'Database error'}
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
