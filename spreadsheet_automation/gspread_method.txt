gspreadのメゾット一覧

※下記サイトから抜粋（参照）
https://qiita.com/plumfield56/items/dab6230512f3381fdcad#gc%E3%81%AE%E6%93%8D%E4%BD%9C

■名前、URL、IDからスプレッドシートのworkbookを取得
・名前でworkbookを取得	gc.open_by_key('TITLE')
・IDでworkbookを取得	gc.open_by_key('ID')
・URLでworkbookを取得	gc.open_by_url('URL')
・workbookの作成 ※マイドライブに作成される	gc.create('NAME')
_________________________＿＿＿_________________________

■workbookを操作して、タイトルやシートの取得をするメソッド
・workbookのタイトル取得	workbook.title
・workbookのID取得	workbook.id
・indexでworksheetを取得	workbook.get_worksheet(0)
・名前でworksheetを取得	workbook.worksheet("sheet1")
・全てのworksheetを取得	workbook.worksheets()
・worksheetの作成	workbook.add_worksheet(title="A worksheet", rows="100", cols="20")
・worksheetの削除	workbook.del_worksheet(worksheet)
_________________________＿＿＿_________________________

■データを取得するメソッド一覧
・worksheet名を取得	worksheet.title
・worksheetIDを取得	worksheet.id
・A1形式でセルの値を取得	worksheet.acell('B1').value
・R1C1形式でセルの値を取得	worksheet.cell(1, 2).value
・A1形式でセルの関数を取得	worksheet.acell('B1', value_render_option='FORMULA').value
・R1C1形式でセルの関数を取得	worksheet.cell(1, 2, value_render_option='FORMULA').value
・●行目のデータをリストで取得	worksheet.row_values(1)
・●列目のデータをリストで取得	worksheet.col_values(1)
・worksheetの全データをリストで取得	worksheet.get_all_values()
・worksheetの全データを辞書で取得	worksheet.get_all_records()
_________________________＿＿＿_________________________

■データを更新するメソッド一覧
A1形式でセルの更新	worksheet.update_acell('B1', 'word')
R1C1形式でセルの更新	worksheet.update_cell(1, 2, 'word')
指定範囲での更新	worksheet.update('A1:B2', [[1, 2], [3, 4]])
_________________________＿＿＿_________________________

■データを検索するメソッド一覧
| 文字の検索 | worksheet.find("word") |
| 正規表現での検索 | worksheet.find(re.compile(r'正規表現'))|
| 文字の検索(一致する全て) | worksheet.findall("word") |
| 正規表現での検索(一致する全て) | worksheet.findall(re.compile(r'正規表現'))|| 範囲を配列で取得
_________________________＿＿＿_________________________
