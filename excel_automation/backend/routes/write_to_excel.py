from openpyxl import load_workbook

# アカウント登録の有無を確認
if not in :
    response_content ="未登録のアカウントです。"

# openpyxlでExcelファイルを作成
excel_path="sample.xlsm"
wb = load_workbook(filename=excel_path, read_only=True)
ws = wb.active



wb.save("sample.xlsm")
