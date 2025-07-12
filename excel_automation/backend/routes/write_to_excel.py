from openpyxl import load_workbook


# 調べるセルの範囲を確認と登録有無の確認用にユーザー名、メールアドレスのリスト化
def check_num_target_cells(sheet, check_row_num, check_column_num):

    num_target_cells = 0
    mail_address_list = []
    user_name_list = []

    while sheet.cell(row=check_row_num, column=check_column_num).value != None:
        mail_address_list.append(sheet.cell(row=check_row_num, column=check_column_num).value)
        user_name_list.append(sheet.cell(row=check_row_num, column=check_column_num + 1).value)
        check_row_num += 1
        num_target_cells += 1

    return num_target_cells, mail_address_list, user_name_list


# メールアドレスとユーザー名の登録確認
def check_account(mail_address, user_name, work_flag):

    excel_path =  # 絶対PATH
    wb = load_workbook(filename=excel_path, read_only=True)
    sheet = wb.worksheets[1]

    check_row_num = 3
    check_column_num = 1
    # num_target_cells, mail_address_list, user_name_list = check_num_target_cells(sheet, check_row_num, check_column_num)

    num_target_cells = 0
    mail_address_list = []
    user_name_list = []

    while sheet.cell(row=check_row_num, column=check_column_num).value != None:
        mail_address_list.append(sheet.cell(row=check_row_num, column=check_column_num).value)
        user_name_list.append(sheet.cell(row=check_row_num, column=check_column_num + 1).value)
        check_row_num += 1
        num_target_cells += 1

    if mail_address in mail_address_list and user_name in user_name_list:
        for i in range(num_target_cells):
            # 入力したメールアドレスと対象セルのメールアドレスが一致する場合
            if mail_address == mail_address_list[i]:
                if user_name == user_name_list[i]:
                    response_content = "以下の項目を確認、入力の上、最後に送信ボタンを押してください。"
                    return response_content, mail_address, user_name
                # ユーザー名が不一致の場合
                else:
                    response_content = "入力した情報に誤りがあります。管理者に確認してください。"
                    return response_content, mail_address, user_name
    else:
        response_content = "入力したユーザー名、もしくはメールアドレスに誤りがあります。"
        return response_content, mail_address, user_name


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
