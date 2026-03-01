"""
Modelo base de Producto utilizado por todas las implementaciones.
"""
from typing import Tuple, Dict, Any

class Producto: 
    """
    Clase que representa un producto con métodos de conversión
    para diferentes estructuras de datos.
    """
    
    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """
        Constructor de la clase Producto.
        
        Args:
            id_producto (int): Identificador único
            nombre (str): Nombre del producto
            cantidad (int): Cantidad en inventario
            precio (float): Precio unitario
        """
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
    
    # Propiedades (getters)
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @property
    def precio(self) -> float:
        return self._precio
    
    # Setters con validación
    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")
    
    @precio.setter
    def precio(self, nuevo_precio: float):
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            raise ValueError("El precio no puede ser negativo")
    
    def __str__(self) -> str:
        return f"ID:{self._id:3d} | {self._nombre:20s} | Cant:{self._cantidad:5d} | ${self._precio:8.2f}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool: #Para comparación en conjuntos (por ID)
        if isinstance(other, Producto):
            return self._id == other._id
        return False
    
    def __hash__(self) -> int:
        """Para usar en conjuntos (hash por ID)"""
        return hash(self._id)
    
    # ===== FORMATOS PARA DIFERENTES ESTRUCTURAS =====
    def to_tuple(self) -> Tuple[int, str, int, float]: #Formato para TUPLAS - INMUTABLE.
        return (self._id, self._nombre, self._cantidad, self._precio)
    
    def to_list(self) -> list: #Formato para LISTAS - MUTABLE.
        return [self._id, self._nombre, self._cantidad, self._precio]
    
    def to_dict(self) -> Dict[str, Any]: #Formato para DICCIONARIOS - CLAVE-VALOR
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio
        }
    
    def to_set_element(self) -> tuple: #Formato para CONJUNTOS - HASHABLE
        return (self._id, self._nombre, self._cantidad, self._precio)
    
    # ===== CONSTRUCTORES DESDE DIFERENTES ESTRUCTURAS =====
    
    @staticmethod
    def from_tuple(tupla: Tuple[int, str, int, float]):
        """Crea producto desde tupla"""
        return Producto(tupla[0], tupla[1], tupla[2], tupla[3])
    
    @staticmethod
    def from_list(lista: list):
        """Crea producto desde lista"""
        return Producto(lista[0], lista[1], lista[2], lista[3])
    
    @staticmethod
    def from_dict(diccionario: Dict[str, Any]):
        """Crea producto desde diccionario"""
        return Producto(
            diccionario['id'],
            diccionario['nombre'],
            diccionario['cantidad'],
            diccionario['precio']
        )
    
    @staticmethod
    def from_set_element(elemento: tuple): #Crea producto desde elemento de conjunto
        return Producto(elemento[0], elemento[1], elemento[2], elemento[3])
    
    # ===== FORMATO PARA ARCHIVO =====
    
    def to_file_string(self) -> str: #Convierte a formato para guardar en archivo
        return f"{self._id},{self._nombre},{self._cantidad},{self._precio:.2f}\n"
    
    @staticmethod
    def from_file_string(linea: str): #Crea producto desde línea de archivo
        try:
            partes = linea.strip().split(',')
            if len(partes) != 4:
                return None
            return Producto(
                int(partes[0]), 
                partes[1], 
                int(partes[2]), 
                float(partes[3])
            )
        except (ValueError, IndexError):
            return None