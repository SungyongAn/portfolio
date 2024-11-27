from pydantic import BaseModel


class CaluculationPayload(BaseModel):
    num_times: int
    num_range: int


class CaluculationResponse(BaseModel):
    question_list : list[int]
    answer: float

class Divide_residueResponse(BaseModel):
    question_list : list[int]
    answer: float
