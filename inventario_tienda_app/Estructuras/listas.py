"""
IMPLEMENTACIÓN CRUD CON LISTAS
"""
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Inventario.modelos.producto import Producto

class ListaInventario:
    """
    Implementación de inventario usando LISTA.
    """
    
    def __init__(self, gestor=None):
        self.gestor = gestor
        self.productos: List[Producto] = []
        self.nombre_implementacion = "LISTAS"
        self._cargar_desde_archivo()
    
    def _cargar_desde_archivo(self): #Carga productos desde archivo
        if self.gestor:
            self.productos = self.gestor.cargar_como_lista()
    
    def _guardar_en_archivo(self) -> bool: #Guarda en archivo
        if self.gestor:
            return self.gestor.guardar_desde_lista(self.productos)
        return True
    
    def _buscar_indice_por_id(self, id_buscar: int) -> Optional[int]: #Busca índice por ID
        for i, producto in enumerate(self.productos):
            if producto.id == id_buscar:
                return i
        return None
    
    # ===== CRUD =====
    
    def create(self, producto: Producto) -> bool: #CREATE - Añadir producto
        if self._buscar_indice_por_id(producto.id) is not None:
            print(f"  ✗ Error: ID {producto.id} ya existe")
            return False
        
        self.productos.append(producto)
        
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto añadido")
            return True
        else:
            self.productos.pop()
            return False
    
    def read(self, id_buscar: int = None) -> List[Producto]: #READ - Leer producto(s)
        if id_buscar:
            indice = self._buscar_indice_por_id(id_buscar)
            if indice is not None:
                return [self.productos[indice]]
            return []
        return self.productos.copy()
    
    def update(self, id_producto: int, cantidad: int = None, precio: float = None) -> bool: #UPDATE - Actualizar producto"""
        indice = self._buscar_indice_por_id(id_producto)
        if indice is None:
            print(f"  ✗ No existe ID {id_producto}")
            return False
        
        producto = self.productos[indice]
        try:
            if cantidad is not None:
                producto.cantidad = cantidad
            if precio is not None:
                producto.precio = precio
            
            if self._guardar_en_archivo():
                print(f"  ✓ [{self.nombre_implementacion}] Producto actualizado")
                return True
            return False
        except ValueError as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def delete(self, id_producto: int) -> bool: #DELETE - Eliminar producto
        indice = self._buscar_indice_por_id(id_producto)
        if indice is None:
            print(f"  ✗ No existe ID {id_producto}")
            return False
        
        eliminado = self.productos.pop(indice)
        
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto eliminado")
            return True
        else:
            self.productos.insert(indice, eliminado)
            return False
    
    # ===== OPERACIONES ESPECÍFICAS =====
    
    def ordenar_por_precio(self, descendente: bool = False): #Ordena productos por precio
        self.productos.sort(key=lambda p: p.precio, reverse=descendente)
        self._guardar_en_archivo()
        print(f"  ✓ Lista ordenada por precio")
    
    def ordenar_por_cantidad(self, descendente: bool = False): #Ordena productos por cantidad
        self.productos.sort(key=lambda p: p.cantidad, reverse=descendente)
        self._guardar_en_archivo()
        print(f"  ✓ Lista ordenada por cantidad")
    
    def obtener_primeros_n(self, n: int) -> List[Producto]: #Obtiene primeros n productos
        return self.productos[:n]
    
    def obtener_ultimos_n(self, n: int) -> List[Producto]: #Obtiene últimos n productos
        return self.productos[-n:] if n > 0 else []