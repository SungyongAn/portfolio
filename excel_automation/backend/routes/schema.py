from pydantic import BaseModel


class CheckAccountPayload(BaseModel):
    mail_address: str
    user_name: str
    work_flag: str


class WriteToExcelPayload(BaseModel):
    mail_address: str
    user_name: str
    time_worked: int
    work_flag: str


class CheckAccountResponseGeneric(BaseModel):
    response_content: str
    mail_address: str
    user_name: str
    # work_flag: str


class WriteToExcelResponseGeneric(BaseModel):
    response_content: str
