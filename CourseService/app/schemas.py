from pydantic import BaseModel
from typing import Optional, List

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None

class LessonCreate(LessonBase):
        pass


class LessonResponse(LessonBase):
    id: int

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    instructor_id: str

class CourseCreate(CourseBase):
    lessons: List[LessonCreate] = []

class CourseResponse(CourseBase):
    id: int
    lessons: List[LessonResponse] = []
    class Config:
        from_attributes = True


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    instructor_id: Optional[str] = None
    lessons: Optional[List[LessonCreate]] = None

    class Config:
        from_attributes = True

