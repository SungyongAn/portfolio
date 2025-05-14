from fastapi import APIRouter

from routes.calculation import addition, divide, divide_residue, multiply, subtract
from routes.schema import (
    CaluculationPayload,
    CaluculationResponse,
    DividePayload,
    DivideresidueResponse,
)

router = APIRouter()


@router.post("/page_addition")
async def page_addition(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = addition(
        caluculation_payload.num_range,
        caluculation_payload.identification_code,
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_subtract")
async def page_subtract(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = subtract(
        caluculation_payload.num_range,
        caluculation_payload.identification_code,
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_divide")
async def page_divide(divide_payload:DividePayload) -> CaluculationResponse:
    question_list, answer = divide(divide_payload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_divide_residue")
async def page_divide_residue(divide_payload:DividePayload) -> DivideresidueResponse:
    question_list, answer, residue = divide_residue(divide_payload.num_range)
    return DivideresidueResponse(question_list=question_list, answer=answer, residue=residue)


@router.post("/page_multiply")
async def page_multiply(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = multiply(
        caluculation_payload.num_range,
        caluculation_payload.identification_code,
        )
    return CaluculationResponse(question_list=question_list, answer=answer)
