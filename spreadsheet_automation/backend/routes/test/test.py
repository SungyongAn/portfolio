import gspread
from pathlib import Path


# ユーザー名から情報を記載する行の確認
def check_target_num_row(sheet, user_name):
    # 作業日報の作業Aの名前登録の最上段（固定）、他作業も同行での入力となるため作業Aをから行を特定する。
    check_row_num = 3
    check_column_num = 1

    while sheet.cell(check_row_num, check_column_num).value != user_name:
        check_row_num += 1

    return check_row_num


def write_to_test0001(today_date, user_name, work_type, time_worked):
    # サービスアカウントキーファイル
    KEY_FILE = Path.home() / "Desktop" / "hale-safeguard-431900-e2-50938872b873.json"

    # 認証
    gc = gspread.oauth(credentials_filename=KEY_FILE)
    
    sheet_id = "1Tnfb4urS8LxOa4fMjDcdRJeGpErraQdzGXFFe42GNdo"

    # スプレッドシトを指定 
    workbook = gc.open_by_key(sheet_id)
    sheet = workbook.get_worksheet(0)
    
    # 作業内容に応じたセルの行位置
    work_type_dict = {"A": 1, "B": 9, "C": 21}
    
    # ユーザー名から情報を記載する行の確認
    target_num_row = check_target_num_row(sheet, user_name)
    
    # 正常に入力されているかどうかの確認用リスト、入力前のセルの中身を記録する。
    for_check_before = ""

    # 日付を入力するセル列
    date_cell_col = work_type_dict[work_type[0]] + 1
    # 入力前の日付を保存
    for_check_before = sheet.cell(target_num_row, date_cell_col).value
    # 日付の入力
    sheet.update_cell(target_num_row, date_cell_col, today_date)

    # 作業回数を加算するセル列
    num_of_operations_cell_column = work_type_dict[work_type[0]] + 2
    # 入力前の作業回数を保存
    for_check_before = sheet.cell(target_num_row, num_of_operations_cell_column).value
    # 作業回数の加算
    if sheet.cell(target_num_row, num_of_operations_cell_column).value == None:
        sheet.update_cell(target_num_row, num_of_operations_cell_column, 1)
    else:
        num_of_tasks_this_time = int(sheet.cell(target_num_row, num_of_operations_cell_column).value) + 1
        sheet.update_cell(target_num_row, num_of_operations_cell_column, num_of_tasks_this_time)

    # 作業回数の更新が正常に行われたか確認
    if for_check_before is None:
        expected_value = 1
    else:
        expected_value = int(for_check_before) + 1
    if expected_value != int(sheet.cell(target_num_row, num_of_operations_cell_column).value):
        print(for_check_before, expected_value, sheet.cell(target_num_row, num_of_operations_cell_column).value)
        response_content = "作業回数の更新でエラーが発生しました。"
        return response_content

    # 作業時間を記入するセル列
    time_worked_cell_column = work_type_dict[work_type[0]] + 2 + int(work_type[1])
    # 入力前の作業時間を保存
    for_check_before = sheet.cell(target_num_row, time_worked_cell_column).value
    # 作業時間の記入
    if for_check_before is None:
        sheet.update_cell(target_num_row, time_worked_cell_column, time_worked)
    else:
        total_time_worked = int(sheet.cell(target_num_row, time_worked_cell_column).value) + time_worked
        sheet.update_cell(target_num_row, time_worked_cell_column, total_time_worked)

    # 作業時間の入力が正常に行われたか確認
    if for_check_before == sheet.cell(target_num_row, time_worked_cell_column).value:
        response_content = "作業時間の更新でエラーが発生しました。"
        return response_content

    response_content = "入力が終わりました。"

    return response_content


if __name__ == "__main__":
    today_date = "2025/07/14"
    user_name = "桑田"
    work_type = "A1"
    time_worked = 60
    
    response_content = write_to_test0001(today_date, user_name, work_type, time_worked)
    print(response_content)
