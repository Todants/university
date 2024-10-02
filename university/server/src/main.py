from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from src.db import Student, Professor, Department, Group, get_db
from src.models import DepartmentModel, ProfessorModel, StudentModel

Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://postres:123@localhost:5432/univ"
engine = create_async_engine(DATABASE_URL)


app = FastAPI()

SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# from balancer import balance_students_and_groups

app = FastAPI()

@app.post("/departments/")
async def create_department(department: DepartmentModel, db: AsyncSession = Depends(get_db)):
    new_department = Department(
        name=department.name
    )
    db.add(new_department)
    await db.commit()
    return new_department


@app.get("/departments/{department_name}")
async def get_department(department_name: str, db: AsyncSession = Depends(get_db)):
    department = await db.get(Department, department_name)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@app.get("/departments/")
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department))
    departments = result.scalars().all()
    return departments


@app.put("/departments/{department_name}")
async def update_department(department_name: str, new_name: str, db: AsyncSession = Depends(get_db)):
    department = await db.get(Department, department_name)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    department.name = new_name
    await db.commit()
    return department


@app.delete("/departments/{department_name}")
async def delete_department(department_name: str, db: AsyncSession = Depends(get_db)):
    department = await db.get(Department, department_name)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    await db.delete(department)
    await db.commit()
    return {"message": "Department deleted successfully"}


@app.post("/professors/")
async def create_professor(professor: ProfessorModel, db: AsyncSession = Depends(get_db)):

    department = await db.get(Department, professor.department_name)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    new_professor = Professor(
        name=professor.name,
        department_name=professor.department_name,
    )
    db.add(new_professor)
    await db.commit()

    # await rebalance_groups(db, professor.department_name)

    return new_professor


@app.get("/professors/{professor_id}")
async def get_professor(professor_id: int, db: AsyncSession = Depends(get_db)):
    professor = await db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@app.get("/professors/")
async def get_all_professors(department_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Professor).where(Professor.department_name == department_name))
    professors = result.scalars().all()
    return professors


@app.put("/professors/{professor_id}")
async def update_professor(professor_id: int, professor_update, db: AsyncSession = Depends(get_db)):
    professor = await db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    professor.name = professor_update.name or professor.name
    professor.department_name = professor_update.department_name or professor.department_name
    await db.commit()

    # await rebalance_groups(db, professor.department_name)
    return professor


@app.delete("/professors/{professor_id}")
async def delete_professor(professor_id: int, db: AsyncSession = Depends(get_db)):
    professor = await db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    # Reassign groups to other professors before deletion
    # await reassign_groups_on_professor_removal(professor, db)

    await db.delete(professor)
    await db.commit()

    # await rebalance_groups(db, professor.department_name)
    return {"message": "Professor deleted successfully"}


@app.post("/students/")
async def create_student(student: StudentModel, db: AsyncSession = Depends(get_db)):
    # Ensure department exists and has professors
    department = await db.get(Department, student.department_name)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    professors = (await db.execute(select(Professor).where(Professor.department_name == student.department_name))).scalars().all()
    if not professors:
        raise HTTPException(status_code=400, detail="No professors available in this department")

    new_student = Student(
        first_name=student.first_name,
        last_name = student.last_name,
        birth_date = student.birth_date,
        enroll_date = student.enroll_date,
        photo = student.photo,
        group_id=None
    )
    db.add(new_student)
    await db.commit()

    # Rebalance groups
    # await rebalance_groups(db, student.department_name)

    return new_student


@app.get("/students/{student_id}")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students/")
async def get_all_students(department_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.department_name == department_name))
    students = result.scalars().all()
    return students


@app.put("/students/{student_id}")
async def update_student(student_id: int, student_update, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = student_update.name or student.name
    student.department_name = student_update.department_name or student.department_name
    await db.commit()

    # await rebalance_groups(db, student.department_name)
    return student


@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()

    # await rebalance_groups(db, student.department_name)
    return {"message": "Student deleted successfully"}


async def rebalance_groups(db: AsyncSession, department_name: str):
    # Get all professors and students in the department
    professors = (await db.execute(select(Professor).where(Professor.department_name == department_name))).scalars().all()
    students = (await db.execute(select(Student).where(Student.department_name == department_name))).scalars().all()

    # Call the balancing function
    groups = balance_students_and_groups(professors, students)

    # Apply the new group assignments
    for group_data in groups:
         group = Group(professor_id=group_data['professor_id'])
         db.add(group)
         for student in group_data['students']:
             student.group_id = group.id

    await db.commit()