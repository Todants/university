import math

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from src.models import Group, Instructor, Student
from collections import defaultdict

MAX_STUDENTS_PER_GROUP = 1


async def balance_groups_task(department_id: int, db: Session, queue):
    balance_info = balance_groups(department_id, db)
    await queue.put(balance_info)


def balance_groups(department_id: int, db: Session):
    students = db.execute(select(Student).filter(Student.department_id == department_id)).scalars().all()
    instructors = db.execute(select(Instructor).filter(Instructor.department_id == department_id)).scalars().all()

    num_students = len(students)
    num_instructors = len(instructors)

    if num_instructors == 0:
        raise ValueError("No instructors in the department")

    A = math.ceil(num_students / MAX_STUDENTS_PER_GROUP)
    B = min(num_students, num_instructors)
    num_groups = max(A, B)

    students_per_group = math.ceil(num_students / num_groups)
    groups_per_instructor = math.ceil(num_groups / num_instructors)

    groups_to_delete = db.query(Group).options(joinedload(Group.students)).join(Instructor, Group.instructor_id == Instructor.id).filter(Instructor.department_id == department_id).all()

    for student in students:
        student.group_id = None

    for group in groups_to_delete:
        db.delete(group)

    for i in range(num_groups):
        instructor = instructors[i // groups_per_instructor]
        group = Group(name=f"Group {i + 1}", instructor_id=instructor.id)
        db.add(group)

    db.commit()

    groups = db.execute(
        select(Group)
        .join(Instructor, Group.instructor_id == Instructor.id)
        .filter(Instructor.department_id == department_id)
    ).scalars().all()
    for idx, student in enumerate(students):
        student.group_id = groups[idx % len(groups)].id

    db.commit()

    instructors_groups = defaultdict(list)
    for gr in groups:
        instructors_groups[gr.instructor_id].append(gr.name)

    return [{
            "id": instructor.id,
            "names": f"{instructor.first_name} {instructor.last_name}",
            "groups": ", ".join(instructors_groups[instructor.id]),
        } for instructor in instructors
    ]


if __name__ == '__main__':
    from database import get_sync_db
    from fastapi import Depends

    df = Depends(get_sync_db)
    balance_groups(2, df)
