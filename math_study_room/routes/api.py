from fastapi import APIRouter
from routes.schema import (
    CaluculationPayload,
    CaluculationResponse,
)
from routes.calculation import add, subtract, divide, multiply

router = APIRouter()


@router.post("/page_add")
async def page_add(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = add(caluculation_payload.num_times, caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_subtract")
async def page_subtract(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = subtract(caluculation_payload.num_times, caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_divide")
async def page_divide(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = divide(caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_multiply")
async def page_multiply(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = multiply(caluculation_payload.num_times, caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)
