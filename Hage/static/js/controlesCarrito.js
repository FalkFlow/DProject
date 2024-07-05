window.onload = function () {
    cargarCarrito();
  };

const cargarCarrito = () => {
    let localCarrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let carrito = document.getElementById('carrito');

    carrito.innerHTML = '';
  
    localCarrito.forEach(producto => {
      const productosCart = document.createElement('div');
      productosCart.className = 'row border-bottom';
  
      productosCart.innerHTML = `
        <div class="card mb-3">
          <div class="row no-gutters">
            <div class="col-md-4">
              <img src="${producto.imagen}" class="card-img" alt="${producto.nombre}">
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">${producto.nombre}</h5>
                <p class="card-text">Precio: $${producto.precio}</p>
                <p class="card-text">Cantidad: ${producto.cantidad}</p>
                <button class="btn btn-danger" onclick="eliminarDelCarro(${producto.id})" >Eliminar del carrito</button>
              </div>
            </div>
          </div>
        </div>
      `;
  
      carrito.appendChild(productosCart);
    });
  
  };


  const agregar = (productoId, productoN, productoPrecio, productoImagen) => {
    console.log(productoId);
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let producto = carrito.find(item => item.id === productoId);
  
    if (producto) {
      producto.cantidad += 1;
    } else {
      carrito.push({
        id: productoId,
        nombre: productoN,
        precio: productoPrecio,
        imagen: productoImagen,
        cantidad: 1
      });
    }
  
    localStorage.setItem('carrito', JSON.stringify(carrito));
    cargarCarrito();
  };

  const eliminarDelCarro = (productoId) => {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let index = carrito.findIndex((i) => {
      return parseInt(i.id) === productoId;
    });
  
    if (index !== -1) {
      carrito.splice(index, 1);
  
      localStorage.setItem('carrito', JSON.stringify(carrito));
    }
    cargarCarrito();
  };