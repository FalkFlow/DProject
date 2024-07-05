from django.urls import path # type: ignore
from . import views


urlpatterns = [
    path('', views.mostrar, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.user_login, name='login'),
    path('registro/', views.registro, name='register'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
]