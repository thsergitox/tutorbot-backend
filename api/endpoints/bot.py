from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai.groqconnetion import groqConnection

router = APIRouter()


class ModelRequest(BaseModel):
    question: str
    name: str


@router.post('/ask')
async def ask_question(req: ModelRequest):

    question = req.question
    name = req.name
    try:
        content = groqConnection.ask_groq(question, name)
        return {'res': content}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to ask to groq" + str(e))



