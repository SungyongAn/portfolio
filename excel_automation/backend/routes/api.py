from fastapi import APIRouter
from routes.write_to_excel import write_to_excel
from routes.check_account import check_account

from routes.schema import (
    CheckAccountPayload,
    CheckAccountResponseGeneric,
    WriteToExcelPayload,
    WriteToExcelResponseGeneric,
    )

router = APIRouter()


@router.post("/page_check_account")
async def page_check_account(check_account_payload: CheckAccountPayload) -> CheckAccountResponseGeneric:
    response_content, mail_address, user_name = check_account(check_account_payload.mail_address, check_account_payload.user_name, check_account_payload.work_flag)
    return CheckAccountResponseGeneric(response_content=response_content, mail_address=mail_address, user_name=user_name) # previous_content=previous_content


@router.post("/page_write_to_excel")
async def page_write_to_excel(write_to_excel_payload: WriteToExcelPayload) -> WriteToExcelResponseGeneric:
    response_content  = write_to_excel(write_to_excel_payload.today_date, write_to_excel_payload.user_name, write_to_excel_payload.work_type, write_to_excel_payload.time_worked)
    return WriteToExcelResponseGeneric(response_content=response_content)

