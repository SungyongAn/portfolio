from pydantic import BaseModel


class Caluculation_integerPayload(BaseModel):
    num_range: int


class Divide_integerPayload(BaseModel):
    num_range: int


class CaluculationPayload(BaseModel):
    num_range: list[int]
    identification_code : int


class DividePayload(BaseModel):
    num_range: list[int]


class CaluculationResponse(BaseModel):
    question_list : list[float]
    answer: float


class DivideresidueResponse(BaseModel):
    question_list : list[float]
    answer: float
    residue: int
