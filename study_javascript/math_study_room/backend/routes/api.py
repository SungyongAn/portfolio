from fastapi import APIRouter

from routes.calculation import create_questions

from routes.schema import (
    QuestionRequestPayload,
    QuestionResponseGeneric,
    )

router = APIRouter()


@router.post("/questions", response_model=QuestionResponseGeneric)
async def questions(questions_payload: QuestionRequestPayload) -> QuestionResponseGeneric:
    questions, answers = create_questions(
        questions_payload.type,
        questions_payload.arithmetic,
        questions_payload.digits,
        questions_payload.numquestions,
        )
    return QuestionResponseGeneric(questions=questions, answers=answers)
