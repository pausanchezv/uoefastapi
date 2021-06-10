
from pydantic.main import BaseModel


class ActivityRequest(BaseModel):
    name: str
    course_id: int


class ActivityRequestPartial(BaseModel):
    name: str


class CourseActivityResponse(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ActivityResponse(ActivityRequest):

    course: "ActivityCourseResponse"

    class Config:
        orm_mode = True


from app.schemas.course import ActivityCourseResponse
ActivityResponse.update_forward_refs()
