from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import DatabaseError, IntegrityError
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
    new_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        password=user.password  # Asegúrate de hash la contraseña antes de guardarla
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'user_id': new_user.id, 'username': new_user.username, 'name': new_user.name, 'email': new_user.email}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with the same username or email already exists")
    except DatabaseError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


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
