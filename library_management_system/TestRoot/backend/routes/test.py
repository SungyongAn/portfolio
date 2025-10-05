from routes.schema import AllPayload


def test(payload: AllPayload) -> dict:

    # 受け取ったデータをログ出力（デバッグ用）
    print("[TEST] 受信したペイロード:")
    print(f"  user_id: {payload.user_id}")
    print(f"  username: {payload.username}")
    print(f"  email: {payload.email}")
    print(f"  title: {payload.title}")
    print(f"  author: {payload.author}")
    print(f"  barcode: {payload.barcode}")
    print(f"  その他のフィールド: {payload.dict(exclude_none=True)}")

    # 常に成功メッセージとデータを返す
    return {
        "message": "通信に成功しました",
        "data": payload.dict(exclude_none=True)  # 受信したデータも返す
    }
