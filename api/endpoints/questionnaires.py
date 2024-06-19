from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from fastapi import Depends

from db.models import Questionnaire
from db.session import SessionLocal
from ai.groqconnetion import groqConnection

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ModelRequest(BaseModel):
    num_preg: int
    topic: str

class UpdateScoreRequest(BaseModel):
    score: int


@router.post('/create')
async def create(req: ModelRequest,  db: Session = Depends(get_db)):
    num_preg = req.num_preg
    topic = req.topic

    try:
        content = groqConnection.generate_exam(num_preg, topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate exam: " + str(e))

    try:
        new_questionnaire = Questionnaire(
            user_id=1,
            title=topic,
            content=content,
        )
        db.add(new_questionnaire)
        db.commit()
        db.refresh(new_questionnaire)

        return {'res': content, "id": new_questionnaire.id}
    except DatabaseError:
        return {'res': 'Bad query'}


@router.get('/all/{user_id}')
async def get_questionnaires(user_id: int, db: Session = Depends(get_db)) -> dict:
    questionnaires = db.query(Questionnaire).filter(Questionnaire.user_id == user_id).all()

    if not questionnaires:
        raise HTTPException(status_code=404, detail="No questionnaires found for the given user_id")

    result = []
    for questionnaire in questionnaires:
        result.append({
            'id': questionnaire.id,
            'title': questionnaire.title,
            'content': questionnaire.content,
            'score': questionnaire.score
        })

    return {'questionnaires': result}


@router.get('/{id}')
async def get_questionnaire(id: int, db: Session = Depends(get_db)) -> dict:
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == id).first()
    if questionnaire:
        return {'title': questionnaire.title, 'description': questionnaire.description, 'questions': questionnaire.questions}
    else:
        return {'message': 'Questionnaire not found'}


@router.put('/{id}/score')
async def update_score(id: int, req: UpdateScoreRequest, db: Session = Depends(get_db)):
    try:
        questionnaire = db.query(Questionnaire).filter(Questionnaire.id == id).first()
        if not questionnaire:
            raise HTTPException(status_code=404, detail="Questionnaire not found")

        questionnaire.score = req.score
        db.commit()
        db.refresh(questionnaire)

        return {'id': questionnaire.id, 'score': questionnaire.score}
    except DatabaseError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))