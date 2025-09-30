from pydantic import BaseModel
from typing import Optional, List

# -------------------------------
# Lessons
# -------------------------------


class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    class Config:
        from_attributes = True

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# -------------------------------
# Courses
# -------------------------------
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float

class CourseCreate(CourseBase):
    lessons: List[LessonCreate] = []

class CourseResponse(CourseBase):
    id: int
    instructor_id: str
    lessons: List[LessonResponse] = []
    class Config:
        from_attributes = True

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    lessons: Optional[List[LessonCreate]] = None
    class Config:
        from_attributes = True
