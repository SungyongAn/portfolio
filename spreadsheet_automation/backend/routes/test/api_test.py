from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

# 自作モジュールのインポート
from schema import ReceiveUserDataPayload, RelayGeneric
from backend_test import write_to_test0001

app = FastAPI(title="データ入力API", version="1.0.0")

# テンプレートとスタティックファイルの設定
templates = Jinja2Templates(directory="templates")

# Google SheetsのIDを設定（実際のスプレッドシートIDに変更してください）
SHEET_ID = "your_google_sheet_id_here"

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    """
    データ入力フォームを表示
    """
    # test.htmlの内容を直接返す
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>データ入力</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>データ入力フォーム</h1>
    <form method="POST" action="/submit">
        <div class="form-group">
            <label for="name">名前:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">メールアドレス:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <button type="submit">データを送信</button>
    </form>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/submit")
async def submit_data(
    name: str = Form(...),
    email: str = Form(...)
):
    """
    フォームデータを受け取り、Google Sheetsに書き込む
    """
    try:
        # フォームデータをPydanticモデルで検証
        user_data = ReceiveUserDataPayload(
            user_name=name,
            email=email
        )
        
        # Google Sheetsに書き込み
        result_message = write_to_test0001(SHEET_ID)
        
        # 成功レスポンスを返す
        success_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>送信完了</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .success {{
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 4px;
            border: 1px solid #c3e6cb;
        }}
        .back-link {{
            margin-top: 20px;
        }}
        .back-link a {{
            color: #007bff;
            text-decoration: none;
        }}
        .back-link a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>送信完了</h1>
    <div class="success">
        <p><strong>送信が完了しました！</strong></p>
        <p>名前: {user_data.user_name}</p>
        <p>メールアドレス: {user_data.email}</p>
        <p>結果: {result_message}</p>
    </div>
    <div class="back-link">
        <a href="/">← フォームに戻る</a>
    </div>
</body>
</html>
        """
        return HTMLResponse(content=success_html)
        
    except Exception as e:
        # エラーハンドリング
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>エラー</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .error {{
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 4px;
            border: 1px solid #f5c6cb;
        }}
        .back-link {{
            margin-top: 20px;
        }}
        .back-link a {{
            color: #007bff;
            text-decoration: none;
        }}
        .back-link a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>エラーが発生しました</h1>
    <div class="error">
        <p>データの送信中にエラーが発生しました。</p>
        <p>エラー詳細: {str(e)}</p>
    </div>
    <div class="back-link">
        <a href="/">← フォームに戻る</a>
    </div>
</body>
</html>
        """
        return HTMLResponse(content=error_html, status_code=500)

# API エンドポイント（JSON形式での送受信）
@app.post("/api/submit", response_model=RelayGeneric)
async def api_submit_data(user_data: ReceiveUserDataPayload):
    """
    JSON形式でデータを受け取るAPIエンドポイント
    """
    try:
        # Google Sheetsに書き込み
        result_message = write_to_test0001(SHEET_ID)
        
        return RelayGeneric(RelayGenericGeneric=result_message)
        
    except Exception as e:
        return RelayGeneric(RelayGenericGeneric=f"エラーが発生しました: {str(e)}")

@app.get("/health")
async def health_check():
    """
    ヘルスチェック用エンドポイント
    """
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    # サーバー起動設定
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
