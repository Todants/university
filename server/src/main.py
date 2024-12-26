import asyncio
from collections import defaultdict

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.database import get_async_db, get_sync_db
from src.models import Student, Instructor, Department, Group
from src.schemas import StudentCreate, InstructorCreate
from starlette.websockets import WebSocketDisconnect
from src.balance import balance_groups_task

app = FastAPI()

balance_update_queue = asyncio.Queue()


@app.post("/students/")
async def create_student(
        student: StudentCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_async_db),
        sync_db: Session = Depends(get_sync_db)
):
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

    background_tasks.add_task(balance_groups_task, student.department_id, sync_db, balance_update_queue)
    return {"student": new_student}


@app.post("/instructors/")
async def create_instructor(
        instructor: InstructorCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_async_db),
        sync_db: Session = Depends(get_sync_db)
):
    result = await db.execute(select(Department).filter(Department.id == instructor.department_id))
    department = result.scalars().first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    new_instructor = Instructor(**instructor.dict())
    db.add(new_instructor)
    await db.commit()

    background_tasks.add_task(balance_groups_task, instructor.department_id, sync_db, balance_update_queue)
    return {"instructor": new_instructor}


@app.get("/instructors/")
async def get_instructor(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Instructor))
    instructors = result.scalars().all()
    result = await db.execute(select(Group))
    groups = result.scalars().all()

    instructors_groups = defaultdict(list)
    for gr in groups:
        instructors_groups[gr.instructor_id].append(gr.name)

    return [{
            "id": instructor.id,
            "names": f"{instructor.first_name} {instructor.last_name}",
            "groups": ", ".join(instructors_groups[instructor.id]),
        } for instructor in instructors
    ]


from fastapi.websockets import WebSocket


@app.websocket("/ws/balance")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            balance_info = await balance_update_queue.get()
            print(balance_info)
            await websocket.send_json(balance_info)
    except WebSocketDisconnect:
        print("client disconnected")
