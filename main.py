from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from database.database import Base, engine
from routes.students import router as students_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API REST de Estudiantes",
    description="API REST  para la gestión de estudiantes con FastAPI y SQLite",
    version="1.0.0"
)


templates = Jinja2Templates(directory="templates")


app.include_router(students_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )