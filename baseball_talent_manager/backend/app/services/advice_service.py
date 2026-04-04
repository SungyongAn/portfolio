import logging
import os

from fastapi import HTTPException, status
from google import genai
from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.models.user import User

logger = logging.getLogger(__name__)


def get_advice(db: Session, user_id: int) -> dict:
    # 1. ユーザー存在チェック
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたユーザーが存在しません",
        )

    # 2. 測定記録取得（承認済みのみ・日付昇順）
    measurements = (
        db.query(Measurement)
        .filter(
            Measurement.user_id == user_id,
            Measurement.status == "approved",
        )
        .order_by(Measurement.measurement_date.asc())
        .all()
    )

    if not measurements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="承認済みの測定記録が存在しません",
        )

    # 3. プロンプト生成
    records_text = "\n".join(
        [
            f"- {m.measurement_date}: 50m走={m.sprint_50m}秒 ベースランニング={m.base_running}秒 "
            f"遠投={m.throwing_distance}m 球速={m.pitch_speed}km/h "
            f"打球速度={m.batting_speed}km/h スイング速度={m.swing_speed}km/h "
            f"ベンチプレス={m.bench_press}kg スクワット={m.squat}kg"
            for m in measurements
        ]
    )

    prompt = f"""
以下は高校野球部員（{user.name}、{user.grade}年生）の測定データです。

{records_text}

このデータをもとに以下を提案してください。
1. 適性ポジション（理由付き）
2. 強化すべき測定項目とその理由
3. 具体的な練習メニュー（週単位）

日本語で回答してください。
"""

    # 4. Gemini API呼び出し
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        advice = response.text
    except Exception as e:
        error_message = str(e)
        logger.error(f"Gemini API error: {error_message}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AIアドバイスの生成に失敗しました: {error_message}",
        )

    return {
        "user_id": user.id,
        "name": user.name,
        "advice": advice,
    }
