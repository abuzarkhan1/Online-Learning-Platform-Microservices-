from sqlalchemy.orm import Session
from . import models, schemas
from .config.logger import logger

def get_course(db: Session, course: schemas.CourseCreate):
    logger.info(f"Creating course: {course.title}")
    db_course = models.Course(
        title=course.title,
        description=course.description,
        price=course.price,
        instructor_id=course.instructor_id
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    logger.info(f"Course created with ID: {db_course.id}")

    for lesson in course.lessons:
        logger.info(f"Adding lesson: {lesson.title} to course ID: {db_course.id}")
        db_lesson = models.Lesson(
            title=lesson.title,
            content=lesson.content,
            course_id=db_course.id
        )
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        logger.info(f"Lesson created with ID: {db_lesson.id}")

    return db_course
