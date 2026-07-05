import os
import django

# Configuración para usar el ORM de Django fuera de un proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_montajes.settings')
django.setup()

# Importamos lo que necesitamos
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def fix_user_table():
    """Arregla la tabla de usuarios para que los campos is_reparador e is_montador tengan valores predeterminados."""
    with connection.cursor() as cursor:
        # Añadir valores predeterminados a los campos is_reparador e is_montador
        cursor.execute("ALTER TABLE auth_user MODIFY COLUMN is_reparador TINYINT(1) NOT NULL DEFAULT 0")
        cursor.execute("ALTER TABLE auth_user MODIFY COLUMN is_montador TINYINT(1) NOT NULL DEFAULT 0")
    
    print("Tabla de usuarios arreglada correctamente.")

def create_superuser():
    """Crea un superusuario si no existe."""
    if not User.objects.filter(username='admin').exists():
        try:
            User.objects.create(
                username='admin',
                email='admin@example.com',
                password=make_password('admin123'),
                is_staff=True,
                is_active=True,
                is_superuser=True
            )
            print("Superusuario 'admin' creado correctamente con contraseña 'admin123'.")
        except Exception as e:
            print(f"Error al crear superusuario: {e}")
    else:
        print("El superusuario 'admin' ya existe.")

if __name__ == "__main__":
    try:
        fix_user_table()
        create_superuser()
        print("Proceso completado con éxito.")
    except Exception as e:
        print(f"Error general: {e}") 