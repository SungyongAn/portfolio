from datetime import datetime, timedelta
from openpyxl import Workbook


def write_dates_to_excel(filename, sheet_name="Sheet1"):

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("日付の形式が無効です。YYYY-MM-DD形式で入力してください。")
        return

    if start_date > end_date:
        print("開始日は終了日よりも前の日付である必要があります。")
        return

    # openpyxlでExcelファイルを作成
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    current_date = start_date
    row_num = 1
    column_num = 1

    while current_date <= end_date:
        ws.cell(row=row_num, column=column_num, value=current_date.strftime("%Y-%m-%d"))
        comparison_month = current_date.month
        current_date += timedelta(days=1)
        month = current_date.month
        row_num += 1
        # 月を跨いだ時に列をずらして一番上から入力する。
        if month != comparison_month:
            column_num += 1
            row_num = 1

    wb.save(filename)


if __name__ == "__main__":
    filename = "日付の出力.xlsx"
    start_date_str = "2025-01-01"
    end_date_str = "2025-03-31"
    write_dates_to_excel(filename, sheet_name="MySheet")
