from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from .config.logger import logger


def create_course(db: Session, course: schemas.CourseCreate, current_user: dict):
    logger.info(f"[START] Creating course '{course.title}' by InstructorID={current_user['id']}")

    try:
        db_course = models.Course(
            title=course.title,
            description=course.description,
            price=course.price,
            instructor_id=current_user["id"]
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        logger.info(f"[SUCCESS] Course created | CourseID={db_course.id}, Title='{db_course.title}'")

        # Add lessons if provided
        for lesson in course.lessons:
            logger.info(f"[INFO] Adding lesson '{lesson.title}' to CourseID={db_course.id}")
            db_lesson = models.Lesson(
                title=lesson.title,
                content=lesson.content,
                course_id=db_course.id
            )
            db.add(db_lesson)
            db.commit()
            db.refresh(db_lesson)
            logger.info(f"[SUCCESS] Lesson created | LessonID={db_lesson.id}")

        return db_course

    except Exception as e:
        logger.exception(f"[EXCEPTION] Failed to create course | Error={str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_courses(db: Session, skip: int = 0, limit: int = 100, current_user: dict = None):
    logger.info(
        f"[START] Fetching courses | user_id={current_user.get('id') if current_user else None}, "
        f"role={current_user.get('role') if current_user else None}, skip={skip}, limit={limit}"
    )

    try:
        courses = db.query(models.Course).offset(skip).limit(limit).all()
        logger.info(f"[SUCCESS] Fetched {len(courses)} courses")
        return courses

    except Exception as e:
        logger.exception(f"[EXCEPTION] Error fetching courses | Error={str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_course_by_id(db: Session, course_id: int, current_user: dict = None):
    logger.info(
        f"[START] Fetching course by ID={course_id} | "
        f"user_id={current_user.get('id') if current_user else None}, "
        f"role={current_user.get('role') if current_user else None}"
    )

    try:
        course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not course:
            logger.warning(f"[NOT FOUND] Course not found | CourseID={course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info(f"[SUCCESS] Found course | CourseID={course.id}, Title='{course.title}'")
        return course

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"[EXCEPTION] Error fetching course by ID | Error={str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



def update_course(db: Session, course_id: int, course_update: schemas.CourseUpdate, current_user: dict):
    logger.info(f"[START] Updating CourseID={course_id} by UserID={current_user['id']}")

    try:
        course = db.query(models.Course).filter(models.Course.id == course_id).first()

        if not course:
            logger.warning(f"[NOT FOUND] Cannot update | CourseID={course_id} not found")
            raise HTTPException(status_code=404, detail="Course not found")

        if course.instructor_id != current_user['id']:
            logger.warning(f"[FORBIDDEN] UserID={current_user['id']} tried to update CourseID={course_id}")
            raise HTTPException(status_code=403, detail="You are not allowed to update this course")

        for var, value in vars(course_update).items():
            if value is not None:
                setattr(course, var, value)

        db.commit()
        db.refresh(course)
        logger.info(f"[SUCCESS] Course updated | CourseID={course.id}, Title='{course.title}'")

        return course

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"[EXCEPTION] Failed to update CourseID={course_id} | Error={str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def delete_course(db: Session, course_id: int, current_user: dict):
    logger.info(f"[START] Deleting CourseID={course_id} by UserID={current_user['id']}")

    try:
        course = db.query(models.Course).filter(models.Course.id == course_id).first()

        if not course:
            logger.warning(f"[NOT FOUND] Cannot delete | CourseID={course_id} not found")
            raise HTTPException(status_code=404, detail="Course not found")

        # Optional: Check if the current user owns the course
        if course.instructor_id != current_user['id']:
            logger.warning(f"[FORBIDDEN] UserID={current_user['id']} tried to delete CourseID={course_id}")
            raise HTTPException(status_code=403, detail="You are not allowed to delete this course")

        db.delete(course)
        db.commit()
        logger.info(f"[SUCCESS] Course deleted | CourseID={course_id}")

        return {"message": "Course deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"[EXCEPTION] Failed to delete CourseID={course_id} | Error={str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
