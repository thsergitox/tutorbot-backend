from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai.groqconnetion import groqConnection

router = APIRouter()


class ModelRequest(BaseModel):
    question: str


@router.post('/ask')
async def ask_question(req: ModelRequest):

    question = req.question
    try:
        content = groqConnection.ask_groq(question)
        return {'res': content}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to ask to groq" + str(e))



