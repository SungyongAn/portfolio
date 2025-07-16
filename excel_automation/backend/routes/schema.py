from pydantic import BaseModel


# アカウントチェックの送信
class CheckAccountPayload(BaseModel):
    mail_address: str
    user_name: str
    work_flag: str


# アカウントチェックの受信
class CheckAccountResponseGeneric(BaseModel):
    response_content: str
    mail_address: str
    user_name: str


# Excelファイルへの書込み送信
class WriteToExcelPayload(BaseModel):
    today_date: str
    user_name: str
    work_type: str
    time_worked: int


# Excelファイルへの書込み結果の返信
class WriteToExcelResponseGeneric(BaseModel):
    response_content: str
