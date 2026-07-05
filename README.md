```md
# Gestión de Montajes - Django

Aplicación web desarrollada con **Django** para la gestión de montajes e instalaciones.

El proyecto permite registrar montajes, consultar su estado, gestionar usuarios, revisar el historial de trabajos y visualizar estadísticas generales.

Este proyecto fue desarrollado como proyecto académico durante el ciclo de **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

## Funcionalidades

- Registro e inicio de sesión de usuarios.
- Gestión de montajes e instalaciones.
- Seguimiento del estado de los montajes.
- Historial de trabajos realizados.
- Dashboard principal.
- Estadísticas del sistema.
- Gestión de usuarios.
- Interfaz web responsive.

## Tecnologías utilizadas

- Python
- Django
- MySQL
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Git y GitHub

## Instalación y ejecución

Para ejecutar el proyecto en local, se pueden seguir estos pasos:

1. Clonar el repositorio:

`git clone https://github.com/josemompean/gestion-montajes-django.git`

2. Entrar en la carpeta del proyecto:

`cd gestion-montajes-django`

3. Crear un entorno virtual:

`python -m venv venv`

4. Activar el entorno virtual en Windows:

`venv\Scripts\activate`

5. Instalar las dependencias:

`pip install -r requirements.txt`

6. Configurar la base de datos MySQL en el archivo `settings.py`.

7. Aplicar las migraciones:

`python manage.py migrate`

8. Crear un superusuario:

`python manage.py createsuperuser`

9. Ejecutar el servidor:

`python manage.py runserver`

10. Abrir la aplicación en el navegador:

`http://127.0.0.1:8000/`

## Estructura del proyecto

- `gestion_montajes/`: configuración principal del proyecto Django.
- `montajes/`: aplicación principal de gestión de montajes.
- `manage.py`: archivo principal de administración de Django.
- `requirements.txt`: dependencias del proyecto.
- `README.md`: documentación del proyecto.
- `.gitignore`: archivos y carpetas excluidos del repositorio.

## Objetivo del proyecto

El objetivo de este proyecto es aplicar conocimientos de desarrollo web con Django, gestión de bases de datos, autenticación de usuarios, plantillas HTML, estilos CSS y organización de un proyecto backend.

## Aprendizajes aplicados

Durante el desarrollo de este proyecto se trabajaron conceptos como:

- Desarrollo web con Django.
- Modelado de datos.
- Gestión de usuarios y autenticación.
- Conexión con base de datos MySQL.
- Creación de vistas, formularios y plantillas.
- Uso de HTML, CSS y JavaScript.
- Organización de archivos estáticos.
- Control de versiones con Git y GitHub.

## Autor

**José Mompeán Roca**  
Desarrollador Junior | Soporte IT
