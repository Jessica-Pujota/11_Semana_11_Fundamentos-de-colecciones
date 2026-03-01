""" IMPLEMENTACIÓN CRUD CON CONJUNTOS """
from typing import Set, Tuple, Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Inventario.modelos.producto import Producto
class ConjuntoInventario: #Implementación de inventario usando CONJUNTOS
    def __init__(self, gestor=None):
        self.gestor = gestor
        self.productos: Set[Tuple[int, str, int, float]] = set()
        self.nombre_implementacion = "CONJUNTOS"
        self._cargar_desde_archivo()
    
    def _cargar_desde_archivo(self): #Carga productos desde archivo
        if self.gestor:
            self.productos = self.gestor.cargar_como_conjunto()
    
    def _guardar_en_archivo(self) -> bool: #Guarda en archivo
        if self.gestor:
            return self.gestor.guardar_desde_conjunto(self.productos)
        return True
    
    def _buscar_por_id(self, id_buscar: int) -> Optional[Tuple]: #Busca producto por ID
        for producto in self.productos:
            if producto[0] == id_buscar:
                return producto
        return None
    
    # ===== CRUD =====
    def create(self, producto: Producto) -> bool: #CREATE - Añadir producto
        if self._buscar_por_id(producto.id):
            print(f"  ✗ Error: ID {producto.id} ya existe")
            return False
        elemento = producto.to_set_element()
        self.productos.add(elemento)
        
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto añadido")
            return True
        else:
            self.productos.remove(elemento)
            return False
    
    def read(self, id_buscar: int = None) -> List[Tuple]: #READ - Leer producto(s)
        if id_buscar:
            producto = self._buscar_por_id(id_buscar)
            return [producto] if producto else []
        return list(self.productos)
    
    def update(self, id_producto: int, cantidad: int = None, precio: float = None) -> bool: #UPDATE - Actualizar producto
        producto_tuple = self._buscar_por_id(id_producto)
        if not producto_tuple:
            print(f"  ✗ No existe ID {id_producto}")
            return False
        
        id_val, nombre, cant_old, prec_old = producto_tuple
        nueva_cant = cantidad if cantidad is not None else cant_old
        nuevo_precio = precio if precio is not None else prec_old
        
        if nueva_cant < 0 or nuevo_precio < 0:
            print("  ✗ Valores negativos no permitidos")
            return False
        
        nuevo_producto = (id_val, nombre, nueva_cant, nuevo_precio)
        
        self.productos.remove(producto_tuple)
        self.productos.add(nuevo_producto)
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto actualizado")
            return True
        else:
            self.productos.add(producto_tuple)
            self.productos.remove(nuevo_producto)
            return False
    
    def delete(self, id_producto: int) -> bool: #DELETE - Eliminar producto
        producto = self._buscar_por_id(id_producto)
        if not producto:
            print(f"  ✗ No existe ID {id_producto}")
            return False
        
        self.productos.remove(producto)
        
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto eliminado")
            return True
        else:
            self.productos.add(producto)
            return False
    
    # ===== OPERACIONES ESPECÍFICAS =====
    
    def demostrar_operaciones_conjuntos(self): #Demuestra operaciones de conjuntos
        print(f"\n  🔷 OPERACIONES DE CONJUNTOS:")
        
        conj_a = {p for p in self.productos if p[2] > 10}  # Cant > 10
        conj_b = {p for p in self.productos if p[3] < 100}  # Precio < 100
        print(f"    A (cant>10): {len(conj_a)} productos")
        print(f"    B (precio<100): {len(conj_b)} productos")
        print(f"    Unión (A∪B): {len(conj_a | conj_b)}")
        print(f"    Intersección (A∩B): {len(conj_a & conj_b)}")
        print(f"    Diferencia (A-B): {len(conj_a - conj_b)}")