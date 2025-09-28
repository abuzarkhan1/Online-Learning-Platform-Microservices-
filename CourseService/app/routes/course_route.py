from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, controller
from ..config import database
from ..auth import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)

@router.post("/", response_model=schemas.CourseResponse)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.create_course(db, course, current_user)


@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.get_courses(db, skip=skip, limit=limit, current_user=current_user)


@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course_by_id(
    course_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.get_course_by_id(db, course_id, current_user)


@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.update_course(db, course_id, course_update, current_user)


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.delete_course(db, course_id, current_user)
