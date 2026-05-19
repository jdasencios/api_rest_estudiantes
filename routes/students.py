from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.student import Student, StudentCreate, StudentUpdate, StudentResponse


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.dni == student.dni).first()

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un estudiante con ese DNI."
        )

    new_student = Student(
        dni=student.dni,
        name=student.name,
        age=student.age,
        grade=student.grade,
        is_approved=student.is_approved,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


@router.get("/students/average")
def get_students_average(db: Session = Depends(get_db)):
    average_grade = db.query(func.avg(Student.grade)).scalar()

    if average_grade is None:
        return {
            "average_grade": 0,
            "message": "No hay estudiantes registrados."
        }

    return {
        "average_grade": round(average_grade, 2)
    }


@router.get(
    "/students/table",
    response_class=HTMLResponse
)
def get_students_table(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return templates.TemplateResponse(
        "partials/students_table.html",
        {
            "request": request,
            "students": students
        }
    )


@router.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )

    return student


@router.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )

    student_with_same_dni = db.query(Student).filter(
        Student.dni == student_data.dni,
        Student.id != student_id
    ).first()

    if student_with_same_dni:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe otro estudiante con ese DNI."
        )

    student.dni = student_data.dni
    student.name = student_data.name
    student.age = student_data.age
    student.grade = student_data.grade
    student.is_approved = student_data.is_approved
    student.updated_at = datetime.now()

    db.commit()
    db.refresh(student)

    return student


@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Estudiante eliminado correctamente."
    }


@router.post(
    "/students/bulk",
    status_code=status.HTTP_201_CREATED
)
def create_students_bulk(
    students: list[StudentCreate],
    db: Session = Depends(get_db)
):
    created_students = []
    dni_enviados = set()

    for student in students:
        if student.dni in dni_enviados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El DNI {student.dni} está duplicado en la carga masiva."
            )

        dni_enviados.add(student.dni)

        existing_student = db.query(Student).filter(Student.dni == student.dni).first()

        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un estudiante con el DNI {student.dni}."
            )

        now = datetime.now()
        new_student = Student(
            dni=student.dni,
            name=student.name,
            age=student.age,
            grade=student.grade,
            is_approved=student.is_approved,
            created_at=now,
            updated_at=now
        )

        db.add(new_student)
        created_students.append(new_student)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al insertar estudiantes. Verifique que los DNI sean únicos."
        )

    for student in created_students:
        db.refresh(student)

    return {
        "message": "Estudiantes creados correctamente.",
        "total": len(created_students),
        "students": created_students
    }
