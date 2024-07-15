from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from .models import * # type: ignore
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def mostrar(request):
    productos_destacados = productos.objects.filter(destacado=True)
    perfil = request.session.get('perfil')
    context = {
        'productos': productos_destacados, 
        'perfil': perfil
        }
    return render(request, 'index.html', context)


def catalogo(request):
    all_productos = productos.objects.all()
    all_categorias = categorias.objects.all()
    perfil = request.session.get('perfil')
    context = {
        'productos': all_productos, 
        'categorias': all_categorias, 
        'perfil': perfil,
        }
    return render(request, 'productos.html', context)

def nosotros(request):
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        }
    return render(request, 'nosotros.html', context)

def contacto(request):
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        }
    return render(request, 'contacto.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usuario')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('/admin')
                else:
                    try:
                        profile = usuarios.objects.get(username=user)
                        request.session['perfil'] = profile.rol
                    except usuarios.DoesNotExist:
                        form.add_error(None, 'Perfil no encontrado para el usuario.')
                        return render(request, 'login.html', {'form': form})

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
            profile = usuarios.objects.create(username=user, rol='cliente')  
            request.session['perfil'] = 'cliente'  # O el rol que corresponda
            
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registro.html', {'form': form}) 

    
def agregar_producto(request):
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        }
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud')  
    else:
        form = ProductoForm()
    context.update({'form': form})
    return render(request, 'añadir_producto.html', context)

def carritos(request):
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        }
    return render(request, 'carrito.html', context)

def pago(request):
    
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        }
    return render(request, 'pago.html', context)


def producto_list(request):
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        }
    productos_list = productos.objects.all()
    context.update({'productos': productos_list})
    return render(request, 'crud.html', context)


def salir(request):
    logout(request)
    return redirect('index')


def modificar(request, id):
    producto = get_object_or_404(productos, pk=id)
    perfil = request.session.get('perfil')
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Redirigir a otra página, por ejemplo
            return redirect('crud')
    else:
        form = ProductoForm(instance=producto)
    
    context = {
        'form': form,
        'producto': producto,# Pasar el producto al contexto
        'perfil': perfil,
    }
    return render(request, 'modificar_producto.html', context)


def eliminar(request, id):
    producto = get_object_or_404(productos, pk=id)
    producto.delete()
    return redirect('crud')