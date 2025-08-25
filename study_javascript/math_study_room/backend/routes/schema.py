from pydantic import BaseModel


class NonDivisionCalculatorIntegerPayload(BaseModel):
    num_range: int


class DivideIntegerPayload(BaseModel):
    num_range: int


class NonDivisionCalculatorFloatPayload(BaseModel):
    num_range: list[int]
    identification_code: int


class DivideFloatPayload(BaseModel):
    num_range: list[int]


class NonDivisionCalculatorResponseGeneric(BaseModel):
    question_list: list[float]
    answer: float


class DivideResponseGeneric(BaseModel):
    question_list: list[float]
    answer: float
    residue: int
