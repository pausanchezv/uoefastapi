from typing import List, Optional, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import UseOfEnglishCourse
from app.schemas import CourseRequest


class CRUDCourse(CRUDBase[UseOfEnglishCourse, CourseRequest, CourseRequest]):

    def create(self, db: Session, *, obj_in: Union[CourseRequest, BaseModel]) -> UseOfEnglishCourse:
        """
        Creates a new course
        """
        return super().create(db, obj_in=obj_in)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[UseOfEnglishCourse]:
        """
        Returns a list of courses
        """
        return super().get_multi(db, skip=skip, limit=limit)
        #return db.query(self.model).all().offset(skip).limit(limit).all()

    def get(self, db: Session, obj_id: int) -> Optional[UseOfEnglishCourse]:
        """
        Obtains a course
        """
        return super().get(db, obj_id=obj_id)

    def delete(self, db: Session, *, obj_id: int) -> UseOfEnglishCourse:
        """
        Removes a course
        """
        return super().delete(db, obj_id=obj_id)


course = CRUDCourse(UseOfEnglishCourse)
