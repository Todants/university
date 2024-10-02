from pydantic import BaseModel

class DepartmentModel(BaseModel):
    name : str


class ProfessorModel(BaseModel):
    name : str
    department_name: str


class StudentModel(BaseModel):
    name : str
    department_name: str
