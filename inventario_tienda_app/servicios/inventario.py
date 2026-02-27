#Módulo que implementa la clase Inventario con operaciones CRUD y persistencia.
import json
import os
from modelos.producto import Producto
class Inventario: #Clase que gestiona el inventario de productos.
    """ Utiliza un diccionario como colección principal para almacenar productos,
    con el ID como clave para acceso rápido O(1). """    
    
    def __init__(self, archivo_datos='datos/inventario.json'): #Constructor de la clase Inventario.
        self._productos = {}  # Diccionario {id: Producto}
        self._archivo_datos = archivo_datos
        self._ids_disponibles = set()  # Conjunto para IDs disponibles
        self.cargar_desde_archivo()
    
    def generar_nuevo_id(self): #Genera un nuevo ID único para un producto.
        if self._ids_disponibles:
            return min(self._ids_disponibles)  # Reutiliza el ID más pequeño disponible
        
        # Si no hay IDs disponibles, genera el siguiente ID secuencial
        return max(self._productos.keys()) + 1 if self._productos else 1
    
    def añadir_producto(self, nombre, cantidad, precio):#Añade un nuevo producto al inventario.
        nuevo_id = self.generar_nuevo_id()
        producto = Producto(nuevo_id, nombre, cantidad, precio)
        self._productos[nuevo_id] = producto
        
        # Si el ID estaba en disponibles, lo removemos
        if nuevo_id in self._ids_disponibles:
            self._ids_disponibles.remove(nuevo_id)
        
        self.guardar_en_archivo()
        return producto
    def eliminar_producto(self, id_producto): #Elimina un producto del inventario por su ID.
        if id_producto in self._productos:
            # Elimina el producto y guarda su ID para reutilización
            del self._productos[id_producto]
            self._ids_disponibles.add(id_producto)
            self.guardar_en_archivo()
            return True
        return False
    def actualizar_producto(self, id_producto, cantidad=None, precio=None): #Actualiza la cantidad y/o precio de un producto.
        if id_producto not in self._productos:
            return False
        producto = self._productos[id_producto]
        if cantidad is not None:
            producto.cantidad = cantidad
        if precio is not None:
            producto.precio = precio
        self.guardar_en_archivo()
        return True
    def buscar_por_nombre(self, nombre): #Busca productos por nombre (búsqueda parcial).
        nombre = nombre.lower()
        resultados = []
        for producto in self._productos.values():
            if nombre in producto.nombre.lower():
                resultados.append(producto)
        return resultados
    
    def obtener_producto(self, id_producto): #Obtiene un producto por su ID.
        return self._productos.get(id_producto)
    def mostrar_todos(self): #Retorna todos los productos ordenados por nombre.
        return sorted(self._productos.values(), key=lambda p: p.nombre)
    
    def guardar_en_archivo(self): #Guarda el inventario en un archivo JSON. Serializa los objetos Producto a diccionarios para su almacenamiento.
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self._archivo_datos), exist_ok=True)
            datos = {
                'productos': [p.to_dict() for p in self._productos.values()],
                'ids_disponibles': list(self._ids_disponibles)
            }
            with open(self._archivo_datos, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")
    def cargar_desde_archivo(self): #Carga el inventario desde un archivo JSON. Deserializa los datos y recrea los objetos Producto.
        try:
            if not os.path.exists(self._archivo_datos):
                return
            with open(self._archivo_datos, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            # Limpiar inventario actual
            self._productos.clear()
            # Recrear productos desde los datos
            for prod_datos in datos.get('productos', []):
                producto = Producto.from_dict(prod_datos)
                self._productos[producto.id] = producto
            # Cargar IDs disponibles
            self._ids_disponibles = set(datos.get('ids_disponibles', []))
        except FileNotFoundError:
            # El archivo no existe, empezamos con inventario vacío
            pass
        except json.JSONDecodeError:
            print("Error: El archivo de datos está corrupto")
        except Exception as e:
            print(f"Error al cargar el inventario: {e}")
    def __len__(self): #Retorna la cantidad de productos en el inventario
        return len(self._productos)
    def __iter__(self): #Permite iterar sobre los productos
        return iter(self._productos.values())