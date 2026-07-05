import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_montajes.settings')
django.setup()

# Importar lo necesario
from django.db import connection

def check_and_create_tables():
    with connection.cursor() as cursor:
        # Verificar si existe la tabla auth_user_user_permissions
        cursor.execute("SHOW TABLES LIKE 'auth_user_user_permissions'")
        if not cursor.fetchone():
            print("Creando tabla auth_user_user_permissions...")
            cursor.execute("""
                CREATE TABLE `auth_user_user_permissions` (
                    `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `user_id` bigint NOT NULL,
                    `permission_id` int NOT NULL,
                    UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`, `permission_id`),
                    CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
                    CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
                )
            """)
            print("Tabla auth_user_user_permissions creada.")
        else:
            print("La tabla auth_user_user_permissions ya existe.")
        
        # Verificar si existe la tabla auth_user_groups
        cursor.execute("SHOW TABLES LIKE 'auth_user_groups'")
        if not cursor.fetchone():
            print("Creando tabla auth_user_groups...")
            cursor.execute("""
                CREATE TABLE `auth_user_groups` (
                    `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `user_id` bigint NOT NULL,
                    `group_id` int NOT NULL,
                    UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`, `group_id`),
                    CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
                    CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
                )
            """)
            print("Tabla auth_user_groups creada.")
        else:
            print("La tabla auth_user_groups ya existe.")
        
        # Verificar campo fecha_inicio en montajes_montaje
        cursor.execute("SHOW COLUMNS FROM `montajes_montaje` LIKE 'fecha_inicio'")
        if not cursor.fetchone():
            print("Creando campo fecha_inicio en montajes_montaje...")
            cursor.execute("ALTER TABLE `montajes_montaje` ADD COLUMN `fecha_inicio` datetime(6) NULL")
            print("Campo fecha_inicio creado.")
        else:
            print("El campo fecha_inicio ya existe en montajes_montaje.")
        
        # Verificar campo fecha_finalizacion en montajes_montaje
        cursor.execute("SHOW COLUMNS FROM `montajes_montaje` LIKE 'fecha_finalizacion'")
        if not cursor.fetchone():
            print("Creando campo fecha_finalizacion en montajes_montaje...")
            cursor.execute("ALTER TABLE `montajes_montaje` ADD COLUMN `fecha_finalizacion` datetime(6) NULL")
            print("Campo fecha_finalizacion creado.")
        else:
            print("El campo fecha_finalizacion ya existe en montajes_montaje.")

if __name__ == "__main__":
    check_and_create_tables()
    print("Verificación de tablas completada.") 