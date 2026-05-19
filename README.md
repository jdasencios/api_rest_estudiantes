# api_rest_estudiantes
instalación:
1. inicializar
   uv init

2. instalar fastapi:
   uv add "fastapi[standard]"
3. Activar entorno virtual
   source .venv/scripts/activate

4. Instalar dependencias  
   pip install fastapi uvicorn sqlalchemy jinja2 pydantic

5. Ejecutar el proyecto
    uvicorn main:app --reload   



# Endpoints principales

Método	Ruta	Descripción

POST	/students	Crear un estudiante

GET	/students	Obtener todos los estudiantes

GET	/students/{id}	Obtener estudiante por ID

PUT	/students/{id}	Actualizar estudiante

DELETE	/students/{id}	Eliminar estudiante

POST	/students/bulk	Crear estudiantes de forma masiva

GET	/students/average	Obtener promedio de notas

GET	/students/table	Renderizar tabla HTML parcial

# Modelo de estudiante

{
  "id": 1,
  "dni": "12345678",
  "name": "Juan Pérez",
  "age": 20,
  "grade": 15.5,
  "is_approved": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

# Crear estudiante

curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"dni":"12345678","name":"Juan Pérez","age":20,"grade":15.5,"is_approved":true}'

# Obtener todos los estudiantes

curl http://127.0.0.1:8000/students

# Obtener estudiante por ID

curl http://127.0.0.1:8000/students/1

# Actualizar estudiante

curl -X PUT http://127.0.0.1:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"dni":"12345678","name":"Juan Pérez Actualizado","age":21,"grade":17.5,"is_approved":true}'

 # Eliminar estudiante 

 curl -X DELETE http://127.0.0.1:8000/students/1

 # Crear estudiantes de forma masiva

 curl -X POST http://127.0.0.1:8000/students/bulk \
  -H "Content-Type: application/json" \
  -d '[
    {"dni":"11111111","name":"Ana Torres","age":19,"grade":18.5,"is_approved":true},
    {"dni":"22222222","name":"Luis Ramos","age":22,"grade":13.5,"is_approved":false},
    {"dni":"33333333","name":"María López","age":20,"grade":16.0,"is_approved":true}
  ]'
  
# Obtener promedio de notas

curl http://127.0.0.1:8000/students/average

# Obtener tabla HTML parcial

curl http://127.0.0.1:8000/students/table

# Prueba con navegador

http://127.0.0.1:8000

# La base de datos SQLite se crea automáticamente al ejecutar el proyecto por primera vez.

students.db
