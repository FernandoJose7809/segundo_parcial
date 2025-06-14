# 📘 Segundo Parcial – Sistema de Gestión Académica con Predicción de Notas

## 📦 Docker 

Se creó una carpeta llamada `docker/` que contiene los `Dockerfile` para el **backend** y el **frontend**.

Además, se añadió un archivo `.sh` que ejecuta automáticamente los siguientes comandos al iniciar el contenedor:

* `makemigrations` y `migrate` para aplicar cambios al modelo.
* Creación automática de un superusuario si no existe.

También se modificó el archivo `docker-compose.yml`:

* Se cambió el puerto por defecto de PostgreSQL de `5432` a `5433` para evitar conflictos.

---

## ⚙️ Entorno `.env`

Se configuró un archivo `.env` para centralizar variables sensibles y facilitar el despliegue:

* Configuración de la base de datos.
* Credenciales del superusuario.
* Secret key y otros parámetros de entorno.

---

## 🧱 Estructura del Backend

El backend se encuentra en `Backend/app/`, y está dividido en aplicaciones lógicas:

```
Backend/
└── app/
    ├── grade/
    ├── group/
    ├── queter/
    ├── students/
    ├── subjects/
    └── teacher/
```

### 📂 Descripción de Aplicaciones y Modelos

#### `grade/`

* `Grade`: Representa el año escolar (ej. 2024, 2025).
* `StudentCourse`: Relaciona estudiantes con un año escolar.
* `DegreeSubject`: Define las materias asignadas por año escolar.

#### `group/`

* `Group`: Cursos o paralelos dentro de un año escolar.
* `GroupTeacher`: Asocia un profesor con una materia y un grupo.

#### `queter/`

* `Quetar`: Define los trimestres o periodos académicos con fechas de inicio y fin.
* `FollowUp`: Registra el rendimiento académico del estudiante: asistencia, tareas, presentaciones y exámenes.

#### `students/`

* `Student`: Contiene información personal del estudiante.

#### `subjects/`

* `Subject`: Lista de materias del colegio.

#### `teacher/`

* `Teacher`: Información personal del docente.
* `TeacherSubject`: Materias que cada docente está autorizado a impartir.

---

## 🔄 Serializers y CRUDs

Cada modelo cuenta con su correspondiente `serializer` para permitir la comunicación entre el backend y el frontend mediante API REST.

Se implementaron operaciones CRUD básicas, aunque en algunos modelos no es necesario implementar todos los métodos (por ejemplo, en relaciones intermedias).

---

## 🤖 Predicción de Notas (Machine Learning)

Se planea agregar un módulo de Machine Learning para predecir la **posible nota final** de un estudiante en una materia específica, en función de su rendimiento académico (tareas, presentaciones, exámenes, etc.).

* El modelo será entrenado con un dataset ya disponible.
* Se utilizará **Random Forest** en lugar de regresión lineal múltiple por su mejor capacidad de generalización.
* El entrenamiento se realizará en **Jupyter Notebook** y se exportará como archivo `.pkl`.
* Desde Django, se cargará el modelo para hacer predicciones en una vista específica.

También se contempla la posibilidad de **reentrenar el modelo** periódicamente con nuevos datos.

---

## 🗃️ Diagrama de Base de Datos

![Diagrama de la BD](DiagramBD.png)

# Nuevos Cambios
El contendido en el archivo group ha sido eliminado y todo lo que tendia se ha llevado 
