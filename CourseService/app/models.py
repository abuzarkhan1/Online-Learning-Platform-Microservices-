from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.config.database import Base

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    price = Column(Float)
    instructor_id  = Column(String, nullable=False)
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course", back_populates="lessons")