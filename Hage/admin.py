from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(usuarios)
admin.site.register(categorias)
admin.site.register(productos)
admin.site.register(carrito)
admin.site.register(carrito_producto)
admin.site.register(orden)
