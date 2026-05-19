from fastapi import FastAPI

from database.database import Base, engine
from routes.students import router as students_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API REST de Estudiantes",
    description="API REST  para la gestión de estudiantes con FastAPI y SQLite",
    version="1.0.0"
)


app.include_router(students_router)


@app.get("/")
def home():
    return {
        "message": "API REST de Estudiantes",
        "docs": "http://127.0.0.1:8000/docs",
        "students": "http://127.0.0.1:8000/students",
        "students_average": "http://127.0.0.1:8000/students/average",
        "students_table": "http://127.0.0.1:8000/students/table"
    }
