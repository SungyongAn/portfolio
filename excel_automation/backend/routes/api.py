from fastapi import APIRouter

from routes.write_to_excel import (
    response_content
)
from routes.schema import (
    WriteToExcelPayload,
    WriteToExcelResponseGeneric,
    )

router = APIRouter()


@router.post("/write_to_excel")
async def write_to_excel(write_to_payload: WriteToExcelPayload) -> WriteToExcelResponseGeneric:
    response_content  = write_to_excel(
        write_to_payload.mail_address,
        write_to_payload.user_name,
        write_to_payload.time_worked,
        write_to_payload.sheet_flag,
        )
    return WriteToExcelResponseGeneric()

