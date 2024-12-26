from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InstructorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime


class InstructorCreate(InstructorBase):
    department_id: int


class InstructorResponse(InstructorBase):
    id: int
    employ_date: datetime
    department_id: int


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime


class StudentCreate(StudentBase):
    department_id: int


class StudentResponse(StudentBase):
    id: int
    enroll_date: datetime
    group_id: Optional[int]
    department_id: int
