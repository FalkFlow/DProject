from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
class usuarios(models.Model):
    username = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=settings.ROLES)
    
    def __str__(self):
        return self.name


class categorias(models.Model):
    name = models.CharField(max_length=100)
    activate = models.BooleanField(default=True) # En caso de que la categoria no este disponible
    
    def __str__(self):
        return self.name
    
    
class productos(models.Model):
    name = models.CharField(max_length=100)
    categoria = models.ForeignKey('categorias', on_delete=models.CASCADE)
    precio = models.IntegerField(default=0)
    imagen = models.CharField(max_length=1000) # Guardar imagen en nube y guardar url
    activate = models.BooleanField(default=True) # En caso de que el producto no este disponible
    destacado = models.BooleanField(default=False) # Mostrar en la pagina principal
    
    def __str__(self):
        return self.name
    
class carrito(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.cantidad + ' ' + self.producto.name

class carrito_producto(models.Model):
    carrito = models.ForeignKey('carrito', on_delete=models.CASCADE)
    producto = models.ManyToManyField('productos')
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.cantidad + ' ' + self.producto.name
    
class orden(models.Model):
    estados = (
        ('pendiente', 'pendiente'),
        ('enviado', 'enviado'),
        ('entregado', 'entregado')
    )
    
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    carrito = models.ForeignKey('carrito', on_delete=models.CASCADE)
    carrito_detalle = models.ForeignKey('carrito_producto', on_delete=models.CASCADE, null=True)
    direccion = models.CharField(max_length=1000)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=estados, default='pendiente')
    
    def __str__(self):
        return self.usuario.username + ' ' + self.estado