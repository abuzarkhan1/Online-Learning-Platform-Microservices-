from sqlalchemy.orm import Session
from . import models, schemas
from .config.logger import logger

def create_course(db: Session, course: schemas.CourseCreate):
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


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching all courses with skip={skip} and limit={limit}")
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    logger.info(f"Fetched {len(courses)} courses")
    return courses


def getCourseById(db: Session, course_id: int):
    logger.info(f"Fetching course with ID: {course_id}")
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course:
        logger.info(f"Course found: {course.title}")
    else:
        logger.warning(f"No course found with ID: {course_id}")
    return course

def updateCourse(db: Session, course_id: int, course_update: schemas.CourseUpdate):
    logger.info(f"Updating course with ID: {course_id}")
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        logger.warning(f"No course found with ID: {course_id} for update")
        return None

    for var, value in vars(course_update).items():
        if value is not None:
            setattr(course, var, value)

    db.commit()
    db.refresh(course)
    logger.info(f"Course updated: {course.title}")
    return course

def deleteCourse(db: Session, course_id: int):
    logger.info(f"Deleting course with ID: {course_id}")
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        logger.warning(f"No course found with ID: {course_id} for deletion")
        return None

    db.delete(course)
    db.commit()
    logger.info(f"Course deleted with ID: {course_id}")
    return course