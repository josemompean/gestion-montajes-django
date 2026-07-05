from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='montajes/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('', views.lista_montajes, name='lista_montajes'),
    path('mis-montajes/', views.mis_montajes, name='mis_montajes'),
    path('historial/', views.historial_montajes, name='historial'),
    path('historial-admin/', views.historial_admin, name='historial_admin'),
    path('estadisticas-montajes/', views.estadisticas_montajes, name='estadisticas_montajes'),
    path('montaje/<int:montaje_id>/', views.detalle_montaje, name='detalle_montaje'),
    path('montaje/<int:montaje_id>/iniciar/', views.iniciar_montaje, name='iniciar_montaje'),
    path('montaje/<int:montaje_id>/finalizar/', views.finalizar_montaje, name='finalizar_montaje'),
]
