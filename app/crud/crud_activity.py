from app.crud.base import CRUDBase
from app.models import UseOfEnglishActivity
from app.schemas import ActivityRequest


class CRUDActivity(CRUDBase[UseOfEnglishActivity, ActivityRequest, ActivityRequest]):
    pass


activity = CRUDActivity(UseOfEnglishActivity)
