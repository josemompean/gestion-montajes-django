import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_montajes.settings')
django.setup()

# Importar lo necesario
from django.db import connection

def fix_permission_tables():
    with connection.cursor() as cursor:
        # Comprobar y corregir la tabla auth_user_user_permissions
        try:
            print("Verificando tabla auth_user_user_permissions...")
            cursor.execute("SHOW TABLES LIKE 'auth_user_user_permissions'")
            if cursor.fetchone():
                # La tabla existe, verificar su estructura
                try:
                    cursor.execute("SELECT user_id FROM auth_user_user_permissions LIMIT 1")
                    print("La tabla auth_user_user_permissions parece estar bien estructurada.")
                except Exception:
                    # Si hay un error en la consulta, recrear la tabla
                    print("Recreando tabla auth_user_user_permissions...")
                    cursor.execute("DROP TABLE IF EXISTS auth_user_user_permissions")
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
                    print("Tabla auth_user_user_permissions recreada correctamente.")
            else:
                # La tabla no existe, crearla
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
                print("Tabla auth_user_user_permissions creada correctamente.")
        except Exception as e:
            print(f"Error al verificar/arreglar tabla auth_user_user_permissions: {e}")
        
        # Comprobar y corregir la tabla auth_user_groups
        try:
            print("Verificando tabla auth_user_groups...")
            cursor.execute("SHOW TABLES LIKE 'auth_user_groups'")
            if cursor.fetchone():
                # La tabla existe, verificar su estructura
                try:
                    cursor.execute("SELECT user_id FROM auth_user_groups LIMIT 1")
                    print("La tabla auth_user_groups parece estar bien estructurada.")
                except Exception:
                    # Si hay un error en la consulta, recrear la tabla
                    print("Recreando tabla auth_user_groups...")
                    cursor.execute("DROP TABLE IF EXISTS auth_user_groups")
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
                    print("Tabla auth_user_groups recreada correctamente.")
            else:
                # La tabla no existe, crearla
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
                print("Tabla auth_user_groups creada correctamente.")
        except Exception as e:
            print(f"Error al verificar/arreglar tabla auth_user_groups: {e}")

if __name__ == "__main__":
    fix_permission_tables()
    print("Proceso completado.") 