from pydantic.main import BaseModel


class UserCourseRequest(BaseModel):
    user_id: int
    course_id: int


class UserCourseResponse(BaseModel):
    user_id: int
    course_id: int

    class Config:
        orm_mode = True
