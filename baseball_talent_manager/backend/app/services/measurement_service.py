from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.models.user import User
from app.schemas.measurement import (
    ApproveResponse,
    MeasurementCreateRequest,
    MeasurementCreateResponse,
    MeasurementItem,
    MeasurementListResponse,
    MeasurementSubmitResponse,
)
from app.services.notification_service import notify_user, notify_role


# マネージャーによる測定結果の登録
def create_measurement(
    db: Session, measurement_data: MeasurementCreateRequest
) -> MeasurementCreateResponse:

    # user_idのユーザーが存在するか確認
    existing_user = db.query(User).filter(User.id == measurement_data.user_id).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたユーザーが存在しません",
        )

    # 同じユーザー・同じ計測日の重複チェック
    existing_measurement = (
        db.query(Measurement)
        .filter(
            Measurement.user_id == measurement_data.user_id,
            Measurement.measurement_date == measurement_data.measurement_date,
        )
        .first()
    )

    # ステータスチェック
    if existing_measurement:
        if existing_measurement.status == "rejected":
            # 上書き更新
            existing_measurement.sprint_50m = measurement_data.sprint_50m
            existing_measurement.base_running = measurement_data.base_running
            existing_measurement.throwing_distance = measurement_data.throwing_distance
            existing_measurement.pitch_speed = measurement_data.pitch_speed
            existing_measurement.batting_speed = measurement_data.batting_speed
            existing_measurement.swing_speed = measurement_data.swing_speed
            existing_measurement.bench_press = measurement_data.bench_press
            existing_measurement.squat = measurement_data.squat
            existing_measurement.status = "draft"
            existing_measurement.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(existing_measurement)
            return MeasurementCreateResponse(
                measurement_id=existing_measurement.id,
                message="否認済みの測定記録を上書き更新しました",
            )
        else:
            # draft / pending_member / pending_coach / approved はエラー
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="同じ日の測定記録が既に存在します",
            )

    measurement = Measurement(
        user_id=measurement_data.user_id,
        measurement_date=measurement_data.measurement_date,
        sprint_50m=measurement_data.sprint_50m,
        base_running=measurement_data.base_running,
        throwing_distance=measurement_data.throwing_distance,
        pitch_speed=measurement_data.pitch_speed,
        batting_speed=measurement_data.batting_speed,
        swing_speed=measurement_data.swing_speed,
        bench_press=measurement_data.bench_press,
        squat=measurement_data.squat,
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    return MeasurementCreateResponse(
        measurement_id=measurement.id,
        message="測定記録を登録しました",
    )


# 測定結果の取得ロールに応じた分岐あり
def get_measurements(
    db: Session, current_user: User, include_all: bool = False  # 追加
) -> MeasurementListResponse:

    # memberでもinclude_all=Trueなら全件取得
    if current_user.role == "member" and not include_all:
        query = (
            db.query(Measurement, User.name, User.grade)
            .join(User, Measurement.user_id == User.id)
            .filter(Measurement.user_id == current_user.id)
        )
    else:
        query = db.query(Measurement, User.name, User.grade).join(
            User, Measurement.user_id == User.id
        )

    results = query.all()

    result_list = [
        MeasurementItem(
            measurement_id=row.Measurement.id,
            user_id=row.Measurement.user_id,
            name=row.name,
            grade=row.grade,
            measurement_date=row.Measurement.measurement_date,
            sprint_50m=row.Measurement.sprint_50m,
            base_running=row.Measurement.base_running,
            throwing_distance=row.Measurement.throwing_distance,
            pitch_speed=row.Measurement.pitch_speed,
            batting_speed=row.Measurement.batting_speed,
            swing_speed=row.Measurement.swing_speed,
            bench_press=row.Measurement.bench_press,
            squat=row.Measurement.squat,
            status=row.Measurement.status,
            manager_confirmed=row.Measurement.manager_confirmed,
        )
        for row in results
    ]

    return MeasurementListResponse(measurements=result_list)


# measurement_idを指定しての測定結果の取得
def get_measurement_by_id(db: Session, measurement_id: int) -> Measurement | None:
    return db.query(Measurement).filter(Measurement.id == measurement_id).first()


# マネージャーから部員への測定結果の承認依頼
async def submit_measurement(
    db: Session,
    measurement_id: int,
    current_user: User,
) -> MeasurementSubmitResponse:

    measurement = get_measurement_by_id(db, measurement_id)

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="測定記録が存在しません",
        )

    if measurement.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この測定記録は承認フローを発行できません",
        )

    measurement.status = "pending_member"
    measurement.updated_at = datetime.now(timezone.utc)
    db.commit()

    # 🔔 通知追加
    await notify_user(
        measurement.user_id,
        {
            "type": "approval_requested",
            "message": "測定記録の確認依頼が届いています",
        },
    )

    return MeasurementSubmitResponse(
        measurement_id=measurement.id,
        message="承認依頼を行いました。",
    )


