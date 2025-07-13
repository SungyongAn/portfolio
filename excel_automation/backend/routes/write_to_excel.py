from openpyxl import load_workbook


# Excelファイルへの作業内容の書込み
def write_to_excel(mail_address, user_name, time_worked, work_flag):

    excel_path = "sample.xlsx"

    wb = load_workbook(filename=excel_path, read_only=True)

    response_content_flag = False
    response_content = ""

    # アカウント情報の登録有無の確認（仮）
    sheet = wb.worksheets[1]
    response_content_flag, response_content = check_account(sheet, mail_address, user_name, response_content_flag, wb)

    if response_content_flag == True:
        return response_content

    else:
        sheet = wb.worksheets[0]

    wb.save("sample.xlsx")
