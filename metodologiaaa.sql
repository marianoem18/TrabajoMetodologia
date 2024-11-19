-- Activar soporte para claves foráneas
PRAGMA foreign_keys = ON;

-- Tabla proveedores
CREATE TABLE proveedores (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT, 
    nombre VARCHAR(100),
    direccion VARCHAR(120),
    telefono VARCHAR(15),
    email VARCHAR(50)
);

-- Tabla productos
CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT, 
    nombre VARCHAR(100),
    precio NUMERIC(10, 2),
    descripcion TEXT, 
    id_proveedor INTEGER,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

-- Tabla stock
CREATE TABLE stock (
    id_stock INTEGER PRIMARY KEY AUTOINCREMENT, 
    cantidad INTEGER,
    id_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla compras
CREATE TABLE compras (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT, 
    fecha_compra DATE,
    metodo_de_pago VARCHAR(60),
    cantidad INTEGER, 
    id_proveedor INTEGER,
    id_stock INTEGER,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_stock) REFERENCES stock(id_stock)
);

-- Tabla clientes
CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, 
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    telefono VARCHAR(15),
    email VARCHAR(50),
    direccion VARCHAR(150)
);

-- Tabla ventas
CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT, 
    fecha_venta DATE,
    metodo_de_pago VARCHAR(60),
    id_cliente INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Tabla facturación
CREATE TABLE facturacion (
    id_facturacion INTEGER PRIMARY KEY AUTOINCREMENT, 
    cantidad INTEGER,
    precio_unitario NUMERIC,
    subtotal NUMERIC(10, 2),
    id_producto INTEGER,
    id_venta INTEGER,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
);