async def member_approve(
    db: Session,
    measurement_id: int,
    action: str,
    current_user: User,
) -> ApproveResponse:

    measurement = get_measurement_by_id(db, measurement_id)

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="測定記録が存在しません",
        )

    if measurement.status != "pending_member":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この測定記録は承認フローを発行できません",
        )

    if action not in ["approve", "reject"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="actionはapproveまたはrejectを指定してください",
        )

    if action == "reject":
        measurement.status = "rejected"

    elif action == "approve":
        measurement.status = "pending_coach"

    measurement.updated_at = datetime.now(timezone.utc)
    db.commit()

    # 🔔 approve時のみ通知
    if action == "approve":
        await notify_role(
            "coach",
            {
                "type": "approval_requested",
                "message": "測定記録の承認依頼が届いています",
            },
            db,
        )

    message = "承認しました" if action == "approve" else "否認しました"

    return ApproveResponse(
        message=message,
        status=measurement.status,
    )


async def coach_approve(
    db: Session,
    measurement_id: int,
    action: str,
    current_user: User,
) -> ApproveResponse:

    measurement = get_measurement_by_id(db, measurement_id)

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="測定記録が存在しません",
        )

    if measurement.status != "pending_coach":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この測定記録は承認フローを発行できません",
        )

    if action not in ["approve", "reject"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="actionはapproveまたはrejectを指定してください",
        )

    if action == "reject":
        measurement.status = "rejected"
        measurement.updated_at = datetime.now(timezone.utc)
        db.commit()

        # 🔔 否認通知
        await notify_user(
            measurement.user_id,
            {
                "type": "rejected",
                "message": "測定記録が否認されました",
            },
        )
        await notify_role(
            "manager",
            {
                "type": "rejected",
                "message": "測定記録が否認されました",
            },
            db,
        )

    elif action == "approve":
        measurement.status = "approved"
        measurement.updated_at = datetime.now(timezone.utc)
        db.commit()

        # 🔔 承認通知
        await notify_user(
            measurement.user_id,
            {
                "type": "approved",
                "message": "測定記録が承認されました",
            },
        )
        await notify_role(
            "manager",
            {
                "type": "approved",
                "message": "測定記録が承認されました",
            },
            db,
        )

    message = "承認しました" if action == "approve" else "否認しました"

    return ApproveResponse(
        message=message,
        status=measurement.status,
    )


def confirm_measurement(
    db: Session,
    measurement_id: int,
    current_user: User,
) -> ApproveResponse:
    # 1. レコード取得（存在チェック）
    measurement = get_measurement_by_id(db, measurement_id)

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="測定記録が存在しません",
        )

    # 2. ステータスチェック（approved のみ）
    if measurement.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="承認済みの測定記録のみ確定できます",
        )

    # 3. 既にconfirm済みの場合（任意だが推奨）
    if measurement.manager_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既に確定済みです",
        )

    # 4. manager_confirmed = True に更新
    measurement.manager_confirmed = True
    measurement.updated_at = datetime.now(timezone.utc)

    # 5. commit
    db.commit()

    return ApproveResponse(
        message="確定しました",
        status=measurement.status,
    )
