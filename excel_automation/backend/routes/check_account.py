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


# 作業内容からExcel内の対象のセルを確認
# def check_work_type_row(work_flag):
#     work_type_row_dic = {"A": 1, "B": 9, "C": 21}
#     work_type_row = work_type_row_dic[work_flag]
#     return work_type_row


# 前回の作業状況の確認
# def cehck_previous_content(work_flag, user_name_list_num, previous_content, sheet):

#     work_type_row = check_work_type_row(work_flag)

#     # 前回の作業日の確認
#     previous_date = sheet.cell(row=work_type_row + 1, column=user_name_list_num).value
#     # 初めての作業の時
#     if previous_date == None:
#         previous_content.append("はじめの作業になります。")
#     # 2回目以降の作業の時
#     else:
#         previous_content.append(previous_date)
    
#     # 指定した作業内容の前回までの進捗状況を確認
#     # 対象の作業の前回までのトータル時間
#     # 前回までの作業回数
#     previous_num_of_operations = sheet.cell(row=work_type_row + 2, column=user_name_list_num).value
#     if 
#         previous_content.append(previous_num_of_operations)

#     return previous_content


# メールアドレスとユーザー名の登録確認
def check_account(mail_address, user_name, work_flag):

    # 対象のExcelファイルを開く（絶対PATH）
    excel_path = "/Users/sungyongan/workspace/portfolio/excel_automation/backend/routes/sample.xlsx" 
    wb = load_workbook(filename=excel_path, read_only=True)
    # アカウント管理用のシートを指定
    sheet = wb.worksheets[1]

    # アカウント情報の記載の最上段のセル位置（固定）
    check_row_num = 3
    check_column_num = 1

    # ループ処理時に確認する範囲の初期値
    num_target_cells = 0
    # 登録済みメールアドレスの一覧作成用
    mail_address_list = []
    # 登録済みユーザー名の一覧作成用
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
