from fastapi import APIRouter

from app.api.endpoints import courses, user_courses, activities, users, authentication, exercises, versioning_test

api_router = APIRouter()

api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(user_courses.router, prefix="/user-courses", tags=["User Courses"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activities"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(authentication.router, prefix="/authentication", tags=["Authentication"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
api_router.include_router(versioning_test.router, prefix="/versioning", tags=["Versioning"])
