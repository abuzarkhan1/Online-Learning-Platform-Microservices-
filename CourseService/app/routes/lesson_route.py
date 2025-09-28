from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, controller
from ..config import database
from ..auth import get_current_user

router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)

@router.post("/{course_id}", response_model=schemas.LessonResponse)
def create_lesson(
    course_id: int,
    lesson: schemas.LessonCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.create_lesson(db, lesson, course_id)


@router.get("/course/{course_id}", response_model=list[schemas.LessonResponse])
def get_lessons(
    course_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.get_lessons(db, course_id)


@router.get("/{lesson_id}", response_model=schemas.LessonResponse)
def get_lesson_by_id(
    lesson_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.get_lesson_by_id(db, lesson_id)


@router.put("/{lesson_id}", response_model=schemas.LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_update: schemas.LessonUpdate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.update_lesson(db, lesson_id, lesson_update, current_user)


@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.delete_lesson(db, lesson_id, current_user)
