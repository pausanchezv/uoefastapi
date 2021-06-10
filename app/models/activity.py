from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.course import UseOfEnglishCourse
    from app.models.exercise import UseOfEnglishExercise


class UseOfEnglishActivity(Base):
    """
    Use of English Activity
    """
    __tablename__ = "uoe_activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    # An activity belongs to a course
    course_id = Column(Integer, ForeignKey('uoe_course.id'))
    course = relationship("UseOfEnglishCourse", back_populates="activities")

    # An activity has many exercises
    exercises = relationship("UseOfEnglishExercise", back_populates="activity", cascade="all, delete")