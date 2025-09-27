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
        db_course = controller.get_course(db, course)
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
