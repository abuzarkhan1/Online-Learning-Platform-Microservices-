from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, controller
from ..config import database
from ..auth import get_current_user
from ..config.logger import logger

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/", response_model=schemas.CourseResponse)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(
        f" [REQUEST] Create course attempt by user_id={current_user.get('user_id')} "
        f"(role={current_user.get('role')}) | Title: '{course.title}'"
    )

    if current_user.get("role") != "instructor":
        logger.warning(
            f" [FORBIDDEN] User {current_user.get('user_id')} "
            f"(role={current_user.get('role')}) tried to create a course."
        )
        raise HTTPException(
            status_code=403,
            detail="Only instructors can create courses"
        )

    try:
        db_course = controller.create_course(db, course)
        logger.info(
            f" [SUCCESS] Course created successfully | "
            f"CourseID={db_course.id}, Title='{db_course.title}', "
            f"CreatedBy=user_id={current_user.get('user_id')}"
        )
        return db_course

    except HTTPException as http_err:
        logger.error(
            f" [HTTP ERROR] While creating course | "
            f" User={current_user.get('user_id')} | Error={http_err.detail}"
        )
        raise

    except Exception as e:
        logger.exception(
            f"  [EXCEPTION] Unexpected error while creating course | "
            f"User={current_user.get('user_id')} | Error={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(
        f" [REQUEST] Get courses attempt by user_id={current_user.get('user_id')} "
        f"(role={current_user.get('role')}) | skip={skip}, limit={limit}"
    )

    try:
        courses = controller.get_courses(db, skip=skip, limit=limit)
        logger.info(
            f" [SUCCESS] Fetched {len(courses)} courses | "
            f"RequestedBy=user_id={current_user.get('user_id')}"
        )
        return courses

    except HTTPException as http_err:
        logger.error(
            f" [HTTP ERROR] While fetching courses | "
            f" User={current_user.get('user_id')} | Error={http_err.detail}"
        )
        raise

    except Exception as e:
        logger.exception(
            f"  [EXCEPTION] Unexpected error while fetching courses | "
            f"User={current_user.get('user_id')} | Error={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course_by_id(
    course_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(
        f" [REQUEST] Get course by ID attempt by user_id={current_user.get('user_id')} "
        f"(role={current_user.get('role')}) | CourseID={course_id}"
    )

    try:
        course = controller.getCourseById(db, course_id=course_id)
        if not course:
            logger.warning(
                f" [NOT FOUND] No course found with ID={course_id} | "
                f"RequestedBy=user_id={current_user.get('user_id')}"
            )
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        logger.info(
            f" [SUCCESS] Fetched course | CourseID={course.id}, Title='{course.title}' | "
            f"RequestedBy=user_id={current_user.get('user_id')}"
        )
        return course

    except HTTPException as http_err:
        logger.error(
            f" [HTTP ERROR] While fetching course by ID | "
            f" User={current_user.get('user_id')} | Error={http_err.detail}"
        )
        raise

    except Exception as e:
        logger.exception(
            f"  [EXCEPTION] Unexpected error while fetching course by ID | "
            f"User={current_user.get('user_id')} | Error={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(
        f" [REQUEST] Update course attempt by user_id={current_user.get('user_id')} "
        f"(role={current_user.get('role')}) | CourseID={course_id}"
    )

    if current_user.get("role") != "instructor":
        logger.warning(
            f" [FORBIDDEN] User {current_user.get('user_id')} "
            f"(role={current_user.get('role')}) tried to update a course."
        )
        raise HTTPException(
            status_code=403,
            detail="Only instructors can update courses"
        )

    try:
        updated_course = controller.updateCourse(db, course_id, course_update)
        if not updated_course:
            logger.warning(
                f" [NOT FOUND] No course found with ID={course_id} for update | "
                f"RequestedBy=user_id={current_user.get('user_id')}"
            )
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        logger.info(
            f" [SUCCESS] Course updated successfully | "
            f"CourseID={updated_course.id}, Title='{updated_course.title}', "
            f"UpdatedBy=user_id={current_user.get('user_id')}"
        )
        return updated_course

    except HTTPException as http_err:
        logger.error(
            f" [HTTP ERROR] While updating course | "
            f" User={current_user.get('user_id')} | Error={http_err.detail}"
        )
        raise

    except Exception as e:
        logger.exception(
            f"  [EXCEPTION] Unexpected error while updating course | "
            f"User={current_user.get('user_id')} | Error={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(
        f" [REQUEST] Delete course attempt by user_id={current_user.get('user_id')} "
        f"(role={current_user.get('role')}) | CourseID={course_id}"
    )

    if current_user.get("role") != "instructor":
        logger.warning(
            f" [FORBIDDEN] User {current_user.get('user_id')} "
            f"(role={current_user.get('role')}) tried to delete a course."
        )
        raise HTTPException(
            status_code=403,
            detail="Only instructors can delete courses"
        )

    try:
        course = controller.getCourseById(db, course_id)
        if not course:
            logger.warning(
                f" [NOT FOUND] No course found with ID={course_id} for deletion | "
                f"RequestedBy=user_id={current_user.get('user_id')}"
            )
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        db.delete(course)
        db.commit()

        logger.info(
            f" [SUCCESS] Course deleted successfully | "
            f"CourseID={course_id}, Title='{course.title}', "
            f"DeletedBy=user_id={current_user.get('user_id')}"
        )
        return {"detail": "Course deleted successfully"}

    except HTTPException as http_err:
        logger.error(
            f" [HTTP ERROR] While deleting course | "
            f" User={current_user.get('user_id')} | Error={http_err.detail}"
        )
        raise

    except Exception as e:
        logger.exception(
            f"  [EXCEPTION] Unexpected error while deleting course | "
            f"User={current_user.get('user_id')} | Error={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )