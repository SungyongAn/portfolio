from pydantic import BaseModel


class NonDivisionWriteToExcelIntegerPayload(BaseModel):
    time_worked: int



class DivideResponseGeneric(BaseModel):
    question_list: list[float]
    answer: float
    residue: int
