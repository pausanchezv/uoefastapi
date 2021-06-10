import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Table, Column, Integer, Date, ForeignKey, DateTime

from app.core.database import Base


# UserCourses = Table(
#     'user_courses',
#     Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('course_id', Integer, ForeignKey('uoe_course.id')),
#     Column('endDate', Date)
# )


class UserCourses(Base):
    """
    User Courses
    """
    __tablename__ = "user_courses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('uoe_course.id'))
    start_date = Column(DateTime, default=datetime.datetime.now)
