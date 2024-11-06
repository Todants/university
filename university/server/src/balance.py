import math

from fastapi import Depends
from sqlalchemy.orm import Session
from src.models import Group, Instructor, Student
from src.database import get_sync_db

MAX_STUDENTS_PER_GROUP = 10


def balance_groups(department_id: int, db: Session = Depends(get_sync_db)):
    print(db, type(db))
    students = db.query(Student).filter(Student.department_id == department_id).all()
    instructors = db.query(Instructor).filter(Instructor.department_id == department_id).all()

    num_students = len(students)
    num_instructors = len(instructors)

    if num_instructors == 0:
        raise ValueError("No Instructors")

    A = math.ceil(num_students / MAX_STUDENTS_PER_GROUP)
    B = min(num_students, num_instructors)
    num_groups = max(A, B)

    students_per_group = math.ceil(num_students / num_groups)
    groups_per_instructor = math.ceil(num_groups / num_instructors)

    for group in db.query(Group).filter(Group.department_id == department_id):
        if not group.students:
            db.delete(group)

    for i in range(num_groups):
        group = Group(name=f"Group {i + 1}", department_id=department_id)
        db.add(group)

    db.commit()

    groups = db.query(Group).filter(Group.department_id == department_id).all()
    for idx, student in enumerate(students):
        group = groups[idx // students_per_group]
        student.group_id = group.id

    db.commit()
    return {"num_groups": num_groups, "students_per_group": students_per_group,
            "groups_per_instructor": groups_per_instructor}
