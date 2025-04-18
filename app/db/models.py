# from datetime import datetime, UTC
# from typing import Optional

# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
# from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String

from app.db.session import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Integer, default=1)
#     created_at = Column(DateTime, default=lambda: datetime.now(UTC))
#     updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

#     contributions = relationship("ImageContribution", back_populates="user")


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    season = Column(String, nullable=False)  # e.g., "Spring Summer 1999"

    # user_id = Column(Integer, ForeignKey("users.id"))
    # image_url = Column(String, nullable=False)
    # confidence = Column(Integer)  # Model's confidence score
    # is_verified = Column(Integer, default=0)  # Whether the contribution has been verified
    # created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    # updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # user = relationship("User", back_populates="contributions")


# class ModelVersion(Base):
#     __tablename__ = "model_versions"

#     id = Column(Integer, primary_key=True, index=True)
#     version = Column(String, nullable=False)
#     path = Column(String, nullable=False)
#     metrics = Column(Text)  # JSON string containing model metrics
#     created_at = Column(DateTime, default=lambda: datetime.now(UTC))
#     is_active = Column(Integer, default=0) 