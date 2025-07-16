from datetime import datetime, timedelta
from openpyxl import Workbook


# 指定期間の合計日数の計算
def get_num_days():
    time_difference = end_date - start_date
    num_days = time_difference.days
    return num_days


def write_dates_to_excel(filename, sheet_name="Sheet1"):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # 指定期間の合計日数の計算
    num_days = get_num_days()

    # 記入開始の日付をループ処理用の変数として代入
    current_date = start_date

    # セルの入力開始位置の指定（例）column = 1 は縦列の"A"となり、 row = 1 は横列のため入力された数字そのままの扱い
    row_num = 1
    column_num = 1

    # 月毎に列をずらして年月日をセルに記入
    for _ in range(num_days):
        comparison_month = current_date.month
        input_date = current_date.strptime(str(current_date), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        ws.cell(row=row_num, column=column_num, value=input_date)
        current_date += timedelta(days=1)
        month = current_date.month
        row_num += 1
        # 月を跨いだ時に列をずらして一番上から入力する。
        if month != comparison_month:
            column_num += 1
            row_num = 1

    wb.save(filename)


if __name__ == "__main__":
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 3, 31)
    filename = "日付の出力2.xlsx"
    sheet_name_zero = "MySheet"
    write_dates_to_excel(filename, sheet_name=sheet_name_zero)
