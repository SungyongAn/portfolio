from pydantic import BaseModel


class WriteToExcelPayload(BaseModel):
    mail_address: str
    user_name : str
    time_worked: int
    sheet_flag: str


class WriteToExcelResponseGeneric(BaseModel):
    question_list: list[float]
    answer: float
    residue: int
