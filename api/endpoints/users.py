from fastapi import APIRouter
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
async def create_user(user: CreateUser,  db: Session = Depends(get_db)) -> dict:
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




@router.get('/{username}')
async def get_user_data(username: str,  db: Session = Depends(get_db)) -> dict:
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            return {'user_id': user.id, 'username': user.username, 'name': user.name, 'email': user.email}
        else:
            return {'message': 'User not found'}
    except DatabaseError:
        return {'error': 'I dunno'}
