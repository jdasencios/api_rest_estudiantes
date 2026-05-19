from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.database import Base, engine
from routes.students import router as students_router


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API REST de Estudiantes",
    description="API REST básica para la gestión de estudiantes con FastAPI y SQLite",
    version="1.0.0"
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app.include_router(students_router)


@app.get("/")
def home():
    """
    Endpoint raíz simple.
    Devuelve JSON para evitar errores por plantillas en la ruta principal.
    """
    return {
        "message": "API REST de Estudiantes funcionando correctamente",
        "docs": "/docs",
        "students": "/students",
        "students_table": "/students/table",
        "web_page": "/web"
    }


@app.get("/web", response_class=HTMLResponse)
def web_page(request: Request):
    """
    Página HTML mínima para probar HTMX.
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
