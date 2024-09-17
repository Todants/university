from sqlalchemy import create_engine, Column, String, Integer, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey

Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/univ"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)


class Group(Base):
    __tablename__ = 'group'
    name = Column(String, primary_key=True)

    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    enroll_date = Column(DateTime)
    photo = Column(LargeBinary)
    group_name = Column(String, ForeignKey('group.name'))

    group = relationship("Group", back_populates="students")
    subjects = relationship("Subject", back_populates="student")


class Instructor(Base):
    __tablename__ = 'instructor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    employ_date = Column(DateTime)
    photo = Column(LargeBinary)

    department_name = Column(String, ForeignKey('department.name'))
    department = relationship("Department", back_populates="instructors")


class Department(Base):
    __tablename__ = 'department'
    name = Column(String, primary_key=True)

    instructors = relationship("Instructor", back_populates="department")


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", back_populates="subjects")
