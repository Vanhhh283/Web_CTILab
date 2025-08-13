from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///lab.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    student_id = Column(String)
    email = Column(String)
    phone = Column(String)
    supervisor = Column(String)
    program = Column(String)
    k = Column(String) 
    research_topic = Column(String)

    schedules = relationship("StudentSchedule", back_populates="student", cascade="all, delete")

class StudentSchedule(Base):
    __tablename__ = "student_schedules"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    title = Column(String)        
    description = Column(String)     
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)

    student = relationship("Student", back_populates="schedules")

Base.metadata.create_all(engine)
