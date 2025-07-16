import openpyxl as px
from openpyxl.worksheet.table import Table, TableStyleInfo
import random



#　excelのシートの中のA1,B1,C1,D1にDay,Product,Place,Feeと書き込む
wb = px.Workbook()  # 新しいworkbookを作る。wbは別の名称も可能だけど、基本的にはworkbookの略称を使用する。
ws = wb.active  # 作成したworkbookの操作を可能にする。
sheet = wb.worksheets[0]  # workbook内のシートの指定
ws.title = 'sheet_1'
ws['A1'] = '月日'
ws['B1'] = '製品'
ws['C1'] = '支店'
ws['D1'] = '利益'

# B列に製品1と製品2のどちらかをランダム生成する
for k in range(2, 501):
    a = ('製品1', '製品2')
    ws['B'+ str(k)] = random.choice(a)

# C列に企業１と企業2のどちらかをランダム生成する
for m in range(2, 501):
    b = ('支店1', '支店2')
    ws['C'+ str(m)] = random.choice(b)

# D列に80～155の範囲の値の中から数字をランダムに生成する
for n in range(2, 501):
    ws['D'+ str(n)] = random.randint(10000, 100000)

#ランダムに生成する月日の範囲を2020-1-1～2020―12-17と決める
from datetime import timedelta 
from datetime import date
import random
start_date = date(2025, 1, 1)
end_date = date(2025, 6, 17)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
random_date = start_date + timedelta(days=random_number_of_days)

 #A列に2020―1-1～2020―12―17の範囲でランダムに生成する
for p in range(2, 500):
    start_date = date(2025, 1, 1)
    end_date = date(2025, 6, 17)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    ws['A'+ str(p)] = (random_date)
    #セルの大きさ調整
    sheet.column_dimensions['A'].width = 13

# テーブルを生成する
table = Table(displayName='Table1', ref='A1:D500')

# テーブルのスタイルを決めておく
table_style = TableStyleInfo(name='TableStyleMedium8', showRowStripes=True)

# テーブルのスタイルを設定
table.tableStyleInfo = table_style

# 変更内容を保存する
wb.save('/Users/sungyongan/Desktop/sample1.xlsx')
