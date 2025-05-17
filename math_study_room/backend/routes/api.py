from fastapi import APIRouter

from routes.calculation import addition_integer, subtract_integer, addition, divide, divide_residue, multiply, subtract, multiply_integer
from routes.schema import (
    Caluculation_integerPayload,
    CaluculationPayload,
    CaluculationResponse,
    DividePayload,
    DivideresidueResponse,
)

router = APIRouter()

@router.post("/page_addition_integer")
async def page_addition(caluculation_integer_payload:Caluculation_integerPayload) -> CaluculationResponse:
    question_list, answer = addition_integer(
        caluculation_integer_payload.num_range,
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_subtract_integer")
async def page_subtract(caluculation_payload:Caluculation_integerPayload) -> CaluculationResponse:
    question_list, answer = subtract_integer(
        caluculation_payload.num_range,
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


@router.post("/page_multiply_integer")
async def page_multiply(caluculation_payload:Caluculation_integerPayload) -> CaluculationResponse:
    question_list, answer = multiply_integer(
        caluculation_payload.num_range,
        )
    return CaluculationResponse(question_list=question_list, answer=answer)


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
