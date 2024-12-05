from fastapi import APIRouter
from routes.schema import (
    CaluculationPayload,
    DividePayload,
    CaluculationResponse,
    Divide_residueResponse,
)
from routes.calculation import addition, subtract, divide, divide_residue, multiply

router = APIRouter()


@router.post("/page_addition")
async def page_addition(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = addition(
        caluculation_payload.num_range,
        caluculation_payload.identification_code
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_subtract")
async def page_subtract(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = subtract(
        caluculation_payload.num_range,
        caluculation_payload.identification_code
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_divide")
async def page_divide(dividePayload:DividePayload) -> CaluculationResponse:
    question_list, answer = divide(dividePayload.num_range)
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_divide_residue")
async def page_divide_residue(dividePayload:DividePayload) -> Divide_residueResponse:
    question_list, answer, residue = divide_residue(dividePayload.num_range)
    return Divide_residueResponse(question_list=question_list, answer=answer, residue=residue)


@router.post("/page_multiply")
async def page_multiply(caluculation_payload:CaluculationPayload) -> CaluculationResponse:
    question_list, answer = multiply(caluculation_payload.num_range, caluculation_payload.identification_code)
    return CaluculationResponse(question_list=question_list, answer=answer)
