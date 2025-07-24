from fastapi import APIRouter
from routes.check_account import check_account
from routes.backend_test import write_to_test0001

from routes.schema import (
    CheckAccountPayload,
    CheckAccountResponseGeneric,
    BackendTestPayload,
    BackendTestResponseGeneric,
    )

router = APIRouter()


@router.post("/page_check_account")
async def page_check_account(check_account_payload: CheckAccountPayload) -> CheckAccountResponseGeneric:
    response_content, mail_address, user_name = check_account(check_account_payload.mail_address, check_account_payload.user_name, check_account_payload.work_flag)
    return CheckAccountResponseGeneric(response_content=response_content, mail_address=mail_address, user_name=user_name) # previous_content=previous_content


@router.post("/page_write_to_test0001")
async def page_write_to_test0001(write_to_excel_payload: BackendTestPayload) -> BackendTestResponseGeneric:
    response_content  = write_to_test0001(write_to_excel_payload.today_date, write_to_excel_payload.user_name, write_to_excel_payload.work_type, write_to_excel_payload.time_worked)
    return BackendTestResponseGeneric(response_content=response_content)

