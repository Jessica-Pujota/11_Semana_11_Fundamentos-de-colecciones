""" IMPLEMENTACIÓN CRUD CON TUPLAS """
from typing import Tuple, List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Inventario.modelos.producto import Producto
class TuplaInventario:#Implementación de inventario usando TUPLAS (inmutable).
    
    def __init__(self, gestor=None):
        self.gestor = gestor
        self.productos: List[Tuple[int, str, int, float]] = []
        self.nombre_implementacion = "TUPLAS"
        self._cargar_desde_archivo()
    
    def _cargar_desde_archivo(self): #Carga productos desde archivo
        if self.gestor:
            self.productos = self.gestor.cargar_como_tuplas()
    
    def _guardar_en_archivo(self) -> bool: #Guarda en archivo
        if self.gestor:
            return self.gestor.guardar_desde_tuplas(self.productos)
        return True
    
    def _buscar_por_id(self, id_buscar: int) -> Optional[Tuple]: #Busca producto por ID
        for producto in self.productos:
            if producto[0] == id_buscar:
                return producto
        return None
    
    def _buscar_indice_por_id(self, id_buscar: int) -> Optional[int]: #Busca índice por ID
        for i, producto in enumerate(self.productos):
            if producto[0] == id_buscar:
                return i
        return None
    
    # ===== CRUD =====
    
    def create(self, producto: Producto) -> bool: #CREATE - Añadir producto
        if self._buscar_por_id(producto.id):
            print(f"  ✗ Error: ID {producto.id} ya existe.")
            return False            