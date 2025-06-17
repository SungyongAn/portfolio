from fastapi import APIRouter
from flash_mental_arithmetic.backend.schema import (
    CaluculationPayload,
    CaluculationResponse,
    Divide_residueResponse,
)
from routes.calculation import add, subtract, divide, divide_residue, multiply

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
    question_list, answer = divide(caluculation_payload.num_times, caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_divide_residue")
async def page_divide_residue(caluculation_payload:CaluculationPayload) -> Divide_residueResponse:
    question_list, answer, residue = divide_residue(caluculation_payload.num_times, caluculation_payload.num_range)
    return Divide_residueResponse(question_list=question_list, answer=answer, residue=residue)


@router.post("/page_multiply")
async def page_multiply(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = multiply(caluculation_payload.num_times, caluculation_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)
