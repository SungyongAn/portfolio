from fastapi import APIRouter

from routes.calculation import add
from routes.schema import (
    CaluculationPayload,
    CaluculationResponse,
)

router = APIRouter()


@router.post("/page_add")
async def page_add(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = add(caluculation_payload.num_times, caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)
