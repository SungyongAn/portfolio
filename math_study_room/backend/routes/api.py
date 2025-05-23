from fastapi import APIRouter

from routes.calculation import (
    addition_int,
    subtract_int,
    addition_float,
    divide_float,
    divide_int,
    multiply_float,
    subtract_float,
    multiply_int,
)
from routes.schema import (
    NonDivisionCalculatorIntegerPayload,
    NonDivisionCalculatorFloatPayload,
    NonDivisionCalculatorResponseGeneric,
    DivideFloatPayload,
    DivideResponseGeneric,
    DivideIntegerPayload,
)

router = APIRouter()


@router.post("/page_addition_int")
async def page_addition_int(caluculation_integer_payload: NonDivisionCalculatorIntegerPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = addition_int(
        caluculation_integer_payload.num_range,
    )
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)


@router.post("/page_subtract_int")
async def page_subtract_int(caluculation_payload: NonDivisionCalculatorIntegerPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = subtract_int(
        caluculation_payload.num_range,
    )
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)


@router.post("/page_multiply_int")
async def page_multiply_int(caluculation_payload: NonDivisionCalculatorIntegerPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = multiply_int(
        caluculation_payload.num_range,
    )
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)


@router.post("/page_divide_int")
async def page_divide_int(divide_payload: DivideIntegerPayload) -> DivideResponseGeneric:
    question_list, answer, residue = divide_int(divide_payload.num_range)
    return DivideResponseGeneric(question_list=question_list, answer=answer, residue=residue)


@router.post("/page_addition_float")
async def page_addition_float(caluculation_payload: NonDivisionCalculatorFloatPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = addition_float(
        caluculation_payload.num_range,
        caluculation_payload.identification_code,
    )
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)


@router.post("/page_subtract_float")
async def page_subtract_float(caluculation_payload: NonDivisionCalculatorFloatPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = subtract_float(
        caluculation_payload.num_range,
        caluculation_payload.identification_code,
    )
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)


@router.post("/page_divide_float")
async def page_divide_float(divide_payload: DivideFloatPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = divide_float(divide_payload.num_range)
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)


@router.post("/page_divide_int")
async def page_divide_int(divide_payload: DivideFloatPayload) -> DivideResponseGeneric:
    question_list, answer, residue = divide_int(divide_payload.num_range)
    return DivideResponseGeneric(question_list=question_list, answer=answer, residue=residue)


@router.post("/page_multiply_float")
async def page_multiply_float(caluculation_payload: NonDivisionCalculatorFloatPayload) -> NonDivisionCalculatorResponseGeneric:
    question_list, answer = multiply_float(
        caluculation_payload.num_range,
        caluculation_payload.identification_code,
    )
    return NonDivisionCalculatorResponseGeneric(question_list=question_list, answer=answer)
