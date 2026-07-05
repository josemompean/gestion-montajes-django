import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_montajes.settings')
django.setup()

# Importar lo necesario
from django.contrib.auth.models import User
from django.db import connection

def create_superuser():
    # Primero arreglamos la tabla auth_user
    with connection.cursor() as cursor:
        # Asegurarse de que los campos is_reparador e is_montador tengan valores predeterminados
        try:
            cursor.execute("ALTER TABLE auth_user MODIFY COLUMN is_reparador TINYINT(1) NOT NULL DEFAULT 0")
            cursor.execute("ALTER TABLE auth_user MODIFY COLUMN is_montador TINYINT(1) NOT NULL DEFAULT 0")
            print("Campos is_reparador e is_montador configurados correctamente.")
        except Exception as e:
            print(f"Error al configurar campos: {e}")
    
    # Crear el superusuario directamente en la base de datos
    try:
        with connection.cursor() as cursor:
            # Verificar si el usuario admin ya existe
            cursor.execute("SELECT id FROM auth_user WHERE username = 'admin'")
            if cursor.fetchone():
                print("El usuario 'admin' ya existe, actualizando contraseña y privilegios...")
                # Actualizar el usuario existente para que sea superusuario
                cursor.execute("""
                    UPDATE auth_user 
                    SET is_superuser = 1, is_staff = 1, is_active = 1, 
                        password = 'pbkdf2_sha256$600000$NxfKADdzOHQ1yAF7KKdkTw$EX79yBHQWFXa9NLc/4UpYQsdDt7BzpNsXUE31V72bvA=' 
                    WHERE username = 'admin'
                """)
                print("Usuario 'admin' actualizado con contraseña 'admin123'")
            else:
                print("Creando usuario 'admin'...")
                # Insertar nuevo usuario (contraseña es 'admin123' hasheada)
                cursor.execute("""
                    INSERT INTO auth_user 
                    (username, password, is_superuser, is_staff, is_active, first_name, last_name, email, date_joined, is_reparador, is_montador)
                    VALUES 
                    ('admin', 'pbkdf2_sha256$600000$NxfKADdzOHQ1yAF7KKdkTw$EX79yBHQWFXa9NLc/4UpYQsdDt7BzpNsXUE31V72bvA=', 1, 1, 1, '', '', 'admin@example.com', NOW(), 0, 0)
                """)
                print("Usuario 'admin' creado con contraseña 'admin123'")
    except Exception as e:
        print(f"Error al crear/actualizar usuario: {e}")

if __name__ == "__main__":
    create_superuser()
    print("Proceso completado.") 