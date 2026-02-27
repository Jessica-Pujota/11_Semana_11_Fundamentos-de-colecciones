#Módulo que define la clase Producto para el sistema de inventario
class Producto:  #    Clase que representa un producto en el inventario.
    """
    Atributos:
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        cantidad (int): Cantidad disponible en inventario
        precio (float): Precio unitario del producto
    """
    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.
        Args:
            id_producto (int): ID único del producto
            nombre (str): Nombre del producto
            cantidad (int): Cantidad inicial
            precio (float): Precio unitario
        """
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
    
    # Getters y Setters
    @property
    def id(self): #Getter del ID del producto
        return self._id
    @property
    def nombre(self): #Getter del nombre del producto
        return self._nombre
    @nombre.setter
    def nombre(self, nuevo_nombre): #Setter del nombre del producto
        if nuevo_nombre and isinstance(nuevo_nombre, str):
            self._nombre = nuevo_nombre
        else:
            raise ValueError("El nombre debe ser una cadena no vacía")
    @property
    def cantidad(self): #Getter de la cantidad del producto
        return self._cantidad
    @cantidad.setter
    def cantidad(self, nueva_cantidad): #Setter de la cantidad del producto
        if isinstance(nueva_cantidad, int) and nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad debe ser un número entero no negativo")
    @property
    def precio(self): #Getter del precio del producto
        return self._precio
    @precio.setter
    def precio(self, nuevo_precio): #Setter del precio del producto
        if isinstance(nuevo_precio, (int, float)) and nuevo_precio > 0:
            self._precio = float(nuevo_precio)
        else:
            raise ValueError("El precio debe ser un número positivo")
    def to_dict(self):
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio
        }
    @classmethod
    def from_dict(cls, datos): #Crea un objeto Producto a partir de un diccionario.
    
        return cls(
            id_producto=datos['id'],
            nombre=datos['nombre'],
            cantidad=datos['cantidad'],
            precio=datos['precio']
        )
    
    def __str__(self): #Representación en string del producto
        return f"ID: {self._id} | {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"
    
    def __repr__(self): #Representación para depuración
        return f"Producto(id={self._id}, nombre='{self._nombre}', cantidad={self._cantidad}, precio={self._precio})"