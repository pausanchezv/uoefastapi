from typing import Union, Dict, List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models import UseOfEnglishExercise, OpenCloze, KeywordTransformation
from app.models.exercise import OpenSpace, OpenSpaceSolution
from app.schemas import ExerciseRequest, OpenClozeRequest, KWTransformationRequest
from sqlalchemy.orm import Session


class CRUDExercise(CRUDBase[Union[OpenCloze, KeywordTransformation], ExerciseRequest, ExerciseRequest]):

    @staticmethod
    def create_open_space_solutions(db: Session, created_exercise: OpenSpace, solutions: Dict[int, str]):
        """
        Creates an open space solution
        """

        saved_solutions: List[OpenSpaceSolution] = []

        for key, value in solutions.items():
            saved_solutions += [OpenSpaceSolution(exercise_id=created_exercise.id, number=key, text=value)]

        db.add_all(saved_solutions)
        db.commit()

    def create_open_cloze(self, db: Session, *, obj_in: Union[OpenClozeRequest, BaseModel]) -> OpenCloze:
        """
        Creates an open cloze solution
        """

        solutions = obj_in.solutions
        obj_in.solutions = []

        created_exercise = super().create(db, obj_in=obj_in)

        self.__class__.create_open_space_solutions(db, created_exercise, solutions)

        return created_exercise

    def create_keyword_transformation(self, db: Session, *, obj_in: Union[KWTransformationRequest, BaseModel]) -> KeywordTransformation:
        """
        Creates a keyword transformation
        """
        return super().create(db, obj_in=obj_in)


exercise = CRUDExercise(UseOfEnglishExercise)
open_cloze = CRUDExercise(OpenCloze)
keyword_transformation = CRUDExercise(KeywordTransformation)
