from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel


class Group(BaseModel):
    name : str


class StudentModel(BaseModel):
    first_name : str
    last_name : str
    birth_date : datetime
    enroll_date : datetime
    # photo : UploadFile
    department_name : str


class InstructorModel(BaseModel):
    first_name : str
    last_name : str
    birth_date : datetime
    employ_date : datetime
    photo : UploadFile


class DepartmentModel(BaseModel):
    name : str


class SubjectModel(BaseModel):
    name : str


class ProfessorModel(BaseModel):
    name : str
    department_name: str

