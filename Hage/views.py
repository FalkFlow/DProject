from django.shortcuts import render, redirect # type: ignore
from .models import * # type: ignore
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def mostrar(request):
    productos_destacados = productos.objects.filter(destacado=True)
    context = {'productos': productos_destacados}
    return render(request, 'index.html', context)


def catalogo(request):
    all_productos = productos.objects.all()
    all_categorias = categorias.objects.all()
    context = {'productos': all_productos, 'categorias': all_categorias}
    return render(request, 'productos.html', context)

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    return render(request, 'contacto.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usuario')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    profile = usuarios.objects.get(username=user)
                    request.session['perfil'] = profile.rol
                except usuarios.DoesNotExist:
                    form.add_error(None, 'Perfil no encontrado para el usuario.')
                login(request, user) 
                return redirect('index')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos, intente nuevamente')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Crear el perfil de usuario
            profile = usuarios.objects.create(username=user, rol='cliente')  
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registro.html', {'form': form})
    
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo')  
    else:
        form = ProductoForm()
    return render(request, 'añadir_producto.html', {'form': form})

def carrito(request):
    return render(request, 'carrito.html')

def pago(request):
    return render(request, 'pago.html')


"""producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')
    
    carritos_activos = Carrito.objects.filter(usuario=request.user, activo=True)
    
    if carritos_activos.exists():
        carrito = carritos_activos.first()
    else:
        carrito = Carrito.objects.create(usuario=request.user)
    
    detalle_carrito = DetalleCarrito.objects.create(
        carrito=carrito,
        precio_unitario=producto.precio_normal
    )
    
    detalle_carrito.productos.add(producto)
    
    return redirect('inicio')
    
    def ver_carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user, activo=True)
        
        for detalle in carrito.detalles.all():
            detalle.subtotal = detalle.productos.first().precio_final() * detalle.cantidad
            detalle.save()
            
        total_venta = carrito.detalles.all().aggregate(Sum('subtotal'))['subtotal__sum']
    except Carrito.DoesNotExist:
        carrito = None
        total_venta = 0
    
    perfil = request.session.get('perfil') 
    
    context = {
        'carrito': carrito,
        'perfil': perfil,
        'total_venta': total_venta,
    }
    
    return render(request, 'store/cart.html', context)

@login_required
@role_required('admin', 'cliente')
def eliminar_producto_carrito(request, id):
    detalle = get_object_or_404(DetalleCarrito, id=id)
    detalle.delete()
    
    return redirect('ver_carrito')

    """