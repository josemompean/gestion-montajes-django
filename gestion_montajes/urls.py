from django.contrib import admin
from django.urls import path, include
from montajes.views import login_view  # Importa la vista del login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='home'),  # La raíz redirige al login
    path('montajes/', include('montajes.urls')),  # Rutas de la app montajes
]
