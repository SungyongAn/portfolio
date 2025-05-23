from pydantic import BaseModel


class CaluculationIntegerPayload(BaseModel):
    num_range: int


class DivideIntegerPayload(BaseModel):
    num_range: int


class CaluculationFloatPayload(BaseModel):
    num_range: list[int]
    identification_code : int


class DivideFloatPayload(BaseModel):
    num_range: list[int]


class CaluculationResponse(BaseModel):
    question_list : list[float]
    answer: float


class DivideResponse(BaseModel):
    question_list : list[float]
    answer: float
    residue: int
