import asyncio

from sqlalchemy import Column, String, Integer, DateTime, LargeBinary
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import ForeignKey

Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://admin:123@localhost:5432/univ"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
# asyncio.run(init_models())

SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    async with SessionLocal() as session:
        yield session


class Group(Base):
    __tablename__ = 'groups'
    id_group = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    professor_id = Column(Integer, ForeignKey('professors.id_professor'))
    instructor_id = Column(Integer, ForeignKey('instructor.id_instructor'))

    # professor = relationship("Professor", back_populates="groups")
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = 'students'
    id_student = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    enroll_date = Column(DateTime)
    photo = Column(LargeBinary)

    group_id = Column(Integer, ForeignKey('groups.id_group'))
    subjects = relationship("Subject", back_populates="student")


class Instructor(Base):
    __tablename__ = 'instructor'
    id_instructor = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    employ_date = Column(DateTime)
    photo = Column(LargeBinary)

    department_name = Column(String, ForeignKey('department.name'))
    groups = relationship("Group", back_populates="instructors")


class Department(Base):
    __tablename__ = 'department'
    name = Column(String, primary_key=True)

    subjects = relationship("Instructor", back_populates="department")
    instructors = relationship("Instructor", back_populates="department")
    professors = relationship("Professor", back_populates="department")


class Subject(Base):
    __tablename__ = 'subject'
    id_subject = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    department_name = Column(String, ForeignKey('department.name'))
    student = relationship("Student", back_populates="subjects")

class Professor(Base):
    __tablename__ = 'professors'
    id_professor = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)

    department_name = Column(String, ForeignKey('department.name'))
    groups = relationship("Group", back_populates="professor")
