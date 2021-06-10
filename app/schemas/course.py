from typing import List, TYPE_CHECKING, Optional

from pydantic import validator, constr
from pydantic.main import BaseModel


class CourseRequest(BaseModel):
    name: constr(min_length=3, max_length=3, regex=r'^(FCE|CAE|CPE)$') = "FCE"
    level: constr(min_length=2, max_length=2, regex=r'^(A|B|C)(1|2)$') = "B2"
    description: str
    background_color: str

    @validator('name')
    def name_length(cls, value):
        if len(value) != 3:
            raise ValueError('Name should have exactly 3 characters')
        return value


class CourseRequestPartial(BaseModel):
    description: str
    background_color: str


class CourseUser(BaseModel):

    id: int
    email: str

    class Config:
        orm_mode = True


class CourseResponse(CourseRequest):

    activities: "List[CourseActivityResponse]"

    class Config:
        orm_mode = True


class CourseResponseWithUsers(CourseResponse):

    users: List[CourseUser]

    class Config:
        orm_mode = True


class ActivityCourseResponse(CourseRequest):

    class Config:
        orm_mode = True


from app.schemas.activity import CourseActivityResponse
CourseResponse.update_forward_refs()
CourseResponseWithUsers.update_forward_refs()
