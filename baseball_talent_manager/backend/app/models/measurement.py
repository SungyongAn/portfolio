from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    measurement_date = Column(Date, nullable=False)
    sprint_50m = Column(Float, nullable=False)
    base_running = Column(Float, nullable=False)
    throwing_distance = Column(Float, nullable=False)
    pitch_speed = Column(Float, nullable=False)
    batting_speed = Column(Float, nullable=False)
    swing_speed = Column(Float, nullable=False)
    bench_press = Column(Float, nullable=False)
    squat = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, server_default="draft")
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="measurements")
