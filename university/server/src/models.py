from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    instructors = relationship('Instructor', back_populates='department')
    subjects = relationship('Subject', back_populates='department')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='subjects')


class Instructor(Base):
    __tablename__ = 'instructors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    employ_date = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='instructors')
    groups = relationship('Group', back_populates='instructor')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    enroll_date = Column(DateTime, default=func.now())
    group_id = Column(Integer, ForeignKey('groups.id'), default=None)
    department_id = Column(Integer, ForeignKey('departments.id'))

    group = relationship('Group', back_populates='students')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructor_id = Column(Integer, ForeignKey('instructors.id'))

    instructor = relationship('Instructor', back_populates='groups')
    students = relationship('Student', back_populates='group')
