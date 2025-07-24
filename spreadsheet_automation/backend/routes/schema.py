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


# スプレットシートへの書込み送信
class BackendTestPayload(BaseModel):
    today_date: str
    user_name: str
    work_type: str
    time_worked: int


# スプレットシートへの書込み結果の返信
class BackendTestResponseGeneric(BaseModel):
    response_content: str
