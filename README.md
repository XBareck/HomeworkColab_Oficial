[README.md](https://github.com/user-attachments/files/33470821/README.md)
# HomeworkColab

**Plataforma web colaborativa para la gestión y retroalimentación de tareas académicas.**

HomeworkColab centraliza y formaliza algo que hoy ocurre de manera informal entre estudiantes —compartir trabajos, comentarlos y ayudarse entre pares— a través de chats y redes sociales. El resultado es contenido desordenado, información que se pierde y nula posibilidad de filtrar o encontrar material de calidad.

La plataforma ofrece un repositorio académico organizado por asignaturas y categorías, con retroalimentación estructurada entre estudiantes, en una interfaz simple y accesible desde cualquier dispositivo.

> Proyecto de título — Ingeniería en Informática, IP Santo Tomás (2025).

## Características principales

- **Repositorio de trabajos**: subida y almacenamiento de tareas/informes, clasificados por categoría (asignatura) y etiquetas.
- **Búsqueda y filtrado**: localización rápida de contenido por título, categoría o palabras clave.
- **Retroalimentación entre pares**: sistema de comentarios y sugerencias sobre cada trabajo publicado.
- **Autenticación segura**: registro e inicio de sesión para proteger el acceso a la plataforma.
- **Interfaz responsive**: diseño adaptable a escritorio y móvil, construido con Bootstrap.

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python, Django (Flask como alternativa secundaria) |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Base de datos | SQLite (desarrollo/pruebas) · MySQL (producción) |
| Testing | pytest (pruebas unitarias y funcionales) |
| Metodología | XP (Extreme Programming) |

## Modelo de datos

La aplicación gira en torno a cinco entidades principales:

- **Usuario** — estudiante registrado en la plataforma.
- **Trabajo** — tarea o informe subido por un usuario, asociado a una categoría.
- **Categoría** — clasificación temática de los trabajos (ej. Programación, Base de Datos, Cálculo).
- **Comentario** — retroalimentación de un usuario sobre un trabajo.
- **Etiqueta** — palabra clave para facilitar la búsqueda y el filtrado.

## Casos de uso clave

| ID | Caso de uso | Descripción |
|---|---|---|
| CU-1 | Subir nuevo trabajo | El estudiante sube un trabajo con título, descripción, categoría y archivo adjunto. |
| CU-2 | Buscar contenido | El estudiante busca y filtra trabajos por título, etiqueta o categoría. |
| CU-3 | Comentar y colaborar | El estudiante retroalimenta un trabajo mediante comentarios y sugerencias. |
| CU-4 | Autenticación segura | Registro e inicio de sesión con validación de credenciales. |

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/XBareck/HomeworkColab.git
cd HomeworkColab

# 2. Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones (crea la base de datos SQLite local)
python manage.py migrate

# 5. Levantar el servidor de desarrollo
python manage.py runserver
```

La aplicación quedará disponible en `http://127.0.0.1:8000/`.

> Ajusta los nombres de archivo/comandos anteriores si tu proyecto usa una estructura distinta (por ejemplo, si el entry point no es `manage.py`).

## Pruebas

```bash
pytest
```

## Autor

**Tomás Hernández** — Ingeniero Informático
[github.com/XBareck](https://github.com/XBareck)
