from pydantic import BaseModel


class CaluculationPayload(BaseModel):
    num_range: int
    identification_code : int


class DividePayload(BaseModel):
    num_range: int


class CaluculationResponse(BaseModel):
    question_list : list[float]
    answer: float


class Divide_residueResponse(BaseModel):
    question_list : list[float]
    answer: float
    residue: int
