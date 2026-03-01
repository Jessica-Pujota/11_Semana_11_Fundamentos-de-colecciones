""" IMPLEMENTACIÓN CRUD CON DICCIONARIOS"""
from typing import Dict, Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Inventario.modelos.producto import Producto
class DiccionarioInventario: #Implementación de inventario usando DICCIONARIO.
    
    def __init__(self, gestor=None):
        self.gestor = gestor
        self.productos: Dict[int, Producto] = {}
        self.nombre_implementacion = "DICCIONARIOS"
        self._cargar_desde_archivo()
    
    def _cargar_desde_archivo(self): #Carga productos desde archivo
        if self.gestor:
            self.productos = self.gestor.cargar_como_diccionario()
    
    def _guardar_en_archivo(self) -> bool: #Guarda en archivo
        if self.gestor:
            return self.gestor.guardar_desde_diccionario(self.productos)
        return True
    
    # ===== CRUD ======
    def create(self, producto: Producto) -> bool: #CREATE - Añadir producto
        if producto.id in self.productos:
            print(f"  ✗ Error: ID {producto.id} ya existe")
            return False
        
        self.productos[producto.id] = producto
        
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto añadido")
            return True
        else:
            del self.productos[producto.id]
            return False
    
    def read(self, id_buscar: int = None) -> List[Producto]: #READ - Leer producto(s)
        if id_buscar:
            producto = self.productos.get(id_buscar)
            return [producto] if producto else []
        return list(self.productos.values())
    
    def update(self, id_producto: int, cantidad: int = None, precio: float = None) -> bool: #UPDATE - Actualizar producto
        if id_producto not in self.productos:
            print(f"  ✗ No existe ID {id_producto}")
            return False
        
        producto = self.productos[id_producto]
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
        if id_producto not in self.productos:
            print(f"  ✗ No existe ID {id_producto}")
            return False
        
        eliminado = self.productos.pop(id_producto)
        if self._guardar_en_archivo():
            print(f"  ✓ [{self.nombre_implementacion}] Producto eliminado")
            return True
        else:
            self.productos[id_producto] = eliminado
            return False
    
    # ===== OPERACIONES ESPECÍFICAS =====
    def filtrar_por_condicion(self, **condiciones) -> Dict[int, Producto]: #Filtra productos por condiciones
        resultado = self.productos.copy()
        
        if 'precio_max' in condiciones:
            resultado = {k: v for k, v in resultado.items() 
                        if v.precio <= condiciones['precio_max']}
        if 'precio_min' in condiciones:
            resultado = {k: v for k, v in resultado.items() 
                        if v.precio >= condiciones['precio_min']}
        if 'cantidad_min' in condiciones:
            resultado = {k: v for k, v in resultado.items() 
                        if v.cantidad >= condiciones['cantidad_min']}
        return resultado
    def agrupar_por_rango_precio(self) -> Dict[str, List[Producto]]: #Agrupa productos por rangos de precio
        grupos = {
            'económico (< $50)': [],
            'medio ($50-$200)': [],
            'caro (> $200)': []
        }
        
        for producto in self.productos.values():
            if producto.precio < 50:
                grupos['económico (< $50)'].append(producto)
            elif producto.precio <= 200:
                grupos['medio ($50-$200)'].append(producto)
            else:
                grupos['caro (> $200)'].append(producto)
        
        return grupos
    def estadisticas_por_categoria(self) -> Dict[str, dict]: #Calcula estadísticas por categoría
        grupos = self.agrupar_por_rango_precio()
        estadisticas = {}
        
        for categoria, productos in grupos.items():
            if productos:
                cantidades = [p.cantidad for p in productos]
                precios = [p.precio for p in productos]
                estadisticas[categoria] = {
                    'cantidad': len(productos),
                    'total_uds': sum(cantidades),
                    'precio_prom': sum(precios) / len(precios),
                    'precio_max': max(precios),
                    'precio_min': min(precios)
                }
            else:
                estadisticas[categoria] = {'cantidad': 0}
        return estadisticas