from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base


if TYPE_CHECKING:
    from app.models import UseOfEnglishCourse, UserCourses


class User(Base):
    """
    Use of English User
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    number = Column(Integer, default=0)

    courses = relationship("UseOfEnglishCourse", secondary="user_courses", back_populates="users")
