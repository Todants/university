from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.balance import balance_groups
from src.database import get_async_db, get_sync_db
from src.models import Student, Instructor, Department
from src.schemas import StudentCreate, InstructorCreate
from starlette.background import BackgroundTask

app = FastAPI()


@app.post("/students/")
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_async_db), sync_db: Session = Depends(get_sync_db)):
    result = await db.execute(select(Department).filter(Department.id == student.department_id))
    department = result.scalars().first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    result = await db.execute(select(Instructor).filter(Instructor.department_id == student.department_id))
    instructors = result.scalars().all()
    if not instructors:
        raise HTTPException(status_code=400, detail="No instructors in the department")

    new_student = Student(**student.dict())
    db.add(new_student)
    await db.commit()

    balance_data = balance_groups(student.department_id)
    return {"student": new_student, "balance_data": balance_data}


@app.post("/instructors/")
async def create_instructor(
        instructor: InstructorCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_async_db),
):
    print(db, type(db))
    result = await db.execute(select(Department).filter(Department.id == instructor.department_id))
    department = result.scalars().first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    new_instructor = Instructor(**instructor.dict())
    db.add(new_instructor)
    await db.commit()

    balance_data = balance_groups(instructor.department_id)
    return {"instructor": new_instructor, "balance_data": balance_data}

from fastapi.websockets import WebSocket


@app.websocket("/ws/balance")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        balance_info = ...
        await websocket.send_json(balance_info)