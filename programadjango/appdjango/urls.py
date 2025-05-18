from django.urls import path

from django.contrib import admin
from .views import vistaLogin, vistaRegistro, vistaInicio, vistaReconocimientos, vistaAjustes, eliminarCuenta, cambiar_contrasena, deteccion_resultado, guardar_animal_BBDD, recuperar_contrasena, cambio_contrasena, reestablecer_contrasena 
#importamos las vistas que vamos a usar en los distintos html
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistaLogin, name="login"),
    path('registro/', vistaRegistro, name='registro'),  
    path('inicio/', vistaInicio, name='inicio'),  
    path('reconocimiento/', vistaReconocimientos, name='reconocimientos'),
    path('ajustes/', vistaAjustes, name='ajustes'),
    path('eliminarCuenta/', eliminarCuenta, name='eliminarCuenta'),
    path('cambiarContrasena/', cambiar_contrasena, name="cambiar_contrasena"),
    path("resultado/", deteccion_resultado, name="resultado"),
    path("guardar_animal/", guardar_animal_BBDD, name="guardar_animal"),
    path("recuperar_contrasena/", recuperar_contrasena, name= 'recuperar_contrasena'),
    path("cambio_contrasena/", cambio_contrasena, name= 'cambio_contrasena'),
    path("restablecer_contrasena/", reestablecer_contrasena, name="reestablecer_contrasena")
]
