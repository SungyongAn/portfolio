from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI()

# データモデル
class UserData(BaseModel):
    name: str
    age: int
    email: str
    message: str = ""

# HTMLテンプレート（インラインで定義）
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI データ入力</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .result { background-color: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>FastAPI データ入力フォーム</h1>
    <form method="POST" action="/submit">
        <div class="form-group">
            <label for="name">名前:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="age">年齢:</label>
            <input type="number" id="age" name="age" required>
        </div>
        <div class="form-group">
            <label for="email">メールアドレス:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="message">メッセージ:</label>
            <textarea id="message" name="message" rows="4"></textarea>
        </div>
        <button type="submit">データを送信</button>
    </form>
</body>
</html>
'''

@app.get("/", response_class=HTMLResponse)
async def show_form():
    return HTML_FORM

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
):
    # Pythonでデータ処理
    user_data = UserData(name=name, age=age, email=email, message=message)
    
    # データ処理の例
    processed_info = {
        "processed_name": user_data.name.title(),

        "message_length": len(user_data.message),
        "timestamp": datetime.now().isoformat()
    }
    
    # ログ出力
    print(f"受信データ: {processed_info}")
    
    # JSONレスポンス
    return {
        "status": "success",
        "message": "データを正常に受信しました",
        "data": processed_info
    }

@app.get("/api/data")
async def get_all_data():
    """APIエンドポイントの例"""
    return {"message": "これはAPIエンドポイントです"}

if __name__ == "__main__":
    print("FastAPIサーバーを起動中...")
    print("ブラウザで http://localhost:8000 にアクセスしてください")
    print("API文書は http://localhost:8000/docs で確認できます")
    uvicorn.run(app, host="0.0.0.0", port=8000)
