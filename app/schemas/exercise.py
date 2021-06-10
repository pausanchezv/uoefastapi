from typing import Dict, Optional, List

from pydantic.main import BaseModel


class ExerciseRequest(BaseModel):
    title: str
    activity_id: int


class OpenClozeRequest(ExerciseRequest):
    text: str
    solutions: Optional[Dict[int, str]]


class KWTransformationRequest(ExerciseRequest):
    phrase: str


class CourseExerciseResponse(BaseModel):
    id: int
    name: str
    level: str

    class Config:
        orm_mode = True


class ActivityExerciseResponse(BaseModel):
    id: int
    name: str
    course: CourseExerciseResponse

    class Config:
        orm_mode = True


class ExerciseResponse(BaseModel):

    id: int
    title: str
    discriminator: str
    activity: ActivityExerciseResponse

    class Config:
        orm_mode = True


class OpenSpaceSolution(BaseModel):

    number: int
    text: str

    class Config:
        orm_mode = True


class OpenClozeResponse(ExerciseResponse):
    text: str

    solutions: List[OpenSpaceSolution]

    class Config:
        orm_mode = True


class KWTransformationResponse(ExerciseResponse):
    phrase: str

    class Config:
        orm_mode = True
