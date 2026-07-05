# Gestión de Montajes - Django

Aplicación web desarrollada con **Django** para la gestión de montajes e instalaciones de equipos.

El proyecto permite registrar montajes, consultar su estado, gestionar usuarios, revisar el historial de trabajos realizados y visualizar estadísticas generales desde una interfaz web.

Este proyecto fue desarrollado como proyecto académico durante el ciclo de **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

## Funcionalidades

- Registro e inicio de sesión de usuarios.
- Gestión de montajes e instalaciones.
- Seguimiento del estado de los montajes.
- Historial de trabajos realizados.
- Dashboard principal.
- Estadísticas generales del sistema.
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

## Capturas del proyecto

### Panel principal de montajes

![Panel principal de montajes](docs/img/listado-montajes.png)

### Detalle de un montaje

![Detalle de un montaje](docs/img/detalle-montaje.png)

### Dashboard de estadísticas

![Dashboard de estadísticas](docs/img/dashboard-estadisticas.png)

### Estadísticas por montador

![Estadísticas por montador](docs/img/estadisticas-montador.png)

### Historial de montajes finalizados

![Historial de montajes finalizados](docs/img/montajes-finalizados.png)

## Instalación y ejecución

Para ejecutar el proyecto en local, se pueden seguir estos pasos:

### 1. Clonar el repositorio

```bash
git clone https://github.com/josemompean/gestion-montajes-django.git
cd gestion-montajes-django
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual en Windows

```bash
venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar la base de datos

El proyecto utiliza **MySQL**. Es necesario configurar los datos de conexión en el archivo `settings.py`.

### 6. Aplicar las migraciones

```bash
python manage.py migrate
```

### 7. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor

```bash
python manage.py runserver
```

### 9. Abrir la aplicación en el navegador

```text
http://127.0.0.1:8000/
```

## Estructura del proyecto

- `gestion_montajes/`: configuración principal del proyecto Django.
- `montajes/`: aplicación principal de gestión de montajes.
- `staticfiles/`: archivos estáticos del proyecto.
- `docs/img/`: capturas utilizadas en la documentación.
- `manage.py`: archivo principal de administración de Django.
- `requirements.txt`: dependencias del proyecto.
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