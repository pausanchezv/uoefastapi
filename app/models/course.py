from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


if TYPE_CHECKING:
    from app.models import UseOfEnglishActivity, User, UserCourses


class UseOfEnglishCourse(Base):
    """
    Use of English Course
    """
    __tablename__ = "uoe_course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(3), unique=True, nullable=False)
    level = Column(String(2), unique=True, nullable=False)
    description = Column(String(64), nullable=False)
    background_color = Column(String(16), nullable=False)
    activities = relationship("UseOfEnglishActivity", back_populates="course", cascade="all, delete")

    users = relationship("User", secondary="user_courses", back_populates="courses", lazy='dynamic')
